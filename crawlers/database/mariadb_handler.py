import mysql.connector

class MariaDBHandler:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",
            collation="utf8mb4_general_ci" 
        )
        self.cursor = self.connection.cursor()

    def save_data(self, data):
        query = """
        INSERT INTO thongtin (title, price, address, area)
        VALUES (%s, %s, %s, %s)
        """
        values = (data['title'], data['price'], data['address'], data['area'])
        self.cursor.execute(query, values)
        self.connection.commit()