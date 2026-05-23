from pathlib import Path

from email import policy

from email.parser import BytesParser



class EMLLoader:


    def load_folder(
        self,
        folder="emails/incoming"
    ):

        files = list(
            Path(folder).glob(
                "*.eml"
            )
        )

        loaded = []


        for file in files:

            with open(
                file,
                "rb"
            ) as f:

                msg = BytesParser(
                    policy=policy.default
                ).parse(
                    f
                )


            loaded.append(

                {
                    "file": file,

                    "message": msg
                }

            )

        return loaded
    