# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor Boston, MA 02110-1301,  USA




from datetime import datetime
import time
import math

#Timer class
#Handles a timer for a player
class Timer:
    def __init__(self):
        self.last_time=datetime.now()
        self.remaining=0 #seconds remaining
        self.bytime=0 #seconds of byoyo time
        
        self.running=0 #if the timer is running
        self.inited=0 #if the timer has been initialized
    
    #Initialize the timer to have a time and byoyo time
    def set_time(self,time,bytime):
        self.remaining=int(time)*60
        self.bytime=int(bytime)
        self.running=0
        self.inited=1
    
    #start the timer
    def start(self):
        self.last_time=datetime.now()
        self.running=1
        
    #stop the timer
    def stop(self):
        if self.running:
            t=datetime.now()
            self.remaining-=self.get_diff(t-self.last_time)
            if self.remaining<0:self.remaining=0
        self.running=0
    
    #get the difference between two times in seconds as a float
    def get_diff(self, diff):
        return diff.seconds+diff.microseconds/1000000.0
        
    #get the time remaining in seconds
    def get_time(self):
        t=datetime.now()
        clock=self.remaining+self.bytime
        if self.running:
            clock-=self.get_diff(t-self.last_time)
        
        ret=int(math.ceil(clock))
        if ret<0:ret=0
        return ret
    
    #get the time remaining in HH:MM:SS format
    def get_time_str(self):
        clock=self.get_time()
        return time.strftime('%H:%M:%S', time.gmtime(clock))
        #return time.strftime("%M:%S")
