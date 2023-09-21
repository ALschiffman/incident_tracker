from flask_app import app
from flask_app.controllers import classes
from flask_app.controllers import incidents
from flask_app.controllers import students
from flask_app.controllers import users

if __name__=="__main__":
    app.run(debug=True)