from pathlib import Path


class StartupValidator:


    def validate(self):


        required = [

            ".env",

            "config/settings.yaml",

            "credentials.json"
        ]


        missing = []


        for path in required:


            if not Path(path).exists():


                missing.append(
                    path
                )


        if missing:


            raise Exception(

                "Missing required files: "

                +

                ", ".join(
                    missing
                )
            )