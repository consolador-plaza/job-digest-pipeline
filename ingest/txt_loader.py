from pathlib import Path



class TXTLoader:


    def load_folder(
        self,
        folder="emails/incoming"
    ):

        records = []


        files = list(
            Path(folder).glob(
                "*.txt"
            )
        )


        for file in files:

            content = file.read_text(

                encoding="utf-8",

                errors="ignore"
            )


            records.append(

                {
                    "file": file,

                    "content": content
                }

            )

        return records