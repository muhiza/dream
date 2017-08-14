from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

#New import which is used to query the database fields.

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department, Role

"""
Form to add or edit the department
"""

class DepartmentForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[DataRequired()])
	submit = SubmitField('Submit')



# Defining the roles Form.

class RoleForm(FlaskForm):
	name = StringField('Role', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[DataRequired()])
	submit = SubmitField('Submit')



class EmployeeAssignForm(FlaskForm):
	"""
	Setting all the fields we want to use here.
	"""

	department = QuerySelectField(query_factory = lambda: Department.query.all(), get_label="name")
	role       = QuerySelectField(query_factory = lambda: Role.query.all(), get_label="name")
	submit    = SubmitField('Submit')