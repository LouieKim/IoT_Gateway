#REFERENCE: https://docs.python.org/ko/3/library/sqlite3.html

import sqlite3
import datetime

def getControlHistory(date:str) -> list:
    conn = sqlite3.connect("samin.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM control_history_tb WHERE date_id >= '%s'" %date)

    listRows = cur.fetchall()
    conn.close()
    
    return listRows

def setControlHistory(mode:str, targetPower:int, active:str, errCode:int) -> str:
    conn = sqlite3.connect("samin.db")
    cur = conn.cursor()

    now_date = datetime.datetime.now()
    sql_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

    insertValues = [sql_date, mode, targetPower, active, errCode]

    cur.execute("INSERT INTO control_history_tb VALUES(?, ?, ?, ?, ?)", insertValues)

    print("========== Insert Success =========")

    conn.commit()
    conn.close()

    return "success"

def getDeviceHistory(date:str) -> list:
    conn = sqlite3.connect("samin.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_history_tb WHERE date_id >= '%s'" %date)
    listRows = cur.fetchall()
    conn.close()
    
    return listRows

def setDeviceHistory(targetPower:int, predictPower:int, currentPower:int) -> str:
    conn = sqlite3.connect("samin.db")
    cur = conn.cursor()

    now_date = datetime.datetime.now()
    sql_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

    insertValues = [sql_date, targetPower, predictPower, currentPower]

    cur.execute("INSERT INTO device_history_tb VALUES(?, ?, ?, ?)", insertValues)

    print("========== Insert Success =========")

    conn.commit()
    conn.close()

    return "success"

#dictDeviceStatus = {'targetPower': 500, 'predictPower': 156, 'currentPower': 55}
#setDeviceHistory(dictDeviceStatus['targetPower'], dictDeviceStatus['predictPower'], dictDeviceStatus['currentPower'])