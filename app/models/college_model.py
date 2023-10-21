from app import mysql

class College(object):

    def __init__(self, college_code=None, college_name=None):
        self.college_code = college_code
        self.college_name = college_name

    def add(self):
        cursor = mysql.connection.cursor()

        sql = f"INSERT INTO college(college_code, college_name) VALUES ('{self.college_code}', '{self.college_name}')"
        cursor.execute(sql)
        mysql.connection.commit()

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * from college"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls, college_code):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE from college where college_code = '{college_code}'"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False

    @classmethod
    def update(cls, college_code, new_college_name):
        try:
            with mysql.connection.cursor() as cursor:
                sql = "UPDATE college SET college_name = %s WHERE college_code = %s"
                cursor.execute(sql, (new_college_name, college_code))
                mysql.connection.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    @classmethod
    def get_college_by_id(cls, college_code):
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT * FROM college WHERE college_code = %s", (college_code,))
        college_data = cursor.fetchone()
        cursor.close()
        return college_data

    @classmethod
    def search_college(cls, query):
        try:
            with mysql.connection.cursor() as cursor:
                sql = "SELECT * FROM college WHERE college_code LIKE %s OR college_name LIKE %s"
                cursor.execute(sql, (f"%{query}%", f"%{query}%"))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @classmethod
    def unique_code(cls, college_code):
        cursor = mysql.connection.cursor()
        sql = "SELECT college_code FROM college WHERE college_code = %s"
        cursor.execute(sql, (college_code,))
        result = cursor.fetchone()
        return result is not None
