import numpy as np
from datetime import datetime, timedelta
import sqlite3

database = 'achyuthahebbar.db'
rasi_name = ['MESHA','VRISHABHA','MITHUNA','KARKATAKA','SIMHA','KANYA','TULA','VRISHCHIKA','DHANU','MAKARA','KUMBHA','MEENA']
tithi_name = ['PADYA','BIDIGE','TADIGE','CHOUTHI','PANCHAMI','SHASTI','SAPTAMI','ASTAMI','NAVAMI','DASHAMI','YEKADASHI','DWADASHI','TRAYODASI','CHATURDASI','HUNNIME','PADYA','BIDIGE','TADIGE','CHOUTHI','PANCHAMI','SHASTI','SAPTAMI','ASTAMI','NAVAMI','DASHAMI','YEKADASHI','DWADASHI','TRAYODASI','CHATURDASI','AMAVASYE']
nakshatra_name = ['ASWINI','BHARANI','KRUTHIKA','ROHINI','MRUGASIRA','ARDRA','PUNARVASU','PUSHYA','ASHLESHA','MAKHA','HUBBA','UTTARA','HASTA','CHITRA','SWATHI','VISHAKHA',
    'ANURADHA','JESHTA','MOOLA','POORVASHADA','UTTARASHADA','SHRAVANA','DHANISHTA','SHATABHISHA','POORVABHADRA','UTTARABHADRA','REVATHI']
x1 = ['KETU','SUKRA','RAVI','CHANDRA','KUJA','RAHU','GURU','SANI','BUDHA']
y1 = [7,20,6,10,7,18,16,19,17]
graha = ['LAGN','RAVI','BUDH','SUKR','KUJA','GURU','SANI','CHAN','RAHU','KETU','URAN','NEPT','PLUT']
div = ['RASI', 'DREKKANA', 'SAPTHAMSA', 'NAVAMSA','DASAMSA','DWADASAMSA', 'SHODASAMSA']
plnt = np.zeros(shape=(26,1))
pret = np.zeros(shape=(3,1))
mid_bhav = np.zeros(shape=(12,1))
beg_bhav = np.zeros(shape=(12,1))
bhavas = np.empty([12,3], dtype=object)
varga = np.zeros(shape=(13,7))
tt = np.zeros(shape=(4,1))
planpos = np.empty([12,6], dtype=object)
epoch = 0
pos_in_kundali = {
    graha[0] : [None]*7,
    graha[1] : [None]*7,
    graha[2] : [None]*7,
    graha[4] : [None]*7,
    graha[3] : [None]*7,
    graha[5] : [None]*7,
    graha[6] : [None]*7,
    graha[7] : [None]*7,
    graha[8] : [None]*7,
    graha[9] : [None]*7,
    graha[10] : [None]*7,
    graha[11] : [None]*7,
    graha[12] : [None]*7,
}
charts = np.empty([7,1], dtype=object)
dasa_remain = ''
co = 0.0
h6 = 0.0
b6 = 0.0
JD = 0.0
rs = 0.0
longt = 0
lat = 0
ret = False
lonsun = 0.0
lonlan = 0.0
Ms = 0.0
Ls = 0.0
aya = 0.0
obliq = 0.0
sidtime = 0.0
dash='-'
tithi = ''
nakshatra = ''
pada = 0
rasi = ''
arka = ''

pi = np.pi
p2 = pi / 180
def sin(x):
    return np.sin(x)
def cos(x):
    return np.cos(x)
def rad(x):
    return np.deg2rad(x)
def deg(x):
    return np.rad2deg(x)
def epow(x):
    return np.float_power(10,x)
def fract(x):
    return (x-int(x))
def atan(x):
    return np.arctan(x)
def sqrt(x):
    return np.sqrt(x)
def atan2(x,y):
    return np.arctan2(x,y)

def constant(dttm):
    dttm = dttm-timedelta(hours=5,minutes=30)
    d = dttm.day
    m = dttm.month
    y = dttm.year
    h = dttm.hour
    mn = dttm.minute
    x = h/24
    z = mn/1440
    dt = d + x + z
    cons = 367*y - (7*(y+((m+9)//12)))//4 + (275*m)//9 + dt - 730530
    return cons

def constant_h6(dttm):
    h = dttm.hour
    m = dttm.minute
    h6 = (h + m/60 - 17.5)/24
    return h6

def constant_b6(dttm):
    global b6
    d = dttm.day
    m = dttm.month
    y = dttm.year
    h = dttm.hour
    mn = dttm.minute
    if m<3:
        m += 12
        y -= 1
    a = y//100
    b = 30.6 * (m+1)
    l = int(b)
    j = 365*y+(y//4)+l+2-a+(a//4)+d
    w = (h + mn / 60 - 17.5)/24
    b6 = (j - 694025 + w) / 36525
    return b6

def julian_date(dttm):
    d = dttm.day
    m = dttm.month
    y = dttm.year
    h = dttm.hour
    mn = dttm.minute
    d = d + (h/24) + (m/(24*60))
    if m==1 or m==2:
        m1 = m+12
        y1 = y-1
    else:
        m1 = m
        y1 = y
    A = y1//100
    B = 2 - A + (A//4)
    C = int(365.25*y1)
    D = int(30.6001*(m1+1))
    JD = int(B+C+D+d+1720994.5)
    return JD

def planet (N,i,w,a,e,M,pno):
    global lonsun, rs
    if (pno==1):
        E = M + (180/pi) * e * sin(rad(M)) * (1 + e * cos(rad(M)))
        x = cos(rad(E)) - e
        y = sin(rad(E)) * sqrt(1 - e*e)
        rs = sqrt(x*x + y*y)
        v = deg(atan2(rad(y), rad(x)))
        lonsun = (v + w) % 360
        return lonsun

    else:
        while (M < 0):
            M += 360
        E=0
        E0 = M + (180/pi) * e * sin(rad(M)) * (1+e*cos(rad(M)))
        for ix in range(0,10):
            E1 = E0-(E0-(180/pi)*e*sin(rad(E0))-M)/(1-e*cos(E0))
            if abs(E0-E1) <= 0.005:
                E=E1
                break
            else:
                E0=E1
                ix += 1
        x = a * (cos(rad(E)) - e)
        y = a * sqrt(1 - e*e) * sin(rad(E))
        r = sqrt(x*x+y*y)
        v = deg(atan2(y, x))
        vw = rad(v+w)
        rn = rad(N)
        ri = rad(i)
        xh = r * (cos(rn) * cos(vw) - sin(rn) * sin(vw) * cos(ri))
        yh = r * (sin(rn) * cos(vw) + cos(rn) * sin(vw) * cos(ri))
        zh = r * (sin(vw) * sin(ri))
        lonecl = atan2(yh, xh)
        latecl = atan2(zh, sqrt(xh*xh+yh*yh))

        xh = r * cos(lonecl) * cos(latecl)
        yh = r * sin(lonecl) * cos(latecl)
        xs = rs * cos(rad(lonsun))
        ys = rs * sin(rad(lonsun))
        xg = xh+xs
        yg = yh+ys
        lonplan = deg(atan(yg/xg))
        if xg < 0:
            lonplan += 180
        elif yg < 0:
            lonplan += 360
        return lonplan

def preturb(JD,co):
    global pret
    T = (JD-2415020)/36525
    A = (T/5)+0.1
    P = 237.4755+3034.9061*T
    Q = 265.91650+1222.1139*T
    V = 5*Q-2*P
    B = Q-P
    pret[0] = (0.3314-0.0103*A)*sin(rad(V)) - 0.0644*A*cos(rad(V))
    pret[1] = (0.1609*A - 0.0105)*cos(rad(V)) + (0.0182*A - 0.8142)*sin(rad(V)) - 0.1488*sin(rad(B)) - 0.0408*sin(rad(2*B)) + 0.0856*sin(rad(B))*cos(rad(Q)) + 0.0813*cos(rad(B))*sin(rad(Q))

    Mj = 19.8950 + 0.0830853001 * co
    Ms = 316.967 + 0.0334442282 * co
    Mu = 142.5905 + 0.011725806 * co
    pret[2] = (0.04*sin(rad(Ms-2*Mu+6))) + (0.035*sin(rad(Ms-3*Mu+33))) + (-0.015*sin(rad(Mj-Mu+20)))

def sun(co,ret):
    global Ms, Ls, plnt
    N = 0
    i = 0
    w = 282.9404 + (4.70935*epow(-5))*co
    a = 1
    e = 0.016709 - (1.151*epow(-9)*co)
    Ms = 356.0470 + 0.9856002585*co
    while (Ms < 0):
        Ms += 360
    Ls = (w+Ms)%360
    pno = 1
    sun = planet (N, i, w, a, e, Ms, pno) - plnt[0]
    if  (sun < 0):
        sun += 360
    if (ret == False):
        plnt[pno] = sun
    else:
        plnt[pno+13] = sun

def mercury(co,ret):
    global plnt
    N = 48.3313 + (3.2487*epow(-5)) * co
    i = 7.0047 + (5*epow(-8)) * co
    w = 29.1241 + (1.01444*epow(-5)) * co
    a = 0.387098
    e = 0.205635 + (5.59*epow(-10)) * co
    M = 168.6562 + (4.0923344368 * co)
    pno = 2
    plane = planet (N, i, w, a, e, M, pno) - plnt[0]
    if (plane < 0):
        plane += 360
    if (ret == False):
        plnt[pno] = plane
    else:
        plnt[pno+13] = plane

def venus(co,ret):
    global plnt
    N = 76.6799 + (2.4659*epow(-5)) * co
    i = 3.3946 + (2.75*epow(-8)) * co
    w = 54.891 + (1.38374*epow(-5)) * co
    a = 0.72333
    e = 0.006773 - (1.302*epow(-9)) * co
    M = 48.0052 + (1.6021302244 * co)
    pno = 3
    plane = planet (N, i, w, a, e, M, pno) - plnt[0]
    if (plane < 0):
        plane += 360
    if (ret == False):
        plnt[pno] = plane
    else:
        plnt[pno+13] = plane

def mars(co,ret):
    global plnt
    N = 49.5574 + (2.11081*epow(-5)) * co
    i = 1.8497 - (1.78*epow(-8)) * co
    w = 286.5016 + (2.92961*epow(-5)) * co
    a = 1.523688
    e = 0.093405 + (2.516*epow(-9)) * co
    M = 18.6021 + (0.5240207766 * co)
    pno = 4
    plane = planet (N, i, w, a, e, M, pno) - plnt[0]
    if (plane < 0):
        plane += 360
    if (ret == False):
        plnt[pno] = plane
    else:
        plnt[pno+13] = plane

def jupiter(co,ret):
    global plnt
    N = 100.4542 + (2.76854*epow(-5)) * co
    i = 1.3030 - (1.557*epow(-7)) * co
    w = 273.8777 + (1.64505*epow(-5)) * co
    a = 5.20256
    e = 0.048498 + (4.469*epow(-9)) * co
    M = 19.8950 + 0.0830853001 * co
    M += pret[0]
    pno = 5;
    plane = planet (N, i, w, a, e, M, pno) - plnt[0]
    if (plane < 0):
        plane += 360
    if (ret == False):
        plnt[pno] = plane
    else:
        plnt[pno+13] = plane

def saturn(co,ret):
    global plnt
    N = 113.6634 + (2.3898*epow(-5)) * co
    i = 2.4886 - (1.081*epow(-7)) * co
    w = 339.3939 + (2.97661*epow(-5)) * co
    a = 9.55475
    e = 0.055546 - (9.499*epow(-9)) * co
    M = 316.967 + 0.0334442282 * co
    M += pret[1]
    pno = 6
    plane = planet (N, i, w, a, e, M, pno) - plnt[0]
    if (plane < 0):
        plane += 360
    if (ret == False):
        plnt[pno] = plane
    else:
        plnt[pno+13] = plane

def moon(co,ret):
    global plnt
    N = 125.1228 - 0.0529538083*co
    i = 5.1454
    w = 318.0634 + 0.1643573223*co
    a = 60.2666
    e = 0.054900
    M = 115.3654 + 13.0649929509*co
    while M < 0.0:
        M += 360.0
    E0 = M + (180/pi) * e * sin(rad(M)) * (1+e*cos(rad(M)))
    for ix in range(0,10):
        E1 = E0-(E0-(180/pi)*e*sin(rad(E0))-M)/(1-e*cos(E0))
        if abs(E0-E1) <= 0.005:
            E=E1
            break
        else:
            E0=E1
    x = a * (cos(rad(E)) - e)
    y = a * sqrt(1 - e*e) * sin(rad(E))
    r = sqrt(x*x+y*y)
    v = deg(atan2(y, x))
    vw = rad(v+w)
    rn = rad(N)
    ri = rad(i)
    xh = r * (cos(rn) * cos(vw) - sin(rn) * sin(vw) * cos(ri))
    yh = r * (sin(rn) * cos(vw) + cos(rn) * sin(vw) * cos(ri))
    lonecl = deg(atan2(yh, xh));
    if lonecl >= 360:
        while lonecl > 360:
            lonecl -= 360
    elif lonecl < 0:
        while lonecl < 0:
            lonecl += 360
    lon_corr = (3.82394*epow(-5)) * (365.2422 * (epoch - 2000)-co)
    lonecl += lon_corr
    Lm = N+w+M
    D = Lm-Ls
    F = Lm-N
    longt = (-1.274 * sin(rad(M - 2*D))) + (0.658 * sin(rad(2*D))) + (-0.186 * sin(rad(Ms))) + (-0.059 * sin(rad(2*M - 2*D))) + (-0.057 * sin(rad(M - 2*D + Ms))) +	(0.053 * sin(rad(M + 2*D))) + (0.046 * sin(rad(2*D - Ms))) + (0.041 * sin(rad(M - Ms))) + (-0.035 * sin(rad(D))) + (-0.031 * sin(rad(M + Ms))) + (-0.015 * sin(rad(2*F - 2*D))) + (0.011 * sin(rad(M - 4*D)))
    moon = lonecl + longt - plnt[0]
    if moon < 0:
        moon +=360
    rahu = N - plnt[0]
    if rahu >= 360:
        while rahu > 360:
            rahu-= 360
    elif rahu < 0:
        while rahu < 0:
            rahu += 360
    ketu = (N+180)%360 - plnt[0]
    if ketu >= 360:
        while ketu > 360:
            ketu-= 360
    elif ketu < 0:
        while ketu < 0:
            ketu += 360
    if ret==False:
        plnt[7] = moon
        plnt[8] = rahu
        plnt[9] = ketu
    else:
        plnt[20] = moon
        plnt[21] = rahu
        plnt[22] = ketu

def uranus(co,ret):
    global plnt
    N = 74.0005 + (1.3978*epow(-5)) * co
    i = 0.7733 - (1.9*epow(-8)) * co
    w = 96.6612 + (3.0565*epow(-5)) * co
    a = 19.18171 - (1.55*epow(-8)) * co
    e = 0.047318 + (7.45*epow(-9)) * co
    M = 142.5905 + 0.011725806 * co
    M += pret[2];
    pno = 10;
    plane = planet (N, i, w, a, e, M, pno) - plnt[0]
    if plane < 0:
        plane += 360
    if ret == False:
        plnt[pno] = plane
    else:
        plnt[pno+13] = plane

def neptune(co,ret):
    global plnt
    N = 131.7806 + (3.0173*epow(-5)) * co
    i = 1.77 - (2.55*epow(-7)) * co
    w = 272.8461 - (6.027*epow(-6)) * co
    a = 30.05826 + (3.313*epow(-8)) * co
    e = 0.008606 + (2.15*epow(-9)) * co
    M = 260.2471 + 0.005995147 * co
    pno = 11
    plane = planet (N, i, w, a, e, M, pno) - plnt[0]
    if plane < 0:
        plane += 360
    if ret == False:
        plnt[pno] = plane
    else:
        plnt[pno+13] = plane

def pluto(b6,ret):
    global plnt
    M = 360 * ((0.19434 + 0.40254 * b6) % 1)
    M -= 0.1 * sin((M + plnt[1]) * (pi/180))
    w = 200.02 + 0.002 * b6
    N = 86.49 - 0.038 * b6
    e = 0.248644
    i = 17.146778 - 0.005531 * b6
    a = 39.52
    pno = 12
    plane = planet (N, i, w, a, e, M, pno) - plnt[0]
    if plane < 0:
        plane += 360
    if ret == False:
        plnt[pno] = plane
    else:
        plnt[pno+13] = plane

def ayan(b6):
    global plnt
    plnt[0] = 22.460148 + 1.396042*b6 + (b6*b6*(3.08*epow(-4)))

def get_epoch(dttm):
    global epoch
    day_of_year = dttm.timetuple().tm_yday
    year = dttm.year
    epoch = year + (day_of_year/365)

def first_bhava(a,c):
    r = aya
    w = obliq * p2
    b = a * 15 + 90.0
    if b >= 360.0:
        b -= 360.0
    a *= pi/12
    c *= p2
    if a==0.0 and c==0.0:
        return 90.0
    g = atan(-cos(a)/(sin(c) * sin(w)/cos(c) + sin(a)*cos(w)))
    g /= p2
    if g < 0.0:
        g += 180.0
    if b - g > 75.0:
        g += 180.0
    g -= r
    if g < 0.0:
        g += 360.0
    if g > 360.0:
        g -= 360.0
    return g

def mid_bhava(j,k,u):
    for l in range(0,3):
        m = j + k * l
        if m >= 360.0:
            m -= 360.0
        v = u+l-1
        mid_bhav[v] = m
        l +=1

def bhava(b6,h6,longt,lat):
    global aya, obliq, sidtime, bhavas
    aya = plnt[0]
    obliq = 23.452294 - 0.0130125 * b6
    a = 24 * fract(0.2769 + 100.00214 * b6)
    b = h6 * 24 + 12
    c = longt / 15
    sidtime = 24 * fract((a+b+c)/24)
    if sidtime < 0:
        sidtime += 24.0
    a = first_bhava(sidtime, lat)
    b = first_bhava(sidtime - 6.0, 0.0)
    c = (180 + b - a) / 3
    if b > a:
        c -= 120
    d = 60.0 - c
    mid_bhava(a, c, 1)
    mid_bhava(b+180, d, 4)
    mid_bhava(a+180, c, 7)
    mid_bhava(b, d, 10)
    beg_bhav[0] = (mid_bhav[11]+mid_bhav[0]) / 2
    if mid_bhav[0] < mid_bhav[11]:
        beg_bhav[0] += 180.0
    if beg_bhav[0] >= 360.0:
        beg_bhav[0] -= 360.0
    for i in range(1,12):
        beg_bhav[i] = (mid_bhav[i-1]+mid_bhav[i]) / 2
        if mid_bhav[i] < mid_bhav[i-1]:
            beg_bhav[i] += 180.0
        if beg_bhav[i] > 360.0:
            beg_bhav[i] -= 360.0
        i += 1
    for i in range(0,12):
        bhavas[i] = [i+1,beg_bhav[i],mid_bhav[i]]
# MISCELLENEOUS
def dasa_remaining():
    global dasa_remain
    d = plnt[7]
    d = 9 * fract(d/120)
    n = fract(d)
    q = int(d)
    pl = x1[q]
    bal = (1-n)*y1[q]
    yr = int(bal)
    bal = fract(bal)
    bal *= 12
    mn = int(bal)
    bal = fract(bal)
    bal *= 30
    dt = 0
    if bal%1 == 0:
        dt = int(bal)
    dt = int(bal+1)
    dasa_remain = str(pl) + ' DASA REMAINING AT BIRTH : ' + str(dt) + ' DAYS, ' + str(mn) + ' MONTHS, ' + str(yr) + ' YEARS'

def misc():
    global tithi, nakshatra, pada, rasi
    tith = (plnt[7]-plnt[1])/12
    while tith < 0.0:
        tith += 30.0
    tt[0] = tith
    nakshatr = plnt[7]*3/40
    tt[1] = nakshatr
    pada = int(4 * fract(tt[1])+1)
    yog = (plnt[7]+plnt[1])*3/40
    if yog > 27.0:
        yog -= 27.0
    tt[2] = yog
    ti = int(tt[0]) + 1
    if ti == 30:
        ti = 29
    else:
        ti = ti % 15 - 1
    if ti == -1:
        ti = 14
    na = int(tt[1])
    yo = int(tt[2])
    ras = plnt[7]/30
    ra = int(ras)
    tt[3] = ras
    tithi = tithi_name[ti]
    nakshatra = nakshatra_name[na]
    rasi = rasi_name[ra]
    dasa_remaining()

# VARGA TABLES
def saptavarga_table_computation(y,x,t):
    global varga, pos_in_kundali, arka
    j = np.zeros(shape=(8,1))
    q = int(x/30)
    z = int(q+1)
    j[1] = z%12
    r = 30 * fract(x/30)
    if r>=0 and r<10:
        m=1
    elif r>=10 and r<20:
        m=5
    else:
        m=9
    z = q+m
    j[2] = z%12
    z = int(x*7.0/30 + 1)
    j[3] = z%12
    z = int(x*9/30 + 1)
    j[4] = z%12
    r = int(10 * fract(x/30))
    if q%2==0:
        m=1
    else:
        m=9
    z = q+r+m
    j[5] = z%12
    r = int(12 * fract(x/30))
    z = q+r+1
    j[6] = z%12
    z = int(x * 16.0/30 + 1)
    j[7] = z%12
    for i in range(1,8):
        if j[i]==0:
            j[i]=12
        i += 1
    for i in range(1,8):
        varga[t][i-1] = j[i]
        i += 1
    for i in range(1,8):
        n = int(j[i][0])
        m = y[0:4]
        pos_in_kundali[m][i-1] = n
    if t==1:
        arka = rasi_name[int(j[1][0])-1]

def saptavarga_table():
    saptavarga_table_computation('LAGNA',mid_bhav[0],0)
    saptavarga_table_computation('RAVI',plnt[1],1)
    saptavarga_table_computation('BUDHA',plnt[2],2)
    saptavarga_table_computation('SUKRA',plnt[3],3)
    saptavarga_table_computation('KUJA',plnt[4],4)
    saptavarga_table_computation('GURU',plnt[5],5)
    saptavarga_table_computation('SANI',plnt[6],6)
    saptavarga_table_computation('CHANDRA',plnt[7],7)
    saptavarga_table_computation('RAHU',plnt[8],8)
    saptavarga_table_computation('KETU',plnt[9],9)
    saptavarga_table_computation('URANUS',plnt[10],10)
    saptavarga_table_computation('NEPTUNE',plnt[11],11)
    saptavarga_table_computation('PLUTO',plnt[12],12)

def table():
    global charts
    for i in range (0,7):
        html = '<tr class="h_cell">' + '<td id="house_12" class= "house_cell">' + generate_house(i,12) + '</td><td id="house_1" class= "house_cell">' + generate_house(i,1) + '</td><td id="house_2" class= "house_cell">' + generate_house(i,2) + '</td><td id="house_3" class= "house_cell">' + generate_house(i,3) + '</td>' + '</tr><tr  class="h_cell">' + '<td id="house_11" class= "house_cell">' + generate_house(i,11) + '</td><td id="house_13" class= "house_cell" rowspan="2" colspan="2">' + generate_house(i,13) + '</td><td id="house_4" class= "house_cell">' + generate_house(i,4) + '</td>' + '</tr><tr class="h_cell">' + '<td id="house_10" class= "house_cell">' + generate_house(i,10) + '</td><td id="house_5" class= "house_cell">' + generate_house(i,5) + '</td>' + '</tr><tr class="h_cell">' + '<td id="house_9" class= "house_cell">' + generate_house(i,9) + '</td><td id="house_8" class= "house_cell">' + generate_house(i,8) + '</td><td id="house_7" class= "house_cell">' + generate_house(i,7) + '</td><td id="house_6" class= "house_cell">' + generate_house(i,6) + '</td>' + '</tr>'
        charts[i] = html

def generate_house(index, num):
    list = []
    for key, value in pos_in_kundali.items():
        if value[index] == num:
            list.append(key)
    if num == 13:
        list.append(div[index] + ' KUNDALI')
    html = ''
    if len(list) > 0:
        for item in list:
            html += item + '  '
    return html

def planet_position():
    global planpos
    for i in range(1,13):
        plan_pos = ''
        aa = plnt[i]
        a = int(aa/30 + 1)
        b = int(aa * 3 / 40)
        c = int(4 * fract(aa * 3.0 / 40) + 1)
        bb = plnt[i+13]
        if (bb < aa):
            plan_pos = 'RETROGRADE'
        else:
            plan_pos = 'DIRECT'
        planpos[i-1] = [graha[i],aa,a,nakshatra_name[b],c,plan_pos]
        i += 1

def vimst(a,b,c):
    d = plnt[7]
    d = 9 * fract(d/120)
    n = fract(d)
    q = int(d)
    p = n * y1[q]
    a = c + b/12 + a/360
    e = a + 100.0
    b = a - p
    counter = dasabhukti(q,a,e,b,0)
    b = a - p
    dasbuk = dasabhukti(q,a,e,b,counter)
    return dasbuk

def dasabhukti(qz,az,ez,bz,i):
    if i>0:
        db = np.empty([i,5], dtype=object)
    counter = 0

    for c in range(qz,qz+9):
        if c>8:
            c-=9
        for d in range(0,9):
            n = c+d
            if n>8:
                n -= 9
            bz += y1[c] * y1[n] / 120
            if bz<az:
                continue
            p = int(bz)
            r = int(12 * fract(bz))
            t = int(30 * fract(12 * fract(bz)) + 1)
            if r==0:
                p -= 1
                r = 12
            elif r==2 and t>28:
                t -= 28
                r = 3
            if i>0:
                db[counter] = [x1[c],x1[n],t,r,p]
            counter += 1
        if i>0:
            db[counter] = ['','','','','']
        counter += 1
        if bz>ez:
            break
    if i>0:
        return db
    else:
        return counter

def addDays(d,i):
    return (d + timedelta(days=i))

class Astro():
    def __init__(self, pob, dob, tob, latitude, longitude, name):
        latit = latitude.split('.')
        longit = longitude.split('.')
        lat = float(latit[0]) + (float(latit[1]) / 60)
        longt = float(longit[0]) + (float(longit[1]) / 60)
        db = dob.split('.')
        tb = tob.split(':')
        d = int(db[0])
        m = int(db[1])
        y = int(db[2])
        hr = int(tb[0])
        mn = int(tb[1])
        dttm = datetime(y,m,d,hr,mn)
        h6 = constant_h6(dttm)
        b6 = constant_b6(dttm)
        co = constant(dttm)
        JD = julian_date(dttm)
        ret = False
        get_epoch(dttm)
        preturb(JD,co)
        ayan(b6)
        sun(co,ret)
        mercury(co,ret)
        venus(co,ret)
        mars(co,ret)
        jupiter(co,ret)
        saturn(co,ret)
        moon(co,ret)
        uranus(co,ret)
        neptune(co,ret)
        pluto(b6,ret)
        ret = True
        dttm = dttm + timedelta(hours=1)
        b6 = constant_b6(dttm)
        co = constant(dttm)
        JD = julian_date(dttm)
        get_epoch(dttm)
        preturb(JD,co)
        sun(co,ret)
        mercury(co,ret)
        venus(co,ret)
        mars(co,ret)
        jupiter(co,ret)
        saturn(co,ret)
        moon(co,ret)
        uranus(co,ret)
        neptune(co,ret)
        pluto(b6,ret)
        dttm = dttm - timedelta(hours=1)
        planet_position()
        bhava(b6,h6,longt,lat)
        saptavarga_table()
        dasbuk = vimst(float(d), float(m), float(y))
        misc()
        table()

        if tt[0] < 15.0:
            paksha = "SUKLA"
        else:
            paksha = "KRISHNA"

        if name == "":
            name = "guest"

        samvat = ''
        masa = ''
        dd = dttm
        for z in range(0,2):
            conn = sqlite3.connect(database)
            panch = conn.cursor().execute("SELECT masa, paksha, samvat FROM panchanga WHERE DATE = ?",(dd.date(),)).fetchall()
            conn.close()
            p = ''
            ms = ''
            for x in panch:
                ms = x[0]
                p = x[1]
                if samvat == '':
                    samvat = x[2]
            if paksha=="SUKLA" and tithi=="PADYA":
                if p==paksha:
                    masa = ms
                    break
                else:
                    addDays(dd, 1)
            else:
                masa = ms
                break

        self.name = name
        self.pob = pob
        self.bhavas = bhavas
        self.varga = varga
        self.dasa_remain = dasa_remain
        self.aya = aya
        self.obliq = obliq
        self.sidtime = sidtime
        self.dob = dob
        self.tob = dttm.strftime("%I:%M %p")
        self.lat = latitude
        self.lon = longitude
        self.day = dttm.strftime("%A")
        self.tt = tt
        self.tithi = tithi
        self.nakshatra = nakshatra
        self.rasi = rasi
        self.pada = pada
        self.planpos = planpos
        self.dasbuk = dasbuk
        self.charts = charts
        self.arka = arka
        self.paksha = paksha
        self.samvat = samvat
        self.masa = masa
        self.filename_e = f'JATAKA-{name}-{dob}-{tob}-ESSENTIAL'
        self.filename_f = f'JATAKA-{name}-{dob}-{tob}-COMPLETE'
        self.graha = graha
