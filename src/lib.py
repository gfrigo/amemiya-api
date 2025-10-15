from hashlib import sha256


def get_hash(data: str | bytes | int | float) -> str:
    if not isinstance(data, (str, bytes, int, float)):
        raise TypeError("Invalid data type")

    else:
        if isinstance(data, (int, float)):
            data = str(data)

    return sha256(data.encode()).hexdigest()

if __name__ == "__main__":
    print(get_hash("senhaCerta"))
