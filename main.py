from flask import Flask, render_template


from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField

from wtforms.validators import  DataRequired,Email,Length
import requests
from datetime import datetime
API="868c5469fc5add3122d3e7e8313c8f3e"
url="https://api.openweathermap.org/data/2.5/weather"
paramaters={
   "lat":"30.461515",
    "lon":"31.177681",
    "appid":API
}



class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=8)])
    submit = SubmitField(label="Log In")


app = Flask(__name__)

app.secret_key = "some secret string"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login",methods=["GET" ,"POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@gmail.com" and login_form.password.data == "123456789":
            response = requests.get(url=url, params=paramaters)
            datajason = response.json()
            description = datajason["weather"][0]["main"]
            tempreature = int(datajason["main"]["temp"] - 273.15)
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)

            return render_template("success.html",temp=tempreature,des=description,time=current_time)
        else:
            return render_template("denied.html")
    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)