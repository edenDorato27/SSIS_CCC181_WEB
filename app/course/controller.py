from flask import Flask, render_template, redirect, request, jsonify, flash, url_for
from . import course_bp
import app.models.course_model as courseModel
from app.course.forms import CourseForm

headings = ("Course Code", "Course name", "College Code", "Actions")

@course_bp.route('/')
def home_page():
    return render_template('home.html')

@course_bp.route('/course')
def course():
    course_info = courseModel.Course.all()
    return render_template('course.html', headings = headings, data = course_info)

@course_bp.route('/course/add', methods=['POST','GET'])
def add():
    form = CourseForm(request.form)
    college_code = courseModel.Course.get_college_code()
    
    if request.method == 'POST' and form.validate():
        check_id = form.course_code.data
        course_exists = courseModel.Course.unique_code(check_id)

        if course_exists:
            flash("Course code already exists! Please enter a course code", 'error')
        else:
            course = courseModel.Course(
                course_code=check_id,
                course_name=form.course_name.data,
                college_code=form.college_code.data,
               
            )
            course.add()
            flash("Course added successfully!", 'success')
            return redirect(url_for('course.course'))
    
    return render_template('add_course.html', form=form, college=college_code)

@course_bp.route('/course/edit', methods=["GET", "POST"])
def edit_course():
    course_code = request.args.get('course_code')
    form = CourseForm()
    college_code = courseModel.Course.get_college_code()
    course_data = courseModel.Course.get_course_by_id(course_code)

    if course_data:
        # Ensure that student_data is not empty before accessing elements
        course_data_dict = {
            "course_code": course_data['course_code'],
            "course_name": course_data['course_name'],
            "college_code": course_data['college_code'],
            
        }
    else:
        # Handle the case where no student data was found
        flash("Course not found.", "error")
        return redirect(url_for("course.course"))

    if request.method == "POST" and form.validate():
        new_course_name = form.course_name.data
        new_college_code = form.college_code.data

        if courseModel.Course.update(course_code, new_course_name, new_college_code):
            flash("Course information updated successfully!", "success")
            return redirect(url_for("course.course"))
        else:
            flash("Failed to update course information.", "error")

    return render_template("edit_course.html", form=form, info=course_data_dict, college=college_code)

@course_bp.route("/course/delete", methods=["POST"])
def delete_course():
    try:
        course_code = request.form.get('course_code')
        if courseModel.Course.delete(course_code):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed")
    except Exception as e:
        # Log the error for debugging purposes
        course_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@course_bp.route('/course/search', methods=['POST'])
def search_course():
    try:
        search_query = request.form.get('searchTerm')  # Updated to 'searchTerm'
        # Perform a database query based on the search_query
        search_results = courseModel.Course.search_course(search_query)
        return jsonify(search_results)
    except Exception as e:
        # Handle errors and return an error response
        return jsonify(error=str(e)), 500


