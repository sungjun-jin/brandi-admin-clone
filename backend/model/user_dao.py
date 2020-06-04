import pymysql
import datetime

class UserDao:

    def insert_seller_key(self, new_user, db_connection):
        cursor = db_connection.cursor()

        seller_key_insert_sql = """
        INSERT INTO seller_keys(
            user
        ) VALUES (
            %(user)s
            )
        """
        cursor.execute(seller_key_insert_sql, new_user)

    def insert_seller(self, new_user, db_connection):
        cursor = db_connection.cursor()

        seller_insert_sql =  """
                INSERT INTO sellers (
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
                    ) VALUES (
                        (SELECT id FROM seller_keys WHERE user = %(user)s),
                        2,
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
        SELECT count(user)
        FROM seller_keys 
        WHERE user = %(user)s
        """

        cursor.execute(check_user_sql,new_user)
        user = cursor.fetchone()
        return user

    def check_user(self, get_user, db_connection):
        cursor = db_connection.cursor()

        check_user_sql = """
        SELECT id, user 
        FROM seller_keys 
        WHERE user = %(user)s
        """

        cursor.execute(check_user_sql, get_user)
        user = cursor.fetchone()
        return user 

    def check_password(self, get_user, db_connection):
        cursor = db_connection.cursor()
        check_pw_sql = """
        SELECT password, 
            authority_id 
        FROM sellers 
        WHERE seller_key_id = 
            (SELECT id 
            FROM seller_keys 
            WHERE user = %(user)s)
        """
        
        cursor.execute(check_pw_sql, get_user)
        password = cursor.fetchone()
        return password


    def get_seller_infos(self, user, db_connection):
        cursor = db_connection.cursor(pymysql.cursors.DictCursor)
        seller_infos_get_sql = """
        SELECT
            sellers.id, 
            seller_key_id,
            auth.name AS authorization,
            sellers.is_deleted,
            attributes.name AS attribute,
            profile,
            status.name,
            sellers.name AS kor_name,
            eng_name,
            user.user AS user_id,
            background_image,
            simple_introduction,
            detail_introduction,
            site_url,         
            service_number,          
            zip_code,        
            address,
            detail_address,
            bank,
            account_owner,
            bank_account,
            shipping_information,
            refund_information,
            model_height,
            model_size_top,
            model_size_bottom,
            model_size_foot,
            feed_message
        FROM sellers
        INNER JOIN authorities AS auth ON sellers.authority_id = auth.id
        INNER JOIN seller_attributes AS attributes ON sellers.seller_attribute_id = attributes.id
        INNER JOIN seller_status AS status ON sellers.seller_status_id = status.id
        INNER JOIN seller_keys AS user ON sellers.seller_key_id = user.id        
        WHERE seller_key_id = %s AND end_date = '2037-12-31 23:59:59';
        """
        cursor.execute(seller_infos_get_sql, user)
        return cursor.fetchall()
        

    def get_supervisor_infos(self, user, db_connection):
        cursor = db_connection.cursor(pymysql.cursors.DictCursor)
        supervisor_infos_get_sql = """
        SELECT * 
        FROM supervisor_infos        
        WHERE seller_id = (SELECT id FROM sellers WHERE seller_key_id = %s AND end_date = '2037-12-31 23:59:59');        
        """
        cursor.execute(supervisor_infos_get_sql, user)
        return cursor.fetchall()

    def get_buisness_hours(self, user, db_connection):
        cursor = db_connection.cursor(pymysql.cursors.DictCursor)
        buisness_hours_get_sql = """
        SELECT * 
        FROM buisness_hours        
        WHERE seller_id = (SELECT id FROM sellers WHERE seller_key_id = %s AND end_date = '2037-12-31 23:59:59');        
        """
        cursor.execute(buisness_hours_get_sql, user)
        return cursor.fetchall()
    
    def get_seller_histories(self, user, db_connection):
        cursor = db_connection.cursor(pymysql.cursors.DictCursor)
        seller_histories_get_sql = """
        SELECT 
            start_date,
            status.name
        FROM sellers
        INNER JOIN seller_status AS status ON sellers.seller_status_id = status.id
        WHERE seller_key_id = %s;         
        """
        cursor.execute(seller_histories_get_sql, user)
        return cursor.fetchall()

    def register_seller(self, seller_infos, db_connection):
        cursor = db_connection.cursor()
        seller_register_sql = """
        UPDATE sellers 
        SET 
            profile=%(profile)s,
            background_image=%(background_image)s,
            simple_introduction=%(simple_introduction)s,
            detail_introduction=%(detail_introduction)s 
        WHERE seller_key_id=%(seller_key_id)s;
        """
        cursor.execute(seller_register_sql, seller_infos)


    def get_sellerlist(self, db_connection):
        cursor = db_connection.cursor(pymysql.cursors.DictCursor)
        sellers_list_sql = """
        SELECT
            sellers.id, 
            seller_keys.user,
            sellers.eng_name,
            sellers.name,
            seller_attributes.id,
            seller_attributes.name,
            seller_status.id,
            seller_status.name,
            supervisor_infos.name,
            supervisor_infos.phone_number,
            supervisor_infos.email,
            (SELECT COUNT('product_keys.product_number') 
                FROM product_keys 
                WHERE sellers.seller_key_id = product_keys.seller_key_id) as number_of_product,
            sellers.site_url,
            DATE_FORMAT(start_date, '%Y-%m-%d %H:%i:%s') AS created_at
        FROM sellers
        INNER JOIN seller_keys ON sellers.seller_key_id = seller_keys.id
        INNER JOIN seller_status ON sellers.seller_status_id = seller_status.id
        INNER JOIN seller_attributes ON sellers.seller_attribute_id = seller_attributes.id
        LEFT JOIN `supervisor_infos` ON supervisor_infos.seller_id = sellers.id AND supervisor_infos.order=1
        LEFT JOIN product_keys ON sellers.seller_key_id = product_keys.seller_key_id
        WHERE end_date = '2037-12-31 23:59:59' and authority_id = 2
        ORDER BY sellers.id DESC;
        """
        cursor.execute(sellers_list_sql)
        sellers = cursor.fetchall()
        return sellers

    def get_seller_action(self, db_connection):
        cursor = db_connection.cursor()
        seller_actions_sql = """
        SELECT seller_status_id, action_type
        FROM seller_actions
        """
        cursor.execute(seller_actions_sql)
        seller_actions = cursor.fetchall()
        return seller_actions


