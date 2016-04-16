from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc, distinct
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from datetime import datetime

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Lola's Bookstore Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///bookstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """Creates a state token and returns to user in login page.
       The state token is created to prevent Cross Site Forgery.
    """
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """Logs user in using Facebook's authentication
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type='\
        'fb_exchange_token&client_id=%s&client_secret=%s&'\
        'fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?'\
        '%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "url sent for API access:%s" % url
    print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in
    # order to properly logout, let's strip out the information
    # before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?'\
        '%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;'\
        'border-radius: 150px;-webkit-border-radius: 150px;'\
        '-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """Dissconnects user from Facebook and invalidates the access token.
    """
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?'\
        'access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Logs user in using GooglePlus's authentication
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # stored_credentials = login_session.get('credentials')
    # if stored_credentials is not None and gplus_id == stored_gplus_id:
    stored_gplus_id = login_session.get('gplus_id')
    stored_accessToken = login_session.get('access_token')
    if stored_accessToken is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already '
                                 'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'\
        '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Dissconnects user from GooglePlus and invalidates the access token.
    """
    # Only disconnect a connected user.
    # credentials = login_session.get('credentials')
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    """Dissconnects user from from whichever authentication provider they
       logged in with.
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('getLatestBooks'))
    else:
        flash("You were not logged in")
        return redirect(url_for('getLatestBooks'))


@app.route('/')
def getLatestBooks():
    """Displays on the home page the last 5 books that have
       been created/updated and the list of categories.
    """
    categories = getCategories()
    books = session.query(Book).order_by(desc(Book.dateUpdated)).limit(5)

    return render_template('home.html', categories=categories, books=books)


@app.route('/books/<string:book_category>')
def getBooksByCategory(book_category):
    """Retrieves all books in the given category and displays the books
       on the bookCategories page.
    """
    categories = getCategories()
    books = session.query(Book).filter_by(category=book_category).all()

    return render_template('bookCategories.html', book_category=book_category,
                           categories=categories, books=books)


@app.route('/books/<int:book_id>')
def getBookDetails(book_id):
    """Retrieves the book details of the book with the given book id
       and displays the book on the bookDetails page.
    """
    book = session.query(Book).filter_by(id=book_id).one()
    return render_template('bookDetails.html', book=book)


@app.route('/books/add/', methods=['GET', 'POST'])
def addBook():
    """Accepts two methods: Get and Post.  For the GET method, it displays the
       the addBook page for the neccessary book info to be entered.  For the
       POST method it retrieves the information from the input form, adds a
       new book and redirects user to the home page.  It also verifies that
       user is logged in.  If user is not logged in, they are redirected
       to the login page.
    """
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newBook = Book(user_id=login_session['user_id'],
                       title=request.form['title'],
                       author=request.form['author'],
                       category=request.form['category'],
                       price=float(request.form['price']),
                       dateUpdated=datetime.today(),
                       inventoryCount=int(request.form['inventoryCount']),
                       description=request.form['description'])
        session.add(newBook)
        session.commit()
        flash('%s has been Successfully Created' % newBook.title)
        return redirect(url_for('getLatestBooks'))
    else:
        categories = getCategories()
        return render_template('addBook.html', categories=categories)


@app.route('/books/<int:book_id>/edit/', methods=['GET', 'POST'])
def editBook(book_id):
    """Accepts two methods: Get and Post.  For the GET method, it displays the
       the editBook page for the neccessary book info to be entered.  For the
       POST method it retrieves the information from the input form, updates
       the new information for the given book and redirects user to the
       home page. It also verifies that user is loggedin.  If user is
       not logged in, they are redirected to the login page.  It then confirms
       that the user is the creator of the book they are attempting to edit.
    """
    if 'username' not in login_session:
        return redirect('/login')

    book = session.query(Book).filter_by(id=book_id).one()
    if book.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
            "to edit this book. Please create your own book in order to "\
            "edit.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        book.author = request.form['author']
        book.category = request.form['category']
        book.price = float(request.form['price'])
        book.inventoryCount = int(request.form['inventoryCount'])
        book.description = request.form['description']
        book.dateUpdated = datetime.today()
        session.add(book)
        session.commit()
        flash('%s has been Successfully Edited' % book.title)
        return redirect(url_for('getLatestBooks'))
    else:
        categories = getCategories()
        return render_template('editBook.html', categories=categories,
                               book=book)


@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    """Accepts two methods: Get and Post.  For the GET method, it displays the
       the deleteBook page for the given book deletion to be confirmed.
       For the POST method it deletes the given book and redirects user to
       the home page. It also verifies that user is loggedin.  If user is
       not logged in, they are redirected to the login page. It also confirms
       that the user is the creator of the book they are attempting to delete.
    """
    if 'username' not in login_session:
        return redirect('/login')

    book = session.query(Book).filter_by(id=book_id).one()
    if book.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
            "to delete this book. Please create your own book in order "\
            "to delete.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(book)
        session.commit()
        flash('%s Successfully Deleted' % book.title)
        return redirect(url_for('getLatestBooks'))
    else:
        return render_template('deleteBook.html', book=book)


@app.route('/books/JSON')
def allBooksJSON():
    """Returns a JSON representation of all available books.
    """
    books = session.query(Book).all()
    return jsonify(books=[r.serialize for r in books])


@app.route('/books/<int:book_id>/JSON')
def singleBookJSON(book_id):
    """Returns a JSON representation of the given book.
    """
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(Book=book.serialize)


def getCategories():
    """Returns a list of all catgegories.
    """
    categories = session.query(distinct(Book.category)).\
        order_by(asc(Book.category)).all()
    categories = [x[0].encode() for x in categories]
    return categories


def createUser(login_session):
    """Creates a new user.
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Returns user object for the given userId.
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """Return user object for the given user's email.
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
