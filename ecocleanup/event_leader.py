from ecocleanup import app
from ecocleanup import db
from flask import redirect, render_template, session, url_for, request

@app.route('/event_leader')
@app.route('/event_leader/home')
def event_leader_home():
    """Event Leader Homepage endpoint."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    from datetime import date
    today = date.today()  

    # Get events created by this leader
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.*,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count
            FROM events e
            WHERE e.event_leader_id = %s
            ORDER BY e.event_date;
        ''', (session['user_id'],))
        my_events = cursor.fetchall()

    return render_template('event_leader_home.html', 
                         my_events=my_events,
                         today=today)


@app.route('/event_leader/create_event', methods=['GET', 'POST'])
def event_leader_create_event():
    """Create a new cleanup event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    if request.method == 'POST':
        event_name = request.form['event_name']
        location = request.form['location']
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        duration = request.form['duration']
        event_type = request.form['event_type']

        # Calculate end_time based on start_time and duration
        from datetime import datetime, timedelta
        start = datetime.strptime(start_time, '%H:%M')
        duration_int = int(duration)
        end = start + timedelta(hours=duration_int)
        # end = start + timedelta(hours=float(duration))
        end_time = end.strftime('%H:%M')
        
        supplies = request.form['supplies']
        safety = request.form['safety_instructions']
        description = request.form.get('description', '')
        # event_type = request.form.get('event_type', 'cleanup')

        try:
            duration_int = int(duration)
            if duration_int < 1 or duration_int > 8:
                return render_template('event_leader_create_event.html', 
                                    error='Duration must be between 1 and 8 hours')
        except ValueError:
            return render_template('event_leader_create_event.html', 
                                error='Duration must be a whole number')

        with db.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO events (
                    event_name, location, event_date, start_time, end_time,
                    duration, supplies, safety_instructions, description,
                    event_type, event_leader_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (event_name, location, event_date, start_time, end_time,
                  duration, supplies, safety, description, event_type, session['user_id']))

        return redirect(url_for('event_leader_home', created=True))

    return render_template('event_leader_create_event.html')

@app.route('/event_leader/manage_events')
def event_leader_manage_events():
    """Manage existing events with filters."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    from datetime import date
    today = date.today().isoformat()
    
    # Get filter parameters
    date_filter = request.args.get('date', '')
    location_filter = request.args.get('location', '')
    type_filter = request.args.get('type', '')
    status_filter = request.args.get('status', '')  # upcoming/past

    # Build query
    query = '''
        SELECT e.*,
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as registered_count,
               (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id AND attendance = 'attended') as attended_count,
               (SELECT num_attendees FROM eventoutcomes WHERE event_id = e.event_id) as attendees_count,
               (SELECT bags_collected FROM eventoutcomes WHERE event_id = e.event_id) as bags_count,
               (SELECT recyclables_sorted FROM eventoutcomes WHERE event_id = e.event_id) as recyclables_count
        FROM events e
        WHERE e.event_leader_id = %s
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
    
    if status_filter == 'upcoming':
        query += ' AND e.event_date >= CURRENT_DATE'
    elif status_filter == 'past':
        query += ' AND e.event_date < CURRENT_DATE'
    
    query += ' ORDER BY e.event_date DESC;'

    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        events = cursor.fetchall()
        
        # Get unique event types for filter dropdown
        cursor.execute('''
            SELECT DISTINCT event_type FROM events 
            WHERE event_leader_id = %s 
            ORDER BY event_type;
        ''', (session['user_id'],))
        event_types = cursor.fetchall()

    return render_template('event_leader_manage_events.html', 
                          events=events, 
                          today=today,
                          event_types=event_types,
                          date_filter=date_filter,
                          location_filter=location_filter,
                          type_filter=type_filter,
                          status_filter=status_filter)

@app.route('/event_leader/edit_event/<int:event_id>', methods=['GET', 'POST'])
def event_leader_edit_event(event_id):
    """Edit an event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    if request.method == 'POST':
        event_name = request.form['event_name']
        location = request.form['location']
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        duration = request.form['duration']
        event_type = request.form['event_type']

        # Calculate end_time
        from datetime import datetime, timedelta
        try:
            if len(start_time) > 5:  # HH:MM:SS 
                start = datetime.strptime(start_time, '%H:%M:%S')
            else:  # HH:MM 
                start = datetime.strptime(start_time, '%H:%M')
        except ValueError:
            start = datetime.strptime('09:00', '%H:%M')
            
        end = start + timedelta(hours=int(duration))
        end_time = end.strftime('%H:%M')
        
        supplies = request.form['supplies']
        safety = request.form['safety_instructions']
        description = request.form.get('description', '')
        # event_type = request.form.get('event_type', 'cleanup')

        with db.get_cursor() as cursor:
            cursor.execute('''
                UPDATE events SET
                    event_name = %s, location = %s, event_date = %s,
                    start_time = %s, end_time = %s, duration = %s,
                    supplies = %s, safety_instructions = %s,
                    description = %s, event_type = %s
                WHERE event_id = %s AND event_leader_id = %s;
            ''', (event_name, location, event_date, start_time, end_time,
                  duration, supplies, safety, description, event_type,
                  event_id, session['user_id']))

        return redirect(url_for('event_leader_manage_events', updated=True))

    # GET request
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT * FROM events
            WHERE event_id = %s AND event_leader_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

    return render_template('event_leader_edit_event.html', event=event)

@app.route('/event_leader/cancel_event/<int:event_id>', methods=['POST'])
def event_leader_cancel_event(event_id):
    """Cancel an event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        # Delete related records first
        cursor.execute('DELETE FROM eventoutcomes WHERE event_id = %s;', (event_id,))
        cursor.execute('DELETE FROM feedback WHERE event_id = %s;', (event_id,))
        cursor.execute('DELETE FROM eventregistrations WHERE event_id = %s;', (event_id,))
        cursor.execute('DELETE FROM events WHERE event_id = %s AND event_leader_id = %s;',
                      (event_id, session['user_id']))

    return redirect(url_for('event_leader_manage_events', cancelled=True))

@app.route('/event_leader/volunteers/<int:event_id>')
def event_leader_volunteers(event_id):
    """View volunteers registered for an event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        # Check if event belongs to this leader
        cursor.execute('''
            SELECT * FROM events
            WHERE event_id = %s AND event_leader_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

        if not event:
            return redirect(url_for('event_leader_manage_events'))

        # Get registered volunteers
        cursor.execute('''
            SELECT u.user_id, u.username, u.full_name, u.email,
                   u.contact_number, er.attendance, TO_CHAR(er.registered_at, 'YYYY-MM-DD HH24:MI') as registered_at
            FROM users u
            JOIN eventregistrations er ON u.user_id = er.volunteer_id
            WHERE er.event_id = %s
            ORDER BY u.full_name;
        ''', (event_id,))
        volunteers = cursor.fetchall()

    return render_template('event_leader_volunteers.html', 
                         event=event, volunteers=volunteers)

@app.route('/event_leader/remove_volunteer/<int:event_id>/<int:volunteer_id>', methods=['POST'])
def event_leader_remove_volunteer(event_id, volunteer_id):
    """Remove a volunteer from an event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        cursor.execute('''
            DELETE FROM eventregistrations
            WHERE event_id = %s AND volunteer_id = %s
            AND EXISTS (
                SELECT 1 FROM events
                WHERE event_id = %s AND event_leader_id = %s
            );
        ''', (event_id, volunteer_id, event_id, session['user_id']))

    return redirect(url_for('event_leader_volunteers', event_id=event_id))

@app.route('/event_leader/attendance/<int:event_id>', methods=['GET', 'POST'])
def event_leader_track_attendance(event_id):
    """Track volunteer attendance."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    if request.method == 'POST':
        attended = request.form.getlist('attended')

        with db.get_cursor() as cursor:
            # First, set all to 'no-show'
            cursor.execute('''
                UPDATE eventregistrations
                SET attendance = 'no-show'
                WHERE event_id = %s;
            ''', (event_id,))
            
            # Then update attended volunteers to 'attended'
            for vol_id in attended:
                cursor.execute('''
                    UPDATE eventregistrations
                    SET attendance = 'attended'
                    WHERE event_id = %s AND volunteer_id = %s;
                ''', (event_id, vol_id))

        return redirect(url_for('event_leader_volunteers', event_id=event_id, attendance_saved=True))
   
    # GET request
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT * FROM events
            WHERE event_id = %s AND event_leader_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()

        cursor.execute('''
            SELECT u.user_id, u.username, u.full_name,
                   er.attendance
            FROM users u
            JOIN eventregistrations er ON u.user_id = er.volunteer_id
            WHERE er.event_id = %s
            ORDER BY u.full_name;
        ''', (event_id,))
        volunteers = cursor.fetchall()

    return render_template('event_leader_attendance.html', 
                         event=event, volunteers=volunteers)

@app.route('/event_leader/outcomes/<int:event_id>', methods=['GET', 'POST'])
def event_leader_record_outcomes(event_id):
    """Record event outcomes (attendees, rubbish bags, recyclables)."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    if request.method == 'POST':
        attendees = request.form['attendees']
        bags = request.form['bags']
        recyclables = request.form['recyclables']
        other = request.form.get('other', '')

        with db.get_cursor() as cursor:
            # Check if outcomes already exist
            cursor.execute('SELECT outcome_id FROM eventoutcomes WHERE event_id = %s;', (event_id,))
            exists = cursor.fetchone()
            
            if exists:
                # Update existing outcomes
                cursor.execute('''
                    UPDATE eventoutcomes SET
                        num_attendees = %s,
                        bags_collected = %s,
                        recyclables_sorted = %s,
                        other_achievements = %s,
                        recorded_by = %s,
                        recorded_at = CURRENT_TIMESTAMP
                    WHERE event_id = %s;
                ''', (attendees, bags, recyclables, other, session['user_id'], event_id))
            else:
                # Insert new outcomes
                cursor.execute('''
                    INSERT INTO eventoutcomes (
                        event_id, num_attendees, bags_collected,
                        recyclables_sorted, other_achievements, recorded_by
                    ) VALUES (%s, %s, %s, %s, %s, %s);
                ''', (event_id, attendees, bags, recyclables, other, session['user_id']))

        return redirect(url_for('event_leader_manage_events', recorded=True))

    # GET request
    with db.get_cursor() as cursor:
        # First get event details
        cursor.execute('''
            SELECT e.*,
                (SELECT COUNT(*) FROM eventregistrations 
                    WHERE event_id = e.event_id AND attendance = 'attended') as attended_count
            FROM events e
            WHERE e.event_id = %s AND e.event_leader_id = %s;
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()
        
        # Then get outcomes separately if they exist
        cursor.execute('''
            SELECT * FROM eventoutcomes 
            WHERE event_id = %s;
        ''', (event_id,))
        outcomes = cursor.fetchone()

    return render_template('event_leader_outcomes.html', event=event, outcomes=outcomes)

@app.route('/event_leader/feedback')
def event_leader_feedback():
    """View feedback for events."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    # Get filter parameters
    event_filter = request.args.get('event', '')
    rating_filter = request.args.get('rating', '')

    # Base query
    query = '''
        SELECT f.*, e.event_name, e.event_id, u.username, u.full_name
        FROM feedback f
        JOIN events e ON f.event_id = e.event_id
        JOIN users u ON f.volunteer_id = u.user_id
        WHERE e.event_leader_id = %s
    '''
    params = [session['user_id']]

    if event_filter:
        query += ' AND e.event_id = %s'
        params.append(event_filter)
    
    if rating_filter:
        query += ' AND f.rating = %s'
        params.append(rating_filter)
    
    query += ' ORDER BY e.event_date DESC, f.submitted_at DESC;'

    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        feedbacks = cursor.fetchall()
        
        # Calculate average rating
        if feedbacks:
            total = sum(fb['rating'] for fb in feedbacks)
            avg_rating = round(total / len(feedbacks), 1)
        else:
            avg_rating = 0
        
        # Get all events for filter dropdown
        cursor.execute('''
            SELECT event_id, event_name, event_date
            FROM events
            WHERE event_leader_id = %s
            ORDER BY event_date DESC;
        ''', (session['user_id'],))
        events = cursor.fetchall()
        
        # Count events with feedback
        cursor.execute('''
            SELECT COUNT(DISTINCT e.event_id) as count
            FROM events e
            JOIN feedback f ON e.event_id = f.event_id
            WHERE e.event_leader_id = %s;
        ''', (session['user_id'],))
        result = cursor.fetchone()
        events_with_feedback = result['count'] if result else 0

    return render_template('event_leader_feedback.html', 
                          feedbacks=feedbacks, 
                          events=events,
                          events_with_feedback=events_with_feedback,
                          avg_rating=avg_rating)

@app.route('/event_leader/send_reminder/<int:event_id>', methods=['POST'])
def event_leader_send_reminder(event_id):
    """Send reminder to volunteers."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    print(f"Reminder sent for event {event_id}")

    return redirect(url_for('event_leader_volunteers', 
                          event_id=event_id, reminder_sent=True))

@app.route('/event_leader/report/<int:event_id>')
def event_leader_report(event_id):
    """Generate event report."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT e.*,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id) as total_registered,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id AND attendance = 'attended') as actual_attended,
                   (SELECT COUNT(*) FROM eventregistrations WHERE event_id = e.event_id AND attendance = 'no-show') as no_show,
                   (SELECT AVG(rating)::numeric(10,2) FROM feedback WHERE event_id = e.event_id) as avg_rating,
                   (SELECT COUNT(*) FROM feedback WHERE event_id = e.event_id) as feedback_count,
                   eo.num_attendees, eo.bags_collected, eo.recyclables_sorted, eo.other_achievements
            FROM events e
            LEFT JOIN eventoutcomes eo ON e.event_id = eo.event_id
            WHERE e.event_id = %s AND e.event_leader_id = %s;
        ''', (event_id, session['user_id']))
        report = cursor.fetchone()

    return render_template('event_leader_report.html', report=report)