#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPS_Serial_Receiver.py
Use this script to receive and process the NMEA sentence
Created on Wed Jun  6 22:58:06 2018

@author: Aspiring_Wayne
"""


import time
import serial
import pynmea2
import sys
import multiprocessing as mps

def read_serial(Serial_Port,MPS_CONTROL_QUEUE,MPS_RESULT_QUEUE):
    """
    IN: NMEA Sentence from Serial port (USB or Bluetooth)
    OUT: NMEA GGA object
    """
    com = None
    reader = pynmea2.NMEAStreamReader()
    Tstart = time.time()
    ManagementTimer = time.time() #用來使讀取 MPS_CONTROL_QUEUE 時不要太頻繁
    FirstTimeConnected = False
    name = mps.current_process().name
    pid=mps.current_process().pid
    print("[Info] Initializing read_serial @ GPS_Serial_Receiver.py.")
    print("[Info] Process information:\n\tName:{}\n\tPID:{}".format(name,pid))
    while True:
        # 程式間互通有無的管道
        if ManagementTimer - time.time() > 1:
            # Check the status of management.
            command = MPS_CONTROL_QUEUE.get()
            if not command.startswith("[RS]"):
                MPS_CONTROL_QUEUE.put(command)
            # 收到控制程式終止訊號即停止運作
            elif command == "[RS]Terminate":
                print("[Info] Shutdown read_serial @ GPS_Serial_Receiver.py.")
                break
            #如果不是這邊給這邊的指令就放回去
            else:
                MPS_CONTROL_QUEUE.put(command)
        
        # 測試時 40秒後自動關閉
        if time.time() - Tstart > 40:
            print("[Info] Shutdown read_serial @ GPS_Serial_Receiver.py. (40s reached)")
            break
        # 如果還沒有成功連線：嘗試連接指定的埠口
        if com is None:
            try:
                com = serial.Serial(Serial_Port, timeout=5.0)
                FirstTimeConnected = True
                MPS_CONTROL_QUEUE.pur("[RS]Connected")
            # 失敗
            except serial.SerialException:
                print('could not connect to %s' % Serial_Port)
                time.sleep(5.0)
                continue
        data = com.read(16)
        for msg in reader.next(data):
            #print(msg)
            if msg.sentence_type == "GGA":
                #print("GGA\tLon:{}\tLat:{}\tAlt:{}".format(msg.longitude,msg.latitude,msg.altitude))
                #print("{},{}{},{}{},{}{}\n".format(time.strftime("%Y%m%dT%H%M%S"),msg.latitude,msg.lat_dir,msg.longitude,msg.lon_dir,msg.altitude,msg.altitude_units))
                print("{}{},{}{},{}{}\n".format(msg.latitude,msg.lat_dir,msg.longitude,msg.lon_dir,msg.altitude,msg.altitude_units))
