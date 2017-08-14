# tests.py

import unittest

from flask_testing import TestCase

from app import create_app, db
from app.models import Employee, Department, Role


from flask import abort, url_for


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://root:annemuhiza@localhost/dreamteam_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = Employee(username="admin", password="annemuhiza", is_admin=True)

        # create test non-admin user
        employee = Employee(username="test_user", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

# Tests for the models here.
class TestModels(TestBase):
    def test_employee_model(self):
        """
        Counting the number of employees that are in the database
        """
        self.assertEqual(Employee.query.count(), 2)

    # Testing the Department models here.
    def test_department_model(self):
        """
         Counting the number of employees that are in the database now.   
        """
        department = Department(name="IT", description="Information Technologies")
        # Save to the department databse table now.
        db.session.add(department)
        db.session.commit()
        self.assertEqual(Department.query.count(), 1)



    def test_role_model(self):
        """
        Counting the number of roles that are in the database now
        """

        role = Role(name="CEO", description="Run the whole campany")

        # Committing the changes in the database.
        db.session.add(role)
        db.session.commit()
        self.assertEqual(Role.query.count(), 1)


# Writting tests for views here.
class TestViews(TestBase):
    def test_homepage_view(self):
        """
        Testing if the user can access the homepage without logging in first.
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)


    def test_login_view(self):
        """
        Testing and make sure that the user can access login page without him/her logged in first
        """

        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)


    def test_logout_view(self):
        """
        Preventing the user to access the logout page without logging in and redirect the user to the
        login page and then logout page
        """

        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response  = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Preventing the user from accessing the Dashboard page with login in and redirect the user on
        login page and then dashboard. 
        """

        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response     = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


    def test_admin_dashboard_view(self):
        """
        Preventing the user from access the admin_dashboard page before logging in and redirect him
        to the login page and then admin_dashboard after loging in
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


    def test_departments_view(self):
        """
        Preventing the user from access the departments page when he is is not logged in and redirect
        him to the login page and then department after he logs in.
        """
        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response  = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)



    def test_roles_view(self):
        """
        Preventing the users from accessing the role views when they are not logged in and
        redirect them to the login page and then logout roles page after they login
        """

        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)



    def test_employees_view(self):
        """
        Prevent the users from accessing the employees views when they are not logged in and redirect them to
        the login page and then after to the employees page
        """
        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)




# Writting tests for the Errorpages.
class TestErrorPages(TestBase):
    def test_403_forbidden(self):

        """
        Write abort when the user try to access this page
        """
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)



    def test_404_not_found(self):
        response = self.client.get('/404')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)



    def test_500_internal_server_error(self):
        """
        Preventing the users to access the page by calling the abort when the request is made.
        """
        @self.app.route('/500')
        def internal_servetr_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)



if __name__ == '__main__':
    unittest.main()