from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import uuid, os
from datetime import datetime, timedelta

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Fisherman!@localhost/tenantdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    apartment_number = db.Column(db.String(255))


class MaintenanceRequest(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    apartment_number = db.Column(db.String(255))
    area = db.Column(db.String(255))
    description = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    date_time = db.Column(db.String(255))
    status = db.Column(db.String(255))
    comment = db.Column(db.String(255))

    def __init__(self, apartment_number, area, description, photo=None):
        self.id = str(uuid.uuid4())[:8]
        self.apartment_number = apartment_number
        self.area = area
        self.description = description
        self.photo = photo
        self.date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = 'pending'
        self.comment = None


class Tenant(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    check_in_date = db.Column(db.String(255))
    check_out_date = db.Column(db.String(255))
    apartment_number = db.Column(db.String(255))

    def __init__(self, name, phone_number, email, check_in_date, check_out_date, apartment_number):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.apartment_number = apartment_number


class StaffMember(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.id = str(uuid.uuid4())[:8]
        self.name = name


class Manager(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.id = str(uuid.uuid4())[:8]
        self.name = name


class MaintenanceSystem:
    def add_staff_member(self, name):
        staff_member = StaffMember(name=name)
        db.session.add(staff_member)
        db.session.commit()

    def browse_requests(self, filters=None):
        filtered_requests = MaintenanceRequest.query.all()

        if filters:
            if 'apartment_number' in filters:
                filtered_requests = MaintenanceRequest.query.filter_by(
                    apartment_number=filters['apartment_number']).all()

            if 'area' in filters:
                filtered_requests = MaintenanceRequest.query.filter_by(
                    area=filters['area'].lower()).all()

            if 'date_range' in filters:
                start_date, end_date = filters['date_range']
                filtered_requests = MaintenanceRequest.query.filter(
                    MaintenanceRequest.date_time.between(start_date, end_date)).all()

            if 'status' in filters:
                filtered_requests = MaintenanceRequest.query.filter_by(
                    status=filters['status'].lower()).all()

        return filtered_requests

    def update_request_status(self, request_id, new_status, comment):
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if maintenance_request:
            maintenance_request.status = new_status
            maintenance_request.comment = comment
            db.session.commit()
            return True
        return False

    def add_manager(self, name):
        manager = Manager(name=name)
        db.session.add(manager)
        db.session.commit()

    def add_tenant(self, name, phone_number, email, apartment_number):
        check_in_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        check_out_date = (datetime.now() + timedelta(days=365)).strftime(
            '%Y-%m-%d %H:%M:%S')

        tenant = Tenant(name=name, phone_number=phone_number, email=email,
                        check_in_date=check_in_date, check_out_date=check_out_date,
                        apartment_number=apartment_number)
        db.session.add(tenant)
        db.session.commit()

    def move_tenant(self, tenant_id, new_apartment_number):
        tenant = Tenant.query.get(tenant_id)
        if tenant:
            tenant.apartment_number = new_apartment_number
            db.session.commit()
            return True
        return False

    def delete_tenant(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        if tenant:
            db.session.delete(tenant)
            db.session.commit()
            return True
        return False


maintenance_system = MaintenanceSystem()


@app.route('/member_interface')
def member_interface():
    apartment_number = request.args.get('apartment_number')

    requests = MaintenanceRequest.query.filter_by(apartment_number=apartment_number).all()

    return render_template('member_interface.html', requests=requests, apartment_number=apartment_number)


@app.route('/maintenance_staff_interface', methods=['GET', 'POST'])
def maintenance_staff_interface():
    sort_by = request.args.get('sort_by', 'request_id')

    sort_order = request.args.get('sort_order', 'desc')
    new_sort_order = 'asc' if sort_order == 'desc' else 'desc'

    if request.method == 'POST':
        apartment_number = request.form.get('apartment_number')
        area = request.form.get('area')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        status = request.form.get('status')

        filters = {
            'apartment_number': apartment_number,
            'area': area,
            'date_range': (start_date, end_date),
            'status': status
        }

        requests = maintenance_system.browse_requests(filters)
    else:
        requests = maintenance_system.browse_requests()

    if sort_by == 'request_id':
        requests.sort(key=lambda x: x.id, reverse=(sort_order == 'desc'))
    elif sort_by == 'apartment_number':
        requests.sort(key=lambda x: x.apartment_number, reverse=(sort_order == 'desc'))
    elif sort_by == 'area':
        requests.sort(key=lambda x: x.area, reverse=(sort_order == 'desc'))
    elif sort_by == 'description':
        requests.sort(key=lambda x: x.description, reverse=(sort_order == 'desc'))
    elif sort_by == 'date_time':
        requests.sort(key=lambda x: x.date_time, reverse=(sort_order == 'desc'))
    elif sort_by == 'status':
        requests.sort(key=lambda x: x.status, reverse=(sort_order == 'desc'))

    return render_template('maintenance_staff_interface.html', requests=requests, sort_by=sort_by,
                           sort_order=sort_order, new_sort_order=new_sort_order)


@app.route('/update_status', methods=['POST'])
def update_status():
    if request.method == 'POST':
        request_id = request.form['request_id']
        comment = request.form.get('comment', '')

        new_status = 'completed'

        success = maintenance_system.update_request_status(request_id, new_status, comment)

        if success:
            return redirect(url_for('maintenance_staff_interface'))
        else:
            return jsonify({'success': False, 'message': 'Failed to update status'})

    return jsonify({'success': False, 'message': 'Invalid request'})


@app.route('/management_interface', methods=['GET', 'POST'])
def management_interface():
    if request.method == 'POST':
        if 'add_tenant' in request.form:
            name = request.form['name']
            phone_number = request.form['phone_number']
            email = request.form['email']
            apartment_number = request.form['apartment_number']

            maintenance_system.add_tenant(name, phone_number, email, apartment_number)

        elif 'move_tenant' in request.form:
            tenant_id = request.form['tenant_id']
            new_apartment_number = request.form['new_apartment_number']

            maintenance_system.move_tenant(tenant_id, new_apartment_number)

        elif 'delete_tenant' in request.form:
            tenant_id = request.form['tenant_id']
            maintenance_system.delete_tenant(tenant_id)

    tenants = Tenant.query.all()

    sort_by = request.args.get('sort_by', 'id')
    current_order = request.args.get('order', 'asc')

    new_order = 'desc' if current_order == 'asc' else 'asc'

    if sort_by == 'id':
        tenants = sorted(tenants, key=lambda x: x.id, reverse=(new_order == 'desc'))
    elif sort_by == 'name':
        tenants = sorted(tenants, key=lambda x: x.name, reverse=(new_order == 'desc'))
    elif sort_by == 'phone_number':
        tenants = sorted(tenants, key=lambda x: x.phone_number, reverse=(new_order == 'desc'))
    elif sort_by == 'email':
        tenants = sorted(tenants, key=lambda x: x.email, reverse=(new_order == 'desc'))
    elif sort_by == 'check_in_date':
        tenants = sorted(tenants, key=lambda x: x.check_in_date, reverse=(new_order == 'desc'))
    elif sort_by == 'check_out_date':
        tenants = sorted(tenants, key=lambda x: x.check_out_date, reverse=(new_order == 'desc'))
    elif sort_by == 'apartment_number':
        tenants = sorted(tenants, key=lambda x: x.apartment_number, reverse=(new_order == 'desc'))

    return render_template('management_interface.html', tenants=tenants, sort_by=sort_by, order=new_order)


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            role = user.role
            apartment_number = user.apartment_number

            if role == 'manager':
                return redirect(url_for('management_interface'))
            elif role == 'maintenance_staff':
                return redirect(url_for('maintenance_staff_interface'))
            elif role == 'member':
                return redirect(url_for('member_interface', apartment_number=apartment_number))
            else:
                error_message = 'Invalid role.'
        else:
            error_message = 'Invalid username or password. Please try again.'

    return render_template('login.html', error_message=error_message)


@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))


@app.route('/index')
def index():
    requests = maintenance_system.browse_requests()
    return render_template('index.html', requests=requests)


@app.route('/submit_request', methods=['POST'])
def submit_request():
    apartment_number = request.form['apartment_number']
    area = request.form['area']
    description = request.form['description']
    photo = request.form['photoFile'] if 'photoFile' in request.form else None

    request_obj = MaintenanceRequest(apartment_number, area, description, photo)
    db.session.add(request_obj)
    db.session.commit()

    requests = MaintenanceRequest.query.filter_by(apartment_number=apartment_number).all()

    if 'photoFile' in request.files:
        photo_file = request.files['photoFile']

        if photo_file.filename != '':
            filename = secure_filename(photo_file.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo_file.save(photo_path)
        else:
            photo_path = None
    else:
        photo_path = None

    return redirect(url_for('member_interface', apartment_number=apartment_number))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
