import yaml



with open(

    "config/settings.yaml",

    "r",

    encoding="utf8"
) as f:


    CONFIG = yaml.safe_load(
        f
    )