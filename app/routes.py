from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os


app = Flask(__name__, template_folder=os.path.abspath('templates'))
# app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session security
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def portfolio():
    return render_template('portfolio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username  # Store username in session
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('portfolio'))

@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')

if __name__ == '__main__':
    app.run(debug=True)
