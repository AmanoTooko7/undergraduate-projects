#没写完，不想写了
def makeMagList(earthquakeData):
    magList = []
    earthquakes = earthquakeData.get("features")
    for i in range(len(earthquakes)):
        earehquake = earthquakes[i]
        properties = earehquake.get("properties")
        mag = 
