class TrinoQueries:
    def __init__(self, engine):
        self.engine = engine

    def execute_query(self, query):
        if self.engine is None:
            raise Exception("No connection engine provided.")
        try:
            with self.engine.connect() as connection:
                result = connection.execute(query)
                return result.fetchall()
        except Exception as e:
            print("Query execution failed:", str(e))
            return None
