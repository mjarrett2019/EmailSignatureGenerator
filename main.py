from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

class User:
    def __init__(self, email, first, last, job_title, phone, location_id) -> None:
        self.email = email
        self.first = first
        self.last = last
        self.job_title = job_title
        self.phone = phone
        self.location_id = location_id

    def get_name(self):
        name = f"{self.first} {self.last}"
        return name

class Location:
    def __init__(self, location_id, name, address, address2, city, state, zip) -> None:
        self.location_id = location_id
        self.name = name
        self.address = address
        self.address2 = address2
        self.city = city
        self.state = state
        self.zip = zip

    def get_full_address(self):
        if self.address2 == "NULL":
            address = f"{self.address} {self.city}, {self.state} {self.zip}"
        else:
            address = f"{self.address} {self.address2} {self.city}, {self.state} {self.zip}"
        
        return address


@app.route('/signature <email> <pronouns>', methods=['GET', 'POST'])
def signature(email, pronouns):
    """Generates email signature with information from LV Databases"""

    # Create a connection to SQL
    con = sqlite3.connect('src/test.db')
    
    # Create cursor object
    cur = con.cursor()
    
    # SQL query to search for user by email
    query = f"""SELECT * from users
                WHERE email = '{email}'"""
    cur = cur.execute(query)
    data = cur.fetchall()
    
    for i in data:
        user = User(email=i[0],
                    first=i[1],
                    last=i[2],
                    job_title=i[3],
                    phone=i[4],
                    location_id=i[5])
    
    # Get Location
    loc_query = f"""SELECT * from locations
                    WHERE location_id = '{user.location_id}'"""
    cur = cur.execute(loc_query)
    data = cur.fetchall()

    for l in data:
        location = Location(location_id=l[0],
                            name=l[1],
                            address=l[2],
                            address2=l[3],
                            city=l[4],
                            state=l[5],
                            zip=l[6])

    # Generates signature string based on if the user chose to select pronouns
    if pronouns == '---':
        signature = f"<b>{user.get_name()}</b> | {user.job_title} | {location.name}\n | {location.get_full_address()} | Mobile: {user.phone} | {email}"
    else:
        signature = f"<b>{user.get_name()}</b> | {pronouns} | {user.job_title} | {location.name}\n | {location.get_full_address()} | Mobile: {user.phone} | {email}"
    
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