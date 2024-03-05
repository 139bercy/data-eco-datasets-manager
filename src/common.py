from datetime import datetime


def format_filename(filename: str, directory=".", date=None):
    now = date or datetime.now().date()
    return f"{directory}/{now}-{filename}"
