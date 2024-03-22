from datetime import datetime


def format_filename(filename: str, directory=".", date=None):
    now = date or datetime.now().date()
    return f"{directory}/{now}-{filename}"


def make_bytes_size_human_readable(bytes_size: int):
    if bytes_size is None or bytes_size == 0:
        return
    converted_size = bytes_size
    unites = ['octets', 'Ko', 'Mo', 'Go', 'To']
    index = 0
    while converted_size >= 1000 and index < len(unites)-1:
        converted_size /= 1000.0
        index += 1
    return f"{converted_size:.2f} {unites[index]}"
