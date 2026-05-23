from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build

from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials


import os

import base64


from email import (

    message_from_bytes,

    policy
)



SCOPES = [

    "https://www.googleapis.com/auth/gmail.modify"
]



class GmailLoader:


    def authenticate(

        self
    ):


        creds = None


        #
        # existing token
        #

        if os.path.exists(
            "token.json"
        ):


            creds = (

                Credentials

                .from_authorized_user_file(

                    "token.json",

                    SCOPES
                )
            )


        #
        # refresh / first login
        #

        if (

            creds is None

            or

            not creds.valid
        ):


            if (

                creds

                and

                creds.expired

                and

                creds.refresh_token
            ):


                creds.refresh(
                    Request()
                )


            else:


                flow = (

                    InstalledAppFlow

                    .from_client_secrets_file(

                        "credentials.json",

                        SCOPES
                    )
                )


                creds = (

                    flow.run_local_server(
                        port=0
                    )
                )


            #
            # save token
            #

            with open(

                "token.json",

                "w"
            ) as f:


                f.write(
                    creds.to_json()
                )


        service = build(

            "gmail",

            "v1",

            credentials=creds
        )


        return service



    def load(

        self,

        query
    ):


        service = self.authenticate()


        result = (

            service

            .users()

            .messages()

            .list(

                userId="me",

                q=query
            )

            .execute()
        )


        messages = result.get(

            "messages",

            []
        )


        output = []


        for m in messages:


            raw_msg = (

                service

                .users()

                .messages()

                .get(

                    userId="me",

                    id=m["id"],

                    format="raw"
                )

                .execute()
            )


            raw = (

                base64

                .urlsafe_b64decode(

                    raw_msg[
                        "raw"
                    ]
                )
            )


            email_msg = (

                message_from_bytes(

                    raw,

                    policy=policy.default
                )
            )


            output.append(

                {

                    "id": m["id"],

                    "message": email_msg
                }
            )
        

        return output
    
    def get_label_id(

        self,

        name
    ):


        service = self.authenticate()


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


            if l["name"] == name:

                return l["id"]


        return None
    
    def move_label(

        self,

        message_id,

        target
    ):


        service = self.authenticate()


        target_id = self.get_label_id(
            target
        )


        jobs_id = self.get_label_id(
            "Jobs"
        )


        if target_id is None:

            print(
                "LABEL NOT FOUND"
            )

            return


        body = {


            "addLabelIds": [

                target_id
            ]
        }


        if jobs_id:

            body[

                "removeLabelIds"

            ] = [

                jobs_id
            ]


        service.users().messages().modify(

            userId="me",

            id=message_id,

            body=body

        ).execute()