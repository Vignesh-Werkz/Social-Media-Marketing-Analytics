import time

from datacollection.DataCollectionManager import DataCollectionManager

start_time = time.time()

dataCollectionManager = DataCollectionManager()
dataCollectionManager.getLatestSubredditData("singapore")

print("Data collection cycle successfully completed in: " + str(time.time() - start_time) + "s")