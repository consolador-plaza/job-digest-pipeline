from parsers.linkedin import LinkedInParser

from parsers.jobstreet import JobStreetParser

from parsers.indeed import IndeedParser

from parsers.glassdoor import GlassdoorParser



class ParserDetector:


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


        subject = (

            payload.get(

                "Subject",

                ""
            )

            .lower()
        )


        print()


        #
        # LinkedIn
        #

        if (

            "linkedin"

            in

            sender
        ):



            return LinkedInParser()


        #
        # JobStreet
        #

        if (

            "jobstreet"

            in

            sender
        ):



            return JobStreetParser()


        #
        # Indeed
        #

        if (

            "indeed"

            in

            sender
        ):



            return IndeedParser()


        #
        # Glassdoor
        #

        if (

            "glassdoor"

            in

            sender
        ):


            return GlassdoorParser()


        print(
            "NO MATCH"
        )


        return None