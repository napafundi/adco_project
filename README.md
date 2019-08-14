# adco_project

This project was an attempt at creating a computer application to help The Albany Distilling Company with inventory management. I used Python and SQLite to develop the application.

Things I learned:
Python
  -Object Oriented Programming
  -Python list comprehension
  -Conditional statements
  -For/While loops
  -Function creation
  -API usage
  -Unit testing
SQLite
  -DB queries
  -Table creation
  -Insert, Update, and Delete statements
Tkinter
  -GUI design
  -Binding functions to GUI elements
  
Result:
  Although the application worked correctly with minimal bugs, I felt there was a lack of security. Python application's source-code is easily accessible to any user. This would allow anyone with minimal Python knowledge to mess with things. I also learned the importance of application design. The use of one file for all of the code became very messy and unmaintainable. The use of SQLite also prevented the application from sharing data between users. I thought that hosting the DB file within a dropbox folder would solve this. Unfortunately, SQLite DB files require access to the computer's root folder which isn't possible through Dropbox. I went on to re-write this application using MYSQL and AWS RDB hosting services.
