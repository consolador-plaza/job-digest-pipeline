from ingest.eml_loader import EMLLoader

from parsers.detector import ParserDetector


loader = EMLLoader()

emails = loader.load_folder()

print(
    "Emails found:",
    len(emails)
)


detector = ParserDetector()


for e in emails:

    print(
        e["file"]
    )

    parser = detector.detect(
        e["message"]
    )

    if parser:

        print(
            parser.SOURCE
        )

    else:

        print(
            "UNKNOWN"
        )