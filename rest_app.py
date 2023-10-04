import logging
import os
import platform
import signal

import pymysql
from flask import Flask, jsonify, request

import config
from db_connector import connect_to_database, close_connection, get_next_available_row_id_from_db, setup_database, \
    populate_config_table

app = Flask(__name__)

# Configure logging formatting
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

log = logging.getLogger(__name__)


# A simple method route API for backend app
# combining the default path and a given user id to create the url
@app.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def get_user(user_id):
    # For a GET we only need the user id to retrieve the user's name
    # and return in a json with success code 200
    # otherwise return no such user error with code 500
    if request.method == 'GET':

        log.info("Entered GET method call")

        conn = None
        cursor = None
        try:
            # Connect to the database
            conn = connect_to_database()
            if not conn:
                return "Database connection error."

            log.info("connected to database...")
            cursor = conn.cursor()

            try:
                log.debug(f"retrieve user with user_id = %s ;", user_id)
                cursor.execute(f"SELECT * FROM {config.db_name}.users WHERE user_id = %s;", user_id)
                result = cursor.fetchone()

                if result:
                    logging.debug(f"retrieve user with user_id = %s has been retrieved;", user_id)
                    # return jsonify(result)  # Return the result as JSON
                    return jsonify({"status": "ok", "user_name": result[1]}), 200

                else:
                    log.debug(f"User with id %s does not exist;", user_id)
                    return jsonify({"status": "error", "reason": "no such user_id"}), 500

            except pymysql.MySQLError as query_error:
                log.error(f"Query execution error: {query_error}")

        finally:
            log.info("close all connections")
            # Close the connection and cursor
            close_connection(conn, cursor)

    # For a PUT we need the user id and the payload containing the user's name
    # data required to update an existing user
    # we first check if user exists, if not return error with 500
    # otherwise update existing
    if request.method == 'PUT':
        log.info("Entered PUT method call")

        conn = None
        cursor = None

        try:
            # Getting the JSON data payload from request
            request_data = request.json
            user_name = request_data.get('user_name')

            # Connect to the database
            conn = connect_to_database()
            if not conn:
                return jsonify({"status": "error", "reason": "Database connection error."}), 500

            log.info("connected to database...")
            cursor = conn.cursor()

            # Check if user_id exists
            cursor.execute(f"SELECT user_id FROM {config.db_name}.users WHERE user_id = %s", (user_id,))
            existing_user = cursor.fetchone()

            if not existing_user:
                log.warning("Can't update user with id  %s that does not exist", user_id)
                return jsonify({"status": "error", "reason": "no such id."}), 500
            else:
                # Using parameterized query to prevent SQL injection
                update_query = f"UPDATE {config.db_name}.users SET name = %s WHERE user_id = %s"
                cursor.execute(update_query, (user_name, user_id))
                conn.commit()
                log.debug("Update user ...with id %s", user_id)
                return jsonify({"status": "ok", "user_updated": user_name}), 200

        except pymysql.MySQLError as query_error:
            conn.rollback()
            log.error(f"Query execution error: {query_error}")
            return jsonify({"status": "error", "reason": "Database error."}), 500

        except Exception as exception:
            log.error(f"Query execution error: {exception}")
            return jsonify({"status": "error", "reason": "An error occurred."}), 500

        finally:
            log.debug("Close all connections")
            # Close the connection and cursor
            close_connection(conn, cursor)

    # For a DELETE we only need the user id from the path parameter
    # data required to delete an existing user
    # we first check if user exists, if not return error with code 500
    # otherwise delete existing user
    if request.method == 'DELETE':
        log.info("Entered DELETE method call")
        conn = None
        cursor = None

        try:
            conn = connect_to_database()
            if not conn:
                return jsonify({"status": "error", "reason": "Database connection error."}), 500

            log.info("connected to database...")
            cursor = conn.cursor()

            query = f"SELECT user_id FROM {config.db_name}.users WHERE user_id = %s"
            cursor.execute(query, user_id)
            existing_user = cursor.fetchone()

            if not existing_user:
                return jsonify({"status": "error", "reason": "no such id."}), 500
            else:
                delete_query = f"DELETE FROM {config.db_name}.users WHERE user_id = %s"
                cursor.execute(delete_query, user_id)
                conn.commit()
                log.info("Deleted entry from the database...with id %s", user_id)
                return jsonify({"status": "ok", "user_deleted": user_id}), 200

        except pymysql.MySQLError as query_error:
            conn.rollback()
            log.error(f"Query execution error: {query_error}")
            return jsonify({"status": "error", "reason": "Database error."}), 500

        except Exception as exception:
            log.error(f"Query execution error: {exception}")
            return jsonify({"status": "error", "reason": "An error occurred."}), 500

        finally:
            log.debug("Close all connections")
            # Close the connection and cursor
            close_connection(conn, cursor)

    # A simple method route API for backend app
    # combining the default path and a given user id to create the url


@app.route('/users/', methods=['POST'])
# For a POST we need the user id and the payload containing the user's name
# data required to create a new user
# we first check if user exists, if so return error with 500
# otherwise create new user with success code 200
def create_user():
    log.info("Entered POST method call")

    conn = None
    cursor = None

    try:
        # Getting the JSON data payload from request
        request_data = request.json
        user_name = request_data.get('user_name')

        log.debug(f"user name %s", user_name)
        # Connect to the database
        conn = connect_to_database()
        if not conn:
            return jsonify({"status": "error", "reason": "Database connection error."}), 500

        log.info("Connected to the database...")
        cursor = conn.cursor()

        cursor.execute(f"SELECT user_id FROM {config.db_name}.users WHERE user_name = %s;", user_name)
        existing_user = cursor.fetchone()

        # Check if user_id already exists
        if existing_user:
            new_id_for_duplicate_name = get_next_available_row_id_from_db()
            log.debug(f"new id after duplicate %s", new_id_for_duplicate_name)
        else:
            new_id_for_duplicate_name = 1

        insert_query = f"INSERT INTO {config.db_name}.users (user_id, user_name) VALUES (%s, %s)"
        cursor.execute(insert_query, (new_id_for_duplicate_name, user_name))
        conn.commit()
        log.debug("Add new entry to the database...with id %s", new_id_for_duplicate_name)
        return jsonify(
            {"status": "ok", "added_user_id": new_id_for_duplicate_name, "user_added": user_name}), 200

    except pymysql.MySQLError as query_error:
        conn.rollback()
        log.error(f"Query execution error: {query_error}")
        return jsonify({"status": "error", "reason": "Database error."}), 500

    except Exception as exception:
        log.error(f"Query execution error: {exception}")
        return jsonify({"status": str(exception), "reason": "An error occurred."}), 500

    finally:
        # Close the connection and cursor
        close_connection(conn, cursor)


# route to stop the server during jenkins pipeline run
# avoiding perpetual run
@app.route('/stop_server')
def shutdown():
    print("Shutting down gracefully...")
    operating_system = platform.system()
    if operating_system == "Windows":
        os.kill(os.getpid(), signal.CTRL_C_EVENT)
    else:
        os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'


if __name__ == '__main__':
    logging.info("Setting up database tables at class level...")
    setup_database()
    populate_config_table()
    app.run(host='127.0.0.1', debug=True, port=5003)
