from bs4 import BeautifulSoup

from models.job_record import JobRecord
from parsers.base_parser import BaseParser


class IndeedParser(BaseParser):

    SOURCE = "Indeed"

    def extract_html(self, payload):

        if payload.is_multipart():

            for part in payload.walk():

                if (
                    part.get_content_type()
                    ==
                    "text/html"
                ):

                    return part.get_content()

        return ""


    def parse(self, payload):

        html = self.extract_html(
            payload
        )

        soup = BeautifulSoup(
            html,
            "lxml"
        )

        timestamp = payload.get(
            "Date",
            ""
        )

        records = []

        seen = set()

        jobs = soup.find_all(
            "h2"
        )

        for job in jobs:

            link_tag = job.find(
                "a",
                href=True
            )

            if not link_tag:
                continue

            role = (
                link_tag.get_text(
                    strip=True
                )
            )

            url = (
                link_tag[
                    "href"
                ]
            )

            company = "UNKNOWN"

            parent = job.parent

            company_td = parent.find_next(
                "td"
            )

            if company_td:

                txt = company_td.get_text(
                    " ",
                    strip=True
                )

                if txt and len(
                    txt
                ) < 80:

                    company = txt

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

                    link=url
                )

            )

        return records