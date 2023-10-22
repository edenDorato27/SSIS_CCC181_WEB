from flask import Flask, render_template, redirect, request, jsonify, flash, url_for
from . import student_bp
import app.models.student_model as studModel
from app.student.forms import StudentForm

headings = ("ID_Number", "First Name", "Last Name", "Course", "Year", "Gender", "Actions")

@student_bp.route('/')
def home_page():
    return render_template('home.html')

@student_bp.route('/student')
def student():
    student_info = studModel.Student.all()
    return render_template('student.html', headings = headings, data = student_info)

@student_bp.route('/student/add', methods=['POST','GET'])
def add():
    form = StudentForm(request.form)
    course_code = studModel.Student.get_course_code()
    
    if request.method == 'POST' and form.validate():
        check_id = form.id_number.data
        student_exists = studModel.Student.unique_code(check_id)

        if student_exists:
            flash("ID numder already exists! Please enter a unique ID numbers", 'error')
        else:
            student = studModel.Student(
                id_number=check_id,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                course_code=form.course_code.data,
                year_=form.year_.data,
                gender=form.gender.data
            )
            student.add()
            flash("Student added successfully!", 'success')
            return redirect(url_for('student.student'))
    
    return render_template('add_student.html', form=form, course=course_code)

@student_bp.route('/student/edit', methods=["GET", "POST"])
def edit_student():
    id_number = request.args.get('id_number')
    form = StudentForm()
    course_code = studModel.Student.get_course_code()
    student_data = studModel.Student.get_student_by_id(id_number)

    if student_data:
        # Ensure that student_data is not empty before accessing elements
        student_data_dict = {
            "id_number": student_data['id_number'],
            "first_name": student_data['first_name'],
            "last_name": student_data['last_name'],
            "course_code": student_data['course_code'],
            "year_": student_data['year_'],
            "gender": student_data['gender']
        }
    else:
        # Handle the case where no student data was found
        flash("Student not found.", "error")
        return redirect(url_for("student.student"))

    if request.method == "POST" and form.validate():
        new_first_name = form.first_name.data
        new_last_name = form.last_name.data
        new_course_code = form.course_code.data
        new_year = form.year_.data
        new_gender = form.gender.data

        if studModel.Student.update(id_number, new_first_name, new_last_name, new_course_code, new_year, new_gender):
            flash("Student information updated successfully!", "success")
            return redirect(url_for("student.student"))
        else:
            flash("Failed to update student information.", "error")

    return render_template("edit_student.html", form=form, info=student_data_dict, course=course_code)

@student_bp.route("/student/delete", methods=["POST"])
def delete_student():
    try:
        id_number = request.form.get('id_number')
        if studModel.Student.delete(id_number):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed")
    except Exception as e:
        # Log the error for debugging purposes
        student_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@student_bp.route('/student/search', methods=['POST'])
def search_student():
    try:
        search_query = request.form.get('searchTerm')  # Updated to 'searchTerm'
        # Perform a database query based on the search_query
        search_results = studModel.Student.search_student(search_query)
        return jsonify(search_results)
    except Exception as e:
        # Handle errors and return an error response
        return jsonify(error=str(e)), 500


