import logging
import pymysql
import config


# Utility method to provide a connection object to the database
def connect_to_database():
    try:
        conn = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user,
                               passwd=config.db_password,
                               db=config.db_name)
        return conn
    except pymysql.MySQLError as e:
        logging.error("Error connecting to the database: %s", e)
        return None


# Utility method to close a connection and a related cursor
# given the connection and the cursor as parameters
def close_connection(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# Test utility method allowing to get the next unused id from the database
# this allows to run tests and write to database without clash against
# existing rows
def get_next_available_row_id_from_db():
    conn = None
    cursor = None
    try:
        # Connect to the database
        conn = connect_to_database()
        if not conn:
            return "Database connection error."

        cursor = conn.cursor()

        try:
            # Execute the SQL query
            sql = f"SELECT MAX(user_id) FROM {config.db_name}.users"
            cursor.execute(sql)

            # Extract the highest row id in database to find next available id
            max_row_id_index_in_db = cursor.fetchone()[0]

            if max_row_id_index_in_db:
                return max_row_id_index_in_db + 1  # provide id that is not already in db
            else:
                return 1

        except pymysql.MySQLError as query_error:
            logging.error(f"Query execution error: {query_error}")

    finally:
        # Close the connection and cursor
        close_connection(conn, cursor)


# utility method allow to get url, browser and user_name from the database
# this allows to run tests and write to database
def get_app_configuration_from_db():
    conn = None
    cursor = None
    try:
        # Connect to the database
        conn = connect_to_database()
        if not conn:
            return "Database connection error."

        cursor = conn.cursor()

        try:
            # Execute the SQL query
            # Retrieve the config data for a specific user_id
            cursor.execute('SELECT user_name, url, browser FROM config WHERE id = %s', (1,))
            config_data = cursor.fetchone()

            if config_data:
                logging.info("---- config_data :: %s", config_data)
                return config_data

        except pymysql.MySQLError as query_error:
            logging.error(f"Query execution error: {query_error}")

    finally:
        # Close the connection and cursor
        close_connection(conn, cursor)


# utility method to create tables users and config
# then to insert into config table initial url, browser and user_name
# this allows to run tests 
def setup_database():
    schema_name = "mydb"
    conn = None
    cursor = None

    try:
        # Establishing a connection to DB
        conn = connect_to_database()
        conn.autocommit(True)

        # Getting a cursor from Database
        cursor = conn.cursor()

        # Creating the "users" table
        create_users_table = f"CREATE TABLE IF NOT EXISTS `{schema_name}`.`users` (" \
                             "`user_id` INT(11) NOT NULL, " \
                             "`user_name` VARCHAR(30) NOT NULL, " \
                             "`creation_date` DATETIME DEFAULT NOW(), " \
                             "CONSTRAINT user_id_pk PRIMARY KEY (user_id));"

        # Creating the "config" table
        create_config_table = f"CREATE TABLE IF NOT EXISTS `{schema_name}`.`config` (" \
                              "`id` INT(11) NOT NULL, " \
                              "`user_name` VARCHAR(30) NOT NULL, " \
                              "`url` VARCHAR(255) NOT NULL, " \
                              "`browser` VARCHAR(2048) NOT NULL, " \
                              "CONSTRAINT u_config UNIQUE (url), " \
                              "CONSTRAINT id_pk PRIMARY KEY (id));"

        # Execute create table queries
        create_table_queries = [
            create_users_table,
            create_config_table,
        ]

        for query in create_table_queries:
            cursor.execute(query)

        logging.info(f"Tables created successfully if not exist already.")

    except pymysql.MySQLError as query_error:
        logging.error(f"Query execution error: {query_error}")

    finally:
        close_connection(conn, cursor)


# populate config table
def populate_config_table():
    schema_name = "mydb"
    conn = None
    cursor = None

    try:
        # Establishing a connection to DB
        conn = connect_to_database()
        conn.autocommit(True)

        # Getting a cursor from Database
        cursor = conn.cursor()

        # Data to be inserted
        insert_data = {
            'id': '1',
            'url': 'http://127.0.0.1:5003/users/',
            'user_name': 'john',
            'browser': 'Chrome'
        }

        try:
            select_query = "SELECT url, user_name FROM config WHERE url = %s AND user_name = %s"
            cursor.execute(select_query, ('http://127.0.0.1:5003/users/', 'john'))
            result = cursor.fetchone()
            if not result:
                try:
                    insert_query = " INSERT INTO config (id, url, user_name, browser) VALUES (%s,%s, %s, %s) "
                    # Execute the SQL query
                    # Retrieve the config data for a specific user_id
                    cursor.execute(insert_query, (
                        insert_data['id'], insert_data['url'], insert_data['user_name'], insert_data['browser']))
                    conn.commit()

                    logging.info("data inserted into config table")

                except pymysql.MySQLError as query_error:
                    logging.error(f"Query execution error with error: {query_error}")

        except pymysql.MySQLError as query_error:
            logging.error   (f"Query execution error: {query_error}")

    except pymysql.MySQLError as query_error:
        logging.error(f"Query execution error: {query_error}")

    finally:
        close_connection(conn, cursor)


def delete_all_rows(table_name):
    conn = None
    cursor = None
    schema_name = "mydb"

    try:
        # Connect to the database
        conn = connect_to_database()
        if not conn:
            return "Database connection error."

        cursor = conn.cursor()

        try:
            # Delete all rows from the specified table
            delete_query = f"DELETE FROM `{schema_name}`.`{table_name}`;"
            cursor.execute(delete_query)
            conn.commit()

        except pymysql.MySQLError as query_error:
            logging.error(f"Query execution error: {query_error}")

    finally:
        # Close the connection and cursor
        close_connection(conn, cursor)
