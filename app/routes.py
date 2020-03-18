from app import app, mysql
from flask import request
from app.forms import LoginForm
from app.forms import RegisterForm
from app.forms import JourneyInfoForm
from flask import render_template, flash, redirect, url_for
from flask_wtf.csrf import CSRFError
from app import csrf

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
    ##working out total distance of transport type
    cursor.execute("SELECT id, journey_type,distance FROM journey")
    journeys = get_rows()
    type_totals = {}
    labels = []
    values = []
    colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    bus_distance =0
    train_distance =0
    car_distance =0
    walk_distance =0
    cycle_distance =0

    for journey in journeys:
        if journey['journey_type'] == 'bus':
            bus_distance+=int(journey['distance'])
        elif journey['journey_type'] == 'train':
            train_distance += int(journey['distance'])
        elif journey['journey_type'] == 'car':
            car_distance += int(journey['distance'])
        elif journey['journey_type'] == 'walk':
            walk_distance += int(journey['distance'])
        else:
            cycle_distance += int(journey['distance'])

    type_totals={'bus':bus_distance,
                'train':train_distance,
               'car':car_distance,
              'walk':walk_distance,
             'cycle':cycle_distance}
    
    for key, value in type_totals.items():      
        labels.append(key)
        values.append(value)

    #carbon values for carbon graph
    carbon_values = [822, 0, 411, 14, 0]

    #yeary output graph
    months=['jan','feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    cursor.execute("select * from journey where journey_date >= '2020-01-01' AND journey_date < '2020-06-01'")
    results= get_rows()
    print(results)
    
    carbon_list = [a*b for a,b in zip(carbon_values,values)]
    return render_template('home.html', title='LTU Transport Dashboard', max=17000, values = values, labels= labels, carbon = carbon_list, colors = colors, months=months)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/journey', methods=['GET', 'POST'])
def journey():
    
    TYPE_CHOICES = [('1', 'walk'), ('2', 'bus'), ('3', 'train'), ('4', 'car'), ('5', 'bike')]
    form = JourneyInfoForm()

    if form.validate_on_submit():
        print('post')
        
        count = cursor.execute('select * from user where username=%s', form.username.data)  # prevent SqlInject
        cursor.execute('select * from user where username=%s', form.username.data)
        user_details = get_rows()
        user_id = user_details[0]['user_id']

        if count != 0:
           cursor.execute("INSERT INTO journey(user_id, journey_type, distance, journey_date) VALUES (%s, %s, %s, %s)",
           (user_id, form.type.data, form.distance.data, form.journey_date.data))
           conn.commit()
           flash('thanks for adding to our data')
           print(user_id, form.type.data, form.distance.data, form.journey_date.data)
           return render_template('home_after_login.html')

    return render_template('journey.html', form=form)

@app.route('/home_after_login', methods=['GET', 'POST'])
def home_after_login():
    return render_template('home_after_login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST' and form.validate():
            user = form.username.data
            cursor.execute('select * from user where username=%s', form.username.data)
            user_details = get_rows()

            if user_details[0]['username'] == user:
                flash('Welcome back')
                id =user_details[0]['user_id']
                return redirect(url_for('home_after_login', user_id = id ))
            else:
                # no user found
                flash('User not found')
                return render_template('login.html',  title='Sign In', form=form)
    return render_template('login.html',  title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        # check if the user exist in the db
        count = cursor.execute('select * from user where email=%s', form.email.data)  # prevent SqlInject

        if count == 0:
           # count 0 email
           cursor.execute("INSERT INTO user(username, email, password) VALUES (%s, %s, %s)", (form.username.data, form.email.data, form.password.data))
           conn.commit()
           flash('Thanks for registering')
        else:
           # the email exists
           flash('User with this email address exists, please login')       
    return render_template('register.html', title='Register', form=form)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

def check_csrf():
    if not is_oauth(request):
        csrf.protect();
