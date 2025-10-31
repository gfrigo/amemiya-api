from pypika import MySQLQuery, Table

Users = Table("Users")
Roles = Table("Roles")
Companies = Table("Companies")

class User:
    @staticmethod
    def get_data(user_id: int) -> str:
        query = (
            MySQLQuery.from_(Users).select(
                Users.user_name,
                Users.inner_register,
                Users.email,
                Users.telephone,
                Roles.role_name,
                Users.admin,
                Companies.company_name,
                Users.profile_picture_id
            )
            .left_join(Roles).on(Roles.role_id == Users.role_id)
            .left_join(Companies).on(Companies.company_id == Users.company_id)
            .where(Users.user_id == user_id)
        )

        print(str(query))

        return str(query)
