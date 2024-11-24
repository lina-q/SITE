from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Необходимо для работы сессий
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myProjectSITE.db"
db = SQLAlchemy(app)

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Order(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        customer_name = db.Column(db.String(300), nullable=False)
        customer_email = db.Column(db.String(120), nullable=False)
        customer_address = db.Column(db.String(500), nullable=False)
        customer_phone = db.Column(db.String(20), nullable=False)
        order_details = db.Column(db.Text, nullable=False)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route("/index")
@app.route("/")  # переход на главную страницу
def index():
    return render_template('index.html')  # отображаем сайт

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        order_details = request.form['order_details']

        # Создание нового заказа
        new_order = Order(
            customer_name=name,
            customer_email=email,
            customer_address=address,
            customer_phone=phone,
            order_details=order_details
        )

        db.session.add(new_order)
        db.session.commit()

        # Сохраняем данные в сессию
        session['order_data'] = {
            'name': name,
            'email': email,
            'address': address,
            'phone': phone,
            'order_details': order_details
        }

        return render_template('confirmation.html', **session['order_data'])

    # Если метод GET, проверить наличие данных в сессии
    order_data = session.get('order_data', {})
    return render_template('about.html', order_data=order_data)

@app.route("/create")
def create():
    return render_template('create.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Создание нового пользователя
        new_user = Register(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # После регистрации перенаправляем на страницу входа

    return render_template('register.html')  # Отображаем форму регистрации

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Проверка пользователя
        user = Register.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id  # Сохраняем ID пользователя в сессии
            session['user_name'] = user.name  # Сохраняем имя пользователя в сессии
            return redirect(url_for('index'))  # Перенаправляем на главную страницу после входа
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')  # Отображаем форму входа

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Удаляем ID пользователя из сессии
    session.pop('user_name', None)  # Удаляем имя пользователя из сессии
    return redirect(url_for('index'))  # Перенаправляем на главную страницу

if __name__ == '__main__':
    app.run(debug=True)  # чтобы мы могли в реальном времени смотреть изменения сайта