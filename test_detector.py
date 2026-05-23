from parsers.detector import (

    ParserDetector
)



detector = ParserDetector()


samples = [

    "JobStreet Alert",

    "LinkedIn jobs",

    "Indeed alert",

    "Glassdoor jobs"
]


for s in samples:


    parser = detector.detect(
        s
    )


    print(

        s,

        parser.SOURCE
    )