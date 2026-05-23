from datetime import datetime

from config.config import CONFIG

class RunHistoryRepo:


    TAB = CONFIG[
        "sheets"
    ][
        "run_history"
    ]


    def __init__(

        self,

        exporter
    ):


        self.sheet = (

            exporter

            .get_sheet(
                self.TAB
            )
        )


    def add(

        self,

        summary,

        duration
    ):


        self.sheet.append_row(

            [

                str(
                    datetime.now()
                ),

                summary.emails,

                summary.raw,

                summary.inserted,

                summary.duplicates,

                summary.failed,

                round(
                    duration,
                    2
                )
            ]
        )