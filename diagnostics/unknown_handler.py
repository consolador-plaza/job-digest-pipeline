from pathlib import Path

import shutil



class UnknownHandler:


    def save(

        self,

        source_file
    ):


        Path(

            "diagnostics/unknown"

        ).mkdir(

            parents=True,

            exist_ok=True
        )


        shutil.copy(

            source_file,

            "diagnostics/unknown"
        )