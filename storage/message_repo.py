from datetime import datetime


class MessageRepo:


    TAB_NAME = "ProcessedMail"


    def __init__(

        self,

        exporter
    ):


        self.sheet = (

            exporter

            .get_sheet(

                self.TAB_NAME
            )
        )


    def existing_ids(

        self
    ):


        rows = (

            self.sheet

            .get_all_values()
        )


        ids = set()


        for row in rows[1:]:


            if row:

                ids.add(
                    row[0]
                )


        return ids


    def add(

        self,

        gmail_id,

        status
    ):


        self.sheet.append_row(

            [

                gmail_id,

                status,

                str(
                    datetime.now()
                )
            ]
        )