from tkinter import *
import time
import sqlite3
import random
import tempfile
import win32api
import win32print

f = ''
flag = ''
flags = ''

login = sqlite3.connect("admin.db")
l = login.cursor()

c = sqlite3.connect("medicine.db")
cur = c.cursor()

columns = ('Sl No', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')

def make_bill():
    global t, c, B, cur, st, names, qty, sl, named, addd, name1, add, det, vc_id
    price = [0.0] * 10
    det = ['', '', '', '', '', '', '', '']
    det[2] = str(sl)
    for i in range(len(sl)):
        print(sl[i], ' ', qty[i], ' ', names[i])
    for k in range(len(sl)):
        cur.execute("select * from med where sl_no=?", (sl[k],))
        for i in cur:
            price[k] = int(qty[k]) * float(i[4])
            print(qty[k], price[k])
            cur.execute("update med set qty_left=? where sl_no=?", (int(i[3]) - int(qty[k]), sl[k]))
        c.commit()
    det[5] = str(random.randrange(100, 999))
    B = 'bill_' + str(det[5]) + '.txt'
