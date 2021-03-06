import os
from flask_restful import abort, Api
from flask import Flask, request, session
from data import category

from os import getenv
from werkzeug.exceptions import abort
from flask_bootstrap import Bootstrap
#import news_resources
from data import db_session
from data.users import User
from data.goods import Goods
from data.category import Category
from forms.goods import GoodsForm
from forms.index import IndexForm
from forms.user import RegisterForm, LoginForm, EditEmailForm, EditPhoneForm, EditPasswordForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import redirect, render_template
from werkzeug.utils import secure_filename
app = Flask(__name__, static_folder="static")

api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = getenv('SECRET_KEY')

UPLOAD_PATH = 'static/images/'
REMOVE_PATH = 'static/'
Bootstrap(app)

# # для списка объектов
# api.add_resource(news_resources.NewsListResource, '/api/v2/goods')
# # для одного объекта
# api.add_resource(news_resources.NewsResource, '/api/v2/goods/<int:goods_id>')

def add_category():
    try:
        db_sess = db_session.create_session()
        user = Category(
            id=1,
            name="Машинка"
        )
        db_sess.add(user)
        user2 = Category(
            id=2,
            name="Верталёт"
        )
        db_sess.add(user2)
        user3 = Category(
            id=3,
            name="Трактор"
        )
        db_sess.add(user3)
        user4 = Category(
            id=4,
            name="Грузовик"
        )
        db_sess.add(user4)
        user5 = Category(
            id=5,
            name="Самолёт"
        )
        db_sess.add(user5)
        db_sess.commit()
    except:
        pass
@app.route("/", methods=['GET', 'POST'])
def index():
    form = IndexForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods).filter(Goods.title == form.title.data.lower(),
                                            Goods.category == form.category.data).all()

        return render_template("index.html", news=goods, title="Авито2.0", form=form)
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    return render_template("index.html", news=goods, title="Авито2.0", form=form)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        session['phone'] = form.phone.data
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
        db_sess = db_session.create_session()
        form.file.data.save(UPLOAD_PATH + f"{form.title.data.lower()}_{current_user.id}.png") #сохранение каринки
        goods = Goods()
        goods.title = form.title.data.lower()
        goods.description = form.description.data
        goods.price = form.price.data
        goods.picture = f"images/{form.title.data.lower()}_{current_user.id}.png"
        #goods.category = form.category.data
        current_user.goods.append(goods)
        name = db_sess.query(Category).filter(Category.name == form.category.data).first()
        goods.categories.append(name)
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
            filename = secure_filename(form.file.data.filename)  # сохранение каринки
            form.file.data.save(UPLOAD_PATH + filename)  # сохранение каринки
            os.remove(REMOVE_PATH + news.picture)
            news.picture = f"images/{filename}"
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
        os.remove(REMOVE_PATH+news.picture)
        db_sess.delete(news)
        # db_sess.delete(cat)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')
@app.route('/good_buy/<int:id>', methods=['GET', 'POST'])
@login_required
def good_buy(id):
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
    tel = db_sess.query(User).filter(User.id == news.user_id).first()
    return render_template('good.html',
                           news=news,
                           title='Товар',
                           tel=tel)

@app.route('/options', methods=['GET', 'POST'])
@login_required
def options():
    db_sess = db_session.create_session()
    info = db_sess.query(User).filter(User.id == current_user.id).first()
    return render_template('options.html', title='Настройки', info=info)

@app.route('/edit_email', methods=['GET', 'POST'])
@login_required
def edit_email():
    form = EditEmailForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id
                                          ).first()
        if user:
            user.email = form.email.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit_email.html', title='Изменение почты', form=form)

@app.route('/edit_phone', methods=['GET', 'POST'])
@login_required
def edit_phone():
    form = EditPhoneForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id
                                          ).first()
        if user:
            user.phone = form.phone.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit_phone.html', title='Изменение телефона', form=form)

@app.route('/edit_password', methods=['GET', 'POST'])
@login_required
def edit_password():
    form = EditPasswordForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id
                                          ).first()
        if user and user.check_password(form.password.data):
            user.set_password(form.new_password.data)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit_password.html', title='Изменение пароля', form=form)

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
    db_session.global_init("db/avito.db")
    add_category()
    app.run()


if __name__ == '__main__':
    main()

