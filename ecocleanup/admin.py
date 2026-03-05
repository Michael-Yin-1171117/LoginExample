from ecocleanup import app
from ecocleanup import db
from flask import redirect, render_template, session, url_for, request
from datetime import date

@app.route('/admin')
@app.route('/admin/home')
def admin_home():
    """Admin Homepage endpoint."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    # Platform-wide statistics
    with db.get_cursor() as cursor:
        # User statistics
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE role = %s;', ('volunteer',))
        total_volunteers = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE role = %s;', ('event_leader',))
        total_leaders = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE role = %s;', ('admin',))
        total_admins = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE status = %s;', ('active',))
        active_users = cursor.fetchone()['total']
        
        # Event statistics
        cursor.execute('SELECT COUNT(*) as total FROM events;')
        total_events = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM events WHERE event_date >= CURRENT_DATE;')
        upcoming_events_count = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM events WHERE event_date < CURRENT_DATE;')
        completed_events_count = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM eventregistrations;')
        total_registrations = cursor.fetchone()['total']
        
        # Feedback statistics
        cursor.execute('SELECT COUNT(*) as total FROM feedback;')
        total_feedback = cursor.fetchone()['total']
        
        cursor.execute('SELECT AVG(rating)::numeric(10,2) as avg FROM feedback;')
        avg_rating = cursor.fetchone()['avg']
        if avg_rating is None:
            avg_rating = 0
        
        # Participation rate (attended registrations / total registrations * 100)
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN attendance = 'attended' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) as rate
            FROM eventregistrations;
        ''')
        participation_rate = cursor.fetchone()['rate']
        if participation_rate is None:
            participation_rate = 0
        else:
            participation_rate = round(participation_rate, 1)

    return render_template('admin_home.html',
                          total_volunteers=total_volunteers,
                          total_leaders=total_leaders,
                          total_admins=total_admins,
                          active_users=active_users,
                          total_events=total_events,
                          upcoming_events_count=upcoming_events_count,
                          completed_events_count=completed_events_count,
                          total_registrations=total_registrations,
                          total_feedback=total_feedback,
                          avg_rating=avg_rating,
                          participation_rate=participation_rate)

@app.route('/admin/users')
def admin_users():
    """View all users with search and filter."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    status_filter = request.args.get('status', '')

    query = '''
        SELECT user_id, username, full_name, email, role, status
        FROM users
        WHERE 1=1
    '''
    params = []

    if search:
        query += ' AND (full_name ILIKE %s OR username ILIKE %s OR email ILIKE %s)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param])
    
    if role_filter:
        query += ' AND role = %s'
        params.append(role_filter)
    
    if status_filter:
        query += ' AND status = %s'
        params.append(status_filter)
    
    query += ' ORDER BY user_id DESC;'

    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        users = cursor.fetchall()

    return render_template('admin_users.html', 
                          users=users,
                          search=search,
                          role_filter=role_filter,
                          status_filter=status_filter)

@app.route('/admin/user/<int:user_id>')
def admin_user_detail(user_id):
    """View user details."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT user_id, username, full_name, email, role, status,
                   home_address, contact_number, environmental_interests,
                   profile_image
            FROM users WHERE user_id = %s;
        ''', (user_id,))
        user = cursor.fetchone()

    return render_template('admin_user_detail.html', user=user)

@app.route('/admin/user/<int:user_id>/status', methods=['POST'])
def admin_change_user_status(user_id):
    """Change user status."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    new_status = request.form['status']
    
    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE users SET status = %s
            WHERE user_id = %s;
        ''', (new_status, user_id))

    return redirect(url_for('admin_user_detail', user_id=user_id, updated=True))

@app.route('/admin/reports/platform')
def admin_platform_report():
    """Platform-wide reports."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        # Basic statistics
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE role = %s;', ('volunteer',))
        total_volunteers = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE role = %s;', ('event_leader',))
        total_leaders = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE role = %s;', ('admin',))
        total_admins = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM events;')
        total_events = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM eventregistrations;')
        total_registrations = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM feedback;')
        total_feedback = cursor.fetchone()['total']
        
        # Monthly trends
        cursor.execute('''
            SELECT 
                TO_CHAR(event_date, 'YYYY-MM') as month,
                COUNT(*) as events,
                COUNT(er.registration_id) as registrations,
                ROUND(COUNT(CASE WHEN er.attendance = 'attended' THEN 1 END) * 100.0 / NULLIF(COUNT(er.registration_id), 0), 1) as attendance_rate
            FROM events e
            LEFT JOIN eventregistrations er ON e.event_id = er.event_id
            GROUP BY month
            ORDER BY month DESC
            LIMIT 6;
        ''')
        monthly_stats = cursor.fetchall()

        # Events by type
        cursor.execute('''
            SELECT event_type, COUNT(*) as count
            FROM events
            GROUP BY event_type
            ORDER BY count DESC;
        ''')
        events_by_type = cursor.fetchall()

        # Top rated events
        cursor.execute('''
            SELECT e.event_name, AVG(f.rating)::numeric(10,1) as avg_rating, COUNT(f.feedback_id) as review_count
            FROM events e
            JOIN feedback f ON e.event_id = f.event_id
            GROUP BY e.event_id, e.event_name
            ORDER BY avg_rating DESC
            LIMIT 5;
        ''')
        top_rated_events = cursor.fetchall()

        # Top event leaders (by number of events created)
        cursor.execute('''
            SELECT u.full_name, COUNT(e.event_id) as event_count
            FROM users u
            JOIN events e ON u.user_id = e.event_leader_id
            GROUP BY u.user_id, u.full_name
            ORDER BY event_count DESC
            LIMIT 5;
        ''')
        top_leaders = cursor.fetchall()

        # Most active volunteers (by events attended)
        cursor.execute('''
            SELECT u.full_name, COUNT(er.event_id) as event_count
            FROM users u
            JOIN eventregistrations er ON u.user_id = er.volunteer_id
            WHERE er.attendance = 'attended'
            GROUP BY u.user_id, u.full_name
            ORDER BY event_count DESC
            LIMIT 5;
        ''')
        top_volunteers = cursor.fetchall()

    return render_template('admin_platform_report.html',
                          total_volunteers=total_volunteers,
                          total_leaders=total_leaders,
                          total_admins=total_admins,
                          total_events=total_events,
                          total_registrations=total_registrations,
                          total_feedback=total_feedback,
                          monthly_stats=monthly_stats,
                          events_by_type=events_by_type,
                          top_rated_events=top_rated_events,
                          top_leaders=top_leaders,
                          top_volunteers=top_volunteers)

@app.route('/admin/reports/events')
def admin_events_report():
    """Events report."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    query = '''
        SELECT e.event_id, e.event_name, e.event_date, 
               e.location, u.username as leader_name,
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count,
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id AND attendance = 'attended') as attended_count,
               (SELECT COUNT(*) FROM feedback WHERE event_id = e.event_id) as feedback_count,
               (SELECT AVG(rating)::numeric(10,2) FROM feedback WHERE event_id = e.event_id) as avg_rating
        FROM events e
        JOIN users u ON e.event_leader_id = u.user_id
        ORDER BY e.event_date DESC;
    '''

    with db.get_cursor() as cursor:
        cursor.execute(query)
        events = cursor.fetchall()

    return render_template('admin_events_report.html', events=events)

@app.route('/admin/events')
def admin_events():
    """Admin view all events with filters."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    # Get filter parameters
    date_filter = request.args.get('date', '')
    location_filter = request.args.get('location', '')
    type_filter = request.args.get('type', '')
    leader_filter = request.args.get('leader', '')

    # Build query
    query = '''
        SELECT e.*, u.username as leader_name,
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count
        FROM events e
        JOIN users u ON e.event_leader_id = u.user_id
        WHERE 1=1
    '''
    params = []

    if date_filter:
        query += ' AND e.event_date = %s'
        params.append(date_filter)
    
    if location_filter:
        query += ' AND e.location ILIKE %s'
        params.append(f'%{location_filter}%')
    
    if type_filter:
        query += ' AND e.event_type = %s'
        params.append(type_filter)
    
    if leader_filter:
        query += ' AND u.username ILIKE %s'
        params.append(f'%{leader_filter}%')
    
    query += ' ORDER BY e.event_date DESC;'

    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        events = cursor.fetchall()
        
        # Get unique event types for filter dropdown
        cursor.execute('SELECT DISTINCT event_type FROM events ORDER BY event_type;')
        event_types = cursor.fetchall()
        
        # Get unique leaders for filter dropdown
        cursor.execute('''
            SELECT DISTINCT u.user_id, u.username 
            FROM users u 
            JOIN events e ON u.user_id = e.event_leader_id 
            ORDER BY u.username;
        ''')
        leaders = cursor.fetchall()

    return render_template('admin_events.html', 
                          events=events,
                          event_types=event_types,
                          leaders=leaders,
                          date_filter=date_filter,
                          location_filter=location_filter,
                          type_filter=type_filter,
                          leader_filter=leader_filter)

@app.route('/admin/events/edit/<int:event_id>', methods=['GET', 'POST'])
def admin_edit_event(event_id):
    """Admin edit any event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    if request.method == 'POST':
        event_name = request.form['event_name']
        location = request.form['location']
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        duration = request.form['duration']
        event_type = request.form['event_type']
        description = request.form.get('description', '')
        supplies = request.form.get('supplies', '')
        safety_instructions = request.form.get('safety_instructions', '')

        with db.get_cursor() as cursor:
            cursor.execute('''
                UPDATE events SET
                    event_name = %s, location = %s, event_date = %s,
                    start_time = %s, duration = %s, event_type = %s,
                    description = %s, supplies = %s, safety_instructions = %s
                WHERE event_id = %s;
            ''', (event_name, location, event_date, start_time, duration,
                  event_type, description, supplies, safety_instructions, event_id))

        return redirect(url_for('admin_events', updated=True))

    # GET request
    with db.get_cursor() as cursor:
        cursor.execute('SELECT * FROM events WHERE event_id = %s;', (event_id,))
        event = cursor.fetchone()

    return render_template('admin_edit_event.html', event=event)

@app.route('/admin/events/delete/<int:event_id>', methods=['POST'])
def admin_delete_event(event_id):
    """Admin delete any event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        # Delete related records first
        cursor.execute('DELETE FROM eventoutcomes WHERE event_id = %s;', (event_id,))
        cursor.execute('DELETE FROM feedback WHERE event_id = %s;', (event_id,))
        cursor.execute('DELETE FROM eventregistrations WHERE event_id = %s;', (event_id,))
        cursor.execute('DELETE FROM events WHERE event_id = %s;', (event_id,))

    return redirect(url_for('admin_events', deleted=True))

@app.route('/admin/events/<int:event_id>/volunteers')
def admin_event_volunteers(event_id):
    """Admin view volunteers registered for an event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        # Get event details
        cursor.execute('''
            SELECT e.*, u.username as leader_name
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            WHERE e.event_id = %s;
        ''', (event_id,))
        event = cursor.fetchone()
        
        # Get registered volunteers
        cursor.execute('''
            SELECT u.user_id, u.username, u.full_name, u.email,
                   u.contact_number, er.attendance, er.registered_at
            FROM users u
            JOIN eventregistrations er ON u.user_id = er.volunteer_id
            WHERE er.event_id = %s
            ORDER BY u.full_name;
        ''', (event_id,))
        volunteers = cursor.fetchall()

    return render_template('admin_event_volunteers.html', 
                         event=event, volunteers=volunteers)