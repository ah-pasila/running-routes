# Running Routes Helsinki App

## Introduction

This web application contains info about nice running routes in Helsinki.

A normal user can create an account to the application and after doing this, add route suggestions for others to see and try.

Route suggestions can be saved as images to the service (Google Maps? or maybe GPX files - or both?).

Basic info such as length and difficulty can also be saved.

Routes can be rated.

Users can complete routes and save their times. After doing this, they are able to compare their times.

Admins are able to delete users, routes and reviews. Normal users can only delete their own reviews and route suggestions.

## Note on 18th December 2022:

The latest published version: https://tsoha-running-routes.fly.dev/.

For local testing, expression ".replace("://", "ql://", 1)" in db.py should be removed after cloning codes.  

In the Running Routes Helsinki App, a user can create an account and login. After this, the user can save routes, maps, running times and reviews.

It is possible to browse saved routes, maps and reviews. The user can check route information, reviews and times which he/she saved from his/her personal view.

Delete (=updating visibility of rows) and admin role functionalities were unfortunately not implemented in the final version. I'm interested in hearing advice how to get UPDATE-based delete functionality up and running (it seems I did not find proper formulation of the command). 

In terms of security, CSRF tokens were taken into use. Measures to avoid SQL injections and XSS vulnerability were also taken. 

However, there could be more checks related to the length & type of the data and better error handling.
