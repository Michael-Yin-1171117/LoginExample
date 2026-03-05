from ecocleanup import app
from ecocleanup import db
from flask import redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
import re
import os
from werkzeug.utils import secure_filename

flask_bcrypt = Bcrypt(app)
DEFAULT_USER_ROLE = 'volunteer'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def user_home_url():
    if 'loggedin' in session:
        role = session.get('role', None)
        if role == 'volunteer':
            home_endpoint = 'volunteer_home'
        elif role == 'event_leader':
            home_endpoint = 'event_leader_home'
        elif role == 'admin':
            home_endpoint = 'admin_home'
        else:
            home_endpoint = 'logout'
    else:
        home_endpoint = 'login'
    return url_for(home_endpoint)

@app.route('/')
def root():
    """Root endpoint - shows homepage for non-logged-in users, 
       redirects logged-in users to their dashboard."""
    if 'loggedin' in session:
        return redirect(user_home_url())
    return render_template('index.html') 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect(user_home_url())

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        with db.get_cursor() as cursor:
            cursor.execute('''
                SELECT user_id, username, password_hash, role, status
                FROM users WHERE username = %s;
            ''', (username,))
            account = cursor.fetchone()

            if account is not None:
                if account['status'] == 'inactive':
                    return render_template('login.html',
                                         username=username,
                                         account_inactive=True)

                password_hash = account['password_hash']
                if flask_bcrypt.check_password_hash(password_hash, password):
                    session['loggedin'] = True
                    session['user_id'] = account['user_id']
                    session['username'] = account['username']
                    session['role'] = account['role']
                    
                    # Check for event reminders on login
                  #  check_event_reminders(account['user_id'])
                    
                    return redirect(user_home_url())
                else:
                    return render_template('login.html',
                                         username=username,
                                         password_invalid=True)
            else:
                return render_template('login.html',
                                     username=username,
                                     username_invalid=True)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'loggedin' in session:
        return redirect(user_home_url())

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        full_name = request.form['full_name']
        home_address = request.form['home_address']
        contact_number = request.form['contact_number']
        environmental_interests = request.form.get('environmental_interests', '')

        username_error = None
        email_error = None
        password_error = None
        confirm_error = None

        # Check username
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE username = %s;', (username,))
            if cursor.fetchone():
                username_error = 'An account already exists with this username.'
        
        if not username_error and len(username) > 20:
            username_error = 'Your username cannot exceed 20 characters.'
        elif not username_error and not re.match(r'[A-Za-z0-9]+', username):
            username_error = 'Your username can only contain letters and numbers.'

        # Check email
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE email = %s;', (email,))
            if cursor.fetchone():
                email_error = 'An account already exists with this email address.'
        
        if not email_error and len(email) > 320:
            email_error = 'Your email address cannot exceed 320 characters.'
        elif not email_error and not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            email_error = 'Invalid email address.'

        # Password validation (at least 8 chars, mix of character types)
        if len(password) < 8:
            password_error = 'Password must be at least 8 characters long.'
        elif not re.search(r'[A-Z]', password):
            password_error = 'Password must contain at least one uppercase letter.'
        elif not re.search(r'[a-z]', password):
            password_error = 'Password must contain at least one lowercase letter.'
        elif not re.search(r'[0-9]', password):
            password_error = 'Password must contain at least one number.'

        if password != confirm_password:
            confirm_error = 'Passwords do not match.'

        if username_error or email_error or password_error or confirm_error:
            return render_template('signup.html',
                                 username=username,
                                 email=email,
                                 full_name=full_name,
                                 home_address=home_address,
                                 contact_number=contact_number,
                                 environmental_interests=environmental_interests,
                                 username_error=username_error,
                                 email_error=email_error,
                                 password_error=password_error,
                                 confirm_error=confirm_error)
        else:
            # Handle profile image
            profile_image = 'default_profile.png'
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"{username}_{file.filename}")
                    upload_dir = os.path.join(app.root_path, 'static/uploads')
                    if not os.path.exists(upload_dir):
                        os.makedirs(upload_dir)
                    file.save(os.path.join(upload_dir, filename))
                    profile_image = filename

            password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
            with db.get_cursor() as cursor:
                cursor.execute('''
                    INSERT INTO users (
                        username, password_hash, email, role,
                        full_name, home_address, contact_number,
                        environmental_interests, profile_image, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                ''', (username, password_hash, email, DEFAULT_USER_ROLE,
                     full_name, home_address, contact_number,
                     environmental_interests, profile_image, 'active'))

            return render_template('signup.html', signup_successful=True)

    return render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        home_address = request.form['home_address']
        contact_number = request.form['contact_number']
        environmental_interests = request.form.get('environmental_interests', '')

        # Handle profile image update
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{session['username']}_{file.filename}")
                upload_dir = os.path.join(app.root_path, 'static/uploads')
                file.save(os.path.join(upload_dir, filename))
                with db.get_cursor() as cursor:
                    cursor.execute('''
                        UPDATE users SET profile_image = %s WHERE user_id = %s;
                    ''', (filename, session['user_id']))

        with db.get_cursor() as cursor:
            cursor.execute('''
                UPDATE users SET
                    full_name = %s, home_address = %s,
                    contact_number = %s, environmental_interests = %s
                WHERE user_id = %s;
            ''', (full_name, home_address, contact_number,
                  environmental_interests, session['user_id']))

        return redirect(url_for('profile', updated=True))

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT username, email, role, full_name,
                   home_address, contact_number, environmental_interests,
                   profile_image, status
            FROM users WHERE user_id = %s;
        ''', (session['user_id'],))
        profile = cursor.fetchone()

    return render_template('profile.html', profile=profile, updated=request.args.get('updated'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']

        error = None

        with db.get_cursor() as cursor:
            cursor.execute('SELECT password_hash FROM users WHERE user_id = %s;', (session['user_id'],))
            user = cursor.fetchone()
            
            if not flask_bcrypt.check_password_hash(user['password_hash'], current):
                error = 'Current password is incorrect.'

        if not error:
            if len(new) < 8:
                error = 'Password must be at least 8 characters long.'
            elif not re.search(r'[A-Z]', new):
                error = 'Password must contain at least one uppercase letter.'
            elif not re.search(r'[a-z]', new):
                error = 'Password must contain at least one lowercase letter.'
            elif not re.search(r'[0-9]', new):
                error = 'Password must contain at least one number.'
            elif new == current:
                error = 'New password cannot be the same as current password.'
            elif new != confirm:
                error = 'New passwords do not match.'

        if error:
            return render_template('change_password.html', error=error)

        new_hash = flask_bcrypt.generate_password_hash(new).decode('utf-8')
        with db.get_cursor() as cursor:
            cursor.execute('UPDATE users SET password_hash = %s WHERE user_id = %s;',
                         (new_hash, session['user_id']))

        return render_template('change_password.html', success=True)

    return render_template('change_password.html')

@app.route('/logout')
def logout():
    """Logout endpoint.

    Methods:
    - get: Logs the current user out and redirects to the home page.
    """
    session.clear()
    return redirect(url_for('root'))