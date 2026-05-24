import gspread

from google.oauth2.service_account import Credentials

import time 

from gspread.exceptions import APIError

from export.sheets_client import SheetsClient

from export.sheet_initializer import SheetInitializer

class SheetsExporter:

    def __init__(

        self
    ):


        client = (

            SheetsClient()

            .connect()
        )


        self.book = (

            client

            .open(

                "Daily Job Digest"
            )
        )


        SheetInitializer().ensure(

            self.book
        )
       
    def append_jobs(

        self,

        jobs
    ):

        ws = (self.book.worksheet(

            "Daily Job Digest"
        )
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

                ws = (

                    self.book

                    .worksheet(

                        "Daily Job Digest"
                    )
                )


                values = (

                    ws

                    .col_values(
                        6
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


        book = self.book


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