from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

class User:
    def __init__(self, name, job_title, phone) -> None:
        self.name = name
        self.job_title = job_title
        self.phone = phone

class Location:
    def __init__(self, name, address) -> None:
        self.name = name
        self.address = address


@app.route('/signature <email> <pronouns>', methods=['GET', 'POST'])
def signature(email, pronouns):
    """Generates email signature with information from LV Databases"""

    # Create a connection to SQL
    con = sqlite3.connect('lvdatabase.db')
    
    # Create cursor object
    cur = con.cursor()
    
    # SQL query to search for user by email
    query = f"""SELECT * from Users
                WHERE email = {email}"""
    cur = cur.execute(query)
    data = cur.fetchall()
    
    # Create User class instance
    user = User(name=data['Name'], job_title=data['Job Title'], phone=data['Phone'])
    
    # Create Location instance
    location = Location(name=data['Location'], address=data['Address'])

    # Generates signature string based on if the user chose to select pronouns
    if pronouns == 'I Do Not Wish To Select':
        signature = signature = f"<b>{user.name}</b> | {user.job_title} | {location.name}\n | {location.address} | Mobile: {user.phone} | {email}"
    else:
        signature = f"<b>{user.name}</b> | {pronouns} | {user.job_title} | {location.name}\n | {location.address} | Mobile: {user.phone} | {email}"
    
    # Returns the signature string to the HTML document to be rendered to the client
    return render_template('signature.html', signature=signature)



@app.route('/', methods=['GET', 'POST'])
def home():
    """Gets the email and pronouns (if the user chooses) via HTML form"""
    if request.method == "POST":
        email = request.form['email']
        pronouns = request.form['pronouns']
        
        # Returns the email and pronouns to pass it to the /signature route
        return redirect(url_for('signature', email=email, pronouns=pronouns))

    else:
        # Gets the email and pronouns from the user
        email = request.args.get('email')
        pronouns = request.args.get('pronouns')

        return render_template('index.html')



app.run(debug=True)