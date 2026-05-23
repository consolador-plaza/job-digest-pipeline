import re
import quopri
from email import message_from_string

from models.job_record import JobRecord
from parsers.base_parser import BaseParser


class LinkedInParser(BaseParser):

    SOURCE = "LinkedIn"


    def should_skip(
        self,
        text
    ):

        t = text.lower().strip()


        STATIC = {
            "",
            "this company is actively hiring",
            "apply with resume & profile",
        }


        if t in STATIC:
            return True


        if "connection" in t:
            return True


        if "company alum" in t:
            return True


        if "company alumni" in t:
            return True


        return False



    def extract_text(self, payload):

        text = ""

        if payload.is_multipart():

            for part in payload.walk():

                if part.get_content_type() == "text/plain":

                    raw = part.get_payload()

                    text = quopri.decodestring(
                        raw
                    ).decode(
                        errors="ignore"
                    )

                    break

        else:

            body = payload.get_body(
                preferencelist=("plain",)
            )

            if body:

                raw = body.get_payload()

                text = quopri.decodestring(
                    raw
                ).decode(
                    errors="ignore"
                )

        # remove quoted-printable soft wraps:
        text = text.replace(
            "=\n",
            ""
        )

        return text


    def parse(self, payload):

        text = self.extract_text(payload)

        timestamp = payload.get(
            "Date",
            ""
        )

        records = []

        lines = [
            line.strip()
            for line in text.splitlines()
        ]

        i = 0

        while i < len(lines):

            line = lines[i]

            if not line.startswith(
                "View job:"
            ):

                i += 1
                continue


            # extract URL
            url = line.replace(
                "View job:",
                ""
            ).strip()


            # LinkedIn quoted-printable continuation lines
            while (

                i + 1 < len(lines)

                and not lines[i + 1].startswith(
                    "------------------------------------------------"
                )

                and lines[i + 1].strip()

            ):

                nxt = lines[i + 1].strip()


                # stop when next job starts
                if nxt == "This company is actively hiring":

                    break

                if nxt == "Apply with resume & profile":

                    break

                if "connection" in nxt.lower():

                    break

                if nxt.startswith(
                    "See all jobs"
                ):

                    break


                i += 1

                url += nxt


            url = url.replace(
                " ",
                ""
            )


            # walk backwards:
            # URL
            # optional flags
            # Location
            # Company
            # Role

            j = i - 1

            block = []

            while j >= 0:

                current = lines[j]

                if (
                    current.startswith(
                        "------------------------------------------------"
                    )
                ):
                    break

                if not self.should_skip(current):

                    block.append(
                        current
                    )

                j -= 1


            block.reverse()


            if len(block) >= 3:

                role = block[-3]
                company = block[-2]
                location = block[-1]

                records.append(

                    JobRecord(

                        timestamp=timestamp,

                        role=role,

                        company=company,

                        source=self.SOURCE,

                        link=url
                    )
                )

            i += 1

        return records