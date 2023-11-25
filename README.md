# Authentication with Flask

## Overview

In this project I learnt how to add and authenticate users.
This was done using flask_login, The users credentials are stored in the users database.

This was a backend development project. The frontend development was already done.
I had to refactor some of it to work with the backend code.

## Users

When you register you will need to input your details in the 
registration form which will save your details into the users database and then
log you in.

If you are already a user you can log in using your email and password.
If you try to register when you are already signed up a flash message will 
appear instructing you to sign in. If you try to log in 
with incorrect credentials, or you haven't yet signed up, a flash message will appear 
warning you of the error.

When you are logged in you can download a pdf from the secrets page.
The login/register button are removed from the nav bar when you are logged in.

## Technologies / modules
Python
sqlalchemy
flask
flask_login
flask_sqlalchemy
werkzeug.security