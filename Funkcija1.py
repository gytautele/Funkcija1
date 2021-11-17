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
    q = 0
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
    det[5] = str(random.randint(100, 999))
    B = 'bill_' + str(det[5]) + '.txt'
    total = 0.00
    for i in range(10):
        if price[i] != '':
            total += price[i]  # totalling
    m = '\n\n\n'
    m += "===============================================\n"
    m += "                                  No :%s\n\n" % det[5]
    m += " EVANZ MEDICAL STORE COMPANY\n"
    m += " BINALBAGAN BRANCH, NEGROS OCCIDENTAL\n\n"
    m += "-----------------------------------------------\n"
    if t == 1:
        m += "Name: %s\n" % named
        m += "Address: %s\n" % addd
        det[0] = named
        det[1] = addd
        cur.execute('select * from cus')
        for i in cur:
            if i[0] == named:
                det[7] = i[2]
    else:
        m += "Name: %s\n" % name1.get()
        m += "Address: %s\n" % add.get()
        det[0] = name1.get()
        det[1] = add.get()
    m += "-----------------------------------------------\n"
    m += "Product                      Qty.       Price\n"
    m += "-----------------------------------------------\n"
    for i in range(len(sl)):
        if names[i] != 'nil':
            s1 = ' '
            s1 = (names[i]) + (s1 * (27 - len(names[i]))) + s1 * (3 - len(qty[i])) + qty[i] + s1 * (
                        15 - len(str(price[i]))) + str(price[i]) + '\n'
            m += s1
    m += "\n-----------------------------------------------\n"
    if t == 1:
        ntotal = total * 0.8
        m += 'Total' + (' ' * 25) + (' ' * (15 - len(str(total)))) + str(total) + '\n'
        m += "Valued customer Discount" + (' ' * (20 - len(str(total - ntotal)))) + '-' + str(total - ntotal) + '\n'
        m += "-----------------------------------------------\n"
        m += 'Total' + (' ' * 25) + (' ' * (12 - len(str(ntotal)))) + 'PHP ' + str(ntotal) + '\n'
        det[3] = str(ntotal)
    else:
        m += 'Total' + (' ' * 25) + (' ' * (12 - len(str(total)))) + 'PHP ' + str(total) + '\n'
        det[3] = str(total)

    m += "-----------------------------------------------\n\n"
    m += "Dealer 's signature:___________________________\n"
    m += "===============================================\n"
    print(m)
    p = time.localtime()
    det[4] = str(p[2]) + '/' + str(p[1]) + '/' + str(p[0])
    det[6] = m
    bill = open(B, 'w')
    bill.write(m)
    bill.close()
    cb = ('cus_name', 'cus_add', 'items', 'Total_cost', 'bill_dt', 'bill_no', 'bill', 'val_id')
    cur.execute('insert into bills values(?,?,?,?,?,?,?,?)',
                (det[0], det[1], det[2], det[3], det[4], det[5], det[6], det[7]))
    c.commit()
