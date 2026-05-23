from dataclasses import dataclass

from email.utils import parsedate_to_datetime



@dataclass

class JobRecord:


    timestamp: str

    role: str

    company: str

    source: str

    link: str

    unique_key: str = ""

    gmail_id: str = ""


    def __post_init__(

        self
    ):


        try:


            self.timestamp = (

                parsedate_to_datetime(

                    self.timestamp
                )

                .isoformat(
                    timespec="seconds"
                )
            )


        except:


            pass