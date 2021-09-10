import sqlite3
from flask import Flask, request, render_template, flash, redirect, url_for, make_response, session, g
from astro import Astro
from match import Match
from apara import Apara

app = Flask(__name__)
app.secret_key = '12345678'
app.static_folder = 'static'
db = 'achyuthahebbar.db'

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth_login", methods=["post"])
def auth_login():
        session.pop('username',None)
        uid = request.form.get('uid')
        pwd = request.form.get('pwd')
        usr = ["AchyuthaHebbar","Achyutha@276"]
        if usr[0] != uid:
            flash(u"Invalid Username","danger")
            return redirect(url_for("login"))
        else:
            if usr[1] != pwd:
                flash(u"Invalid Password","danger")
                return redirect(url_for("login"))
            else:
                flash(u"Login Successful","success")
                session['username'] = uid
                return redirect(url_for("homepage"))
@app.route("/logout")
def logout():
    flash(u"Logout Successful","success")
    session.pop('username')
    return redirect(url_for("homepage"))

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/jataka_form")
def jataka_form():
    conn = sqlite3.connect(db)
    places = conn.cursor().execute("SELECT city FROM latlong").fetchall()
    conn.close()
    html = ''
    for place in places:
        if place[0] == "BENGALURU":
            html += '<option selected="selected" value="' + place[0] + '">' + place[0] + '</option>'
        else:
            html += '<option value="' + place[0] + '">' + place[0] + '</option>'
    return render_template('jataka_home.html',placelist=html)

@app.route("/jataka/<int:id>")
@app.route("/jataka", methods=['get','post'])
def jataka(id=0):
    if id==0:
        name = request.form.get('name')
        pob = request.form.get('pob')
        dob = request.form.get('dob')
        DB = dob.split('-')
        dtb = DB[2]+'.'+DB[1]+'.'+DB[0]
        tob = request.form.get('tob')
        if request.form['save'] == "yes":
            conn = sqlite3.connect(db)
            rec = conn.cursor().execute("SELECT * FROM record WHERE Place=? AND Date=? AND Time=?",(pob,dtb,tob,)).fetchall()
            if len(rec) == 0:
                try:
                    conn.cursor().execute("INSERT INTO record (name, place, date, time) VALUES (?,?,?,?)", (name,pob,dtb,tob))
                    conn.commit()
                    conn.close()
                    flash("RECORD SAVED")
                except Error :
                    flash("COULDN'T SAVE RECORD")
            else:
                conn.close()
                for serial, name, place, date, time in rec:
                    flash("Record Exists : Name = " + name + ", Place of Birth = " + place + ", Date = " + date + ", Time = " + time)
    else:
        conn = sqlite3.connect(db)
        rec = conn.cursor().execute("SELECT * FROM record WHERE serial = ?",(id,)).fetchall()
        conn.close()
        for serial, nm, pls, date, time in rec:
            name = nm
            pob = pls
            dtb = date
            tob = time

    conn = sqlite3.connect(db)
    places = conn.cursor().execute("SELECT * FROM latlong WHERE city = ?",(pob,)).fetchall()
    conn.close()
    for serial, city, lat, long in places:
        latitude = lat
        longitude = long
        kundali = Astro(pob,dtb,tob,latitude,longitude,name)
    return render_template('horoscope.html', kund=kundali)

@app.route("/match_form")
def match_form():
    conn = sqlite3.connect(db)
    places = conn.cursor().execute("SELECT city FROM latlong").fetchall()
    conn.close()
    html = ''
    for place in places:
        if place[0] == "BENGALURU":
            html += '<option selected="selected" value="' + place[0] + '">' + place[0] + '</option>'
        else:
            html += '<option value="' + place[0] + '">' + place[0] + '</option>'
    return render_template('match_home.html',placelist=html)

@app.route("/match", methods=['post'])
def match():
    bname = request.form.get('vara-name')
    bpob = request.form.get('vara-pob')
    bdob = request.form.get('vara-dob')
    bDB = bdob.split('-')
    bdtb = bDB[2]+'.'+bDB[1]+'.'+bDB[0]
    btob = request.form.get('vara-tob')
    gname = request.form.get('vadhu-name')
    gpob = request.form.get('vadhu-pob')
    gdob = request.form.get('vadhu-dob')
    gDB = gdob.split('-')
    gdtb = gDB[2]+'.'+gDB[1]+'.'+gDB[0]
    gtob = request.form.get('vadhu-tob')
    conn = sqlite3.connect(db)
    bplaces = conn.cursor().execute("SELECT * FROM latlong WHERE city = ?",(bpob,)).fetchall()
    gplaces = conn.cursor().execute("SELECT * FROM latlong WHERE city = ?",(gpob,)).fetchall()
    conn.close()
    for serial, city, lat, long in bplaces:
        blatitude = lat
        blongitude = long
    for serial, city, lat, long in gplaces:
        glatitude = lat
        glongitude = long
    if bname == "":
        bname = "VARA"
    if gname == "":
        gname = "VADHU"
    vadhu = Astro(gpob,gdtb,gtob,glatitude,glongitude,gname)
    vara = Astro(bpob,bdtb,btob,blatitude,blongitude,bname)
    vadhuvara = Match(bpob,bdtb,btob,blatitude,blongitude,gpob,gdtb,gtob,glatitude,glongitude,bname,gname)
    return render_template("vadhuvara.html", vv=vadhuvara, vara=vara, vadhu=vadhu)

@app.route("/apara_form")
def apara_form():
    return render_template('apara_home.html')

@app.route("/apara", methods=["post"])
def apara():
    dod = request.form.get('dod')
    tod = request.form.get('tod')
    cod = request.form.get('cod')
    apra = Apara(dod, tod, cod)
    return render_template("apara.html", apara=apra)

@app.route("/record_list")
def record_list():
    conn = sqlite3.connect(db)
    records = conn.cursor().execute("SELECT * FROM record ORDER BY name ASC").fetchall()
    conn.close()
    return render_template('record_list.html', records=records)

@app.route("/delete_record/<int:id>", methods=['post','get'])
def delete_record(id):
    conn = sqlite3.connect(db)
    conn.cursor().execute("DELETE FROM record WHERE serial = ?",(id,))
    conn.commit()
    conn.close()
    flash("RECORD DELETED")
    return redirect(url_for('jataka_form'))

@app.route("/delete_place")
def delete_place():
    conn = sqlite3.connect(db)
    places = conn.cursor().execute("SELECT * FROM latlong ORDER BY city ASC").fetchall()
    conn.close()
    return render_template('delete_places.html', places=places)

@app.route("/delete_city/<city_name>", methods=['post','get'])
def delete_city(city_name):
    conn = sqlite3.connect(db)
    conn.cursor().execute("DELETE FROM latlong WHERE city = ?",(city_name,))
    conn.commit()
    conn.close()
    flash("CITY DELETED")
    return redirect(url_for('jataka_form'))

@app.route("/edit_city/<city_name>", methods=['post','get'])
def edit_city(city_name):
    conn = sqlite3.connect(db)
    places = conn.cursor().execute("SELECT * FROM latlong WHERE city = ?",(city_name,)).fetchall()
    conn.close()
    return render_template('edit_places.html', places=places)

@app.route("/edit_place/<city_id>", methods=['post','get'])
def edit_place(city_id):
    conn = sqlite3.connect(db)
    place = request.form.get('place').upper()
    conn.cursor().execute("UPDATE latlong SET city = ?, latitude = ?, longitude = ? WHERE serial = ?",(place, request.form.get('lat'), request.form.get('lon'), city_id))
    conn.commit()
    conn.close()
    return redirect(url_for('jataka_form'))

@app.route("/add_place")
def add_place():
    return render_template('add_places.html')

@app.route("/add_city", methods=['post','get'])
def add_city():
    conn = sqlite3.connect(db)
    city = request.form.get('place').upper()
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    conn.cursor().execute("INSERT INTO latlong (city, latitude, longitude) VALUES (?,?,?)", (city,lat,lon))
    conn.commit()
    conn.close()
    return redirect(url_for('jataka_form'))

if __name__ == "__main__":
    app.run(debug=True)
