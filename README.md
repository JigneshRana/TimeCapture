# TimeCapture-V1.0
Capture Keyboard Events, Mouse Actions And Screenshots Screenshot As Per Configuration.

# Description
TimeCapture is written in Python3. which is can be run in backgorund or forground. and track Mouse Activities, Keyboard Key Press, and Take Screenshot on Scheduled Time. Useful for Organization To track Users Activity like what is total working hours, How many time user got ideas, and also collects screenshots of users computer machine. 


# Advantages
+ Use to track realtime actions of the user.
+ Use to track users keyboard actions , mouse actions , as well as screenshots.
+ With little modifications, one can generate productivity reports.
+ Helps to track active working hours, and total ideal hours.
+ Veryusefull when empoyees are working from the remote locations. and you wanted to track.

# Options
You can configure Options in settings.py as your needs. file will look like as following.
options={"Mouse":True,"KeyBorad":True,"ScreenShot":True,"ImageTimeInSec":10,"IdealTimeOutSec":30}

+ Mouse = True / False : To Track Mouse Actions, keep it True
+ KeyBorad = True / False : To Track KeyBorad Actions, keep it True
+ ScreenShot = True / False : To Capture Screen Shot , Keep it True
+ ImageTimeInSec = Time In Seconds : This is Time Internal in Seconds. As per the setting it captures Screenshot in every 10 seconds.
+ IdealTimeOutSec: Configure Ideal Time in seconds. so It will popos up message to user, if screen is ideal for more than 30 seconds.
