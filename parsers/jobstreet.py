import re

from bs4 import BeautifulSoup

from models.job_record import JobRecord

from parsers.base_parser import BaseParser



class JobStreetParser(

    BaseParser
):


    SOURCE = "JobStreet"

    EXCLUDE = {

        "view all matching jobs",

        "contact us",

        "manage alerts",

        "unsubscribe",

        "explore now",

        "edit this alert",

        "unsubscribe from this alert",

        "ph.jobstreet.com"
    }

    def extract_html(

        self,

        payload
    ):


        if payload.is_multipart():

            for part in payload.walk():

                if (

                    part.get_content_type()

                    ==

                    "text/html"
                ):

                    return part.get_content()


        body = payload.get_body(

            preferencelist=(

                "html",

            )

        )


        if body:

            return body.get_content()


        return ""


    def split_text(

        self,

        text
    ):


        lines = [

            x.strip()

            for x in text.splitlines()

            if x.strip()
        ]


        role = ""


        company = "UNKNOWN"


        if len(lines) >= 1:

            role = lines[0]


        if len(lines) >= 2:

            company = lines[1]


        return (

            role,

            company
        )


    def parse(

        self,

        payload
    ):


        html = self.extract_html(
            payload
        )


        soup = BeautifulSoup(

            html,

            "lxml"
        )


        records = []


        timestamp = payload.get(
            "Date",
            ""
        )


        links = soup.find_all(

            "a",

            href=True
        )


        seen = set()


        for link in links:


            href = link.get(
                "href"
            )


            text = link.get_text(

                "\n",

                strip=True
            )


            if len(text) < 10:

                continue


            role, company = (

                self.split_text(
                    text
                )
            )


            if not role:

                continue

            if (

                role.lower()

                in

                self.EXCLUDE
            ):

                continue

            key = (

                role

                +

                company
            )


            if key in seen:

                continue


            seen.add(
                key
            )


            records.append(

                JobRecord(

                    timestamp=timestamp,

                    role=role,

                    company=company,

                    source=self.SOURCE,

                    link=href
                )

            )


        return records