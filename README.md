# Lola's Bookstore
This program simulates a bookstore.  It maintains a list of books that are displayed by category and provides the ability for users to add, udate, and delete books.  All users can views the available books, but users who wish to makes updates, must login.  Login authentication is made available via Facebook and GoogePlus authentication providers.  Once logged in users, are able to add books and update or delete any of they books they have themselves added.  Books added by other users can only be updated/deleted by those users.



To run the program:
1. Setup the database by executing 'python database_setup.py'
2. Populate the database with dummy data by executing 'database_load.py'.
3. Execute the program by executing 'python main.py'.  The program will launch a webserver lisening on port 8000
4. Then from a browser, go to 'http://localhost:8000'.  The application will then be displayed.
