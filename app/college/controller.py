from flask import Flask, render_template, redirect, request, jsonify, flash, url_for
from . import college_bp
import app.models.college_model as collegeModel
from app.college.forms import CollegeForm

headings = ("College_code", "College Name", "Actions")

@college_bp.route('/')
def home_page():
    return render_template('home.html')

@college_bp.route('/college')
def college():
    college_info = collegeModel.College.all()
    return render_template('college.html', headings = headings, data = college_info)

@college_bp.route('/college/add', methods=['POST','GET'])
def add():
    form = CollegeForm(request.form)
    
    if request.method == 'POST' and form.validate():
        check_id = form.college_code.data
        college_exists = collegeModel.College.unique_code(check_id)

        if college_exists:
            flash("Course_code already exists! Please enter a unique Course_code", 'error')
        else:
            college = collegeModel.College(
                college_code=check_id,
                college_name=form.college_name.data,
            )
            college.add()
            flash("College added successfully!", 'success')
            return redirect(url_for('college.college'))
    
    return render_template('add_college.html', form=form)

@college_bp.route('/college/edit', methods=["GET", "POST"])
def edit_college():
    college_code = request.args.get('college_code')
    form = CollegeForm()
    college_data = collegeModel.College.get_college_by_id(college_code)

    if college_data:
        # Ensure that student_data is not empty before accessing elements
        college_data_dict = {
            "college_code": college_data['college'],
            "college_name": college_data['college_name'],
        }
    else:
        # Handle the case where no student data was found
        flash("College not found.", "error")
        return redirect(url_for("college.college"))

    if request.method == "POST" and form.validate():
        new_college_name = form.college_name.data

        if collegeModel.College.update(college_code, new_college_name):
            flash("College information updated successfully!", "success")
            return redirect(url_for("college.college"))
        else:
            flash("Failed to update college information.", "error")

    return render_template("edit_student.html", form=form, info=college_data_dict)

@college_bp.route("/college/delete", methods=["POST"])
def delete_college():
    try:
        college_code = request.form.get('college_code')
        if collegeModel.College.delete(college_code):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed")
    except Exception as e:
        # Log the error for debugging purposes
        college_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@college_bp.route('/college/search', methods=['POST'])
def search_college():
    try:
        search_query = request.form.get('searchTerm')  # Updated to 'searchTerm'
        # Perform a database query based on the search_query
        search_results = collegeModel.College.search_college(search_query)
        
        if search_results is not None:
            return jsonify(search_results)
        else:
            return jsonify([])
    except Exception as e:
        # Handle errors and return an error response
        return jsonify(error=str(e)), 500

