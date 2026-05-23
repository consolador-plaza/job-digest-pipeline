from pathlib import Path

import shutil



class FileArchiver:


    def move_processed(

        self,

        path
    ):


        target = (

            Path(
                "emails/processed"
            )

            /

            Path(
                path
            ).name
        )


        shutil.move(

            path,

            target
        )


    def move_failed(

        self,

        path
    ):


        target = (

            Path(
                "emails/failed"
            )

            /

            Path(
                path
            ).name
        )


        shutil.move(

            path,

            target
        )