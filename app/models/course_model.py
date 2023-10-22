from app import mysql


class Course(object):

    def __init__(self, course_code=None, course_name=None, college_code=None):
        self.course_code = course_code
        self.course_name = course_name
        self.college_code = college_code

    def add(self):
        cursor = mysql.connection.cursor()

        sql = f"INSERT INTO course(course_code, course_name, college_code) \
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
    def delete(cls, course_code):
        """
        Delete a course from the database.

        Args:
            course_code (str): The course_code of the course to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM course WHERE course_code = %s"
            cursor.execute(sql, (course_code,))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error deleting course: {e}")
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
                sql = "SELECT * FROM course WHERE course_code = %s OR course_name = %s OR college_code = %s"
                cursor.execute(sql, (query, query, query))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
        
    @classmethod
    def get_course_by_id(cls, course_code):
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT * FROM course WHERE course_code = %s", (course_code,))
        course_data = cursor.fetchone()
        cursor.close()
        return course_data
    
    @classmethod
    def unique_code(cls, course_code):
        cursor = mysql.connection.cursor()
        sql = "SELECT course_code FROM course WHERE course_code = %s"
        cursor.execute(sql, (course_code,))
        result = cursor.fetchone()
        return result is not None
    
    @classmethod
    def get_college_code(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
            cursor.execute("SELECT college_code FROM college")
            all_colleges = cursor.fetchall()
            cursor.close()
            return all_colleges
        except Exception as e:
            print(f"Error obtaining college_code: {e}")
            return False
        
        
        
    

        
