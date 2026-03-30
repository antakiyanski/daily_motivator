from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Ma'lumotlar bazasi sozlamalari (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Motivatsiyalar ro'yxati
motivations = [
    "Bugun kechagidan yaxshiroq bo'lish uchun imkoniyat!",
    "Kichik qadamlar katta natijalarga olib keladi.",
    "To'xtab qolma, Master, muvaffaqiyat yaqin!",
    "Cybersecurity dunyosini zabt etish vaqti keldi!",
    "Intizom — bu xohish va natija orasidagi ko'prik."
]

# Vazifalar modeli
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# Bazani yaratish (Faqat bir marta ishga tushadi)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todo_list = Todo.query.all()
    quote = random.choice(motivations)
    return render_template('index.html', todo_list=todo_list, quote=quote)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)