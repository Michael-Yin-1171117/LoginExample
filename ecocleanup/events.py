from loginapp import app,db
from flask import render_template,redirect,session,url_for

@app.route("/events")
def events():
    if "loggedin" not in session:
        return redirect("/login")

    cur=db.get_cursor()
    cur.execute("SELECT * FROM events ORDER BY event_date")
    data=cur.fetchall()

    return render_template("events.html",events=data)

@app.route("/join/<int:id>")
def join(id):
    cur=db.get_cursor()
    cur.execute("INSERT INTO registrations(user_id,event_id) VALUES(%s,%s)",
                (session["user_id"],id))
    return redirect("/events")

