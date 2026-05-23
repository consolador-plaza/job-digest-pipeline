class Deduplicator:


    def make_key(

        self,

        role,

        company,

        source
    ):


        return (

            role.strip().lower()

            +

            company.strip().lower()

            +

            source.strip().lower()

        )


    def apply(

        self,

        jobs
    ):


        seen = set()

        output = []


        for j in jobs:


            key = self.make_key(

                j.role,

                j.company,

                j.source
            )


            if key in seen:

                continue


            j.unique_key = key


            seen.add(
                key
            )


            output.append(
                j
            )


        return output