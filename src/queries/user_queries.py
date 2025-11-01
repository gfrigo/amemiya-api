from pypika import MySQLQuery, Table

Users = Table("Users")
Roles = Table("Roles")
Companies = Table("Companies")
Attachments = Table("Attachments")

class User:
    @staticmethod
    def get_data(user_id: int) -> str:
        query = (
            MySQLQuery.from_(Users).select(
                Users.user_id,
                Users.user_name,
                Users.inner_register,
                Users.password,
                Users.email,
                Users.telephone,
                Users.role_id,
                Roles.role_name,
                Users.admin,
                Users.company_id,
                Companies.company_name,
                Attachments.file_data,
                Attachments.file_type,
                Users.active_user
            )
            .left_join(Roles).on(Roles.role_id == Users.role_id)
            .left_join(Companies).on(Companies.company_id == Users.company_id)
            .left_join(Attachments).on(Attachments.attachment_id == Users.profile_picture_id)
            .where(Users.user_id == user_id)
        )

        print(str(query))

        return str(query)
