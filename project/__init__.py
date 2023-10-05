

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application
app = Flask(__name__, template_folder='templates')

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)
from project.main.views import main_blueprint
from project.loaners.views import loaners_blueprint
from project.books.views import books_blueprint
from project.loans.views import loans_blueprint


app.register_blueprint(main_blueprint)
app.register_blueprint(loaners_blueprint, url_prefix='/loaners')
app.register_blueprint(books_blueprint, url_prefix='/books')
app.register_blueprint(loans_blueprint, url_prefix='/loans')


# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
