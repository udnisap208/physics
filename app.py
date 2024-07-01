from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user class
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Mock database of users
users = {
    'user1': User(id=1, username='user1', password='password1'),
    'user2': User(id=2, username='user2', password='password2')
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/')
@login_required
def home():
    return render_template('home.html', username=current_user.username)

@app.route('/recordings')
@login_required
def recordings():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return render_template('recordings.html', months=months)

@app.route('/recordings/<month>')
@login_required
def month_recordings(month):
    weeks = ['week1', 'week2', 'week3', 'week4']
    return render_template('month.html', month=month, weeks=weeks)

@app.route('/recordings/<month>/<week>')
@login_required
def week_recordings(month, week):
    video_url = url_for('static', filename=f'videos/{month}/{week}.mp4')
    return render_template('week.html', month=month, week=week, video_url=video_url)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
