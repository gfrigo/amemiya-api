class User:
    @staticmethod
    def get_data(user_id: int) -> str:
        return f"""
        SELECT
            u.user_name AS user_name, 
            u.inner_register AS inner_register, 
            u.email AS email, 
            u.telephone AS telephone, 
            r.role_name AS role_name, 
            u.admin AS admin, 
            c.company_name AS company_name,
            u.image_path AS image_path
        FROM Users u
        LEFT JOIN Roles r ON r.role_id = u.role_id
        LEFT JOIN Companies c ON c.company_id = u.company_id
        WHERE u.user_id = {user_id};
        """