





def find(longtitude, latitude, l):
    
    array_return[]
    
    for x in xrange(0,len(l)):
        diffx = longtitude - l[x].longtitude
        diffy = latitude - l[x].latititude
        distancediff = diffx^2 + diffy^2
        distancediff = sqrt (distancediff)
        if (distancediff < 0.00005)
            k = {
                long = l[x].longtitude
                lat = l[x].latitude
                k.StopId = l[x].StopId
            }
            array_return.append(k)
            

LoopDataType = {
    "long": 10.00000,
    "lat": 10.00000,
    "StopId": "StopID"
}