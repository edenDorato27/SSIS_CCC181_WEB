from app import mysql


class Course(object):

    def __init__(self, course_code=None, course_name=None, college_code=None):
        self.course_code = course_code
        self.course_name = course_name
        self.college_code = college_code

    def add(self):
        cursor = mysql.connection.cursor()

        sql = f"INSERT INTO course(course_code,course_name, college_code) \
                VALUES('{self.course_code}','{self.course_name}','{self.college_code}')" 

        cursor.execute(sql)
        mysql.connection.commit()

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * from course"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls,course_code):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE from course where course_code= {course_code}"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False
  
    @classmethod
    def update(cls, course_code, new_course_name, new_college_code):
        try:
            with mysql.connection.cursor() as cursor:
                sql = "UPDATE course SET course_name = %s, college_code = %s WHERE course_code = %s"
                cursor.execute(sql, (new_course_name, new_college_code, course_code))
                mysql.connection.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    @classmethod
    def search_course(cls, query):
        try:
            with mysql.connection.cursor() as cursor:
                sql = "SELECT * FROM course WHERE course_code LIKE %s OR course_name LIKE %s OR college_code LIKE %s"
                cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%"))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
        
        
        
    

        
