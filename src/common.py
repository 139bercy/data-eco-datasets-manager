from datetime import datetime


def format_filename(filename: str, directory="."):
    now = datetime.now()
    return f"{directory}/{now.date()}-{filename}"
