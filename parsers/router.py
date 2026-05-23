from parsers.detector import ParserDetector


class ParserRouter:


    def __init__(self):

        self.detector = ParserDetector()


    def parse_email(

        self,

        payload
    ):


        parser = self.detector.detect(
            payload
        )


        if not parser:

            return []


        return parser.parse(
            payload
        )