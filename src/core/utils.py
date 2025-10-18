from fastapi import HTTPException
from hashlib import sha256


def get_hash(data: str | bytes | int | float) -> str:
    if not isinstance(data, (str, bytes, int, float)):
        raise TypeError("Invalid data type")

    else:
        if isinstance(data, (int, float)):
            data = str(data)

    return sha256(data.encode()).hexdigest()


def check_missing_fields(data: dict, required_fields: list) -> None:
    """
    Checks for missing required fields in the provided data dictionary.

    Args:
        data (dict): The data dictionary to check.
        required_fields (list): A list of required field names.

    Raises:
        HTTPException: If any required field is missing, with status 400.
    """
    missing = [field for field in required_fields if not data.get(field)]

    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Request missing required field(s): {', '.join(missing)}"
        )
