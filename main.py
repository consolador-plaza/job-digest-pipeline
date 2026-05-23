from ingest.eml_loader import EMLLoader

from parsers.router import ParserRouter

from validation.validator import Validator

from dedup.deduplicator import Deduplicator

from export.sheets_exporter import SheetsExporter

from logging_utils.logger import PipelineLogger

from archive.file_archiver import FileArchiver

from reporting.summary import RunSummary

from ingest.gmail_loader import GmailLoader

from storage.message_repo import MessageRepo

from state.run_state import RunState

import time

from storage.run_history_repo import RunHistoryRepo

from notifications.email_notifier import EmailNotifier

from storage.parser_health_repo import ParserHealthRepo

from config.config import CONFIG

from validation.startup_validator import StartupValidator

state = RunState()

loader = GmailLoader()

router = ParserRouter()

validator = Validator()

dedup = Deduplicator()

exporter = SheetsExporter()

repo = MessageRepo(exporter)

history = RunHistoryRepo(exporter)

logger = PipelineLogger()

archiver = FileArchiver()

summary = RunSummary()

start = time.time()

StartupValidator().validate()

notifier = EmailNotifier()

health = ParserHealthRepo(
    exporter
)

processed_ids = (

    repo

    .existing_ids()
)

last_run = state.load()


query = (

    "label:"

    +

    CONFIG[
        "gmail"
    ][
        "source_label"
    ]
)


if last_run:

    query += (

        f" after:{last_run}"
    )


emails = loader.load(
    query
)


all_jobs = []

stats = {

    "linkedin": {

        "emails":0,

        "jobs":0,

        "errors":0
    },

    "indeed": {

        "emails":0,

        "jobs":0,

        "errors":0
    },

    "glassdoor": {

        "emails":0,

        "jobs":0,

        "errors":0
    },

    "jobstreet": {

        "emails":0,

        "jobs":0,

        "errors":0
    }
}

processed = 0
failed = 0
duplicates = 0

for email in emails:

    try:
    
        gmail_id = email[
            "id"
        ]

        if gmail_id in processed_ids:


            print(

                "SKIP MAIL:",

                gmail_id
            )


            continue

        payload = email[
            "message"
        ]


        parser_obj = (

            router

            .detector

            .detect(
                payload
            )
        )


        parser_name = (

            parser_obj

            .__class__

            .__name__

            .replace(
                "Parser",
                ""
            )

            .lower()
        )


        stats[
            parser_name
        ][
            "emails"
        ] += 1


        jobs = router.parse_email(
            payload
        )


        stats[
            parser_name
        ][
            "jobs"
        ] += len(
            jobs
        )


        for j in jobs:

            j.gmail_id = gmail_id

            all_jobs.append(
                j
            )




        #
        # SUCCESS PATH
        #

        loader.move_label(

            gmail_id,

            CONFIG[
                "gmail"
            ][
                "processed_label"
            ]
        )

        repo.add(

            gmail_id,

            "SUCCESS"
        )

        processed += 1



    except Exception as ex:


        logger.log(
            ex
        )


        #
        # EXCEPTION PATH
        #

        loader.move_label(

            gmail_id,

            CONFIG[
                "gmail"
            ][
                "failed_label"
            ]
        )

        repo.add(

            gmail_id,

            "FAILED"
        )

        failed += 1

        if "parser_name" in locals():

            stats[
                parser_name
            ][
                "errors"
            ] += 1

        notifier.send(

            "Job Digest FAILED",

            f"""

        Mail ID:

        {gmail_id}


        Error:

        {str(ex)}


        Source:

        {email.get(
            "file"
        )}
        """
        )


logger.log(

    f"RAW {len(all_jobs)}"
)


before = len(
    all_jobs
)

all_jobs = dedup.apply(
    all_jobs
)

after = len(
    all_jobs
)

summary.duplicates = (

    before - after
)


logger.log(

    f"DEDUP {len(all_jobs)}"
)

existing = exporter.existing_keys()

print(
    "EXISTING KEYS:",
    len(
        existing
    )
)

new_jobs = []


for j in all_jobs:


    if j.unique_key in existing:


        print(

            "SKIP DUP:",

            j.role,

            "|",

            j.company
        )


        continue


    new_jobs.append(
        j
    )


all_jobs = new_jobs

exporter.append_jobs(
    all_jobs
)

summary.inserted = len(
    all_jobs
)

summary.raw = before

summary.emails = processed

logger.log(

    f"EMAILS {processed}"
)

logger.log(

    f"FAILED {failed}"
)

print(
    "FAILED:",
    failed
)

summary.failed = failed

for k,v in stats.items():


    status = (

        "PASS"

        if v[
            "errors"
        ] == 0

        else

        "FAIL"
    )


    health.add(

        k,

        status,

        v[
            "emails"
        ],

        v[
            "jobs"
        ],

        v[
            "errors"
        ]
    )

summary.print_summary()

notifier.send(

    "Job Digest SUCCESS",

    f"""

Emails:

{summary.emails}


Raw:

{summary.raw}


Inserted:

{summary.inserted}


Duplicates:

{summary.duplicates}


Failed:

{summary.failed}
"""
)

duration = (

    time.time()

    -

    start
)


history.add(

    summary,

    duration
)


state.save()