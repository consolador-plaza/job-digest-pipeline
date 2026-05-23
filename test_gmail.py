from ingest.gmail_loader import GmailLoader


loader = GmailLoader()


emails = loader.load(

    "label:Jobs newer_than:30d"
)


print(
    "FOUND:",
    len(emails)
)


for e in emails[:10]:


    print("\n----------------")


    print(
        "FROM:",
        e.get(
            "From"
        )
    )


    print(
        "SUBJECT:",
        e.get(
            "Subject"
        )
    )