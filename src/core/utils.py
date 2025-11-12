from hashlib import sha256
from reverse_geocode import search


def get_hash(data: str | bytes | int | float) -> str:
    if not isinstance(data, (str, bytes, int, float)):
        raise TypeError("Invalid data type")

    else:
        if isinstance(data, (int, float)):
            data = str(data)

    return sha256(data.encode()).hexdigest()

def get_geocode_data(latitude: float, longitude: float) -> dict:
    coordinates = latitude, longitude

    return search([coordinates])[0]