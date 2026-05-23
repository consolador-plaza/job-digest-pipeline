import json

from pathlib import Path

from datetime import datetime



class RunState:


    PATH = Path(
        "state/run_state.json"
    )


    def load(

        self
    ):


        if not self.PATH.exists():

            return None


        with open(

            self.PATH,

            "r",

            encoding="utf8"
        ) as f:


            data = json.load(
                f
            )


        return data.get(
            "last_run"
        )


    def save(

        self
    ):


        with open(

            self.PATH,

            "w",

            encoding="utf8"
        ) as f:


            json.dump(

                {

                    "last_run":

                    datetime.now().strftime(

                        "%Y/%m/%d"
                    )
                },

                f,

                indent=4
            )