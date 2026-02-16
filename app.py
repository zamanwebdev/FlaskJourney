from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html", name="Zaman")

@app.route('/profile/<name>')
def profile(name):
    skills = ["Python", "Flask", "WordPress", "Automation"]
    return render_template("profile.html", username=name, skills=skills)

if __name__ == '__main__':
    app.run(debug=True)
