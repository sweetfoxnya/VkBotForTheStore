import sqlite3


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData



def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


def insertBLOB(name, description, price, photo):
    try:
        sqliteConnection = sqlite3.connect('pots.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO product
                                  (name, description, price, photo) VALUES (?, ?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)
        # Convert data into tuple format
        data_tuple = (name, description, price, empPhoto)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def readBlobData(empId):
    try:
        sqliteConnection = sqlite3.connect('pots.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from product where id = ?"""
        cursor.execute(sql_fetch_blob_query, (empId,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1], "Description = ", row[2], "Price = ", row[3])

            print("Storing employee image and resume on disk \n")
            photoPath = f"./in/{row[0]}.jpg"

            writeTofile(row[4], photoPath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")


def checkUser(vkId):
    helper = DBHelper()
    products_ = helper.print_info('user')
    for prod in products_:
        if prod[0] == vkId:
            print("Exist")
            return
    print("Not Exist")
    helper.insert('user',
                  ['id'],
                  [vkId]
                  )
    helper.insert('basket',
                  ['user_id'],
                  [vkId]
                  )



class DBHelper:
    def __init__(self, db_name="pots.db"):
        self.dbname = f"sqlite3:/{db_name}"
        self.conn = sqlite3.connect(db_name)

    def create_table_simple(self, table_name, params):
        column = ""
        for i in range(len(params) - 1):
            column += params[i] + " TEXT, "
        column += params[len(params) - 1] + " TEXT "

        new_table = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT , {column})"
        # print(new_table)
        try:
            # print(new_table)
            self.conn.execute(new_table)
            self.conn.commit()
        except sqlite3.Error as err:
            # print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()

    def update(self, table_name, column_arg, arg, column_change, change):
        update = f"UPDATE {table_name} " \
                 f"SET {column_change} = '{change}' " \
                 f"WHERE {column_arg} = '{arg}' "
        try:
            print(update)
            self.conn.execute(update)
            print("Выполнилось")
            self.conn.commit()
        except sqlite3.Error as err:
            print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()

    def delete(self, table_name, column_arg, arg):
        update = f"DELETE FROM {table_name} " \
                 f"WHERE {column_arg} = '{arg}' "
        try:
            # print(new_insert)
            self.conn.execute(update)
            # print("Выполнилось")
            self.conn.commit()
        except sqlite3.Error as err:
            print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()

    def insert(self, table_name, column_args, args):
        arguments = "'"
        for i in range(len(args) - 1):
            arguments += str(args[i]) + "', '"
        arguments += str(args[len(args) - 1]) + "'"
        # print(arguments)

        columns = ""
        for i in range(len(column_args) - 1):
            columns += str(column_args[i]) + ", "
        columns += str(column_args[len(column_args) - 1])

        new_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({arguments})"
        # print(new_insert)

        try:
            print(new_insert)
            self.conn.execute(new_insert)
            # print("Выполнилось")
            self.conn.commit()
            return True
        except sqlite3.Error as err:
            print('Sql error: %s' % (' '.join(err.args)))
            self.conn.rollback()
            return False

    def print_info(self, table_name):
        new_get = f"SELECT * FROM {table_name}"
        cursor = self.conn.execute(new_get)

        # print("Выполнилось")

        return [row for row in cursor]

    def get(self, table_name, column_args, args):
        query = ""
        for i in range(len(column_args) - 1):
            query += column_args[i] + " = '" + args[i] + "' AND "
        query += column_args[len(column_args) - 1] + " = '" + args[len(column_args) - 1] + "'"

        new_get = f"SELECT * FROM {table_name} WHERE {query}"
        # print(new_get)

        cursor = self.conn.execute(new_get)

        return [row for row in cursor]


    def rollback(self):
        self.conn.rollback()


