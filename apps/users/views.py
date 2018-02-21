# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.db import IntegrityError
from models import *
import random
import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	print "index"
	users=User.objects.all()
	print users	
	context ={ 
		'users': users,
	}
	return render(request, 'users/index.html', context)

def usersnew(request):
	print "users new"
	return render(request, 'users/newuser.html')

def usersedit(request, id):
	print "users edit" + id
	try:
		user=User.objects.get(id=id)
		print user
		context ={ 
			'user': user,
		}
	except User.DoesNotExist:
		print "USER DOES NOT EXIST"
		return redirect ("/users")

	return render(request, 'users/edituser.html', context)

def usersshow(request, id):
	print "show users" + id
	try:
		user = User.objects.get(id=id)
		context = {
			'first_name': user.first_name,
			'last_name' : user.last_name,
			'email': user.email_address,
			'id' : id,
			'created_at':user.created_at,
		}
	except User.DoesNotExist:
		print "USER DOES NOT EXIST"
		return redirect ("/users")
	return render(request, 'users/showuser.html', context)
	
def userscreate(request):
	print "create users"
	if request.method=='POST':
		print "post"

		if len(request.POST['first_name']) < 1 or len(request.POST['last_name']) < 1:
			return redirect("/users/new")

		if EMAIL_REGEX.match(request.POST['email']):
			# IF EMAIL EXISTS IN DB try/catch
			try:
				User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email'])
			except IntegrityError as e:
				if 'constraint' in e.message:
					print "EMAIL ALREADY EXISTS IN DATABASE"
					return redirect("/users/new")


			return redirect("/users/" + str(User.objects.get(email_address=request.POST['email']).id))

		return("/users/new")

def usersdestroy(request, id):
	try:
		b = User.objects.get(id=id)
	except User.DoesNotExist:
		print "USER DOES NOT EXIST"
		return redirect ("/users")
	b.delete() # deletes that particular record


	return redirect("/users")

def usersupdate(request):
	print "update users"
	if request.method=='POST':
		try:
			user = User.objects.get(id=request.POST['id'])
		except User.DoesNotExist:
			print "USER DOES NOT EXIST"
			return redirect ("/users")

		if len(request.POST['first_name']) < 1 or len(request.POST['last_name']) < 1:
			print "NAME MUST NOT BE EMPTY"
			return redirect("/users/" + request.POST['id'])

		user.first_name=request.POST['first_name']
		user.last_name=request.POST['last_name']
		user.email_address=request.POST['email']
		try:
			user.save()
		except IntegrityError as e:
			if 'constraint' in e.message:
				print "EMAIL ALREADY EXISTS IN DATABASE"
				return redirect("/users")
		return redirect("/users/" + request.POST['id'])	

# a GET request to /users - calls the index method to display all the users. This will need a template.
# GET request to /users/new - calls the new method to display a form allowing users to create a new user. This will need a template.

# GET request /users/<id>/edit - calls the edit method to display a form allowing users to edit an existing user with the given id. This will need a template.
# GET /users/<id> - calls the show method to display the info for a particular user with given id. This will need a template.

# POST to /users/create - calls the create method to insert a new user record into our database. This POST should be sent from the form on the page /users/new. Have this redirect to /users/<id> once created.
# GET /users/<id>/destroy - calls the destroy method to remove a particular user with the given id. Have this redirect back to /users once deleted.
# POST /users/update - calls the update method to process the submitted form sent from /users/<id>/edit. Have this redirect to /users/<id> once updated.

# from flask import Flask, request, redirect, render_template, session, flash
# from mysqlconnection import MySQLConnector
# import datetime #time stuff
# import time
# import re #Regex
# import md5 #hasing
# import os, binascii #for hasing


# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# app = Flask(__name__)
# mysql = MySQLConnector(app,'users')
# app.secret_key = '0118999881999119725'
 







# #UPDATE USER post page (EMAIL MUST BE DIFFERENT)
# @app.route('/users/<id>', methods=['POST'])
# def updateuser(id):
# 	first_name = request.form['first_name']
# 	last_name = request.form['last_name']
# 	email=request.form['email']

# 	if(len(first_name)==0):
# 		flash("First Name cannot be empty!")
# 		return redirect('/users/'+str(id)+"/edit")
# 	elif(not first_name.isalpha()):
# 		flash("First Name cannot contain numbers")
# 		return redirect('/users/'+str(id)+"/edit")

# 	if(len(last_name)==0):
#    		flash("Last Name cannot be empty!")
# 		return redirect('/users/'+str(id)+"/edit")
#    	elif(not last_name.isalpha()):
#    		flash("Last Name cannot contain numbers")
# 		return redirect('/users/'+str(id)+"/edit")

# 	if(len(email) < 1):
# 		flash("Email cannot be empty!")
# 		return redirect('/users/'+str(id)+"/edit")
# 	elif not EMAIL_REGEX.match(email):
# 		flash("Invalid Email Address!") 
# 		return redirect('/users/'+str(id)+"/edit")

#     #check if email exists in database already
# 	query = "SELECT * FROM users WHERE email=:email"
# 	data = {'email': email}
# 	i = mysql.query_db(query, data)
# 	if len(i)<1:
# 		query = "UPDATE users SET first_name=:first_name, last_name=:last_name, email=:email, updated_at=Now() WHERE id=:id"
# 		data = {
# 		'id': id,
# 		'first_name':first_name,
# 		'last_name':last_name,
# 		'email':email
# 	}
# 		result = mysql.query_db(query, data)
# 		flash("Please login")
# 	else:
# 		flash("Email already exists")
# 		return redirect('/users/'+str(id)+"/edit")

# 	return redirect('/')

# #View Edit page
# @app.route('/users/<id>/edit')
# def edituser(id):
# 	query = "SELECT id, first_name, last_name, email FROM users WHERE id=:id"
# 	data = {'id': id}
# 	result = mysql.query_db(query, data)
# 	return render_template("edituser.html", user=result[0])

# #Post create page
# @app.route('/users/create', methods=['POST'])
# def createuser():
# 	first_name = request.form['first_name']
# 	last_name = request.form['last_name']
# 	email=request.form['email']


#     #Validations Below
# 	if(len(first_name)==0):
# 		flash("First Name cannot be empty!")
# 		return redirect('/')
# 	elif(not first_name.isalpha()):
# 		flash("First Name cannot contain numbers")
# 		return redirect('/')

# 	if(len(last_name)==0):
#    		flash("Last Name cannot be empty!")
#    		return redirect('/')
#    	elif(not last_name.isalpha()):
#    		flash("Last Name cannot contain numbers")
#    		return redirect('/')

# 	if(len(email) < 1):
# 		flash("Email cannot be empty!")
# 		return redirect('/')
# 	elif not EMAIL_REGEX.match(email):
# 		flash("Invalid Email Address!") 
# 		return redirect('/')

#     #check if email exists in database already
# 	query = "SELECT * FROM users WHERE email=:email"
# 	data = {'email': email}
# 	i = mysql.query_db(query, data)
# 	if len(i)<1:
# 		data =  {'first_name': first_name,'last_name': last_name,'email' : email}
# 		query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, Now(), Now())"
# 		mysql.query_db(query, data)
# 		flash("Please login")
# 	else:
# 		flash("Email already exists")
# 		return redirect('/users/new')
# 	return redirect('/')


# @app.route('/users/<id>/destroy')
# def destroy(id):
# 	query = "DELETE  FROM users WHERE id=:id"
# 	data = {'id': id}
# 	result = mysql.query_db(query, data)
# 	return redirect('/')

# app.run(debug=True)
#   