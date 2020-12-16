import numpy as np
from datetime import datetime, timedelta, date
from astro import Astro

rasi_name = ['MESHA','VRISHABHA','MITHUNA','KARKATAKA','SIMHA','KANYA','TULA','VRISHCHIKA','DHANU','MAKARA','KUMBHA','MEENA']
tithi_name = ['PADYA','BIDIGE','TADIGE','CHOUTHI','PANCHAMI','SHASTI','SAPTAMI','ASTAMI','NAVAMI','DASHAMI','YEKADASHI','DWADASHI','TRAYODASI','CHATURDASI','HUNNIME','PADYA','BIDIGE','TADIGE','CHOUTHI','PANCHAMI','SHASTI','SAPTAMI','ASTAMI','NAVAMI','DASHAMI','YEKADASHI','DWADASHI','TRAYODASI','CHATURDASI','AMAVASYE']
nakshatra_name = ['ASWINI','BHARANI','KRUTHIKA','ROHINI','MRUGASIRA','ARDRA','PUNARVASU','PUSHYA','ASHLESHA','MAKHA','HUBBA','UTTARA','HASTA','CHITRA','SWATHI','VISHAKHA', 'ANURADHA','JESHTA','MOOLA','POORVASHADA','UTTARASHADA','SHRAVANA','DHANISHTA','SHATABHISHA','POORVABHADRA','UTTARABHADRA','REVATHI']
graha_name = ['KETU','SUKRA','RAVI','CHANDRA','KUJA','RAHU','GURU','SANI','BUDHA']
graha_span = [7,20,6,10,7,18,16,19,17]
koota = np.empty([8,4], dtype=object)
bdasa = np.empty([9,5], dtype=object)
gdasa = np.empty([9,5], dtype=object)
bcharts = np.empty([7,1], dtype=object)
gcharts = np.empty([7,1], dtype=object)
bkuja = np.empty([5,3],dtype=object)
gkuja = np.empty([5,3],dtype=object)

def varna_koota(b, g):
    global koota
    varna = 1
    va = ['brahmana', 'kshatriya', 'vaishya', 'shudra']
    var = {va[0]:[rasi_name[3], rasi_name[7], rasi_name[11]], va[1]:[rasi_name[0], rasi_name[4], rasi_name[8]], va[2]:[rasi_name[1], rasi_name[5], rasi_name[9]], va[3]:[rasi_name[2], rasi_name[6], rasi_name[10]]}
    boy = ''
    girl = ''
    for key, value in var.items():
        if b in value:
            boy = key
        if g in value:
            girl = key
    b_index = va.index(boy)
    g_index = va.index(girl)
    if b_index > g_index:
        varna = 0
    koota[0][0] = "varna koota"
    koota[0][1] = boy
    koota[0][2] = girl
    koota[0][3] = varna

def vashya_koota(b, g):
    global koota
    vashya = 0
    vas = {rasi_name[0]:[rasi_name[4], rasi_name[7]], rasi_name[1]:[rasi_name[3], rasi_name[6]], rasi_name[2]:[rasi_name[5]], rasi_name[3]:[rasi_name[7], rasi_name[8]], rasi_name[4]:[rasi_name[6]], rasi_name[5]:[rasi_name[2], rasi_name[11]], rasi_name[6]:[rasi_name[5], rasi_name[9]], rasi_name[7]:[rasi_name[3]], rasi_name[8]:[rasi_name[11]], rasi_name[9]:[rasi_name[0], rasi_name[10]], rasi_name[10]:[rasi_name[0]], rasi_name[11]:[rasi_name[9]]}
    if (g in vas[b] and b in vas[g]) or (g==b):
        vashya = 2
    koota[1][0] = "vashya koota"
    koota[1][1] = b
    koota[1][2] = g
    koota[1][3] = vashya

def tara_koota(b, g):
    global koota
    boy = nakshatra_name.index(b)
    girl = nakshatra_name.index(g)
    tara = 0
    if boy==girl:
        tara=3
    else:
        count = 0
        pos = girl
        for x in nakshatra_name[pos]:
            count += 1
            if pos == boy:
                break
            pos += 1
            if pos == 27:
                pos = 0
        t = count%9
        if t%2==0:
            tara = 3
    koota[2][0] = "tara koota"
    koota[2][1] = b
    koota[2][2] = g
    koota[2][3] = tara

def yoni_koota(b,g):
    global koota
    yoni = 0
    animal = {'kudure':[nakshatra_name[0], nakshatra_name[23]], 'aane':[nakshatra_name[1], nakshatra_name[26]], 'meke':[nakshatra_name[2], nakshatra_name[7]], 'haavu':[nakshatra_name[3], nakshatra_name[4]], 'nayi':[nakshatra_name[18], nakshatra_name[5]], 'ili':[nakshatra_name[9], nakshatra_name[10]], 'bekku':[nakshatra_name[8], nakshatra_name[6]], 'emme':[nakshatra_name[14], nakshatra_name[12]], 'huli':[nakshatra_name[15], nakshatra_name[13]], 'jinke':[nakshatra_name[17], nakshatra_name[16]], 'hasu':[nakshatra_name[11], nakshatra_name[25]], 'mungusi':['ABHIJITH', nakshatra_name[20]], 'simha':[nakshatra_name[24], nakshatra_name[22]], 'manga':[nakshatra_name[19], nakshatra_name[21]]}
    enemy = {'simha':'aane', 'haavu':'mungusi', 'nayi':'jinke', 'manga':'meke', 'kudure':'emme', 'hasu':'huli', 'ili':'bekku'}
    for key, index in animal.items():
        if b in index:
            b_animal = key
            b_mf = index.index(b)
        if g in index:
            g_animal = key
            g_mf = index.index(g)
    enemy_check = False
    for key, value in enemy.items():
        if key == b_animal and value == g_animal:
            enemy_check = True
        elif key == g_animal and value == b_animal:
            enemy_check = True
    if enemy_check == False:
        if b_mf < g_mf or b_mf == g_mf:
            yoni = 4
        else:
            yoni = 2
    koota[3][0] = "yoni koota"
    koota[3][1] = b_animal
    koota[3][2] = g_animal
    koota[3][3] = yoni

def graha_koota(b, g):
    global koota
    g_points = 0
    graha = {graha_name[1]:[[graha_name[8],graha_name[7],graha_name[5]],[graha_name[4],graha_name[6]],[graha_name[2],graha_name[3],graha_name[0]]],
    graha_name[2]:[[graha_name[3],graha_name[4],graha_name[6],graha_name[0]],[graha_name[8]],[graha_name[1],graha_name[7],graha_name[5]]],
    graha_name[3]:[[graha_name[2],graha_name[0],graha_name[8]],[graha_name[4],graha_name[6],graha_name[1],graha_name[7]],[graha_name[5]]],
    graha_name[4]:[[graha_name[2],graha_name[3],graha_name[6],graha_name[0]],[graha_name[1],graha_name[7]],[graha_name[5],graha_name[8]]],
    graha_name[6]:[[graha_name[2],graha_name[3],graha_name[4],graha_name[0]],[graha_name[7],graha_name[5]],[graha_name[8],graha_name[1]]],
    graha_name[7]:[[graha_name[8],graha_name[1],graha_name[5]],[graha_name[5]],[graha_name[2],graha_name[3],graha_name[4],graha_name[0]]],
    graha_name[8]:[[graha_name[2],graha_name[1],graha_name[5]],[graha_name[4],graha_name[6],graha_name[7],graha_name[0]],[graha_name[3]]],
    }
    adhipathi = {graha_name[1]:[rasi_name[1],rasi_name[6]], graha_name[2]:[rasi_name[4]], graha_name[3]:[rasi_name[3]], graha_name[4]:[rasi_name[0],rasi_name[7]], graha_name[6]:[rasi_name[8],rasi_name[11]], graha_name[7]:[rasi_name[9],rasi_name[10]], graha_name[8]:[rasi_name[2],rasi_name[5]]}
    b_ad = ''
    g_ad = ''
    for key, value in adhipathi.items():
        if b in value:
            b_ad = key
        if g in value:
            g_ad = key
    i=0
    girl_for_boy = 0
    boy_for_girl = 0
    if g_ad == b_ad:
        g_points = 5
    else:
        for item in graha[b_ad]:
            if g_ad in item:
                girl_for_boy = i
            i += 1
        i=0
        for item in graha[g_ad]:
            if b_ad in item:
                boy_for_girl = i
            i += 1


        if girl_for_boy == boy_for_girl == 0:
            g_points = 5
        elif girl_for_boy == boy_for_girl == 1:
            g_points = 5
        elif girl_for_boy == 1 and boy_for_girl == 0:
            g_points = 3
        elif girl_for_boy == 0 and boy_for_girl == 1:
            g_points = 3
        elif girl_for_boy == 1 and boy_for_girl == 2:
            g_points = 1
        elif girl_for_boy == 2 and boy_for_girl == 1:
            g_points = 1
        elif girl_for_boy == boy_for_girl == 2:
            g_points = 0
    koota[4][0] = "graha mitratva"
    koota[4][1] = b_ad
    koota[4][2] = g_ad
    koota[4][3] = g_points

def gana_koota(b, g):
    global koota
    gana = 0
    gan = ['deva', 'manushya', 'rakshasa']
    ga_nak = {gan[0]:[nakshatra_name[0], nakshatra_name[4], nakshatra_name[6], nakshatra_name[7], nakshatra_name[12], nakshatra_name[14], nakshatra_name[16], nakshatra_name[21], nakshatra_name[26]],
    gan[1]:[nakshatra_name[1], nakshatra_name[3], nakshatra_name[5], nakshatra_name[10], nakshatra_name[11], nakshatra_name[19], nakshatra_name[20], nakshatra_name[24], nakshatra_name[25]],
    gan[2]:[nakshatra_name[2], nakshatra_name[8], nakshatra_name[9], nakshatra_name[13], nakshatra_name[15], nakshatra_name[17], nakshatra_name[18], nakshatra_name[22], nakshatra_name[23]],}
    b_gana = ''
    g_gana = ''
    for key, value in ga_nak.items():
        if b in value:
            b_gana = key
        if g in value:
            g_gana = key
    if b_gana == g_gana:
        gana = 6
    else:
        if (b_gana == gan[0] and g_gana == gan[1]) or (b_gana == gan[1] and g_gana == gan[0]):
            gana = 3
        elif (b_gana == gan[0] and g_gana == gan[2]) or (b_gana == gan[2] and g_gana == gan[0]):
            gana = 1
    koota[5][0] = "gana koota"
    koota[5][1] = b_gana
    koota[5][2] = g_gana
    koota[5][3] = gana

def rasi_koota(b, g):
    global koota
    r_point = 0
    b_in = rasi_name.index(b)
    g_in = rasi_name.index(g)
    if b_in > g_in:
        dif = b_in - g_in + 1
    else:
        dif = g_in - b_in + 1
    if dif in [3,11,4,10,7,1]:
        r_point = 7
    koota[6][0] = "rasi koota"
    koota[6][1] = b
    koota[6][2] = g
    koota[6][3] = r_point

def nadi_koota(b,g):
    global koota
    n_point = 8
    nadi = {'aadi':[nakshatra_name[0],nakshatra_name[5],nakshatra_name[6],nakshatra_name[11],nakshatra_name[12],nakshatra_name[17],nakshatra_name[18],nakshatra_name[23],nakshatra_name[24]],
    'madhya':[nakshatra_name[1],nakshatra_name[4],nakshatra_name[7],nakshatra_name[10],nakshatra_name[13],nakshatra_name[16],nakshatra_name[19],nakshatra_name[22],nakshatra_name[25]],
    'antya':[nakshatra_name[2],nakshatra_name[3],nakshatra_name[8],nakshatra_name[9],nakshatra_name[14],nakshatra_name[15],nakshatra_name[20],nakshatra_name[21],nakshatra_name[26]]}
    b_nadi = ''
    g_nadi = ''
    for key, value in nadi.items():
        if b in value:
            b_nadi = key
        if g in value:
            g_nadi = key
    if b_nadi == g_nadi:
        n_point = 0
    koota[7][0] = "nadi koota"
    koota[7][1] = b_nadi
    koota[7][2] = g_nadi
    koota[7][3] = n_point

def total_points():
    global comp
    points = 0
    for name,x,y,point in koota:
        points += point
    if points < 19:
        comp = "IC"
    return points

def dasa(blist, glist):
    global bdasa, gdasa
    bd = extract(blist)
    gd = extract(glist)
    b_sama_sandhi_years = []
    g_sama_sandhi_years = []
    for brow in bd:
        samasandhi = False
        for grow in gd:
            bdate = date(brow[3],brow[2],brow[1])
            gdate = date(grow[3],grow[2],grow[1])
            days = (bdate-gdate).days
            if abs(days) < 183:
                g_sama_sandhi_years.append(grow[3])
                samasandhi = True
        if samasandhi:
            b_sama_sandhi_years.append(brow[3])
    final_list(bd, b_sama_sandhi_years, bdasa)
    final_list(gd, g_sama_sandhi_years, gdasa)

def extract(list):
    start_dasa = list[0][0]
    start_index = graha_name.index(start_dasa)
    ret_list = np.empty([9,4], dtype=object)
    i = start_index
    j = i-1
    if j < 0:
        j = 8
    end_date = 0
    end_month = 0
    elapsed_year = 0
    for row in list:
        if row[0] == graha_name[i]:
            if row[1] == graha_name[j]:
                ret_list[0][0] = row[0]
                ret_list[0][1] = row[2]
                ret_list[0][2] = row[3]
                ret_list[0][3] = row[4]
                end_date = row[2]
                end_month = row[3]
                elapsed_year = row[4]
                break
    for k in range(1,9):
        i += 1
        if i > 8:
            i = 0
        graha = graha_name[i]
        span = graha_span[i]
        elapsed_year += span
        ret_list[k][0] = graha
        ret_list[k][1] = end_date
        ret_list[k][2] = end_month
        ret_list[k][3] = elapsed_year
    return ret_list

def final_list(list, ss_list, f_list):
    i = 0
    for row in list:
        f_list[i][0] = row[0]
        f_list[i][1] = row[1]
        f_list[i][2] = row[2]
        f_list[i][3] = row[3]
        if row[3] in ss_list:
            f_list[i][4] = "SS"
        else:
            f_list[i][4] = ""
        i += 1
        if i == 9:
            break

def kuja_dosh(b, g):
    global bkuja, gkuja
    bk = [b[4][0],b[0][0],b[3][0],b[7][0]]
    gk = [g[4][0],g[0][0],g[3][0],g[7][0]]
    find_kuja(bk,bkuja)
    find_kuja(gk,gkuja)
    if bkuja[4][2] >= gkuja[4][2]:
        bkuja[4][1] = "-"
        gkuja[4][1] = "-"
    else:
        bkuja[4][1] = "--"
        gkuja[4][1] = "--"

def find_kuja(list, nump):
    l = ["KUJA","LAGNA","SUKRA","CHANDRA"]
    nump[0][0] = l[0]
    nump[0][1] = int(list[0])
    nump[0][2] = 0
    for i in range(1,4):
        k = int(list[0])
        p = int(list[i])
        if p > k:
            j = 13-(p-k)
        else:
            j = (k-p)+1
        m = 0
        if j in [1,2,4,7,8,12]:
            if i == 1:
                m = 2
            else:
                m = 1
        nump[i][0] = l[i]
        nump[i][1] = p
        nump[i][2] = m
    total = 0
    for row in nump:
        if row[0] in l:
            total += row[2]
    nump[4][0] = "TOTAL"
    nump[4][2] = total

class Match():
    def __init__(self, bpob, bdob, btob, blatitude, blongitude, gpob, gdob, gtob, glatitude, glongitude, bname='VARA', gname='VADHU'):
        vara = Astro(bpob, bdob, btob, blatitude, blongitude, bname)
        bcharts = np.copy(vara.charts)
        bvarga = np.copy(vara.varga)
        vadhu = Astro(gpob, gdob, gtob, glatitude, glongitude, gname)
        gcharts = np.copy(vadhu.charts)
        gvarga = np.copy(vadhu.varga)
        brasi = vara.rasi
        bstar = vara.nakshatra
        grasi = vadhu.rasi
        gstar = vadhu.nakshatra


        varna_koota(brasi, grasi)
        vashya_koota(brasi, grasi)
        tara_koota(bstar, gstar)
        yoni_koota(bstar, gstar)
        graha_koota(brasi, grasi)
        gana_koota(bstar, gstar)
        rasi_koota(brasi, grasi)
        nadi_koota(bstar, gstar)
        dasa(vara.dasbuk, vadhu.dasbuk)
        kuja_dosh(bvarga,gvarga)

        en = False
        en_class = "red"
        if bstar == gstar:
            en = True
        if en:
            if bstar in [nakshatra_name[3], nakshatra_name[5], nakshatra_name[7], nakshatra_name[9], nakshatra_name[15], nakshatra_name[21], nakshatra_name[25], nakshatra_name[26]]:
                en_class = "green"
            elif bstar in [nakshatra_name[0], nakshatra_name[2], nakshatra_name[4], nakshatra_name[6], nakshatra_name[13], nakshatra_name[16], nakshatra_name[24]]:
                en_class = 'yellow'

        to_class = "green"
        if total_points() < 19:
            to_class = "red"

        self.koota = koota
        self.total = total_points()
        self.vara_name = bname
        self.vadhu_name = gname
        self.bdasa = bdasa
        self.gdasa = gdasa
        self.bname = bname
        self.gname = gname
        self.bcharts = bcharts
        self.gcharts = gcharts
        self.bkuja = bkuja
        self.gkuja = gkuja
        self.filename = f'Match-{bname}-{gname}'
        self.en = en
        self.en_class = en_class
        self.star = bstar
        self.to_class = to_class
