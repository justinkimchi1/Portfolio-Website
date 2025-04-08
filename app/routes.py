from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
from authlib.integrations.flask_client import OAuth
import os, json
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__, template_folder=os.path.abspath('templates'))
# app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session security
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

oauth = OAuth(app)

PROJECTS_FILE = os.path.join('data', 'projects.json')

google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/')
def portfolio():
    return render_template('portfolio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        session['can_edit_projects'] = False
        return redirect(url_for('profile'))
    return render_template('login.html')
    

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear() # Remove username from session
    return redirect(url_for('portfolio'))

@app.route('/projects')
def projects():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_projects()
    return render_template('projects.html',
        can_edit=session.get('can_edit_projects', False),
        project_1=data['project_1'],
        project_2=data['project_2'],
        project_3=data['project_3']
    )


@app.route('/resume')
def resume():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('resume.html')

@app.route('/authorize')
def authorize():
    try:
        token = google.authorize_access_token()
        resp = google.get('https://openidconnect.googleapis.com/v1/userinfo')
        user_info = resp.json()
        email = user_info.get('email')
        session['username'] = email
        session['can_edit_projects'] = (email == 'kimsuungjuu@gmail.com')
        return redirect(url_for('profile'))
    except Exception as e:
        print(f"OAuth error: {str(e)}")
        # Clear any potentially corrupted session data
        session.clear()
        # Redirect to login page with error message
        return redirect(url_for('login', error="Authentication failed. Please try again."))

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/save_projects', methods=['POST'])
def save_projects():
    if 'username' not in session or not session.get('can_edit_projects', False):
        return redirect(url_for('login'))

    data = {
        'project_1': request.form.get('project_1', ''),
        'project_2': request.form.get('project_2', ''),
        'project_3': request.form.get('project_3', '')
    }
    save_projects_data(data)
    flash('Projects updated successfully!')
    return redirect(url_for('projects'))


def load_projects():
    if not os.path.exists(PROJECTS_FILE):
        return {
            'project_1': '',
            'project_2': '',
            'project_3': ''
        }
    with open(PROJECTS_FILE, 'r') as f:
        return json.load(f)

def save_projects_data(data):
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
