from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy import exc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

login_manager = LoginManager()
login_manager.init_app(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
 
 
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """Loads the user if the id exists in the database"""
    return db.get_or_404(User, user_id)


@app.route('/')
def home():
    """Renders the homepage"""
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    """
    If you click on register this will render a form where
    you'll input your details which get saved into the users database.
    You will also get logged in
    """
    if request.method == "POST":
        try:
            hashed_salted_password = generate_password_hash(
                request.form.get('password'),
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=request.form.get('email'),
                password=hashed_salted_password,
                name=request.form.get('name'),
            )
            db.session.add(new_user)
            db.session.commit()
            name = request.form.get('name')
            login_user(new_user)
            return redirect(f"/secrets/{name}")
        except exc.IntegrityError as e:
            flash("You've already signed up with that email, login instead")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    """If you already have an account you'll input your login details. If your email matches
    one in the database you will be logged in """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user:
            flash("That email does not exist. Please try again")
            return redirect(url_for("login"))
        if check_password_hash(user.password, password):
            login_user(user)
            name = user.name
            return redirect(f"/secrets/{name}")
        else:
            flash("Password incorrect. Please try again")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/secrets/<name>')
@login_required
def secrets(name):
    """Renders the secrets page if you are logged in"""
    name = current_user.name
    return render_template("secrets.html", name=name)


@app.route('/logout')
def logout():
    """Logs you out"""
    logout_user()
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    """Allows you to download the pdf"""
    return send_from_directory('static', path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)

