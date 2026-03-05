from ecocleanup import app
from ecocleanup import db
from flask import redirect, render_template, session, url_for, request

@app.route('/volunteer')
@app.route('/volunteer/home')
def volunteer_home():
    """Volunteer Homepage endpoint."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403

    # Get upcoming events the volunteer is registered for
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.location
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            WHERE er.volunteer_id = %s
              AND e.event_date >= CURRENT_DATE
            ORDER BY e.event_date, e.start_time;
        ''', (session['user_id'],))
        upcoming_events = cursor.fetchall()

    return render_template('volunteer_home.html', 
                         upcoming_events=upcoming_events)

@app.route('/volunteer/events')
def volunteer_events():
    """Browse cleanup events with filters."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403

    # Get filter parameters
    date_filter = request.args.get('date', '')
    location_filter = request.args.get('location', '')
    type_filter = request.args.get('type', '')
    # Build query
    query = '''
        SELECT e.*,
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count,
               CASE WHEN er.registration_id IS NOT NULL THEN TRUE ELSE FALSE END as is_registered
        FROM events e
        LEFT JOIN eventregistrations er ON e.event_id = er.event_id 
            AND er.volunteer_id = %s
        WHERE e.event_date >= CURRENT_DATE
    '''
    params = [session['user_id']]

    if date_filter:
        query += ' AND e.event_date = %s'
        params.append(date_filter)
    if location_filter:
        query += ' AND e.location ILIKE %s'
        params.append(f'%{location_filter}%')
    if type_filter:
        query += ' AND e.event_type = %s'  
        params.append(type_filter)

    query += ' ORDER BY e.event_date, e.start_time;'

    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        events = cursor.fetchall()

    return render_template('volunteer_events.html', events=events, type_filter=type_filter)

@app.route('/volunteer/event/<int:event_id>')
def volunteer_event_detail(event_id):
    """View detailed information about a specific event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.*, u.full_name as leader_name,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count
            FROM events e
            JOIN users u ON e.event_leader_id = u.user_id
            WHERE e.event_id = %s;
        ''', (event_id,))
        event = cursor.fetchone()
        
        # Check if already registered
        cursor.execute('''
            SELECT * FROM eventregistrations
            WHERE event_id = %s AND volunteer_id = %s;
        ''', (event_id, session['user_id']))
        is_registered = cursor.fetchone() is not None

    return render_template('volunteer_event_detail.html', 
                         event=event, is_registered=is_registered)


@app.route('/volunteer/register/<int:event_id>', methods=['POST'])
def volunteer_register(event_id):
    """Register for an event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        # Get the event date
        cursor.execute('''
            SELECT event_date FROM events WHERE event_id = %s;
        ''', (event_id,))
        new_event = cursor.fetchone()

        # Check for scheduling conflicts
        cursor.execute('''
            SELECT e.event_date FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            WHERE er.volunteer_id = %s AND e.event_date = %s;
        ''', (session['user_id'], new_event['event_date']))
        
        conflict = cursor.fetchone()
        
        if conflict:
            return render_template('volunteer_events.html', 
                                 error='You are already registered for another event on this day.')

        # Register for event
        cursor.execute('''
            INSERT INTO eventregistrations (event_id, volunteer_id)
            VALUES (%s, %s);
        ''', (event_id, session['user_id']))

    return redirect(url_for('volunteer_events', registered=True))

@app.route('/volunteer/history')
def volunteer_history():
    """View participation history."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.event_date, e.location,
                   er.attendance,
                   f.rating, f.comments, f.submitted_at
            FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            LEFT JOIN feedback f ON e.event_id = f.event_id 
                AND f.volunteer_id = er.volunteer_id
            WHERE er.volunteer_id = %s
              AND e.event_date < CURRENT_DATE
            ORDER BY e.event_date DESC;
        ''', (session['user_id'],))
        history = cursor.fetchall()

    return render_template('volunteer_history.html', history=history)

@app.route('/volunteer/feedback/<int:event_id>', methods=['GET', 'POST'])
def volunteer_feedback(event_id):
    """Submit feedback for a completed event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403

    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']

        with db.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO feedback (event_id, volunteer_id, rating, comments)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (event_id, volunteer_id) 
                DO UPDATE SET rating = %s, comments = %s, submitted_at = CURRENT_TIMESTAMP;
            ''', (event_id, session['user_id'], rating, comments, rating, comments))

        return redirect(url_for('volunteer_history', feedback_submitted=True))

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.* FROM events e
            JOIN eventregistrations er ON e.event_id = er.event_id
            WHERE e.event_id = %s AND er.volunteer_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

    return render_template('volunteer_feedback.html', event=event)