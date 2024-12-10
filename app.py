from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'ada_are_mere'  # Change this to a secure random string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Specify the folder where files are uploaded

ALLOWED_EXTENSIONS = {'mp3', 'wav'}
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page if not logged in
bcrypt = Bcrypt(app)

## User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # These are the required Flask-Login methods
    def is_active(self):
        return True  # Always active, or you can implement logic based on user status

    def is_authenticated(self):
        return True  # Always authenticated, or implement your own logic

    def is_anonymous(self):
        return False  # Since we have normal user authentication, this should return False

    def get_id(self):
        return str(self.id)  # This is required by Flask-Login

# Song model
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    songs = Song.query.all()
    return render_template('index.html', songs=songs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):  # Check password
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    
    return render_template('login.html')


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash the password
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Create a new user and save it to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()


        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Admin-only route to add a song
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_song():
    if not current_user.is_admin:  # Use is_admin instead of role
        flash("You do not have permission to add songs.", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        genre = request.form['genre']

        if 'file' not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)

        file = request.files['file']

        # Check if the user uploaded a file and that it's valid
        if file.filename == '':
            flash("No selected file", "danger")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Now save the song record
            new_song = Song(title=title, artist=artist, genre=genre, file_path=filename)
            db.session.add(new_song)
            db.session.commit()

            flash("Song added successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid file format. Please upload an MP3 or WAV file.", "danger")
            return redirect(request.url)

    return render_template('add_song.html')


# Admin-only route to delete a song
@app.route('/delete_song/<int:song_id>', methods=['GET', 'POST'])
@login_required
def delete_song(song_id):
    if not current_user.is_admin:   # Only allow admins to delete songs
        flash('You do not have permission to delete songs.', 'danger')
        return redirect(url_for('index'))

    song = Song.query.get_or_404(song_id)
    db.session.delete(song)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    db.create_all()  # Create tables in the database if they don't exist
    app.run(debug=True)
