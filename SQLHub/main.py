from devicecloud import DeviceCloud
import mysql.connector
import base64
import time
# import pandas as pd

UserN = "jakenardo@gmail.com"
PassW = "Apples123"

try:
    dc = DeviceCloud(UserN, PassW)
    print("Connected to Device Cloud...")

except:
    print("Attempt to connect to Device Cloud failed!")

# show the MAC address of all devices that are currently connected
#
# This is done using Device Cloud DeviceCore functionality

print("== Showing Connected Devices ==")  # This will only show ONLINE devices
for device in dc.devicecore.get_devices():
    if device.is_connected():
        print(device.get_mac())

print("== Assigning messages to send to web API ==")
InMes = """<sci_request version="1.0">
  <send_message cache="false">
    <targets>
      <device id="00000000-00000000-0004F3FF-FF1F3421"/>
    </targets>
    <rci_request version="1.1">
      <do_command target="xbgw">
        <send_serial addr="00:13:A2:00:41:A0:49:8A"
                encoding="base64"> UnM=
        </send_serial>
      </do_command>
    </rci_request>
  </send_message>
 </sci_request>"""

OutMes = """<sci_request version="1.0">
  <send_message cache="false">
    <targets>
      <device id="00000000-00000000-0004F3FF-FF1F3421"/>
    </targets>
    <rci_request version="1.1">
      <do_command target="xbgw">
        <send_serial addr="00:13:a2:00:41:b5:f7:07"
                encoding="base64"> UnM=
        </send_serial>
      </do_command>
    </rci_request>
  </send_message>
 </sci_request>"""

# Test code to try and send a message to a Xbee node. It displays the ping, as well as sends the "InMes" to the xbee
# This code sends "Reserved" message, and should ONLY be used for testing
#
# InObj = dc.get_connection()
# print("Ping is: ", InObj.ping()) # Shows the ping for the response
# InObj.post("/ws/sci", InMes)

# OutObj = dc.get_connection()
# print("Ping is: ", OutObj.ping()) # Shows the ping for the response
# OutObj.post("/ws/sci", OutMes)

try:
    myDB = mysql.connector.connect(
        host="localhost",  # Hostname of the MySQL database
        user="root",  # Enter your username here
        password="Regina123",  # Enter your password here
        database="schema 1"
    )
    print("== Connected to Database ==")
    print(myDB)  # Shows connected Database
    myCursor = myDB.cursor()

    myCursor.execute("SHOW TABLES")
    print("== Tables within connected Database ==")

    for x in myCursor:
        # T[counter] = x
        # counter += 1
        print(x)
        t = x
    # Store the various tables, as variables that can be called upon
    t = str(t)
    t = t.strip("()")
    t = t.split(",")
    # print(t[0].strip("'")) # Test print function, it requires the value to be stripped of the ' to show as a normal string


except:
    print("Connection to database failed!")

# This is done using Device Cloud stream functionality
# print("Here are the data streams currently connected: ")
# for stream in dc.streams.get_streams():
#    print("%s -> %s" % (stream.get_stream_id(), stream.get_current_value()))

# Initializing the required variables
Count1 = 1


def FormatTime(tuple, Sensor_ID):
    xbeeD = tuple.split("'")  # Big block to convert the information required into the form we need it in
    xbeeT = tuple.split("(")  # Isolates the Timestamp, and the DATA stream, to show us what we need
    Data = xbeeD[1]
    Time = xbeeT[2]

    Time = Time.split(", ")
    TimeYMD = Time[0], "-", Time[1], "-", Time[2]
    TimeYMD = ''.join(TimeYMD)
    TimeP = Time[3], ":", Time[4], ":", Time[5]
    TimeP = ''.join(TimeP)

    try:
        decData = base64.b64decode(Data)
        data = decData.decode("ascii")
    except:
        print("Something's not quite right...")
        data = "0"

    if Sensor_ID == "00:13:A2:00:41:A0:49:8A":
        str = "Indoor"
    elif Sensor_ID == "00:13:A2:00:41:B5:F7:07":
        str = "Outdoor"

    print("This is for the", str, "device.")
    print("Timestamp:", TimeYMD, " at ", TimeP)
    print("This is the converted data: ", data)

    if Sensor_ID == "00:13:A2:00:41:A0:49:8A":
        ID = 1
    elif Sensor_ID == "00:13:A2:00:41:B5:F7:07":
        ID = 2
    else:
        ID = 0

    DT = TimeYMD + " " + TimeP
    ST = data

    return ID, DT, ST


def read_sql():
    FetchStatement = "SELECT * FROM ", t[0].strip("'")
    FetchStatement = ''.join(FetchStatement)
    myCursor.execute(FetchStatement)

    myresult = myCursor.fetchall()

    list = []

    for x in myresult:
        print("This is the results from the read...", x)
        list.append(x[2])  # Appends the value of the "state" into a list

    In_State = list[0]
    Out_State = list[1]
    return In_State, Out_State


def commit_sql(Va, Vb, Vc, x, wack):
    # Commit statement that commits into the table the values that we currently have, in format PS_ID, PS_DT, PS_ST
    # Where PS_ID is Parking Spot ID, PS_DT is Date/time, and PS_ST is Parking Spot State
    values = (Va, Vb, Vc)
    CommitStatement = "REPLACE INTO ", t[0].strip("'"), " (Sensor_ID, Timestamp, Sensor_State) VALUES (%s, %s, %s)"
    CommitStatement = ''.join(CommitStatement)

    if 'Rs' in x:
        print("This spot is reserved. Sending reserved signal out towards to the device for 4 seconds.")
        Obj = dc.get_connection()
        # print("Ping is: ", Obj.ping())  # Shows the ping for the response

        if '00:13:A2:00:41:A0:49:8A' in wack:
            for Tz in range(4):
                Obj.post("/ws/sci", InMes)
                print("Sending Rs Message...Iteration:", Tz)
                time.sleep(.5)
        elif '00:13:A2:00:41:B5:F7:07' in wack:
            for Tz in range(4):
                Obj.post("/ws/sci", OutMes)
                print("Sending Rs Message...Iteration:", Tz)
                time.sleep(.5)

    myCursor.execute(CommitStatement, values)
    myDB.commit()
    print("Updating MySQL Record")

    return


while 1:
    # Acquires the separate streams that are currently operating at the beginning of the loop
    # The various PRINT statements are used for testing purposes
    print("-----------------------------------------------------------------------------------------------------------")
    time.sleep(3)  # Give the code a moment to breathe, since the data stream on the gateway only updates every ~5 seconds, we give it a 3 second sleep timer
    print("Instance :", Count1)
    Count1 += 1

    # Specific streams have already been created, this is accessing them, the first is accessing indoor state
    streamIn = dc.streams.get_stream("00000000-00000000-0004F3FF-FF1F3421/xbee.serialIn/[00:13:A2:00:41:A0:49:8A]!")
    # Outdoor stream
    streamOut = dc.streams.get_stream("00000000-00000000-0004F3FF-FF1F3421/xbee.serialIn/[00:13:A2:00:41:B5:F7:07]!")
    print("Indoor Stream ID: ", streamIn.get_stream_id())
    print("Outdoor Stream ID: ", streamOut.get_stream_id())
    xbeeIn = str(streamIn.get_current_value())
    xbeeOut = str(streamOut.get_current_value())

    xbeeInID = streamIn.get_stream_id()
    xbeeInID = xbeeInID.split("/")
    xbeeInID = xbeeInID[2].strip("[]!")

    xbeeOutID = streamOut.get_stream_id()
    xbeeOutID = xbeeOutID.split("/")
    xbeeOutID = xbeeOutID[2].strip("[]!")

    IN_ID, IN_DT, IN_ST = FormatTime(xbeeIn, xbeeInID)
    OUT_ID, OUT_DT, OUT_ST = FormatTime(xbeeOut, xbeeOutID)

    print("== Fetching reservation status from MySQL Database ==")
    IN_CST, OUT_CST = read_sql()

    print("== Updating MySQL with current state ==")
    commit_sql(IN_ID, IN_DT, IN_ST, IN_CST, xbeeInID)
    commit_sql(OUT_ID, OUT_DT, OUT_ST, OUT_CST, xbeeOutID)