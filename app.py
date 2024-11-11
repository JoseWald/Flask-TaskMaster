from datetime import datetime
from flask import Flask, render_template, request, redirect,  url_for
from flask_sqlalchemy import SQLAlchemy



# Référencement de cette application Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/' , methods=['GET' , 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error while adding task'

    else:  
        tasks = ToDo.query.order_by(ToDo.date_created).all() 
        return render_template('index.html' , tasks = tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_del = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error while deleting task'

@app.route('/update/<int:id>' , methods=['POST' , 'GET'])
def update(id):
    return ''

# Création des tables dans la base de données
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
