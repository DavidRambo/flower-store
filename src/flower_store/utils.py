import os
import secrets


def image_rename(obj, file_data) -> str:
    """Generates a name for a file being uploaded."""
    # Randomly rename image to avoid name clashes.
    random_hex = secrets.token_hex(6)

    # Get file extension from uploaded picture.
    f_name, f_ext = os.path.splitext(file_data.filename)

    # Total string must be no greater than 30 characters.
    curr_len = len(f_name) + len(random_hex) + len(f_ext) + 1
    if curr_len > 30:
        # Trim off excess characters from f_name portion
        to_trim = 30 - curr_len
        f_name = f_name[: to_trim + 1]

    upload_name = f_name + "_" + random_hex + f_ext

    return upload_name
