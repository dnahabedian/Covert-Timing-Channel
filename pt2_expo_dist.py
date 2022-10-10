import math
import random
from tabulate import tabulate

random.seed(1237)

#Global vars that we will need
iVal = [2, 6, 10, 14, 18]
bufferMax, m1, m2 = 20, 16, 32
expoMin, expoMed, expoMax = 0, math.log(2), 5
uniMin, uniMed, uniMax = 0, 0.5, 1

# Generate bits for secret message
def secretMessage(x):
    msg = []
    
    for y in range(x):
        msg.append(random.randint(0, 1))

    return msg

# Generate the underflow, overflow, and success values based on chosen distribution,
# Exponential or Uniform
def Implementation(m, i, dist):
    currBuff, currTime = i, 0
    overtPkts = []
    transmitCount, incomingCount, count = 0, i, 0
    timeline, incomingTimeline, TransmitTimeline = [0], [], [0]

    if (dist == 0):  # Use Exponential Distribution if dist == 0
        # Generating the source's pkt times
        for j in range(100):
            overtPkts.append(random.expovariate(1))

        for j in range(i):
            currTime += overtPkts[j]
            incomingTimeline.append(currTime)

        # Generate delays
        delays = []
        for currBit in m:
            if (currBit == 0):
                delays.append(random.uniform(expoMin, expoMed))
            else:
                delays.append(random.uniform(expoMed, expoMax))

    else:  # Use Uniform Distribution if dist == 1
        for j in range(100):
            overtPkts.append(random.uniform(0, 1))

        for j in range(i):
            currTime += overtPkts[j]
            incomingTimeline.append(currTime)

        # Generate delays of the packets
        delays = []
        for currBit in m:
            if currBit == 0:
                delays.append(random.uniform(uniMin, uniMed))
            else:
                delays.append(random.uniform(uniMed, uniMax))

    TransmitTimeline[0] = currTime + delays[0]

    # Setting at which times packets are sent out of the buffer
    for j in range(1, len(delays)):
        TransmitTimeline.append(TransmitTimeline[j - 1] + delays[j])

    # Setting at which times packets are coming into the buffer
    for j in range(i, len(overtPkts)):
        incomingTimeline.append(incomingTimeline[j - 1] + overtPkts[j])

    # Figure out when packets are received and sent, ie merging the two timeline
    while (transmitCount != len(TransmitTimeline) and incomingCount != len(incomingTimeline)):
        if (TransmitTimeline[transmitCount] < incomingTimeline[incomingCount]):
            #A packet is transmitted before one is sent to the buffer
            timeline.append(0)
            transmitCount += 1
        else:
            #A packet is sent to the buffer before one is transmitted
            timeline.append(1)
            incomingCount += 1

    transmitCount = 0
    # Count the amount of overflow and underflow, if at all
    while (transmitCount < len(m)):
        if (timeline[count] == 0):
            currBuff -= 1
            transmitCount += 1
        if (timeline[count] == 1):
            currBuff += 1
        if (currBuff < 0):
            return 0 #Undeflow, return 0
        if (currBuff > bufferMax):
            return 1 #Overflow, return 1
        count += 1

    # Return 2 when no overflow or underflow detected
    return 2

def runSim(mChoice):  
    if (mChoice == 0):
        msg = secretMessage(m1)
    else:
        msg = secretMessage(m2)
  
    #list[0] = underflow, list[1] = overflow, list[2] = success
    uniList = [0, 0, 0]
    expoList = [0, 0, 0]

    tableUni = [['M Size', 'i', 'Underflow', 'Overflow', 'Success']]
    tableExpo = [['M Size', 'i', 'Underflow', 'Overflow', 'Success']]

    punder, pover, psuccess = 0.0, 0.0, 0.0

    for i in iVal:
        for j in range(500):
            uniList[Implementation(
                msg, i, 1)] += 1

        #for j in range(500):
            expoList[Implementation(
                msg, i, 0)] += 1

        punder = uniList[0] / (uniList[0] + uniList[1] + uniList[2])
        pover = uniList[1] / (uniList[0] + uniList[1] + uniList[2])
        psuccess = uniList[2] / (uniList[0] + uniList[1] + uniList[2])

        tableUni.append([len(msg), i, punder, pover, psuccess])

        uniList[0] = 0
        uniList[1] = 0
        uniList[2] = 0
        
        punder = expoList[0] / (expoList[0] + expoList[1] + expoList[2])
        pover = expoList[1] / (expoList[0] + expoList[1] + expoList[2])
        psuccess = expoList[2] / (expoList[0] + expoList[1] + expoList[2])

        tableExpo.append([len(msg), i, punder, pover, psuccess])

        expoList[0] = 0
        expoList[1] = 0
        expoList[2] = 0
        
    print("Uni Dist")
    print(tabulate(tableUni, headers = 'firstrow', tablefmt = 'fancy_grid'))
    print("\n")
    print("Expo Dist")
    print(tabulate(tableExpo, headers = 'firstrow', tablefmt = 'fancy_grid'))

    return 0

runSim(0)
runSim(1)
