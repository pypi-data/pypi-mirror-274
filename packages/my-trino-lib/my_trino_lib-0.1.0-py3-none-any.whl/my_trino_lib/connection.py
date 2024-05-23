import urllib3
from sqlalchemy.engine import create_engine
from trino.auth import BasicAuthentication
import getpass

class TrinoConnection:
    def __init__(self):
        self.engine = None

    def connect(self):
        # Disable insecure request warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Get user credentials
        user = input("Enter your Trino username: ")
        password = getpass.getpass("Enter your Trino password: ")

        # Create the SQLAlchemy engine for querying worklytics data
        self.engine = create_engine(
            f"trino://{user}@people-etl-trino.egdp-analytics.aws.away.black:8443/hive",
            connect_args={
                "auth": BasicAuthentication(user, password),
                "http_scheme": "https",
                "verify": False
            }
        )

    def test_connection(self):
        if self.engine is None:
            raise Exception("No connection. Please run the connect() method first.")
        try:
            with self.engine.connect() as connection:
                result = connection.execute("SELECT 1")
                print("Connection successful:", result.fetchone())
        except Exception as e:
            print("Connection failed:", str(e))

    def get_engine(self):
        return self.engine
