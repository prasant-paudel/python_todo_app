from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    todos = Todo.query.all()
    r = db.engine.execute('select max(id) from todo')
    global id_max
    id_max = 0
    for x in r:
        id_max = x[0]

    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    print('\n', request.form, '\n')
    # print(request.form['1'])
    global id_max
    for id in range(1, id_max):
        try:
            value = request.form[f'{id}']
            if str(value) == 'on':
                print('Status of', id, end=': ')
                print(Todo.query.all()[id-1].complete)
                
                db.engine.execute(f'update todo set complete=1 where id={id};')
                r = db.engine.execute(f'select * from todo where id={id};')
                for i in r:
                    print(i)
                
                print('Status of', id, end=': ')
                print(Todo.query.all()[id-1].complete)
                
        except:
            db.engine.execute(f'update todo set complete=1 where id={id};')
            continue



    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
