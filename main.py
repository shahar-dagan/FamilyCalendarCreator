from flask import Flask, render_template, request, send_file
from ics import Calendar, Event
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        family_members = request.form.getlist("name")
        birthdates = request.form.getlist("birthdate")
        calendar = create_calendar(family_members, birthdates)

        ical_file = "family_birthdays.ics"
        with open(ical_file, "w") as f:
            f.write(str(calendar))

        return send_file(ical_file, as_attachment=True)

    return render_template("index.html")

def create_calendar(names, birthdates):
    calendar = Calendar()
    for name, birthdate in zip(names, birthdates):
        bday_date = datetime.strptime(birthdate, "%Y-%m-%d")
        for year in range(datetime.now().year, datetime.now().year + 50):
            age = year - bday_date.year
            event = Event(name=f"{name}'s Birthday (Age: {age})", begin=datetime(year, bday_date.month, bday_date.day))
            calendar.events.add(event)

    return calendar

if __name__ == "__main__":
    app.run(debug=True)
