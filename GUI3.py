import tkinter as tk
import threading
from time import sleep
import winsound

from FileHandler import FileHandler
from ProcessHandler import ProcessHandler
from User import User


class ProcessPoliceApp(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        
        self._frame = None
        self.geometry = "800x600"
        #self.root.geometry("800x600")
        
        self.user = User()
        self.file_handler = FileHandler()
        self.process_handler = ProcessHandler()
        
        self.isTicking = self.update_isTicking()
        
        self.thread = None
        self.start_thread()
        
        self.change_frame(LoginPage)
        
    def change_frame(self, frame_class):
        
        if self._frame != None:
            self._frame.destroy()
        self._frame = frame_class(self)
        self._frame.grid()
            
    def start_thread(self):
        if self.thread == None:
            self.after(1000, self.start_thread)
            if self.user.user_id != '':
                global kill_thread
                kill_thread = False
                print("Thread Live!")
                self.monitor = ProcessMonitor(self.user)
                self.thread = threading.Thread(target=self.monitor.exe_monitor)
                self.thread.start()
        
    def update_isTicking(self):
        flagged_live = self.process_handler.get_live_flagged_pids()
        if flagged_live != None:
            self.isTicking = True
        else:
            self.isTicking = False


class LoginPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.controller = master
        
        self.username_label = tk.Label(text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry()
        self.username_entry.grid(row=0, column=1)
        
        self.password_label = tk.Label(text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry()
        self.password_entry.grid(row=1, column=1)
        
        self.submit_button = tk.Button(text="Submit", 
                                       command=self.confirm_credentials)
        self.submit_button.grid(row=2, column=0)
        
        self.new_user_button = tk.Button(text="New User",
                                      command=self.add_new_user)
        self.new_user_button.grid(row=2, column=1)
        
        self.master_widgets = [self.username_label, self.username_entry,
                               self.password_label, self.password_entry,
                               self.submit_button, self.new_user_button]
        
    def confirm_credentials(self):
        user_id = self.username_entry.get()
        user_password = self.password_entry.get()       
        
        user_time = self.controller.file_handler.log_in(user_id, user_password)
        if user_time != None:
            print("Successfully Logged on")
            self.controller.user.update_user_attributes(user_id, user_password,
                                                        user_time)
            self.controller.user.print_attributes()
            self.destroy_self()
            self.controller.change_frame(MainPage)
        else:
            print("Invalid Login Information")
            
    def add_new_user(self):
        pass
            
    def destroy_self(self):
        for widget in self.master_widgets:
            widget.destroy()


class MainPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.controller = master
        
        self.isFrameLive = True
        self.isTicking = master.isTicking    
        
        self.clock = tk.Label(text=master.user.user_time, 
                              font = ("Helvetica", 120))
        self.clock.grid(row=0, column=0)
        
        self.add_time_button = tk.Button(text="Add Time", 
                                         command=self.add_time)
        self.add_time_button.grid(row=1, column=1)
        
        self.logout_button = tk.Button(text="Log Out", command=self.log_out)
        self.logout_button.grid(row=1, column=0)
        
        self.master_widgets = [self.clock, self.add_time_button,
                               self.logout_button]
        
        self.maintain_countdown()
        
    def log_out(self):
        global kill_thread
        self.destroy_self()
        kill_thread = True
        self.controller.user = User()
        self.controller.thread = None
        self.controller.start_thread()
        self.controller.change_frame(LoginPage)
    
    def add_time(self):
        self.destroy_self()
        self.controller.change_frame(AddTimePage)
        
    def maintain_countdown(self):
        # update self.ticking --- MIGHT NOT NEED IF THREAD IS UPDATING
        if self.isFrameLive:
            self.update_isTicking()
    
            try:
                user_id = self.controller.user.user_id
                time = self.controller.file_handler.read_user_time(user_id)
                if self.isTicking:
                    if time == "00:00:00":
                        self.controller.process_handler.find_and_destroy()
                    elif time == "00:05:00":
                        winsound.Beep(2500, 2000)
                    elif time == "00:00:30":
                        for i in range(3):
                            winsound.Beep(5000, 500)
                self.clock.configure(text = time)
                if self.isTicking:
                    # UPDATE CLOCK-Fast
                    self.after(200, self.maintain_countdown)
                else:
                    # UPDATE CLOCK-Slow
                    self.after(5000, self.maintain_countdown)
            except Exception:
                print("EXCEPTION IN MAINTAIN COUNTDOWN")
                self.after(850, self.maintain_countdown)
        
    def update_isTicking(self):
        flagged_live = self.controller.process_handler.get_live_flagged_pids()
        if flagged_live != None:
            self.isTicking = True
        else:
            self.isTicking = False
        
    def destroy_self(self):
        for widget in self.master_widgets:
            widget.destroy()


class AddTimePage(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        self.controller = master
        
        self.options = ["Study Linear Algebra", "Study Polish", "Study CS",
                        "Study Spanish", "Homework", "Thesis", "Reading"]
        
        self.activity = tk.StringVar(master)
        self.activity.set(self.options[2])
        
        self.activity_menu = tk.OptionMenu(master, self.activity, *self.options)
        self.activity_menu.grid(row=0, column=0)
        
        self.time_spent = tk.Entry()
        self.time_spent.grid(row=0, column=1)
        
        self.submit_button = tk.Button(text="Submit", command=self.update_time)
        self.submit_button.grid(row=1, column=1)
        
        self.back_button = tk.Button(text="Back", command=self.MainPage)
        self.back_button.grid(row=1, column=0)
        
        self.master_widgets = [self.activity_menu, self.time_spent,
                               self.submit_button, self.back_button]
        
    def update_time(self):
        time_spent = self.time_spent.get()
        time_spent = int(time_spent)*30
        #activity = self.activity.get()
        
        self.controller.user.increase_user_time(time_spent)
        self.controller.user.write_user_time()
        
    def MainPage(self):
        self.destroy_self()
        self.controller.change_frame(MainPage)
        
    def destroy_self(self):
        for widget in self.master_widgets:
            widget.destroy()


class ProcessMonitor():
    
    def __init__(self, user):
        
        self.user = user
        self.process_handler = ProcessHandler()
        self.update_isTicking()

    def exe_monitor(self):
        global kill_thread
        #self.update_isTicking()
        while not self.user.times_up:
            while self.isTicking and not self.user.times_up:
                self.user.reduce_user_time(1)
                if kill_thread:
                    return
                sleep(0.975)
            self.update_isTicking()
            sleep(5)
            if kill_thread:
                return
        self.process_handler.find_and_destroy()
        
    def update_isTicking(self):
        flagged_live = self.process_handler.get_live_flagged_pids()
        if flagged_live != None:
            self.isTicking = True
        else:
            self.isTicking = False


def wrap_up_app():
    if app.user.user_id != '':
        global kill_thread
        kill_thread = True
        
        app.thread.join()    
        app.destroy()
    else:
        app.destroy()


if __name__ == "__main__":
    global kill_thread
    kill_thread = False
    app = ProcessPoliceApp()
    app.protocol("WM_DELETE_WINDOW", wrap_up_app)
    app.mainloop()

