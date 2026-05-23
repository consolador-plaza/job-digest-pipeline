from ingest.eml_loader import EMLLoader

from parsers.jobstreet import JobStreetParser

from dedup.deduplicator import Deduplicator

from export.sheets_exporter import SheetsExporter



loader = EMLLoader()

emails = loader.load_folder()


jobs = []


for e in emails:


    name = str(
        e["file"]
    )


    if "jobstreet" not in name.lower():

        continue


    parser = JobStreetParser()


    records = parser.parse(

        e["message"]
    )


    jobs.extend(
        records
    )


print(

    "RAW:",

    len(jobs)
)


dedup = Deduplicator()


jobs = dedup.apply(
    jobs
)


print(

    "DEDUP:",

    len(jobs)
)


exporter = SheetsExporter()


exporter.append_jobs(
    jobs
)