from ingest.gmail_loader import GmailLoader


loader = GmailLoader()

service = loader.authenticate()


labels = (

    service

    .users()

    .labels()

    .list(

        userId="me"
    )

    .execute()
)


for l in labels.get(

    "labels",

    []
):

    print(

        l["name"],

        " -> ",

        l["id"]
    )