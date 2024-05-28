from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import Api, Resource, reqparse

# До запуска файла следует открыть Python терминал и прописать следующее:
# from main import db затем from main import app после app.app_context().push(), а уже потом db.create_all()


app = Flask(__name__)


# Подключение к существующей базе данных (MySQL),
# Вместо таких значений как name, password, db_name подставить ваши данные!
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://name:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


api = Api()

# Таблица в бзе данных (MySQL)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.String(100), default=datetime.utcnow)
    updated_at = db.Column(db.String(100), default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Класс для работы с API (Function based)
class Tasks_api(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", type=str)
    parser.add_argument("description", type=str)

    # Получение всех задач в формате json
    def get(self):
        # Сериализация: получаем все столбцы из базы данных
        tasks_serializer = []
        x = [col.name for col in Task.__table__.columns]
        for task in Task.query.order_by(Task.created_at).all():
            # Сериализация: добавляем данные из базы данных в переменную task_serializer,
            # а уже эту переменную (библиотеку) добавляем в наш список tasks_serializer
            task_serializer = {}
            for field in x:
                task_serializer[field] = getattr(task, field)
            tasks_serializer.append(task_serializer)
        return tasks_serializer

    # Добавление новой задачи
    def post(self):
        title = self.parser.parse_args()["title"]
        description = self.parser.parse_args()["description"]
        task = Task(title=title, description=description)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении задачи произошла ошибка'

    # Удаление задачи (api)
    def delete(self, id):
        task = Task.query.get_or_404(id)
        try:
            db.session.delete(task)
            db.session.commit()
            return redirect('/')
        except:
            return "При удалении задачи произошла ошибка"

    # Обновление данных (api)
    def put(self, id):
        task = Task.query.get_or_404(id)
        task.title = self.parser.parse_args()["title"]
        task.description = self.parser.parse_args()["description"]
        task.updated_at = datetime.utcnow()
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'При редактировании задачи произошла ошибка'


api.add_resource(Tasks_api, "/tasks/api", "/tasks/api/<int:id>")
api.init_app(app)


# Главная страница
@app.route('/')
def main1():
    # Получаем все задачи из базы данных
    tasks = Task.query.order_by(Task.created_at).all()
    return render_template("tasks-list.html", tasks=tasks)

# Функция для добавления новой задачи
@app.route('/tasks', methods=['POST', 'GET'])
def tasks():
    if request.method == 'POST':
        # Получаем данные c HTML файла и присваиваем их к переменным
        title = request.form['title']
        description = request.form['description']
        # Добавление задачи к базе данных
        task = Task(title=title, description=description)

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении задачи произошла ошибка'
    elif request.method == 'GET':
        return render_template("add-task.html", tasks=tasks)

# Функция для удаления задачи
@app.route('/tasks-delete/<int:id>')
def delete_task(id):
    # Получение данных по id
    task = Task.query.get_or_404(id)
    try:
        # Удаление данных
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении задачи произошла ошибка"


# Функция для обновления задачи
@app.route('/tasks-update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    # Получение данных по id
    task = Task.query.get(id)
    if request.method == 'POST':
        # Изменение данных по столбцам
        task.title = request.form['title']
        task.description = request.form['description']
        task.updated_at = datetime.utcnow()

        try:
            # Сохранение данных на базе данных
            db.session.commit()
            return redirect('/')
        except:
            return 'При редактировании задачи произошла ошибка'
    else:
        return render_template("update-task.html", task=task)


if __name__ == '__main__':
    app.run(debug=True)