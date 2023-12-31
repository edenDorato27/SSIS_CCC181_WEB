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
                sql = """
                    SELECT course.course_code, course.course_name, course.college_code, college.college_name
                    FROM course
                    LEFT JOIN college ON course.college_code = college.college_code
                    WHERE course.course_code LIKE %s 
                    OR course.course_name LIKE %s 
                    OR course.college_code LIKE %s 
                    OR college.college_name LIKE %s
                """
                cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @classmethod
    def filter_course(cls, filter_by, query):
        try:
            with mysql.connection.cursor() as cursor:
                # Construct the SQL query based on the selected column
                columns = ["course_code", "course_name", "college_code", "college_name"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")
                sql = f"""
                    SELECT course.course_code, course.course_name, course.college_code, college.college_name
                    FROM course
                    LEFT JOIN college ON course.college_code = college.college_code
                    WHERE {filter_by} = %s
                """
                cursor.execute(sql, (query,))
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
        
    @classmethod
    def get_all_college_name(cls, course_code):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT college.college_name
                FROM college
                JOIN course
                ON course.college_code = college.college_code
                WHERE course.course_code = %s
            """, (course_code,))
            all_colleges = cursor.fetchall()
            cursor.close()
            return all_colleges
        except Exception as e:
            print(f"Error obtaining college_name: {e}")
            return False
        
        
        
    

        
