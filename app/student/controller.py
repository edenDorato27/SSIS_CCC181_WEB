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
    
    return render_template('add_student.html', form=form)

@student_bp.route('/student/update/', methods=["GET", "POST"])
def update_student():
    form = StudentForm()
    first_name_update = studModel.Student.update()

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


