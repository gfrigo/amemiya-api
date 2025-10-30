fetch: dict = {
    "user": {
        "table": "Users",
        "selection": "*",
        "filter": {
            "active_user": ("active_user = 1", )
        }
    },
    "vehicle": {
        "table"
    }
}

add: dict = {
    "user": {
        "table": "Users",
        "fields": ("user_name", "inner_register", "password", "email", "telephone", "role_id", "admin", "company_id", "profile_picture_id", "active_user")
    },
    "vehicle": {
        "table": ""
    }
}

edit: dict = {
    "user": {
        "table": "Users",
        "fields": ("user_name", "inner_register", "password", "email", "telephone", "role_id", "admin", "company_id", "profile_picture_id", "active_user")
    },
    "vehicle": {
        "table": "Vehicle",
        "fields": ("name", "license_plate", "brand", "model", "year", "notes", "last_used", "last_user_id", "active")
    }
}

remove: dict = {
    "user": {
        "table": "Users"
    },
    "vehicle": {
        "table": ""
    }
}
