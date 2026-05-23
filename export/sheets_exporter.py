import gspread

from google.oauth2.service_account import Credentials

import time 

from gspread.exceptions import APIError

class SheetsExporter:


    SCOPES = [

        "https://www.googleapis.com/auth/spreadsheets",

        "https://www.googleapis.com/auth/drive"
    ]


    def connect(self):

        creds = Credentials.from_service_account_file(

            "credentials/service_account.json",

            scopes=self.SCOPES
        )

        return gspread.authorize(
            creds
        )


    def ensure_sheets(self):


        client = self.connect()


        book = client.open(
            "Daily Job Digest"
        )


        existing = [

            x.title

            for x in book.worksheets()
        ]


        if "Daily Job Digest" not in existing:

            ws = book.add_worksheet(

                title="Daily Job Digest",

                rows=100,

                cols=10
            )

            ws.append_row(

                [

                    "Timestamp",

                    "Role",

                    "Company",

                    "Source",

                    "Link",

                    "Unique Key"
                ]

            )


        if "Parser Diagnostics" not in existing:

            ws = book.add_worksheet(

                title="Parser Diagnostics",

                rows=100,

                cols=10
            )

            ws.append_row(

                [

                    "Timestamp",

                    "Provider",

                    "Email File",

                    "Issue Type",

                    "Details",

                    "Status"
                ]

            )


        print(
            "Worksheets ready"
        )
        
    def append_jobs(

        self,

        jobs
    ):


        book = self.connect().open(

            "Daily Job Digest"
        )


        ws = book.worksheet(

            "Daily Job Digest"
        )


        rows = []


        for j in jobs:


            rows.append(

                [

                    j.timestamp,

                    j.role,

                    j.company,

                    j.source,

                    j.link,

                    j.unique_key,

                    j.gmail_id
                ]

            )


        if rows:

            ws.append_rows(
                rows
            )


            print(

                "Inserted:",

                len(rows)
            )
            
    def existing_keys(

        self
    ):


        retries = 3


        for attempt in range(

            retries
        ):


            try:


                book = (

                    self

                    .connect()

                    .open(

                        "Daily Job Digest"
                    )
                )


                ws = (

                    book

                    .worksheet(

                        "Daily Job Digest"
                    )
                )


                values = (

                    ws

                    .col_values(
                        5
                    )
                )


                return set(

                    values[1:]
                )


            except APIError as ex:


                print(

                    "GOOGLE RETRY:",

                    attempt + 1
                )


                if attempt == (

                    retries - 1
                ):

                    raise


                time.sleep(
                    5
                )


        return set()

    def get_sheet(

        self,

        name
    ):


        book = (

            self

            .connect()

            .open(

                "Daily Job Digest"
            )
        )


        existing = [

            x.title

            for x in book.worksheets()
        ]


        if name not in existing:


            ws = book.add_worksheet(

                title=name,

                rows=100,

                cols=10
            )


            if name == "ProcessedMail":


                ws.append_row(

                    [

                        "gmail_id",

                        "status",

                        "timestamp"
                    ]
                )


        return book.worksheet(
            name
        )