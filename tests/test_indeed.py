from pathlib import Path
import sys

sys.path.append(
    str(
        Path(__file__).parent.parent
    )
)

from ingest.eml_loader import EMLLoader
from parsers.indeed import IndeedParser


loader = EMLLoader()
parser = IndeedParser()


emails = loader.load_folder(
    "fixtures/indeed"
)


assert len(emails) > 0


for e in emails:

    jobs = parser.parse(
        e["message"]
    )

    assert len(jobs) > 0

    for j in jobs:

        assert j.role
        assert j.company


print(
    "INDEED PASS"
)