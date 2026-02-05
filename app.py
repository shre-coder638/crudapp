from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)
db.create_all()


@app.route('/', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_employee = Employee(name=name, email=email)
        db.session.add(new_employee)
        db.session.commit()
    all_employees = Employee.query.all()
    return render_template('index.html', allemp=all_employees)

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/home')
def homepage():
    employee=Employee(name="John Doe", email="Email")
    db.session.add(employee)
    db.session.commit()
    all_employees = Employee.query.all()
    return render_template('Home.html')

@app.route("/delete/<int:id>")
def delete(id):
    employee = Employee.query.filter_by(id=id).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=['GET','POST'])
def update(id):
    employee = Employee.query.filter_by(id=id).first()
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        db.session.commit()
        return redirect("/")
    return render_template('update.html', Employee=employee)
if __name__ == '__main__':
    app.run(debug=True)