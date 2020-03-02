from app import app, mysql
from flask import request
from app.forms import LoginForm
from app.forms import RegisterForm
from flask import render_template, flash, redirect, url_for

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
    carbon_list = []

    carbon_list.append(type_totals['car']*411)
    carbon_list.append( type_totals['bus']*822)
    carbon_list.append(type_totals['train']*14)
    
    print(carbon_list)

    return render_template('home.html', title='LTU Transport Dashboard', max=17000, values = values, labels= labels, colors = colors)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home'))
    return render_template('login.html',  title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        
        # call the connection method
        cursor, conn = connection()
        # check if the user exist in the db
        count = cursor.execute('select * from user where email=%s', form.email.data)  # prevent SqlInject

        if count == 0:
           # count 0 email
           cursor.execute("INSERT INTO user(username, email, password) VALUES (%s, %s, %s)", (form.username.data, form.email.data, form.password.data))
           conn.commit()
           cursor.close()
           flash('Thanks for registering')
           #return redirect(url_for('/login'))
        else:
           # the email exists
           flash('User with this email address exists, please login')
        
    return render_template('register.html', title='Register', form=form)

