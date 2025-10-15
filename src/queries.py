class User:
    @staticmethod
    def get_data(user_id: int) -> str:
        return f"""
        SELECT
            u.name AS name, 
            u.innerRegister AS innerRegister, 
            u.email AS email, 
            u.telephone AS telephone, 
            r.roleName AS roleName, 
            u.admin AS admin, 
            c.companyName,
            u.imagePath
        FROM Users u
        LEFT JOIN Roles r ON r.roleId = u.roleId
        LEFT JOIN Companies c ON c.companyId = u.companyId
        WHERE u.id = {user_id};
        """