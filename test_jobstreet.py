from ingest.eml_loader import EMLLoader

from parsers.jobstreet import JobStreetParser


loader = EMLLoader()

emails = loader.load_folder()


for e in emails:

    name = str(
        e["file"]
    )


    if "jobstreet" not in name.lower():

        continue


    parser = JobStreetParser()

    jobs = parser.parse(
        e["message"]
    )


    print(
        "FOUND:",
        len(jobs)
    )


    for j in jobs[:5]:

        print()

        print(
            "ROLE:",
            j.role
        )

        print(
            "COMPANY:",
            j.company
        )

        print(
            "LINK:",
            j.link
        )