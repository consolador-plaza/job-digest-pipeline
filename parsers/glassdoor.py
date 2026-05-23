from bs4 import BeautifulSoup
from urllib.parse import quote_plus

import re
import quopri

from models.job_record import JobRecord
from parsers.base_parser import BaseParser


class GlassdoorParser(BaseParser):

    SOURCE = "Glassdoor"

    ROLE_PATTERN = re.compile(
        r"\b("
        r"analyst|engineer|scientist|developer|manager|"
        r"specialist|consultant|architect|associate"
        r")\b",
        re.I
    )

    SKIP = {
        "easy apply",
        "employer est.",
        "(",
        ")",
    }

    LOCATION_PATTERN = re.compile(
        r"(city|makati|ortigas|quezon)",
        re.I
    )


    def extract_html(
        self,
        payload
    ):

        raw = payload.get_content()


        # remove quoted-printable wraps first
        raw = raw.replace(
            "=\r\n",
            ""
        )

        raw = raw.replace(
            "=\n",
            ""
        )


        # decode quoted-printable
        raw = quopri.decodestring(
            raw.encode()
        ).decode(
            "utf-8",
            errors="ignore"
        )


        return raw


    def clean(
        self,
        text
    ):

        return re.sub(
            r"\s+",
            " ",
            text
        ).strip()


    def is_role(
        self,
        text
    ):

        return bool(
            self.ROLE_PATTERN.search(
                text
            )
        )


    def is_metadata(
        self,
        text
    ):

        text = text.strip().lower()


        # ratings:
        # 3.6 ★
        if re.match(
            r"^\d+(\.\d+)?\s*★$",
            text
        ):
            return True


        # age:
        # 4d / 2h / 1w
        if re.match(
            r"^\d+\s*[dhwm]$",
            text
        ):
            return True


        skip = {

            "easy apply",

            "best place to work",

            "remote",

            "hybrid",

            "onsite",

            "dayshift",

            "night shift",

            "mid shift",

            "hmo on day 1"

        }


        return text in skip


    def build_search_url(
        self,
        role,
        company
    ):

        query = (

            f'site:glassdoor.com '
            f'"{role}" '
            f'"{company}"'

        )

        return (

            "https://www.google.com/search?q="
            + quote_plus(
                query
            )

        )

    def resolve_glassdoor_link(
        self,
        role,
        company
    ):

        #
        # role + company
        #
        text = (
            f"{role} {company}"
        )


        # remove special chars:
        # &, $, %, ^, |
        text = re.sub(
            r"[^A-Za-z0-9\s-]",
            "",
            text
        )


        # spaces -> dash
        slug = "-".join(
            text.split()
        )


        #
        # Glassdoor SEO:
        #
        # /Job/quezon-city-<slug>-jobs-
        # SRCH_IL.0,11_IC4778230_KO12,<len>.htm
        #
        full_slug = (
            f"quezon-city-{slug}"
        )


        length = len(
            full_slug
        )


        return (

            "https://www.glassdoor.com/Job/"

            f"{full_slug}"

            "-jobs-"

            "SRCH_IL.0,11_"

            "IC4778230_"

            f"KO12,{length}.htm"

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

        seen = set()


        #
        # Glassdoor wrapper cards
        #
        cards = soup.select(
            "a[href*='jobListing.htm']"
        )


        for card in cards:


            lines = [

                self.clean(

                    x.get_text(
                        " ",
                        strip=True
                    )

                )

                for x in card.find_all()

                if x.get_text(
                    strip=True
                )

            ]


            lines = [

                x

                for x in lines

                if x.lower()
                not in self.SKIP

            ]


            role = None
            company = None


            for i, line in enumerate(
                lines
            ):


                if not self.is_role(
                    line
                ):

                    continue


                role = line


                prev = i - 1


                while prev >= 0:

                    candidate = lines[
                        prev
                    ]


                    #
                    # ratings / age /
                    # Easy Apply / badges
                    #
                    if self.is_metadata(
                        candidate
                    ):

                        prev -= 1

                        continue


                    #
                    # locations
                    #
                    if self.LOCATION_PATTERN.search(
                        candidate
                    ):

                        prev -= 1

                        continue


                    company = candidate

                    break


                break


            if not role:
                continue


            key = (
                role,
                company
            )


            if key in seen:
                continue


            seen.add(
                key
            )


            records.append(

                JobRecord(

                    timestamp=payload.get(
                        "Date",
                        ""
                    ),

                    role=role,

                    company=company
                    or "UNKNOWN",

                    source=self.SOURCE,

                    link=self.resolve_glassdoor_link(
                        role,
                        company
                        or ""
                        )

                )

            )


        return records