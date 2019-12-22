import psutil
import win32api
import os

#Only for testing purposes
from time import sleep, time


class ProcessHandler:
    """ 
        Class to monitor and terminate live processes, utilized in User, Gui, 
        and Main classes.   
    """
    
    def __init__(self):
        
        self.processes = self.get_processes()
        self.flagged_processes = []
        self.build_flagged_list()
        
    def get_processes(self):
        """ Return a dictionary populated with all live processes using their 'name' as a key and their pid as a value
        {'name': pid}
        """
        processes = {}
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
                processes[pinfo['name']] = pinfo['pid']
            except psutil.NoSuchProcess:
                pass
        return(processes)    
        
    def find_and_destroy(self):
        """ Searches for flagged_processes and if found, terminates them.
        """
        
        pids = self.get_live_flagged_pids()
        if pids != None:
            for pid in pids:
                print("TERMINATING: " + str(pid))
                self.terminate_process(pid)
        
    def get_live_flagged_pids(self):
        """ Check if flagged processes are currently running and return list of pids for each live flagged process,
        returns None if none are live.
        """
        
        self.update_processes()
        
        live_flagged_pids = []

        for key in self.processes:
            if key in self.flagged_processes:     
                # print(key)
                live_flagged_pids.append(self.processes[key])
                # self.terminate_process(pid)
                
        if len(live_flagged_pids) > 0:
            return live_flagged_pids
        else:
            return None
     
    def terminate_process(self, pid):
        """ Uses a process' pid to terminate it
        """
    
        terminate = 1
        try:
            handle = win32api.OpenProcess(terminate, False, pid)
            win32api.TerminateProcess(handle, -1)
            win32api.CloseHandle(handle)
            # print(key + " --Terminated!")
        except Exception:
            # print(key + " --ACCESS DENIED!")
            pass
        
    def steam_titles(self):
        """ Scans through all Steam files to build a list of installed .exe
            steam applications. Later added to self.flagged_list
        """
        
        path = "C:\Program Files (x86)\Steam1\steamapps\common"
        
        flagged_list = []
    
        #Generate a list with all game directories    
        raw_folders = [x[0] for x in os.walk(path)]
        folders = []
        for f in raw_folders:
            if '\\' not in f[47:]:
                folders.append(f)
        
        #Sift out all .exe files in game directories
        for file_dir in folders:
            for file in os.listdir(file_dir):
                if file.endswith(".exe"):
                    flagged_list.append(file)
                    
        return(flagged_list)
        
    def build_flagged_list(self):
        """ Combines found Steam .exe with known flagged .exe to initialize
            the self.flagged_processes list
        """
        self.flagged_processes = ['Steam.exe', 'Battle.net.exe',
                                  'MinecraftLauncher.exe', 'javaw.exe']
        self.flagged_processes += self.steam_titles()
                    
    def update_processes(self):
        """ Updates self.processes to show only currently running processes
        """
        self.processes = self.get_processes()


if __name__ == "__main__":
    ph = ProcessHandler()
    #pids = ph.get_live_flagged_pids()
    #print(ph.get_processes())
    print(ph.processes)
    ph.find_and_destroy()
