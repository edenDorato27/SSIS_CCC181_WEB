from app import mysql



class Student(object):

    def __init__(self, id_number=None, first_name=None, last_name=None, course_code=None, year_=None, gender=None):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.course_code = course_code
        self.year_ = year_
        self.gender = gender

    def add(self):
        """
        Add a new student to the database.

        Returns:
            bool: True if the addition was successful, False otherwise.
        """
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO student (id_number, first_name, last_name, course_code, year_, gender) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.id_number, self.first_name, self.last_name, self.course_code, self.year_, self.gender))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error adding student: {e}")
            return False
    
    @classmethod
    def unique_code(cls, id_number):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_number FROM student WHERE id_number = %s", (id_number,))
        code = cursor.fetchone()  # Use fetchone() to get a single result
        cursor.close()
        return code

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * from student"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls, id_number):
        """
        Delete a student from the database.

        Args:
            id_number (str): The ID number of the student to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM student WHERE id_number = %s"
            cursor.execute(sql, (id_number,))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error deleting student: {e}")
            return False
  
    @classmethod
    def update(cls, id_number, new_first_name, new_last_name, new_course_code, new_year_, new_gender):
        """
        Update the student's information in the database.

        Args:
            id_number (str): The ID number of the student to be updated.
            new_first_name (str): The new first name.
            new_last_name (str): The new last name.
            new_course_code (str): The new course code.
            new_year_ (int): The new year.
            new_gender (str): The new gender.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE student SET first_name = %s, last_name = %s, course_code = %s, year_ = %s, gender = %s WHERE id_number = %s"
            cursor.execute(sql, (new_first_name, new_last_name, new_course_code, new_year_, new_gender, id_number))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error updating student: {e}")
            return False

    @classmethod
    def get_student_by_id(cls, id_number):
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT * FROM student WHERE id_number = %s", (id_number,))
        student_data = cursor.fetchone()
        cursor.close()
        return student_data
    
    @classmethod
    def search_student(cls, query):
        try:
            with mysql.connection.cursor() as cursor:
                sql = "SELECT * FROM student WHERE id_number LIKE %s OR first_name = %s OR last_name = %s OR course_code = %s OR year_ = %s OR gender = %s"
                cursor.execute(sql, (query, query, query, query, query, query))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @classmethod
    def filter_student(cls, filter_by, query):
        try:
            with mysql.connection.cursor() as cursor:
                # Construct the SQL query based on the selected column
                columns = ["id_number", "first_name", "last_name", "course_code", "year_", "gender"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")
                sql = f"SELECT * FROM student WHERE {filter_by} = %s"
                cursor.execute(sql, (query,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @classmethod
    def get_course_code(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
            cursor.execute("SELECT course_code FROM course")
            all_colleges = cursor.fetchall()
            cursor.close()
            return all_colleges
        except Exception as e:
            print(f"Error obtaining college_code: {e}")
            return False

    
        
    

        
