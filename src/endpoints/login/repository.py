from src.register import Register
from src.core.database import Execute
from src.queries import user_queries
from base64 import b64encode


class LoginRepository:

    @staticmethod
    def get_access(cursor, email: str, password: str) -> dict:
        users_data = Register.fetch(cursor, "user", "active_user = 1")

        for user_entry in users_data:
            if user_entry[4] == email and user_entry[3] == password:
                return {"access": True, "user_id": user_entry[0]}

        return {"access": False, "user_id": None}

    @staticmethod
    def get_user_data(cursor, user_id) -> dict:
        if not user_id:
            return {"access": False, "data": None}

        user_data = Execute.Select.from_string(cursor, user_queries.User.get_data(user_id))[0]

        print(user_data)

        user_id, user_name, inner_register, _,  email, telephone, role_id, role_name, admin, company_id, company_name, picture_data, picture_type, active_user = user_data

        encoded_picture_data = b64encode(picture_data).decode("utf-8")

        if user_data:
            if not active_user:
                return {"access": False, "data": None}

            return {
                "access": True,
                "data": {
                    "user_id": user_id,
                    "user_name": user_name,
                    "inner_register": inner_register,
                    "email": email,
                    "telephone": telephone,
                    "role_name": role_name,
                    "admin": True if admin == 1 else False,
                    "company_name": company_name,
                    "profile_picture": encoded_picture_data
                }
            }

        return {"access": False, "data": None}
