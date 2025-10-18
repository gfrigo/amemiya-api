from src.register import Register
from src.core.database import Execute
from src.queries import user_queries


class LoginRepository:

    @staticmethod
    def get_access(cursor, user: str, password: str) -> dict:
        users_data = Register.fetch(cursor, "user", "active_user = 1")

        for user_entry in users_data:
            if user_entry[1] == user and user_entry[3] == password:
                return {"access": True, "user_id": user_entry[0]}

        return {"access": False, "user_id": None}

    @staticmethod
    def get_user_data(cursor, user_id) -> dict:
        if not user_id:
            return {"access": False, "data": None}

        user_data = Execute.Select.from_string(cursor, user_queries.User.get_data(user_id))[0]

        print(user_data)

        if user_data:
            return {
                "access": True,
                "data": {
                    "user_name": user_data[0],
                    "inner_register": user_data[1],
                    "email": user_data[2],
                    "telephone": user_data[3],
                    "role_name": user_data[4],
                    "admin": user_data[5],
                    "company_name": user_data[6],
                    "image_path": user_data[7]
                }
            }

        return {"access": False, "data": None}
