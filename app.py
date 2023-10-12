from flask import Flask, render_template, Response, request,json, jsonify,redirect,request,flash,session,url_for
from detection import gen_frames,cv2,np
from flask_sqlalchemy import SQLAlchemy
import os,json,ast, datetime,subprocess
import psycopg2, psycopg2.extras,re
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

app.secret_key = 'NANOMERS_GROUP'

db_uri = 'postgresql://postgres:postgres@localhost:5432/Traffic_Light_Management'

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

DB_Host = "localhost"
DB_Name = "Traffic_Light_Management"
DB_User = "postgres"
DB_Pass = "20021914"

conn = psycopg2.connect(dbname=DB_Name, user=DB_User, password=DB_Pass, host=DB_Host)


current_datetime = datetime.datetime.now()
timestamp = current_datetime.strftime(f"%m-%d-%Y %I:%M:%S %p")

class Accounts(db.Model):
    __tablename__ = 'accounts'
    user_id = db.Column(db.INT, primary_key=True)
    username = db.Column(db.VARCHAR(20))
    email = db.Column(db.VARCHAR(30))
    password = db.Column(db.VARCHAR(20))

    # def __init__(self,username,email,password,confirm):
    #     self.username = username
    #     self.email = email
    #     self.password = password
    #     self.confirm = confirm

class Coordinates:
    def __init__(self, coordinates_array):
        self.coordinates_array = coordinates_array
    def save_coordinates(self):
        print(self.coordinates_array)


@app.route('/')

                  

@app.route('/home')
def home():
    cameras= available_cameras()
    camera_brandnames = []
    for camera in cameras:
        camera_info = camera_brand(camera)
        camera_brandnames.append(camera_info)
    nested_array = list(zip(cameras,camera_brandnames))

    page_title = "Home"
    return render_template('/pages/inside/home.html',
                        page_title=page_title,
                        camera_brandnames=camera_brandnames,
                        nested_array = nested_array)
# accessed the coordinates from ajax request

@app.route('/save_bounding', methods=['POST'])
def save_bounding():
    if request.method == "POST":
        drawed_coor = request.json
        # Write the JSON string to the file
        with open(f"static/dist/js/coordinates/{timestamp}.json", "w") as f:
            f.write(drawed_coor)
        # Close the file
        f.close()
        return redirect(url_for('home'))





def available_cameras(max_working_cameras=2):
    non_working_ports = []
    working_ports = []
    available_ports = []
    dev_port = 0
    while len(working_ports) < max_working_cameras: 
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
        else:
            is_reading, img = camera.read()
            if is_reading:
                working_ports.append(dev_port)
            else:
                available_ports.append(dev_port)
        dev_port += 1
    return working_ports

def camera_brand(cam_id):
    # Prepare the external command to extract serial number. 
    p = subprocess.Popen('udevadm info --name=/dev/video{} | grep ID_V4L_PRODUCT= | cut -d "=" -f 2'.format(cam_id),
                         stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p.status = p.wait()
    response = output.decode('utf-8')
    return response.strip()

@app.route('/video_feed', methods=["GET"])
def video_feed():
    # camera_id = int(request.args.get('camera_id', default=0))
    return Response(gen_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/manage_bounding', methods=["GET"])
def manage_bounding():
    page_title = "Manage Bounding"
    camera_id = request.form.get('camera_id')
    # if there are no cameras, it will give an notif
    no_cam_message = "No cameras detected"
    if camera_id is not None:
        return redirect(url_for('home'))
    # Set the camera id
    else:
        camera_id = request.args.get('selected_cam')
        # Get first frame from the video camera and save it into image
        first_frame = extract_first_frame(camera_id)
        if first_frame is not None:
            # Save the image to a folder named "static" in the same directory as the script
            image_filename = f"first_frame.png"
            image_path = os.path.join(app.root_path, "static/dist/img/first_frames", image_filename)
            cv2.imwrite(image_path, first_frame)
            print("Successfully Saved First Frame to static/dist/img/first_frames!") 
            # Manually construct the image URL
        else:
            return render_template('/pages/inside/manage_bounding.html',
                                page_title=page_title)
        return render_template(('/pages/inside/manage_bounding.html'), 
                            page_title=page_title)

# Get the first frame from the selected_camera_id
def extract_first_frame(camera_id):
    cap = cv2.VideoCapture(f"/dev/video{camera_id}")
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    return frame


@app.route('/register', methods = ['GET', 'POST'])
def register():
    page_title = "Register"
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'confirm' in request.form:

        Username =  request.form['username']
        Email =  request.form['email']
        Password = request.form['password']
        Confirm = request.form['confirm']

        _hashed_password = generate_password_hash(Password)
        cursor.execute('SELECT * FROM users Where username = %s', (Username,))
        account = cursor.fetchone()
        print(account)

        if account:
            flash('Account Already Existed!')

        elif not Username or not Password or not Email:
            flash('Please Fill Out The Form!')

        elif not re.match(r'[A-Za-z0-9]+', Username):
            flash('You Have Entered Invalid Email Adress')       

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            flash('You Have Entered Invalid Email Adress')

        elif Password != Confirm:
            flash('You Have Entered Different Password')

        else:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s,%s,%s)" , (Username, Email, _hashed_password))
            conn.commit()
            return redirect(url_for('login'))
            # flash('You Have Successfull Registered!')

    elif request.method == "POST":
        flash('Please Fill Out This Form')
    return render_template('/pages/outside/register.html', page_title=page_title)

@app.route('/index', methods=['GET', 'POST'])
def login():
    page_title="Login"
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username1' in request.form and 'password1' in request.form:
        Username1 = request.form['username1']
        Password1 = request.form['password1']
       

        cursor.execute('SELECT * FROM users WHERE username = %s', (Username1,))
        account = cursor.fetchone()

        if account:
            password_rs = account['password']
            print(password_rs)
            if check_password_hash(password_rs, Password1):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')

        else:
            flash ('Incorrect Username/Password!')

    
    return render_template('login.html',
                            page_title=page_title)     


# @app.route('/success_register', methods=['POST'])
# def success():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         confirm = request.form['confirm']
#         # Here will query the registered account to the database
#         accounts=Accounts(username,email,password,confirm)
#         db.session.add(accounts)
#         db.session.commit()

#         # accountResults = db.session.query(Accounts).filter(Accounts.user_id == 1)
#         # for account in accountResults:
#         #     print(account.username)
#         return render_template('login.html')


@app.route('/recover')
def recover():
    return render_template('/pages/outside/recover.html')


@app.route('/TrafficLightAPI')
def TLapi():
    page_title = "API"
    return render_template('/pages/inside/TrafficLightAPI.html',
                           page_title=page_title)

@app.route('/logout')
def logout():
    return render_template('/login.html')

if __name__ == '__main__':
    app.run(host="localhost", port=8080, threaded=True, debug=True)
