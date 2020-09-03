import sys
import RPi.GPIO as GPIO
import time
import bluetooth
import mysql.connector
from _datetime \
    import datetime
from mysql.connector import Error

GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme

GPIO.setup(26, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

duree = 5


def arroser(temps):
    try:

        #Si on arrose les fraises
        if (int(sys.argv[2]) == 1):
            while (temps > 0):
                GPIO.output(17, GPIO.HIGH)
                time.sleep(duree)
                GPIO.output(17, GPIO.LOW)
                time.sleep(duree)
                temps -= duree

        #Si on arrose les framboises
        elif (int(sys.argv[2]) == 2):
            while (temps > 0):
                GPIO.output(26, GPIO.HIGH)
                time.sleep(duree)
                GPIO.output(26, GPIO.LOW)
                time.sleep(duree)
                temps -= duree

        #Si on arrose les 2
        elif (int(sys.argv[2]) == 3):
            while (temps > 0):
                GPIO.output(17, GPIO.HIGH)
                time.sleep(duree)
                GPIO.output(17, GPIO.LOW)

                GPIO.output(26, GPIO.HIGH)
                time.sleep(duree)
                GPIO.output(26, GPIO.LOW)
                temps -= duree

    except:
        print("some error")

    finally:
        print("clean up")
        GPIO.cleanup()  # cleanup all GPIO


def estHumide():
    humide = False

    # connection à l'arduino
    bd_addr = "98:D3:61:F9:6B:0E"
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    # sock.send(None)

    data = sock.recv(1)
    sock.close()

    if (int(data[0]) == 48):
        print(str(datetime.now()) + "  -  pas humide")
        humide = False
    elif int(data[0]) == 49:
        print(str(datetime.now()) + "  -  humide")
        humide = True
    else:
        print(str(datetime.now()) + "  -  " + str(int(data[0])) + " - erreur")
    return humide


def insererDb(humide):
    heure = int(datetime.now().strftime('%H'))
    jour = int(datetime.now().strftime('%d'))
    mois = int(datetime.now().strftime('%m'))

    # connection à la db
    db = mysql.connector.connect(
        host="sql7.freemysqlhosting.net",
        user="sql7352381",
        passwd="gIsY9CalQF",
        database="sql7352381"
    )

    cursor = db.cursor()

    req = "select id_jour from jour where jour = %s and mois = %s"
    cursor.execute(req, (jour, mois,))
    id_jour = cursor.fetchall()

    req = "insert into test(id_jour, humidite_sol, heure) values (%s,%s, %s)"

    cursor.execute(req, {id_jour[0][0], humide, heure})

    db.commit()


# humidite = estHumide()
# insererDb(humidite)
humidite = False
if (not humidite):
    arroser(int(sys.argv[1]) * 20)
