from parsers.linkedin import LinkedInParser

from parsers.jobstreet import JobStreetParser

from parsers.indeed import IndeedParser

from parsers.glassdoor import GlassdoorParser



class ParserDetector:


    def __init__(

        self
    ):


        self.linkedin = (

            LinkedInParser()
        )


        self.jobstreet = (

            JobStreetParser()
        )


        self.indeed = (

            IndeedParser()
        )


        self.glassdoor = (

            GlassdoorParser()
        )


    def detect(

        self,

        payload
    ):


        sender = (

            payload.get(

                "From",

                ""

            )

            .lower()
        )


        if (

            "linkedin"

            in

            sender
        ):


            return self.linkedin


        if (

            "jobstreet"

            in

            sender
        ):


            return self.jobstreet


        if (

            "indeed"

            in

            sender
        ):


            return self.indeed


        if (

            "glassdoor"

            in

            sender
        ):


            return self.glassdoor


        print(
            "NO MATCH"
        )


        return None