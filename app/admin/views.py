# admin/views.py

# Import the third-parties modules
from flask import Flask, redirect, url_for, abort, render_template, request, flash
from flask_login import current_user, login_required

# Importing the internal modules

from forms import DepartmentForm, RoleForm, EmployeeAssignForm
from .. import db
from ..models import Department, Role, Employee
from . import admin

# Checking if the user is an admin

def check_admin():
	if not current_user.is_admin:
		abort(403)

		"""
		Avoiding another user to enter in the administrator's dashboard.
		"""
@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():

	check_admin()
	departments = Department.query.all()

	"""
	Returning the results in the templates here
	"""
	return render_template('admin/departments/departments.html', departments = departments, title='Department')


@admin.route('/department/add', methods=['GET', 'POST'])
def add_department():
	"""
	Adding the department in the database in order to be stored there
	"""
	check_admin()
	add_dempartment = True
	form = DepartmentForm()
	if request.method == 'POST' and form.validate():
		department = Department(name=form.name.data, description=form.description.data)

		try:
			# Add the department in the database
			db.session.add(department)
			db.session.commit()
			flash('The department has successfully added in the database')
		except:
			# In case there are some error (the department is in the database).
			flash("The department you are trying to add is already exist in the database")
		return redirect(url_for('admin.list_departments'))

	return render_template('admin/departments/department.html', action='Add', form=form
		, add_department=add_department, title='Add Department')


# Make it possible to edit the deportment for the user who is an admin of the system, here.

@admin.route('/admin/department/edit/<int:id>', methods = ['GET', 'POST'])
def edit_department(id):
	check_admin()

	# Set the add_department vartible to false
	add_department = False

	# Making the query which retrieve the data from the database
	department = Department.query.get_or_404(id)

	# Form that we will use is here/.
	form = DepartmentForm()
	if request.method == 'POST' and form.validate_on_submit():
		department.name = form.name.data
		department.description = form.description.data

		# Submitting the data in the database
		db.session.commit()
		flash('The form has been updated successfully')
		return redirect(url_for('admin.list_departments'))
	# Populate the the data in the form when you are editing them.
	form.name.data = department.name
	form.description.data = department.description
	return render_template('admin/departments/department.html', action='Edit',title='Edit department', form=form,
		ada_department=add_department, department=department)


# The views for deleting the department from the database of the admin, here!
@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
def delete_department(id):

	# Check if this user is the admin of the website.
	check_admin()

	department = Department.query.get_or_404(id)
	# Deleting the department from detabase
	db.session.delete(department)
	db.session.commit()
	flash('The department has been deleted from the database successfully')

	return redirect(url_for('admin.list_departments'))
	return render_template(title='Delete department')



# Working with roles in the system, All views that we are going to work on here are for Roles.


@admin.route('/admin/department/roles')
@login_required
def list_roles():
	# Check if the user is admin.
	check_admin()

	# Adding the variable to make sure that we are adding role
	add_role = True

	# Make the query to retrieve all the roles in the database.
	roles = Role.query.all()

	# Display all the roles in the template where we are.
	return render_template('admin/roles/roles.html', roles = roles)



@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')



# Editing the role in the database here.

@admin.route('/admin/role/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
	# check if the user is an admin
	check_admin()

	# Desable the add_role variable here.
	add_role = False

	role = Role.query.get_or_404(id)
	form = RoleForm()
	if request.method == 'POST' and form.validate_on_submit():
		role.name = form.name.data
		role.description = form.description.data

		# Submit the form.
		db.session.add(role)
		db.session.commit()
		flash("The role has been updated successfully")
		return redirect(url_for('admin.list_roles'))


	form.name.data = role.name
	form.description.data = role.description
	return render_template('admin/roles/role.html', add_role=add_role, title='Edit Role',
		form=form, role = role)




# Delete the role from the database here.
@admin.route('/admin/role/delete/<int:id>')
@login_required
def delete_role(id):
	# Check if the user is an admin here.
	check_admin()

	# Make a query here.
	role = Role.query.get_or_404(id)
	# Delete the role
	db.session.delete(role)
	db.session.commit()

	flash("The role has been Deleted successfully")
	return redirect(url_for('admin.list_roles'))
	return render_template(title='Delete the Role')


# The views which are related to the operations that concerns the Employees


@admin.route('/admin/roles/employees')
@login_required
def list_employees():
	"""
	Listing all the employees who are in the system.
	"""
	check_admin()
	employees = Employee.query.all()
	return render_template('/admin/employees/employees.html', employees = employees, title='Employees')





@admin.route('/admin/employees/asign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):

	check_admin()

	# Query the database to get the employees
	employee = Employee.query.get_or_404(id)
	# Preventing the admin to be assigned to roles.
	if employee.is_admin:
		abort(404)

	form = EmployeeAssignForm()

	if request.method == 'POST' and form.validate_on_submit():
		employee.role = form.role.data
		employee.department = form.department.data

		db.session.add(employee)
		db.session.commit()
		flash("The role has been assigned to employee Successfully")
		return redirect(url_for('admin.list_employees'))

	return render_template('admin/employees/employee.html', employee=employee, form=form, title='Assign Role')
