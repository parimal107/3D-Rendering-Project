import serial
import math 

#Modify the following line with your own serial port details
#   Currently set COM3 as serial port at 115.2kbps 8N1

xCoord = input("Enter how many times you would like to travel 50cm in the x dir ")
xCoord = int(xCoord)*int(50) #multiply by 50 bc we are going by increments of 50mm each time for xCoord times
xCounter = 0 #keep track of x coordinate

while(int(xCounter) <= int(xCoord)):
    print("xCounter = " + str(xCounter))
    print("xCoord = " + str(xCoord))

    f = open("measurement.txt" , "w") #stores the measurements
    a = open("measurementWOBootUp.txt" , "w") #stores the measurements without ToF boot up 
     

    s = serial.Serial("COM7", 115200)

    print("Opening: " + s.name)

    s.write(b'1')           #This program will send a '1' or 0x31 

    for i in range(171 + 10): #add 10 because thats how many lines the ToF boot up has
        x = s.readline()        # read one line
        c = x.decode()      # convert byte type to str
        print(c)
        f.write(c) #put the values in it
        print('----------------i = ' , i) #check index val
        if(i > 9): #9 is the value of i right after ToF boot up ouput is finished
            a.write(c)
        
        
    print("Closing: " + s.name)
    s.close()
    f.close() #close the measurement file that we write into 
    a.close() #close the measurement ToF file that we write into 


    b = open("measurementWOBootUp.txt" , "r") #this is the txt file we extract x values from
    storeDist = open("holdDist.txt", "w") #this stores the X values from the ToF output

    counter = 0 #create a counter which sees if we are in a number line 

    for line in b:
        #all values are stored on the odd lines, 0, 2, 4, etc so just skip empty new lines 
        if( counter % 2 == 0): 
            values = line.split(", ") #values is an array that holds the all the values slpit every comma
            distVal = values[1] #store the distance val
            storeDist.write(distVal + '\n') #add to the new txt file
        counter = counter + 1
        
    b.close()
    storeDist.close()
        
    #create XYZ file and populate y and z coords
    holdXYZ = open("holdXYZ.xyz" , "a") #put the x y and z values in this file and append it to the previous file for 3D graphing purposes
    d = open("holdDist.txt" , "r") #get the distance values from this file

    rad = 0
    radInc = 360/171 * (math.pi/180)
    for line in d:
        hyp = int(line)
        z = hyp * math.sin(rad)
        y = hyp * math.cos(rad)
        rad = rad + radInc #increment the angle 
        holdXYZ.write(str(xCounter * 10) + " " + str(y) + " " + str(z) + '\n') #mult xCounter by 10 to conv to mm from cm

    
    holdXYZ.close()
    d.close()
    xCounter = xCounter + 50 #ittirate the xCounter to the next x value
