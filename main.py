import datetime
import os
from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, render_template, request, flash, url_for
from os import getenv
from werkzeug.utils import redirect, secure_filename
from werkzeug.exceptions import abort

#import news_resources
from data import db_session
from data.goods import Goods
from data.users import User
from data.category import Category
from forms.goods import GoodsForm
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import url_for, redirect, render_template, send_file
from werkzeug.utils import secure_filename
app = Flask(__name__, static_folder="static")

api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = getenv('SECRET_KEY')

UPLOAD_PATH = 'static/images/'


# # для списка объектов
# api.add_resource(news_resources.NewsListResource, '/api/v2/goods')
# # для одного объекта
# api.add_resource(news_resources.NewsResource, '/api/v2/goods/<int:goods_id>')

def add_category():
    db_sess = db_session.create_session()
    categories = db_sess.query(Category)
    try:
        user = Category(
            name="Машинка"
        )
        db_sess.add(user)
        user2 = Category(
            name="Верталёт"
        )
        db_sess.add(user2)
        user3 = Category(
            name="Трактор"
        )
        db_sess.add(user3)
        user4 = Category(
            name="Грузовик"
        )
        db_sess.add(user4)
        user5 = Category(
            name="Самолёт"
        )
        db_sess.add(user5)
        db_sess.commit()
    except:
        pass

@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(Goods)
    return render_template("index.html", news=news, title="Авито2.0")

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                form=form,
                                message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if db_sess.query(User).filter(User.phone == form.phone.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            rating=5
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/my_goods', methods=['GET', 'POST'])
@login_required
def my_goods():
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).filter(Goods.user_id == current_user.id)
    if news:
        return render_template("my_goods.html", news=news, title="Авито2.0")
    return redirect("/")


@app.route('/office')
@login_required
def office():
    return render_template("office.html", title="Авито2.0")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                           message="Неправильный логин или пароль",
                           form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = GoodsForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename) #сохранение каринки
        form.file.data.save(UPLOAD_PATH + filename) #сохранение каринки
        db_sess = db_session.create_session()
        goods = Goods()
        goods.title = form.title.data
        goods.description = form.description.data
        goods.price = form.price.data
        goods.picture = f"images/{filename}"
        goods.category = form.category.data
        name = db_sess.query(Category).filter(Category.name == form.category.data).first()
        goods.categories.append(name)
        print(goods)
        current_user.goods.append(goods)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('goods.html', title='Добавление товара',
                           form=form)

@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = GoodsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Goods).filter(Goods.id == id,
                                           Goods.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.description.data = news.description
            form.price.data = news.price
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Goods).filter(Goods.id == id,
                                          Goods.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.description = form.description.data
            news.price = form.price.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('goods.html',
                           title='Редактирование товара',
                           form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).filter(Goods.id == id,
                                      Goods.user == current_user
                                      ).first()
    # cat = db_sess.query(Category).filter(Category.id == id).first()
    if news:
        db_sess.delete(news)
        # db_sess.delete(cat)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/news_info/<int:id>', methods=['GET', 'POST'])
def news_info(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Goods).filter(Goods.id == id).first()
    return render_template('good.html',
                           news=news,
                           title='Товар')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

def main():
    import socket
    db_session.global_init("db/avito.db")
    add_category()
    app.run(host="127.0.0.1", port=5595, debug=True)


if __name__ == '__main__':
    main()

