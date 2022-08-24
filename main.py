from flask import Flask, render_template, request, redirect, url_for

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


@app.route('/signature <email> <pronouns>')
def signature(email, pronouns):
    user = User(name='Matt JARRETT', job_title='Deskside Technician II', phone='248.989.9999')
    location = Location(name='LV Headoffice', address='1 E 57th Street New York, NY 10022')
    signature = f"<b>{user.name}</b> | {pronouns} | {user.job_title} | {location.name}\n | {location.address} | Mobile: {user.phone} | {email}"
    return render_template('signature.html', signature=signature)



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        email = request.form['email']
        pronouns = request.form['pronouns']
        
        return redirect(url_for('signature', email=email, pronouns=pronouns))

    else:
        email = request.args.get('email')
        pronouns = request.args.get('pronouns')

        return render_template('index.html')



app.run(debug=True)