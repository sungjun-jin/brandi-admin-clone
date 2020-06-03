class UserDao:

    def insert_seller_key(self, new_user, db_connection):
        cursor = db_connection.cursor()

        seller_key_insert_sql = """
        insert into seller_keys(
            user
        ) values (
            %(user)s
            )
        """
        cursor.execute(seller_key_insert_sql, new_user)

    def insert_seller(self, new_user, db_connection):
        cursor = db_connection.cursor()

        seller_insert_sql =  """
                insert into sellers (
                    seller_key_id,
                    authority_id,
                    seller_attribute_id,
                    seller_status_id,
                    password,
                    phone_number,
                    name,
                    eng_name,
                    service_number,
                    site_url,
                    editor,
                    start_date,
                    end_date
                    ) values (
                        (select id from seller_keys where user = %(user)s),
                        1,
                        %(seller_attribute_id)s,
                        1,
                        %(password)s,
                        %(phone_number)s,
                        %(name)s,
                        %(eng_name)s,
                        %(service_number)s,
                        %(site_url)s,
                        %(user)s,
                        now(),
                        '2037-12-31 23:59:59'
                        );
                        """
       
        cursor.execute(seller_insert_sql, new_user)

    def check_user_exists(self, new_user, db_connection):
        cursor = db_connection.cursor()

        check_user_sql = """
        select count(user)
        from seller_keys 
        where user = %(user)s
        """

        cursor.execute(check_user_sql,new_user)
        user = cursor.fetchone()
        return user

    def check_user(self, get_user, db_connection):
        cursor = db_connection.cursor()

        check_user_sql = """
        select id, user from seller_keys where user = %(user)s
        """

        cursor.execute(check_user_sql, get_user)
        user = cursor.fetchone()
        return user 

    def check_password(self, get_user, db_connection):
        cursor = db_connection.cursor()
        check_pw_sql = """
        select password, authority_id from sellers where seller_key_id = (select id from seller_keys where user = %(user)s)
        """
        
        cursor.execute(check_pw_sql, get_user)
        password = cursor.fetchone()
        return password

