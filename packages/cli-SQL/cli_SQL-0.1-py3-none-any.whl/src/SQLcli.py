def SQLcli():
    import argparse
    import mysql.connector

    db_config = {

        print("host:"): input("localhost"),
        
        print("user:"): input("your_username"),
        
        print("password:"): input("your_password"),
        
        print("database:"): input("your_database"),

        }

    query = input("Input Your Query Here: ")

    def execute_query(query, db_config):
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(row)
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

    def main():
        parser = argparse.ArgumentParser(description="Execute SQL queries via CLI")
        parser.add_argument("query", help="SQL query to execute")
        args = parser.parse_args()

        execute_query(args.query, db_config)

    if __name__ == "__main__":
        main()

    return
