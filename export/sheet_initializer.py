class SheetInitializer:


    def ensure(

        self,

        book
    ):


        sheets = [

            "Daily Job Digest",

            "RunHistory",

            "ParserHealth"
        ]


        existing = [

            s.title

            for s

            in

            book.worksheets()
        ]


        for name in sheets:


            if name not in existing:


                book.add_worksheet(

                    title=name,

                    rows=1000,

                    cols=20
                )