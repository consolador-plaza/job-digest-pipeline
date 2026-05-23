from pathlib import Path

from datetime import datetime



class PipelineLogger:


    def __init__(self):


        Path(
            "logs"
        ).mkdir(

            exist_ok=True
        )


        self.path = (

            Path(
                "logs"
            )

            /

            "pipeline.log"
        )


    def log(

        self,

        message
    ):


        ts = datetime.now()


        line = (

            f"[{ts}] "

            +

            str(
                message
            )
        )


        print(
            line
        )


        with open(

            self.path,

            "a",

            encoding="utf8"
        ) as f:


            f.write(

                line

                +

                "\n"
            )