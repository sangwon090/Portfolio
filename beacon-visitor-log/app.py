import time
import serial
import sqlite3
from datetime import datetime

from beacon import getBeacons, getDistance, getBeaconId, feedback
from db import Database

STORE_ID = 1

if __name__ == '__main__':
    try:
        scanner = serial.Serial('/dev/tty.usbserial-142420', 9600)
        time.sleep(3)

        db = Database(sqlite3.connect('sqlite.db'))

        print('[ 방문자 목록 ]')
        print('방문자\t방문 장소\t방문 시간')
        for visit in db.findAllVisit():
            user = db.findUserById(visit[1])[1]
            store = db.findStoreById(visit[2])[1]
            timestamp = datetime.fromtimestamp(float(visit[3]))
            print(f'{user}\t{store}\t\t{timestamp}')

        while True:
            beacons = getBeacons(scanner)
            for beacon in beacons:
                if beacon['uuid'] == '00000000000000000000000000000000':
                    continue
                
                beacon_id = getBeaconId(beacon['factory_id'], beacon['uuid'], beacon['identifier'], beacon['mac'])

                if db.findUserByBeacon(beacon_id) == None:
                    continue

                distance = getDistance(-59, beacon['rssi'], 4)
                print('측정된 거리: 약 {0:.2f}m'.format(distance))

                if distance < 0.5:
                    db.addVisit(db.findUserByBeacon(beacon_id)[0], STORE_ID)
                    feedback(scanner)
                    continue
    except KeyboardInterrupt:
        exit(0)