from models.job_record import JobRecord


class Validator:


    def validate(

        self,

        record: JobRecord
    ):


        errors = []


        if not record.role:

            errors.append(
                "Missing Role"
            )


        if not record.company:

            errors.append(
                "Missing Company"
            )


        return errors