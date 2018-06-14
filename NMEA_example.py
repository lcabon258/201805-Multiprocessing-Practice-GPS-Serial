import time
import serial
import pynmea2
import sys
import multiprocessing as mps



def read(filename):
    f = open(filename)
    reader = pynmea2.NMEAStreamReader(f)

    while 1:
        for msg in reader.next():
          print(msg)


def read_serial(filename):
    com = None
    reader = pynmea2.NMEAStreamReader()
    Tstart=time.time()
    count=0
    with open("GPSLog.txt","at") as fout:
        while 1:
            if time.time() - Tstart > 40:
                break
            if com is None:
              try:
                com = serial.Serial(filename, timeout=5.0)
              except serial.SerialException:
                print('could not connect to %s' % filename)
                time.sleep(5.0)
                continue
    
            data = com.read(16)
            for msg in reader.next(data):
                #print(msg)
                
                if msg.sentence_type == "GGA":
                    #print("GGA\tLon:{}\tLat:{}\tAlt:{}".format(msg.longitude,msg.latitude,msg.altitude))
                    print("{},{}{},{}{},{}{}\n".format(msg.timestamp,msg.latitude,msg.lat_dir,msg.longitude,msg.lon_dir,msg.altitude,msg.altitude_units))
                    #print("{}{},{}{},{}{}\n".format(msg.latitude,msg.lat_dir,msg.longitude,msg.lon_dir,msg.altitude,msg.altitude_units))

                #pynmea2.parse(msg)
                #print(dir(msg))
                    #fout.write("{},{}{},{}{},{}{}\n".format(time.strftime("%Y%m%dT%H%M%S",msg.timestamp),msg.latitude,msg.lat_dir,msg.longitude,msg.lon_dir,msg.altitude,msg.altitude_units))
                    fout.write("{},{}{},{}{},{}{}\n".format(count,msg.latitude,msg.lat_dir,msg.longitude,msg.lon_dir,msg.altitude,msg.altitude_units))
                    fout.flush()
                    count = count + 1
if __name__ == "__main__":
    #dev = "/dev/cu.usbmodem1411"
    dev = sys.argv[1]
    read_serial(dev)
