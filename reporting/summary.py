class RunSummary:


    def __init__(

        self
    ):


        self.emails = 0

        self.raw = 0

        self.inserted = 0

        self.failed = 0

        self.duplicates = 0


    def print_summary(

        self
    ):


        print()

        print(
            "====== RUN SUMMARY ======"
        )

        print(
            "Emails:",
            self.emails
        )

        print(
            "Raw:",
            self.raw
        )

        print(
            "Inserted:",
            self.inserted
        )

        print(
            "Duplicates:",
            self.duplicates
        )

        print(
            "Failed:",
            self.failed
        )