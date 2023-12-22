from flask import Flask, render_template, redirect, request, jsonify, flash, url_for, current_app
from wtforms import ValidationError
from . import student_bp
import app.models.student_model as studModel
from app.student.forms import StudentForm
from cloudinary import uploader
from cloudinary.uploader import upload
from cloudinary.uploader import destroy
import cloudinary.api
from cloudinary.utils import cloudinary_url
import cloudinary
import os


headings = ("Profile Picture", "ID_Number", "First Name", "Last Name", "Course", "College", "Year", "Gender", "Actions")

@student_bp.route('/')
def home_page():
    return render_template('home.html')

@student_bp.route("/student")
def student():
    student_info = studModel.Student.all()

    return render_template('student.html', headings=headings, data=student_info)

@student_bp.route('/student/add', methods=['POST', 'GET'])
def add():
    form = StudentForm()
    course_code = studModel.Student.get_course_code()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            profile_pic = request.files['profile_pic']
            check_id = form.id_number.data
            student_exists = studModel.Student.unique_code(check_id)

            if student_exists:
                flash("Student already exists! Please enter a unique id_number", 'error')
            else:
                if profile_pic:
                    # Call the add method from Students class
                    if studModel.Student.add(
                        check_id,
                        form.first_name.data,
                        form.last_name.data,
                        form.course_code.data,
                        form.year_.data,
                        form.gender.data,
                        profile_pic
                    ):
                        print("Student added successfully, and profile photo has been uploaded to Cloudinary")
                        flash("Student added successfully!", 'success')
                    else:
                        flash("Error adding student. Please try again.", 'error')
                else:
                    studModel.Student.add(
                        check_id,
                        form.first_name.data,
                        form.last_name.data,
                        form.course_code.data,
                        form.year_.data,
                        form.gender.data,
                        profile_pic = None)
                    
                    flash("Student added successfully.", 'success')

                # Redirect to the students page or any other page
                return redirect(url_for('student.student'))

        except ValidationError as e:
            flash(str(e), 'error')

    return render_template('add_student.html', form=form, course=course_code)

@student_bp.route('/student/edit', methods=["GET", "POST"])
def edit_student():
    id_number = request.args.get('id_number')
    form = StudentForm()
    course_code = studModel.Student.get_course_code()
    student_data = studModel.Student.get_student_by_id(id_number)
    
    student_data_dict = {}

    if student_data:
        student_data_dict = {
            "id_number": student_data['id_number'],
            "first_name": student_data['first_name'],
            "last_name": student_data['last_name'],
            "course_code": student_data['course_code'],
            "year_": student_data['year_'],
            "gender": student_data['gender']
        }
    else:
        flash("Student not found.", "error")

    if request.method == "POST" and form.validate():
        new_first_name = form.first_name.data
        new_last_name = form.last_name.data
        new_course_code = form.course_code.data
        new_year = form.year_.data
        new_gender = form.gender.data
        
        new_profile_pic = request.files['profile_pic'] if 'profile_pic' in request.files and request.files['profile_pic'].filename != '' else student_data['profile_pic']
        print("Profile picture: ", new_profile_pic)

        
        if studModel.Student.update(id_number, new_first_name, new_last_name, new_course_code, new_year, new_gender, new_profile_pic):
            flash("Student information updated successfully!", "success")
            return redirect(url_for("student.student"))
        else:
            flash("Failed to update student information.", "error")

    return render_template("edit_student.html", form=form, info=student_data_dict, course=course_code, current_profile_pic=student_data['profile_pic'])

@student_bp.route("/student/delete", methods=["POST"])
def delete_student():
    try:
        id_number = request.form.get('id_number')

        # Use the get_student_by_id class method to retrieve the student data
        student = studModel.Student.get_student_by_id(id_number)

        if not student:
            return jsonify(success=False, message="Student not found"), 404

        # Delete the image from Cloudinary using public ID
        if student['profile_pic']:
            try:
                current_path = student['profile_pic']
                print("Current path: ",  current_path)

                # Split the URL by "/"
                path_parts = current_path.split("/")

                # Find the index of "SSIS" in the path_parts
                index_of_ssis = path_parts.index("SSIS")

                # Extract the desired part
                desired_part = "/".join(path_parts[index_of_ssis:index_of_ssis + 2])

                # Remove the file extension
                public_id, _ = os.path.splitext(desired_part)
                print("Public ID: " + public_id)
                # Create a list with a single element
                public_ids_to_delete = [public_id]

                # Use Cloudinary's delete_resources method to delete the image
                image_delete_result = cloudinary.api.delete_resources(public_ids_to_delete, resource_type="image", type="upload")
                print("Cloudinary API Response:", image_delete_result)

                if 'deleted' in image_delete_result and image_delete_result['deleted'][public_id] == 'deleted':
                    # Image deleted successfully
                    print("Successfully deleted from Cloudinary")
                else:
                    # Log the error for debugging purposes
                    current_app.logger.error("Failed to delete image from Cloudinary. Response: %s" % image_delete_result)
            except Exception as e:
                # Log the error for debugging purposes
                current_app.logger.error("Error deleting image from Cloudinary: %s" % str(e))

        # Delete the student record
        if studModel.Student.delete(id_number):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed to delete student")

    except Exception as e:
        # Log the error for debugging purposes
        current_app.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@student_bp.route('/student/search', methods=['POST'])
def search_student():
    try:
        search_query = request.form.get('searchTerm')
        filter_by = request.form.get('filterBy')  # Get the filterBy parameter
        
        if filter_by == 'all':
            # If filterBy is 'all', perform a general search
            search_results = studModel.Student.search_student(search_query)
        else:
            # Otherwise, filter based on the selected column
            search_results = studModel.Student.filter_student(filter_by, search_query)
            
        return jsonify(search_results)
    except Exception as e:
        # Handle errors and return an error response
        return jsonify(error=str(e)), 500

