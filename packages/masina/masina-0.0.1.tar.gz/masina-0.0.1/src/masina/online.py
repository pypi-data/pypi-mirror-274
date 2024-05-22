from datetime import datetime
import traceback
import sys
import re
import os
import csv
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask import send_file, send_from_directory, Response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from mysqlquerys import connect
from mysqlquerys import mysql_rm
from auto import Masina


UPLOAD_FOLDER = r"D:\Python\test"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://newuser_radu:Paroladetest_1234@localhost/cheltuieli_desktop"
app.config['SECRET_KEY'] = "my super secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'

# ini_file = "C:\_Development\Diverse\pypi\cfgm.ini"
ini_file = r"D:\Python\MySQL\masina.ini"
# masina_ini_file = 'static/masina.ini'
# kalendar_ini_file = 'static/kalendar.ini'
create_auto_table = 'sql/auto.sql'
# ini_file = 'static/heroku.ini'
conf = connect.Config(ini_file)


class Users(UserMixin):
    def __init__(self, user_name):
        self.user_name = user_name
        self.db = mysql_rm.DataBase(conf.credentials)
        self.users_table = mysql_rm.Table(conf.credentials, 'users')
        self.all_cars_table = mysql_rm.Table(conf.credentials, 'all_cars')
        # print(25*'#####')

    @property
    def id(self):
        matches = ('username', self.user_name)
        user_id = self.users_table.returnCellsWhere('id', matches)[0]
        return user_id

    @property
    def valid_user(self):
        all_users = self.users_table.returnColumn('username')
        if self.user_name in all_users:
            return True
        else:
            return False

    @property
    def admin(self):
        if self.valid_user:
            matches = ('id', self.id)
            user_type = self.users_table.returnCellsWhere('user_type', matches)[0]
            if user_type == 'admin':
                return True
            else:
                return False

    @property
    def masini(self):
        # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        masini = {}
        matches = ('user_id', self.id)
        cars_rows = self.all_cars_table.returnRowsWhere(matches)
        if cars_rows:
            for row in cars_rows:
                indx_brand = self.all_cars_table.columnsNames.index('brand')
                indx_model = self.all_cars_table.columnsNames.index('model')
                table_name = '{}_{}'.format(row[indx_brand], row[indx_model])
                app_masina = Masina(conf.credentials, table_name=table_name.lower())
                masini[table_name] = app_masina
        return masini

    @property
    def hashed_password(self):
        matches = ('username', self.user_name)
        hashed_password = self.users_table.returnCellsWhere('password', matches)[0]
        return hashed_password

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def add_car(self, brand, model, car_type):
        cols = ('user_id', 'brand', 'model', 'cartype')
        vals = (self.id, brand, model, car_type)
        self.all_cars_table.addNewRow(cols, vals)
        newTableName = '{}_{}'.format(brand, model)
        # pth = os.path.join(os.path.dirname(__file__), create_auto_table)
        self.db.createTableFromFile(create_auto_table, newTableName.lower())

    def get_id_all_cars(self, table_name):
        brand, model = table_name.split('_')
        matches = [('user_id', self.id),
                   ('brand', brand),
                   ('model', model),
                   ]
        print(matches)
        id_all_cars = self.all_cars_table.returnCellsWhere('id', matches)[0]
        return id_all_cars


@login_manager.user_loader
def load_user(user_id):
    print(25*'Ä')
    print(sys._getframe().f_code.co_name, request.method)
    # print('##**##user_id _{}_'.format(user_id), type(user_id))
    try:
        mat = int(user_id)
    except:
        mat = int(re.findall("\[(.+?)\]", user_id)[0])

    matches = ('id', mat)
    users_table = mysql_rm.Table(conf.credentials, 'users')
    name = users_table.returnCellsWhere('username', matches)[0]

    user = Users(name)
    # print('##user.user_access', user.admin)
    print(25 * 'Ä')
    return user


@app.route('/', methods=['GET', 'POST'])
def index():
    print(sys._getframe().f_code.co_name, request.method)
    print('++++', request.method)
    if request.method == 'POST':
        print('lllll')
    else:
        print('BOOOOO')
        if current_user.is_authenticated:
            for table_name, masina_instance in current_user.masini.items():
                try:
                    print(table_name)
                    print(masina_instance.table_alimentari)
                    print()
                    print(masina_instance.table_totals)
                except:
                    print(traceback.format_exc())

    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    print(sys._getframe().f_code.co_name, request.method)
    if request.method == "POST":
        username = request.form['username']
        user = Users(username)
        if not user.valid_user:
            print('User {} not in database'.format(username))
            return redirect(url_for("login"))
        if user.verify_password(request.form['password']):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    print(sys._getframe().f_code.co_name, request.method)
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    print(sys._getframe().f_code.co_name, request.method)
    conf = connect.Config(ini_file)
    data_base = mysql_rm.DataBase(conf.credentials)
    users_table = mysql_rm.Table(conf.credentials, 'users')
    if request.method == 'POST':
        username = request.form['username']
        # email = request.form['email']
        password = request.form['password']
        # car_brand = request.form['car_brand']
        # car_model = request.form['car_model']
        cols = ('username', 'password')
        hash = generate_password_hash(password)
        vals = (username, hash)
        users_table.addNewRow(cols, vals)
        # newTableName = '{}_{}_{}'.format(username, car_brand, car_model)
        # data_base.createTableFromFile(create_auto_table, newTableName)
        user = Users(username)
        login_user(user)
        return redirect(url_for("index"))
    elif request.method == 'GET':
        print('****', request.method)

    return render_template('register.html')


@app.route('/car/<table_name>', methods=['GET', 'POST'])
def car(table_name):
    print(sys._getframe().f_code.co_name, request.method)
    app_masina = Masina(conf.credentials, table_name=table_name.lower())
    if app_masina.no_of_records == 0:
        # return "<h1>Please insert some data</h1>"
        session['current_table'] = table_name.lower()
        session['types_of_costs'] = app_masina.types_of_costs
        return redirect(url_for("addalim"))
    dataFrom, dataBis = app_masina.default_interval
    alim_type = None
    alimentari = app_masina.get_alimentari_for_interval_type(dataFrom, dataBis, alim_type)
    return render_template('masina.html',
                           userDetails=alimentari,
                           dataFrom=dataFrom.date(),
                           dataBis=dataBis.date(),
                           tabel_alimentari=app_masina.table_alimentari,
                           tabel_totals=app_masina.table_totals,
                           types_of_costs=app_masina.types_of_costs
                           )


@app.route('/addalim', methods=['GET', 'POST'])
def addalim():
    print(sys._getframe().f_code.co_name, request.method)
    if request.method == 'POST':
        if "add_alim" in request.form:
            date = request.form['data']
            alim_type = request.form['type']
            brutto = request.form['brutto']
            amount = request.form['amount']
            km = request.form['km']
            comment = request.form['Comment']
            # file = request.files['rfile']
            # file.save(secure_filename(file.filename))
            # fl = file.filename
            # fl = app_masina.alimentari.convertToBinaryData(fl)

            ppu = round(float(brutto) / float(amount), 3)
            id_all_cars = current_user.get_id_all_cars(session['current_table'].lower())
            columns = ['id_users', 'id_all_cars', 'data', 'type', 'brutto', 'amount', 'ppu', 'km', 'comment']
            values = [current_user.id, id_all_cars, date, alim_type, brutto, amount, ppu, km, comment]
            app_masina = Masina(conf.credentials, table_name=session['current_table'].lower())
            app_masina.insert_new_alim(columns, values)
            page_extension = "car/{}".format(session['current_table'].lower())
            return redirect(url_for('car', table_name=session['current_table'].lower()))
    return render_template('addalim.html',
                           table_name=session['current_table'],
                           types_of_costs=session['types_of_costs']
                           )


@app.route('/masina', methods=['GET', 'POST'])
def masina():
    print(sys._getframe().f_code.co_name, request.method)
    credentials = conf.credentials
    # credentials['database'] = 'masina'
    # page = request.args.get('page')
    # print('####credentials', credentials)
    # print('*****conf.credentials', current_user.user_name)
    # print('*****request.form', request.form)
    # print('?????request.args', request.full_path)
    # print('?????request.args', request.values)
    # print('?????request.args', request.get_full_path)
    # print('?????request.args', request.path)
    # app_masina = Masina(ini_file)
    app_masina = Masina(credentials, table_name='hyundai_ioniq')
    dataFrom, dataBis = app_masina.default_interval
    alim_type = None
    if request.method == 'POST':
        print('LLLLLrequest.form', request.form)
        if "filter" in request.form:
            month = request.form['month']
            year = int(request.form['year'])
            alim_type = request.form['type']
            if alim_type == 'all':
                alim_type = None
            dataFrom = request.form['dataFrom']
            dataBis = request.form['dataBis']

            if month != 'interval':
                dataFrom, dataBis = app_masina.get_monthly_interval(month, year)
            elif month == 'interval' and (dataFrom == '' or dataBis == ''):
                dataFrom, dataBis = app_masina.default_interval
            else:
                try:
                    dataFrom = datetime.strptime(dataFrom, "%Y-%m-%d")
                    dataBis = datetime.strptime(dataBis, "%Y-%m-%d")
                except:
                    print(traceback.format_exc())
        elif "add_alim" in request.form:
            date = request.form['data']
            alim_type = request.form['type']
            brutto = request.form['brutto']
            amount = request.form['amount']
            km = request.form['km']
            comment = request.form['Comment']
            file = request.files['rfile']
            file.save(secure_filename(file.filename))
            fl = file.filename
            fl = app_masina.alimentari.convertToBinaryData(fl)

            ppu = round(float(brutto)/float(amount), 3)
            columns = ['data', 'type', 'brutto', 'amount', 'ppu', 'km', 'comment', 'file']
            values = [date, alim_type, brutto, amount, ppu, km, comment, fl]
            redirect(url_for('masina'))
            app_masina.insert_new_alim(columns, values)
        elif 'read_txt_file_content' in request.form:
            file = request.files['myfile']
            filename = secure_filename(file.filename)
            print('filename', filename)
            fl = os.path.join("D:\Python\MySQL", filename)
            file.save(fl)
            with open(fl) as f:
                file_content = f.read()
                print(file_content)
            return file_content
        elif 'save_file_locally' in request.form:
            file = request.files['myfile']
            # file = 'test.csv'

            print('file', file, type(file))
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print('filename', filename, type(filename))
        elif 'upload_file_to_db' in request.form:
            file = request.files['myfile']
            # print('file', file, type(file))
            file.save(secure_filename(file.filename))
            fl = file.filename
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #
            # print('filename', filename, type(filename))
            # fl = os.path.normpath(filename)
            fl = app_masina.alimentari.convertToBinaryData(fl)
            app_masina.alimentari.changeCellContent('file', fl, 'id', 2)
            # print('filename', filename)
            # fl = os.path.join("D:\Python\MySQL", filename)
            # file.save(fl)
            # with open(fl) as f:
            #     file_content = f.read()
            #     print(file_content)
            # return file_content
        # elif 'download_file' in request.form:
        #     print('AAAAAAAAAA')
        #     fl = app_masina.alimentari.returnCellsWhere('file', ('id', 651))
        #     exact_path = "report.csv"
        #
        #     with open(exact_path, 'wb') as file:
        #         file.write(fl[0])
        #     print('BBBBBBBBBBB')
        #     return send_file(exact_path, as_attachment=True)
        #     # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        elif 'export_detail_table_as_csv' in request.form:
            alimentari = app_masina.get_alimentari_for_interval_type(dataFrom, dataBis, alim_type)
            exact_path = "report.csv"
            with open(exact_path, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                for row in alimentari:
                    writer.writerow(row)
            return send_file(exact_path, as_attachment=True)
        else:
            print("AAAA")
    print('*****dataFrom', dataFrom)
    print('*****dataBis', dataBis)
    print('*****alim_type', alim_type)
    alimentari = app_masina.get_alimentari_for_interval_type(dataFrom, dataBis, alim_type)
    return render_template('masina.html',
                           userDetails=alimentari,
                           dataFrom=dataFrom.date(),
                           dataBis=dataBis.date(),
                           tabel_alimentari=app_masina.table_alimentari,
                           tabel_totals=app_masina.table_totals,
                           types_of_costs=app_masina.types_of_costs
                           )


@app.route('/addcar', methods=['GET', 'POST'])
def addcar():
    print(sys._getframe().f_code.co_name, request.method)
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        car_type = request.form['car_type']
        current_user.add_car(brand, model, car_type)
        return redirect(url_for('index'))
    # elif request.method == 'GET':
    #     print('****', request.method)

    return render_template('addcar.html')


if __name__ == "__main__":
    app.run(debug=True)
