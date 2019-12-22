from FileHandler import FileHandler


class User:
    """
        Class to handle a specific user's data. Adding/subtracting and 
        formatting user_time, reading and writing a specific user's data into 
        master_users.txt database. Used in main.py Main class.
    """
    
    def __init__(self, user_id='', user_password='', user_time='00:00:00'):
        
        self.file_handler = FileHandler()                
        self.user_id = user_id
        self.user_password = user_password
        self.user_time = self.initialize_user_time(user_time)
        
        self.handle_new_user_initialization()
        
        self.times_up = False
        
    def handle_new_user_initialization(self):
        # Checks database for existing user... If exists updates user_time,
        # if not creates user in database and user_log
        if self.user_id != '':
            # If user_id not in database
            if self.file_handler.get_user_idx(self.user_id) == None:
                self.file_handler.add_new_user(self.user_id, 
                                               self.user_password)
                self.write_user_time()
            # If user_id already in database
            else:
                self.write_user_time()
        
    @staticmethod
    def initialize_user_time(initial_user_time):
        """ Convert time string "hh:mm:ss" into a dictionary with "hours",
            "minutes", and "seconds" as keys.
        """
        return({"hours":int(initial_user_time[:2]),
                "minutes":int(initial_user_time[3:5]), 
                "seconds":int(initial_user_time[6:])})
                
    def reduce_user_time(self, seconds):
        """ Reduces user time and rewrites it into master_users.txt database.
        """
        
        for sec in range(seconds):
            if self.user_time["seconds"] != 0:
                self.user_time["seconds"] -= 1
            else:
                if self.user_time["minutes"] == 5:
                    print("FIVE MINUTE WARNING")
                if self.user_time["minutes"] != 0:
                    self.user_time["minutes"] -= 1
                    self.user_time["seconds"] = 59
                else:
                    if self.user_time["hours"] != 0:
                        self.user_time["hours"] -= 1
                        self.user_time["minutes"] = 59
                        self.user_time["seconds"] = 59
                    else:
                        #TIMES UP
                        self.times_up = True
                        
        self.write_user_time()
        
    def increase_user_time(self, seconds):
        """ Increases user time and writes it into master_users.txt database.
        """
        
        for sec in range(seconds):
            if self.user_time["seconds"] != 59:
                self.user_time["seconds"] += 1
            else:
                if self.user_time["minutes"] != 59:
                    self.user_time["minutes"] += 1
                    self.user_time["seconds"] = 0
                else:
                    if self.user_time["hours"] != 99:
                        self.user_time["hours"] += 1
                        self.user_time["minutes"] = 0
                        self.user_time["seconds"] = 0
                    else:
                        #More than 99:59:59
                        print("SURPASSED TIME LIMIT")
                        
        self.write_user_time()
                        
    def write_user_time(self):
        """ Updates user time in master_users.txt database.
        """
        formatted_time = self.time_dict2string()
        self.file_handler.write_user_time(self.user_id, formatted_time)
     
    def time_dict2string(self):
        """Returns self.user_time converted from dictionary to "00:00:00" 
           format string.
        """
        
         # Format and convert hours to string
        if len(str(self.user_time["hours"])) < 2:
            hours = "0" + str(self.user_time["hours"])
        else:
            hours = str(self.user_time["hours"])
            
        # Format and convert minutes to string
        if len(str(self.user_time["minutes"])) < 2:
            minutes = "0" + str(self.user_time["minutes"])
        else:
            minutes = str(self.user_time["minutes"])
            
        # Format and convert seconds to string
        if len(str(self.user_time["seconds"])) < 2:
            seconds = "0" + str(self.user_time["seconds"])
        else:
            seconds = str(self.user_time["seconds"])
            
        formatted_time = hours + ":" + minutes + ":" + seconds                   
        return formatted_time
    
    def update_user_attributes(self, user_id=None, user_password=None, 
                               user_time=None):
        """Edits the value of self.user_id, self.user_password, sef.user_time.
           If any parameter == None, the class variable remains unchanged.
        """
        if user_id != None:
            self.user_id = user_id
        if user_password != None:
            self.user_password = user_password
        if user_time != None:
            self.user_time = self.initialize_user_time(user_time)
    
    def print_attributes(self):
        print("user_id: " + self.user_id)
        print("user_password: " + self.user_password)
        print("user_time: " + self.time_dict2string())
        
    def print_time(self):
        """ Prints current time written in master_users.txt for user ---
            Used only for debugging purposes.
        """
        
        print(self.user_time["hours"])
        
        if self.user_time["minutes"] > 9 and self.user_time["seconds"] > 9:
            print(str(self.user_time["minutes"]) + ":" + 
                  str(self.user_time["seconds"]))
        elif self.user_time["minutes"] < 10 and self.user_time["seconds"] > 9:
            print("0" + str(self.user_time["minutes"]) + ":" + 
                  str(self.user_time["seconds"])) 
        elif self.user_time["minutes"] > 9 and self.user_time["seconds"] < 10:   
            print(str(self.user_time["minutes"]) + ":" + "0" +
                  str(self.user_time["seconds"]))
        elif self.user_time["minutes"] < 10 and self.user_time["seconds"] < 10:
            print("0" + str(self.user_time["minutes"]) + ":" + "0" +
                  str(self.user_time["seconds"]))  

if __name__ == "__main__":
    #user = User("dasvot", "12345", "00:00:05")
    #user.write_user_time()
    user = User("backpains", "i<3dylan", "00:00:10")
    user.write_user_time()
