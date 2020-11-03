import sqlite3
from flask import Flask, request, render_template, flash, redirect, url_for, session
from wtforms import *
from astro import Astro

app = Flask(__name__)
app.secret_key = 'secret_key'
ent_name = ''
ent_pob = ''
ent_dob = ''
ent_tob = ''

@app.route("/")
def homepage():
    return render_template("index.html")

class JatakaForm(Form):
    name = StringField('Name')
    pob = StringField('Place Of Birth', [validators.InputRequired()])
    dob = StringField('Date Of Birth', [validators.InputRequired()])
    tob = StringField('Time Of Birth', [validators.InputRequired()])

    def validate_pob(form, field):
        conn = sqlite3.connect("latlong.db")
        pob = field.data.upper()
        place = conn.cursor().execute("SELECT * FROM latlong WHERE city = ?",(pob,)).fetchall()
        conn.close()
        if len(place)==0:
            raise ValidationError('Place Does Not Exist In Database')

class AddPlaceForm(Form):
    place = StringField('Name of Place', [validators.InputRequired()])
    lat = DecimalField('Latitude', [validators.InputRequired()])
    lon = DecimalField('Longitude', [validators.InputRequired()])

    def validate_place(form, field):
        conn = sqlite3.connect("latlong.db")
        plc = field.data.upper()
        place = conn.cursor().execute("SELECT * FROM latlong WHERE city = ?",(plc,)).fetchall()
        conn.close()
        if len(place)>0:
            raise ValidationError('Place Exists In Database')

@app.route("/jataka_form", methods=['get','post'])
def jataka_form():
    global ent_name, ent_pob, ent_dob, ent_tob
    form = JatakaForm(request.form)
    if form.validate():
        ent_name = request.form['name']
        ent_pob = request.form.get('pob')
        ent_dob = request.form.get('dob')
        ent_tob = request.form.get('tob')
        return redirect(url_for('jataka'))
    return render_template('jataka_home.html', form=form)

@app.route("/jataka")
def jataka():
    conn = sqlite3.connect("latlong.db")
    places = conn.cursor().execute("SELECT * FROM latlong WHERE city = ?",(ent_pob.upper(),)).fetchall()
    conn.close()
    for city, lat, long in places:
        latitude = lat
        longitude = long
    kundali = Astro(ent_pob,ent_dob,ent_tob,latitude,longitude,ent_name)
    return render_template('horoscope.html', kund=kundali)

@app.route("/list_places")
def list_places():
    conn = sqlite3.connect("latlong.db")
    places = conn.cursor().execute("SELECT * FROM latlong ORDER BY city ASC").fetchall()
    conn.close()
    output = ''
    row = "<tr><td>{}</td><td>{}</td><td>{}</td></tr>"
    for city, lat, long in places:
        output += row.format(city,lat,long)
    return render_template('places.html', table=output)

@app.route("/add_places", methods=['get','post'])
def add_places():
    form = AddPlaceForm(request.form)
    if form.validate():
        place = request.form.get('place')
        latitude = request.form.get('lat')
        longitude = request.form.get('lon')
        conn = sqlite3.connect("latlong.db")
        places = conn.cursor().execute("INSERT INTO latlong VALUES (?, ?, ?)",(place, latitude, longitude))
        conn.close()
        return redirect(url_for('list_places'))
    return render_template('add_places.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
