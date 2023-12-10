# from flask import Flask, render_template,request, redirect
# #Подключение библиотеки баз данных
# from flask_sqlalchemy import SQLAlchemy


# app = Flask(__name__)
# #Подключение SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# #Создание db
# db = SQLAlchemy(app)
# #Создание таблицы

# class Card(db.Model):
#     #Создание полей
#     #id
#     id = db.Column(db.Integer, primary_key=True)
#     #Заголовок
#     title = db.Column(db.String(100), nullable=False)
#     #Описание
#     subtitle = db.Column(db.String(300), nullable=False)
#     #Текст
#     text = db.Column(db.Text, nullable=False)

#     #Вывод объекта и id
#     def __repr__(self):
#         return f'<Card {self.id}>'
    

# #Задание №1. Создать таблицу User

# class User(db.Model):
#     #Создание полей
#     #id
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     login = db.Column(db.String(100), nullable=False)
#     #Описание
#     password = db.Column(db.String(100), nullable=False)

# class User_Card(db.Model):
#     #Создание полей
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id_U = db.Column(db.Integer)
#     id_C = db.Column(db.Integer)

   






# #Запуск страницы с контентом
# @app.route('/', methods=['GET','POST'])
# def login():
#         error = ''
#         if request.method == 'POST':
#             form_login = request.form['email']
#             form_password = request.form['password']
            
#             #Задание №4. Реализовать проверку пользователей
#             user_db = User.query.all()
#             for i in user_db:
#                 if form_login == i.login and form_password == i.password:
#                     return redirect('/index')
#             else:
#                 error = "не угадал!"
#                 return render_template("login.html", error = error)

            
#         else:
#             return render_template('login.html')



# @app.route('/reg', methods=['GET','POST'])
# def reg():
#     if request.method == 'POST':
#         login= request.form['email']
#         password = request.form['password']
        
#         #Задание №3. Реализовать запись пользователей
#         user = User(login = login, password = password)

#         db.session.add(user)
#         db.session.commit()

        
#         return redirect('/')
    
#     else:    
#         return render_template('registration.html')


# #Запуск страницы с контентом
# @app.route('/index')
# def index():
#     #Отображение объектов из БД
#     cards = Card.query.order_by(Card.id).all()
#     return render_template('index.html', cards=cards)

# #Запуск страницы c картой
# @app.route('/card/<int:id>')
# def card(id):
#     card = Card.query.get(id)

#     return render_template('card.html', card=card)

# #Запуск страницы c созданием карты
# @app.route('/create')
# def create():
#     return render_template('create_card.html')

# #Форма карты
# @app.route('/form_create', methods=['GET','POST'])
# def form_create():
#     if request.method == 'POST':
#         title =  request.form['title']
#         subtitle =  request.form['subtitle']
#         text =  request.form['text']

#         #Создание объкта для передачи в дб

#         card = Card(title=title, subtitle=subtitle, text=text)

#         db.session.add(card)
#         db.session.commit()
#         cards = Card.query.get(title)
        
#         return redirect('/index')
#     else:
#         return render_template('create_card.html')

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template,request, redirect, session
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app)
#Создание таблицы

class Card(db.Model):
    #Создание полей
    #id
    id = db.Column(db.Integer, primary_key=True)
    #Заголовок
    title = db.Column(db.String(100), nullable=False)
    #Описание
    subtitle = db.Column(db.String(300), nullable=False)
    #Текст
    text = db.Column(db.Text, nullable=False)
    #Добавление поля для связи с пользователем
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #Вывод объекта и id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Задание №1. Создать таблицу User

class User(db.Model):
    #Создание полей
    #id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    login = db.Column(db.String(100), nullable=False)
    #Описание
    password = db.Column(db.String(100), nullable=False)
    #Добавление поля для связи с картами
    cards = db.relationship('Card', backref='user', lazy=True)

#Задание №2. Удалить таблицу User_Card, так как она не нужна

#Задание №3. Добавить секретный ключ для сессии
app.secret_key = 'some_secret_key'

#Запуск страницы с контентом
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            #Задание №4. Реализовать проверку пользователей
            user_db = User.query.filter_by(login=form_login).first()
            if user_db and user_db.password == form_password:
                #Задание №5. Сохранить id пользователя в сессии
                session['user_id'] = user_db.id
                return redirect('/index')
            else:
                error = "не угадал!"
                return render_template("login.html", error = error)

            
        else:
            return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login= request.form['email']
        password = request.form['password']
        
        #Задание №3. Реализовать запись пользователей
        user = User(login = login, password = password)

        db.session.add(user)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


#Запуск страницы с контентом
@app.route('/index')
def index():
    #Задание №6. Проверить, что пользователь вошел в систему
    if 'user_id' in session:
        #Отображение объектов из БД
        #Задание №7. Фильтровать карты по текущему пользователю
        cards = Card.query.filter_by(user_id=session['user_id']).order_by(Card.id).all()
        return render_template('index.html', cards=cards)
    else:
        return redirect('/')

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)
    #Задание №8. Проверить, что карта принадлежит текущему пользователю
    if card and card.user_id == session['user_id']:
        return render_template('card.html', card=card, id = id)
    else:
        return redirect('/index')
    

@app.route('/delete/<int:id>')
def delete(id):
    #Проверить, что пользователь вошел в систему
    if 'user_id' in session:
        #Найти card по id
        card = Card.query.get(id)
        #Проверить, что card принадлежит текущему пользователю
        if card and card.user_id == session['user_id']:
            #Удалить card из базы данных
            db.session.delete(card)
            db.session.commit()
            #Перенаправить на главную страницу
            return redirect('/index')
        else:
            #Вернуть ошибку 404, если card не найдена или не принадлежит пользователю
            return redirect('/')
    else:
        #Перенаправить на страницу входа, если пользователь не вошел в систему
        return redirect('/')

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    #Проверить, что пользователь вошел в систему
    if 'user_id' in session:
        #Найти card по id
        card = Card.query.get(id)
        #Проверить, что card принадлежит текущему пользователю
        if card and card.user_id == session['user_id']:
            #Если метод POST, то получить данные из формы и обновить card
            if request.method == 'POST':
                title =  request.form['title']
                subtitle =  request.form['subtitle']
                text =  request.form['text']
                card.title = title
                card.subtitle = subtitle
                card.text = text
                db.session.commit()
                #Перенаправить на страницу card
                return redirect(f'/card/{id}')
            #Если метод GET, то отобразить форму с текущими данными card
            else:
                return render_template('update_card.html', card=card)
        else:
            #Вернуть ошибку 404, если card не найдена или не принадлежит пользователю
            return redirect('/')
    else:
        #Перенаправить на страницу входа, если пользователь не вошел в систему
        return redirect('/')


#Запуск страницы c созданием карты
@app.route('/create')
def create():
    #Задание №9. Проверить, что пользователь вошел в систему
    if 'user_id' in session:
        return render_template('create_card.html')
    else:
        return redirect('/')

#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        #Создание объкта для передачи в дб
        #Задание №10. Добавить поле user_id для связи с пользователем
        card = Card(title=title, subtitle=subtitle, text=text, user_id=session['user_id'])

        db.session.add(card)
        db.session.commit()
        cards = Card.query.get(title)
        
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
