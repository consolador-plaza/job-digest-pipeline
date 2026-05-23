from datetime import datetime

from config.config import CONFIG



class ParserHealthRepo:


    TAB = CONFIG[
        "sheets"
    ][
        "parser_health"
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

        parser,

        status,

        emails,

        jobs,

        errors
    ):


        self.sheet.append_row(

            [

                datetime.now()

                .astimezone()

                .isoformat(

                    timespec="seconds"
                ),

                parser,

                status,

                emails,

                jobs,

                errors
            ]
        )