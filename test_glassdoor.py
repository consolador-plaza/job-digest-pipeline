from ingest.eml_loader import EMLLoader

from parsers.glassdoor import GlassdoorParser


loader = EMLLoader()

emails = loader.load_folder()


for e in emails:

    name = str(
        e["file"]
    )


    if "glassdoor" not in name.lower():

        continue


    parser = GlassdoorParser()


    jobs = parser.parse(

        e["message"]
    )


    print(
        "FOUND:",
        len(jobs)
    )


    for j in jobs[:10]:

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