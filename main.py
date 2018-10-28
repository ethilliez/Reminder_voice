import pandas as pd 
import datetime
import pyttsx3
import time
import calendar

class reminder():
    def __init__(self, file):
        self.engine = pyttsx3.init()
        self.wait_time = 31
        self.DF, self.N_reminders = self.get_reminders(file)
  
    def get_reminders(self, file):
        '''
        Get the reminders file and parse them into a dataframe
        Input:  - file, string, path to csv reminder file
        Output: - DF, dataframe, containing all reminders
                - N_reminders, integer, Total number of reminders saved
        '''
        DF = pd.read_csv(file)
        N_reminders = len(DF.index)
        return DF, N_reminders

    def test_reminders(self, time_now, day_now):
        '''
        Test if there is a reminder for this timestamp time_now and today
        Input: - time_now, string, current time
               - day_now, string, current day
        Output: - message, string, message to be played
        '''
        message = None
        # Get if week or weekend
        if(day_now in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']):
            period = 'week'
        else:
            period = 'weekend'
        # Test for if reminder
        for i in range(0, self.N_reminders):
            if(self.DF['Day'].iloc[i] == day_now or self.DF['Day'].iloc[i] == 'all' or self.DF['Day'].iloc[i] == period):
                if(self.DF['Time'].iloc[i] == time_now): 
                    message = self.DF['Message'].iloc[i]  
        return message

    def main(self):
        '''
        Main program.
        '''
        self.engine.say('Reminders activated.')
        self.engine.runAndWait()
        while True:
            time_now = datetime.datetime.now()
            day_now = calendar.day_name[time_now.weekday()]
            time_now = str(time_now.hour)+':'+str(time_now.minute)
            message = self.test_reminders(time_now, day_now)
            if message != None:
                self.engine.say(message)
                self.engine.runAndWait()
            time.sleep(self.wait_time) # Check again in 31 seconds


if __name__ == '__main__':
    file = 'reminders.csv'
    reminder(file).main()