from cryptography.fernet import Fernet
import datetime


class FileHandler:
    """    
        Class to read (decrypt) and write (encrypt) data into master_users.txt 
        file and user_id.txt logs for future use and for reference in User, 
        Gui, and Main classes.   
    """
    
    def __init__(self):
        self.root_dir = "C:\\Users\\Dylan\\Desktop\\Programming Party\\Python 3\\PC Processes\\Process Manager"
        #self.master_users_path = self.root_dir+"\\users\\master_users.txt"
        self.master_users_path = r"Process Manager\users\master_users.txt"
        #self.key = Fernet.generate_key()
        self.key = b'ehghPwz6S0Y1kKgcaIV9IAWgJ5-ow-pIY_H54l9rX2A='
        self.cipher_suite = Fernet(self.key)

        self.separator = "--------------------"
    
    def log_in(self, user_id, user_password):            
        """ Checks master_users.txt database for given user_id and checks that
            given user_password matches.  If so, returns string user_time, in
            'hh:mm:ss' format, if not, returns None
        """
        
        user_idx = self.get_user_idx(user_id)
        if user_idx == None:
            print("Invalid user_id")
        else:
            with open(self.master_users_path) as file:
                for i, line in enumerate(file):
                    if i > user_idx+2:
                        break
                    elif i == user_idx+1:
                        # WARNING, MIGHT NEED TO SLICE STRING AFTER DECRYPTION
                        # ^ WENT AHEAD AND DID ABOVE -- REQUIRES TESTING ^
                        actual_password = self.decrypt(line).strip()
                        actual_password = actual_password[15:]
                        if user_password != actual_password:
                            # INVALID PASSWORD
                            return None                
                    elif i == user_idx+2:
                        user_time = self.decrypt(line).strip()
                        user_time = user_time[11:]
                        return user_time
                        
    def get_user_idx(self, user_id):
        
        """ 
            If matching user_id in master_users.txt, return row idx of user_id 
            in master_users.txt, if no matching user_id is found, return None.
            Used in self.add_new_user to check if user_id already exists on
            record.
        """
        
        existing_user_ids = {}
        with open(self.master_users_path) as file:
            for idx, line in enumerate(file):
                try:
                    decrypted_line = self.decrypt(line.strip())
                    if 'user_id' in decrypted_line:
                        stripped_line = decrypted_line.strip()
                        existing_user_ids[stripped_line[9:]] = idx
                except Exception:
                    print("Not Encrypted")
                    pass
        
        if user_id in existing_user_ids:
            return existing_user_ids[user_id]
        else:
            return None
        
    def add_new_user(self, user_id, user_password):
        """ Checks to ensure user_id does not currently exist in 
            master_users.txt, and if it does not, creates profile for new user
            in master_users.txt and generates a blank user_id.txt log
        """
        
        if self.get_user_idx(user_id) != None:
            print("user_id \"" + user_id + "\" already exists")
        else:
            self.add_user_to_master(user_id, user_password)
            self.generate_user_log(user_id)
            
    def add_user_to_master(self, user_id, user_password):
        """ Adds a new user to master_users.txt (self.master_users_path). Used
            in self.add_new_user after ensuring user doesn't already exist in
            master_users.txt
        """
        r_file_object = open(self.master_users_path, 'r')
        a_file_object = open(self.master_users_path, 'a')
        
        lines = [self.separator, "user_id: " + user_id,
                 "user_password: " + user_password, "user_time: 00:00:00",
                 self.separator]
       
        for line in lines:
            encrypted_line = self.encrypt(line)
            a_file_object.write(encrypted_line+'\n')
            
        r_file_object.close()
        a_file_object.close()
        
    def generate_user_log(self, user_id):
        """ Generates a blank .txt, named user_id.txt, for later use as a user 
            activity log
        """
        
        path = self.root_dir+"\\users\\" + user_id + ".txt"
        initialize_data = [self.separator, "INITIALIZED ON:", 
                           datetime.datetime.now(), self.separator]
        
        # create
        log = open(path, 'w')
        for line in initialize_data:
            encrypted = self.encrypt(str(line))
            log.write(encrypted + '\n')
        log.close()
                            
    def write_user_time(self, user_id, new_time):
        """ Checks to ensure user_id exists in master_users.txt before
            encrypting and rewriting the value of user_time.
        """
        
        user_idx = self.get_user_idx(user_id)
        if user_idx == None:
            raise Exception("User_id not found in database")
        else:
            lines = open(self.master_users_path).read().splitlines()
            lines[user_idx+2] = self.encrypt("user_time: " + str(new_time))
            open(self.master_users_path, 'w').write('\n'.join(lines))            
        
    def read_user_time(self, user_id):
        
        """ Checks to ensure user_id exists in master_users.txt before 
            decrypting and returning the value of user_time.
        """
        
        user_idx = self.get_user_idx(user_id)
        if user_idx == None:
            raise Exception("User_id not found in database")
        else:
            lines = open(self.master_users_path).read().splitlines()
            decrypted = self.decrypt(lines[user_idx+2]).strip()
            return(decrypted[11:])
        
    def read_file(self):
        
        """ Decrypts and prints entire self.master_users.txt file
        """
        
        with open(self.master_users_path) as file:
            for idx, line in enumerate(file):
                try:
                    print(self.decrypt(line.strip()))
                except Exception:
                    print("Not Encrypted")

    def encrypt(self, string):   
        """ Returns the encrypted version of string
        """      
        string_as_byte = string.encode()
        return(self.cipher_suite.encrypt(string_as_byte).decode())
         
    def decrypt(self, string):
        """ Returns the decrypted version of string
        """
        string_as_byte = string.encode()
        return(self.cipher_suite.decrypt(string_as_byte).decode())
    
        
if __name__ == "__main__":
    file_handler = FileHandler()
    #file_handler.add_new_user('dasvot', '12345')
    #file_handler.add_new_user('bob', 'abcde')
    #file_handler.read_file()
    #file_handler.check_existing_user('a')
    file_handler.write_user_time('dasvot', '01:01:10')

