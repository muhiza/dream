from flask import render_template, flash, redirect, url_for, session

from . import muhiza


@muhiza.route('/tapayi')
def tapayi():
	return render_template('muhiza/home.html')



@muhiza.route('/frank')
def waka():
	return render_template('muhiza/waka.html')

