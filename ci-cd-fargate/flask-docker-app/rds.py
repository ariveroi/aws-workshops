import mysql.connector
import boto3
import json


class RDS:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def get_sales(self):
        secret = self.get_secret()
        if secret is not None:
            secret = json.loads(secret["SecretString"])
            self.connection = mysql.connector.connect(
                host=secret["host"],
                user=secret["username"],
                passwd=secret["password"],
                database=secret["dbname"],
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT * FROM sales")
            data = self.cursor.fetchall()
            self.connection.close()
            return data
        return None

    def get_secret(self):
        secret_name = "awsomebuilder/rds/creds/awsomebuilder-rds"
        region_name = "eu-west-2"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            return get_secret_value_response
        except:
            return None

    def get_products(self, username):
        secret = self.get_secret()
        if secret is not None:
            secret = json.loads(secret["SecretString"])
            self.connection = mysql.connector.connect(
                host=secret["host"],
                user=secret["username"],
                passwd=secret["password"],
                database=secret["dbname"],
            )
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                "SELECT * FROM products WHERE customer = %s", (username,)
            )
            data = self.cursor.fetchall()
            return data
        return None
