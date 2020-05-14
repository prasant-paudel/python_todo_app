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
    
    return render_template('app.html', todos=todos)
    # return render_template('index.html', todos=todos)

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

    # detecting max id
    r = db.engine.execute('SELECT MAX(id) FROM todo')
    global id_max
    id_max = 0
    for x in r:
        id_max = x[0]
    
    for id in range(1, id_max+1):
        try:
            value = request.form[f'{id}']
            if str(value) == 'on':
                db.engine.execute(f'UPDATE todo SET complete=1 WHERE id={id};')
        except:
            db.engine.execute(f'UPDATE todo SET complete=0 WHERE id={id};')
    return redirect(url_for('index'))


@app.route('/delete')
def delete():
    id = request.args['id']
    db.engine.execute(f"DELETE FROM todo WHERE id={id}")
    return redirect(url_for('index'))


# query to the table todo
r = db.engine.execute(f'SELECT * FROM todo;')
print('')
for i in r:
    print(i)
print('')

if __name__ == '__main__':
    app.run()
