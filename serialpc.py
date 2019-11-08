import time, sys, serial
from serial import SerialException
import MySQLdb
from termcolor import colored

SERIALPORT1 = "/dev/cu.usbserial-A7032XZL"  # the default com/serial port the receiver is connected to
BAUDRATE1 = 115200      # default baud rate we talk to DVR

send=0

# CREATE TABLE log2 (id INT AUTO_INCREMENT PRIMARY KEY,ts DATETIME,op VARCHAR(2),data varchar(255));
def insertdata(oper,data):
    conn = MySQLdb.connect(host= "localhost",
                  user="gpscontrol",
                  passwd="qazwsxedc",
                  db="dvr")
    x = conn.cursor()
    #oper="RX"
    #data="data"
    cmd="INSERT INTO log(ts,op, data) VALUES (NOW(),'"
    cmd=cmd+oper+"',"+data+");"
    #print(cmd)

    try:
       x.execute(cmd)
       conn.commit()
    except:
       conn.rollback()
    conn.close()


if __name__ == "__main__":
    try:
        # open up the FTDI serial port to get data transmitted to DVR
        ser1 = serial.Serial(SERIALPORT1, BAUDRATE1, timeout=1)    #timeout=0 means nonblocking
        ser1.flushInput();
        print ("\nCOM Port [", SERIALPORT1, "] found \n")
    except (IOError, SerialException) as e:
        print ("\nCOM Port [", SERIALPORT1, "] not found, exiting...\n")
        exit(1)

    try:

        while True:

            size = ser1.inWaiting()
            if size > 0:
                # rx1 = ser1.read(ser1_waiting)
                rx1 = ser1.read(size)
                # print("rx1:{}".format(rx1))
                rx=repr(rx1).replace("b'","'").replace("\r\n","").replace("\r\n","").replace(chr(92)+"r"+chr(92)+"n","")
                print(repr(rx1))
                insertdata("RX", rx);
                send = send+1
                if send == 15:
                    print("Send String")
                    message_bytes = bytes.fromhex("7E9C0000000167347E")
                    ser1.write(message_bytes)

    except IOError:
        print(IOError)
        print("Some IO Error found, exiting...")
