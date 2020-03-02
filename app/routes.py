from app import app, mysql
from .forms import LoginForm, RegistrationForm
from flask import url_for, redirect, flash, render_template

# ----------------------
# APP ROUTES
# ----------------------
# connect to database
conn = mysql.connect()

# create a database cursor
cursor = conn.cursor()



def get_rows():
    """ gets query results from cursor as
        list of dicts
    """
    fields = [i[0] for i in cursor.description]
    return [ dict(zip(fields, row)) for row in list(cursor.fetchall())]

@app.route('/')
def home():
    """
        Landing page for application
    """
    cursor.execute("SELECT id, journey_type,distance FROM journey")
    journeys = get_rows()
    type_totals = {}
    labels = []
    values = []
    colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    for journey in journeys:

        if journey['journey_type'] not in type_totals.values():
            type_totals [journey['journey_type']] = [journey['distance']]
        else:
            type_totals[journey['journey_type']]+=journey['distance']
    for key, value in type_totals.items():      
        labels.append(key)
        values.append(value)
    values = [int("".join([str(y) for y in x])) for x in values]
    print(values)

    return render_template('home.html', title='LTU Transport Dashboard', max=17000, values = values, labels= labels, colors = colors)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():
        cursor.execute('SELECT email, password FROM user')
        #cursor = db.profiles.find({"email": form.email.data, "password": form.password.data})
        if cursor.rowcount >0:
           flash('You have logged in', 'success')        
           return render_template('home.html')
        else:
            flash('Log in unsuccessful please try again', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #new_profile = {'username' : form.username.data, 'email' : form.email.data, 'password': form.password.data}
        #db.profiles.insert_one(new_profile)
        cursor.execute('INSERT INTO user (username, email, password) VALUES (%s, %s, %s)', form.username.data, form.email.data, form.password.data )
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)