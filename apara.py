import sqlite3
import numpy as np
from datetime import datetime, timedelta, date
from astro import Astro

tithi_name = ['PADYA','BIDIGE','TADIGE','CHOUTHI','PANCHAMI','SHASTI','SAPTAMI','ASTAMI','NAVAMI','DASHAMI','YEKADASHI','DWADASHI','TRAYODASI','CHATURDASI','HUNNIME','AMAVASYE']
paksha_name = ["SUKLA","KRISHNA"]
db = 'achyuthahebbar.db'

def gen_table(dt,ark,mas,paksh,tit,type):
    date_list = []
    ti_pos = tithi_name.index(tit)
    if ti_pos == 13:
        if paksh == paksha_name[0]:
            next_ti_pos = 14
        else:
            next_ti_pos = 15
    elif ti_pos == 14 or ti_pos == 15:
        next_ti_pos = 0
    else:
        next_ti_pos = ti_pos + 1

    start_date = dt.date()

    if type == "S":
        ref = ark
    else:
        ref = mas
        ad = "AD."
        if ad in mas:
            M = mas.split(".")
            ref = M[1]

    year_end = False
    for i in range(0,14):
        for j in range(27,35):
            t = addDays(start_date, j)
            conn = sqlite3.connect(db)
            if type == "S":
                panch = conn.cursor().execute("SELECT date, arka FROM panchanga WHERE DATE = ?",(t,)).fetchall()
            else:
                panch = conn.cursor().execute("SELECT date, masa, tithi FROM panchanga WHERE DATE = ?",(t,)).fetchall()
            conn.close()
            for item in panch:
                if type == "S":
                    arka = item[1]
                else:
                    if tit == "PADYA":
                        x = item[2]
                        if x == tit:
                            arka = item[1]
                        else:
                            y = addDays(t,1)
                            conn = sqlite3.connect(db)
                            p = conn.cursor().execute("SELECT masa FROM panchanga WHERE DATE = ?",(y,)).fetchall()
                            conn.close()
                            for z in p:
                                arka = z[0]
                    else:
                        arka = item[1]
            sunrise = getSunrise(t)
            morning = setTime(t,sunrise)

            time18 = addGhalige(morning,18)
            time24 = addGhalige(morning,24)
            panch1 = getJataka(time18)
            tithi1 = panch1.tithi
            panch2 = getJataka(time24)
            tithi2 = panch2.tithi

            if (tithi1 == tit) and (tithi2 == tit):
                returned_date = t
                if isinstance(returned_date, datetime):
                    returned_date = returned_date.date()
                date_list.append(returned_date)
                if (arka == ref) and (i>1):
                    year_end = True
                    va = returned_date
                break

            elif (tithi1 == tit) and (tithi2 != tit):
                prevday = addDays(time18, -1)
                prevsunrise = getSunrise(prevday.date())
                prevday = setTime(prevday, prevsunrise)
                prevday = addGhalige(prevday, 24)
                returned_date = vyapti(prevday, time18, tit)
                if isinstance(returned_date, datetime):
                    returned_date = returned_date.date()
                date_list.append(returned_date)
                if (arka == ref) and (i>1):
                    year_end = True
                    va = returned_date
                break

            elif (tithi1 != tit) and (tithi2 == tit):
                nextday = addDays(time24, 1)
                nextsunrise = getSunrise(nextday.date())
                nextday = setTime(nextday, nextsunrise)
                nextday = addGhalige(nextday, 18)
                returned_date = vyapti(time24, nextday, tit)
                if isinstance(returned_date, datetime):
                    returned_date = returned_date.date()
                date_list.append(returned_date)
                if (arka == ref) and (i>1):
                    year_end = True
                    va = returned_date
                break

            else:
                if tithi1 == tithi_name[next_ti_pos]:
                    returned_date = t
                    if isinstance(returned_date, datetime):
                        returned_date = returned_date.date()
                    date_list.append(returned_date)
                    if (arka == ref) and (i>1):
                        year_end = True
                        va = returned_date
                    break
        start_date = returned_date
        if year_end:
            break

    date_list = ekadashiCheck(date_list, tit, "M")

    start_date = dt
    if (beforeTwoAm(start_date)):
        addDays(start_date,-1)
    if isinstance(start_date, datetime):
        start_date = start_date.date()

    om = addDays(start_date, 26)
    tp = addDays(start_date, 40)
    os = addDays(start_date, 170)
    oa = addDays(start_date, 345)
    pa = addDays(start_date, 360)
    sa = addDays(va, -2)
    av = addDays(va, -1)
    ss = addDays(va, 1)

    date_list.append(om)
    date_list.append(tp)
    date_list.append(os)
    date_list.append(oa)
    if type == "S":
        date_list.append(pa)
    else:
        date_list.append(sa)
        date_list.append(av)
        date_list.append(ss)
    if type == "N":
        date_list.remove(oa)

    date_list = ekadashiCheck(date_list, tit)
    date_list.sort()

    ind = 1
    f_list = []
    SA = True
    AV = False
    VA = False
    SS = False

    for d in date_list:
        conn = sqlite3.connect(db)
        panch = conn.cursor().execute("SELECT date, week, arka, masa, paksha, tithi FROM panchanga WHERE DATE = ?",(d,)).fetchall()
        conn.close()
        for row in panch:
            Date = datetime.strptime(row[0],"%Y-%m-%d").strftime("%d-%b-%Y")
            Week = row[1]
            Arka = row[2]
            Masa = row[3]
            Paksha = row[4]
            Tithi = row[5]
        masika = ''
        if type == "S":
            if d == om or d == addDays(om,1) or d == addDays(om,2):
                masika = "OONAMASIKA"
            elif d == tp or d == addDays(tp,1) or d == addDays(tp,2):
                masika = "TRIPAKSHIKA"
            elif d == os or d == addDays(os,1) or d == addDays(os,2):
                masika = "OONASHANMASIKA"
            elif d == oa or d == addDays(oa,1) or d == addDays(oa,2):
                masika = "OONABDIKA"
            elif d == pa or d == addDays(pa,1) or d == addDays(pa,2):
                masika = "PATANGA"
            elif d == va or d == addDays(va,1) or d == addDays(va,2):
                masika = "VARSHANTHIKA"
            else:
                masika = str(ind)+".MASIKA"
                ind += 1

        else:
            if d == om or d == addDays(om,1) or d == addDays(om,2):
                masika = "OONAMASIKA"
            elif d == tp or d == addDays(tp,1) or d == addDays(tp,2):
                masika = "TRIPAKSHIKA"
            elif d == os or d == addDays(os,1) or d == addDays(os,2):
                masika = "OONASHANMASIKA"
            elif d == oa or d == addDays(oa,1) or d == addDays(oa,2):
                masika = "OONABDIKA"
            elif (d == sa or d == addDays(sa,1) or d == addDays(sa,2)) and SA:
                if type == "U":
                    masika = "SANKALPA"
                elif type == "N":
                    masika = "OOBABDIKA"
                SA = False
                AV = True
            elif (d == av or d == addDays(av,1) or d == addDays(av,2)) and AV:
                masika = "ABDAVIMOKA"
                AV = False
                VA = True
            elif d == ss:
                masika = "SHUBHASWEEKARA"
            elif (d == va or d == addDays(va,1) or d == addDays(va,2)) and VA:
                masika = "VARSHABDIKA"
                VA = False
                SS = True
            else:
                masika = str(ind)+".MASIKA"
                ind += 1

        f_list.append([masika,Date,Week,Arka,Masa,Paksha,Tithi])

    return np.array(f_list)

def addDays(d,i):
    return (d + timedelta(days=i))

def addMins(d,i):
    return (d + timedelta(minutes=i))

def addGhalige(d,s):
    return (d + timedelta(seconds=s*24*60))

def getSunrise(d):
    conn = sqlite3.connect(db)
    panch = conn.cursor().execute("SELECT date, time FROM panchangatime WHERE DATE = ?",(d,)).fetchall()
    conn.close()
    sunrise = 0.0
    for item in panch:
        sunrise = item[1]
    return sunrise

def setTime(d,t):
    t = str(t)
    ti = t.split(".")
    time = datetime.strptime(ti[0]+ti[1],"%H%M").time()
    return datetime.combine(d, time)

def getJataka(d):
    pb = "BENGALURU"
    dt = d.strftime("%d.%m.%Y")
    tm = d.strftime("%H:%M")
    la = "12.97"
    lo = "77.63"
    return Astro(pb,dt,tm,la,lo)

def vyapti(prevday, nextday, tithi):
    i = 24
    while True:
        c1=0
        c2=0
        m=0
        while True:
            t1 = addMins(prevday, -i*m)
            t2 = addMins(nextday, i*m)
            a1 = getJataka(t1)
            tit1 = a1.tithi
            a2 = getJataka(t2)
            tit2 = a2.tithi
            if tit1 == tithi:
                c1 += 1
            if tit2 == tithi:
                c2 += 1
            if (tit1 != tithi) or (tit2 != tithi):
                break
            else:
                m += 1
        if c1==c2:
            i /= 2
        else:
            if c1 > c2:
                return prevday
            else:
                return nextday

def beforeTwoAm(d):
    beforeTwo = datetime(d.year, d.month, d.day, 2, 0)
    return (d < beforeTwo)

def ekadashiCheck(list, or_tithi, t=""):
    new_list = []
    for item in list:
        nd = item
        for i in range(0,3):
            conn = sqlite3.connect(db)
            panch = conn.cursor().execute("SELECT date, vishesha, tithi FROM panchanga WHERE DATE = ?",(nd,)).fetchall()
            conn.close()
            for x in panch:
                vish = x[1]
                th_tithi = x[2]
            upa = ["YEKADASHI", "PAVASA"]
            for x in upa:
                if x in vish:
                    nd = addDays(nd, 1)
                if or_tithi == "YEKADASHI" and nd == item and vish == "" and th_tithi == "YEKADASHI":
                    nd = addDays(nd, 1)
                if t == "M":
                    if or_tithi == "YEKADASHI" and th_tithi == "DASHAMI":
                        nd = addDays(nd, 1)
        new_list.append(nd)
    return new_list

class Apara():
    def __init__(self, d, t, c):
        dt = datetime.strptime(d+" "+t,"%Y-%m-%d %H:%M")
        jat = getJataka(dt)
        arka = jat.arka
        paksha = jat.paksha
        tithi = jat.tithi
        masa = ''
        date = dt
        for z in range(0,2):
            conn = sqlite3.connect(db)
            panch = conn.cursor().execute("SELECT masa, paksha FROM panchanga WHERE DATE = ?",(date.date(),)).fetchall()
            conn.close()
            p = ''
            m = ''
            print(date, panch)
            for x in panch:
                m = x[0]
                p = x[1]
            if paksha=="SUKLA" and tithi=="PADYA":
                if p==paksha:
                    masa = m
                    break
                else:
                    addDays(date, 1)
            else:
                masa = m
                break

        dt_to_print = dt.strftime("%A %B %d %Y %I:%M:%S %p")
        code = {"S":"SOURAMANA", "U":"CHANDRAMANA", "N":"CHANDRAMANA"}

        tab = gen_table(dt, arka, masa, paksha, tithi, c)
        #print(tab)

        self.head = f"MASIKA LIST FOR {dt_to_print} IST : {arka} {masa} {paksha} {tithi} : {code[c]}"
        self.tab = tab
        self.tail1 = "PANCHANGA BY Dr.SRINIVASA HEBBAR"
        self.tail2 = "THIS IS A COMPUTER GENERATED TABLE. ERRORS MAY OCCUR. CONSULT PANCHANGA FOR CONFIRMATION"
        self.tail3 = "DRIK GANITHA PANCHANGA IS USED FOR COMPUTATION. CALCULATIONS MAY DIFFER FROM OTHER PANCHANGAS"
