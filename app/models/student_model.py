from app import mysql
import cloudinary
import cloudinary.uploader
from cloudinary.uploader import upload, destroy
import re



class Student:

    def __init__(self, id_number=None, first_name=None, last_name=None, course_code=None, year_=None, gender=None, profile_pic=None):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.course_code = course_code
        self.year_ = year_
        self.gender = gender
        self.profile_pic = profile_pic

    @classmethod
    def add(cls, id_number, first_name, last_name, course_code, year_, gender, profile_pic):
        try:
            with mysql.connection.cursor() as cursor:
                if profile_pic:
                    upload_result = cloudinary.uploader.upload(profile_pic, folder="SSIS", resource_type='image')
                    profile_pic_url = upload_result['secure_url']

                    sql = "INSERT INTO student (id_number, first_name, last_name, course_code, year_, gender, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (id_number, first_name, last_name, course_code, year_, gender, profile_pic_url))
                else:
                    sql = "INSERT INTO student (id_number, first_name, last_name, course_code, year_, gender) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (id_number, first_name, last_name, course_code, year_, gender))

            mysql.connection.commit()
            return True
        except mysql.connector.Error as e:
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
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "SELECT student.*, course.course_code, college.college_code FROM student INNER JOIN course ON student.course_code = course.course_code INNER JOIN college ON course.college_code = college.college_code;"
            cursor.execute(sql)
            result = cursor.fetchall()

            for student in result:
                student['profile_pic'] = student['profile_pic']
                
            return result
        except Exception as e:
            print(f"Error fetching all students: {e}")
            return []

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
    def update(cls, id_number, new_first_name, new_last_name, new_course_code, new_year_, new_gender, new_profile_pic):
        try:
            cursor = mysql.connection.cursor()

            existing_student = cls.get_student_by_id(id_number)
            
            if new_profile_pic:
                result = upload(new_profile_pic, folder="SSIS", resource_type='image')
                new_profile_pic_url = result['secure_url']
                
                old_profile_pic_url = existing_student['profile_pic']
                if old_profile_pic_url:
                    public_id = old_profile_pic_url.split('/')[-1].split('.')[0]
                    print("public_id: ", public_id)
                    destroy("SSIS/" + public_id)

            else:
                new_profile_pic_url = None  # Ensuring this is set to None if no new picture is provided

            sql = "UPDATE student SET first_name = %s, last_name = %s, course_code = %s, year_ = %s, gender = %s, profile_pic = %s WHERE id_number = %s"
            cursor.execute(sql, (new_first_name, new_last_name, new_course_code, new_year_, new_gender, new_profile_pic_url, id_number))

            mysql.connection.commit()
            return True
        except Exception as e:
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
            with mysql.connection.cursor(dictionary=True) as cursor:
                sql = """
                    SELECT student.id_number, student.first_name, student.last_name, student.course_code, course.college_code, student.year_, student.gender, student.profile_pic
                    FROM student
                    JOIN course ON student.course_code = course.course_code
                    WHERE student.id_number LIKE %s
                    OR student.first_name LIKE %s
                    OR student.last_name LIKE %s
                    OR student.course_code LIKE %s
                    OR course.college_code LIKE %s
                    OR student.year_ LIKE %s
                    OR student.gender LIKE %s
                """
                cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @classmethod
    def filter_student(cls, filter_by, query):
        try:
            with mysql.connection.cursor(dictionary=True) as cursor:
                # Construct the SQL query based on the selected column
                columns = ["id_number", "first_name", "last_name", "course_code", "college_code", "year_", "gender"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")
                if filter_by == "college_code":
                    sql = f"""
                        SELECT student.id_number, student.first_name, student.last_name, student.course_code, course.college_code, student.year_, student.gender, student.profile_pic
                        FROM student
                        JOIN course ON student.course_code = course.course_code
                        WHERE course.college_code = %s
                    """
                else:
                    sql = f"""
                        SELECT student.id_number, student.first_name, student.last_name, student.course_code, course.college_code, student.year_, student.gender, student.profile_pic
                        FROM student
                        JOIN course ON student.course_code = course.course_code
                        WHERE student.{filter_by} = %s
                    """
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
        
    @classmethod
    def get_all_college(cls, id_number):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT course.college_code 
                FROM course
                JOIN student
                ON student.course_code = course.course_code
                WHERE id_number = %s
            """, (id_number,))
            all_colleges = cursor.fetchall()
            cursor.close()
            return all_colleges
        except Exception as e:
            print(f"Error obtaining college_code: {e}")
            return False
    
    
