import os


tests = [

    "test_linkedin.py",

    "test_indeed.py",

    "test_glassdoor.py",

    "test_jobstreet.py"
]


for t in tests:


    print(
        t
    )


    os.system(

        f"python tests/{t}"
    )