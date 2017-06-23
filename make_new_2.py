import main_2
from peewee import *
import datetime
import os

    
def clear_screen():
    """clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
  
  
class NewEntry:
    """creates a new entry """
    def __init__(self, my_username):
        self.username = my_username
    
    def make_new(self):
        """walks through the process of creating a new entry"""
        while True:
            clear_screen()
            self.task_name = self.get_input("What is the task name?: ").strip()
            print("")
            if self.if_error_2("You did not enter a task name.", 
                self.task_name):
                break
        while True:
            self.time_spent = self.get_input("How much time was spent on the"
                                    " task?"
                                    " (In minutes. Ex: 72): ").strip()
            print("")
            if self.if_error(self.time_spent):
                break 
        
        while True:
            self.notes = self.get_input("What are your notes for this "
                                        "task?: ").strip()
            print("")
            if self.if_error_2("You did not enter any notes.", self.notes):
                break
            
        self.date = datetime.datetime.now()
        self.date_string = self.date.strftime('%m/%d/%Y %H:%M')  
        self.task_number = self.new_task_number()
        self.print_result(self.date_string, self.username, 
            self.task_name, self.time_spent, self.notes, self.task_number)
        self.create_new(self.date, self.username, 
            self.task_name, self.time_spent, self.notes, self.task_number)

    def create_new(self, date=None, username=None, task_name=None, 
        time_spent=None, notes=None, task_number=None):
        """creates a new entry in our database"""
        self.date = date
        self.username = username 
        self.task_name = task_name 
        self.time_spent = time_spent 
        self.notes = notes 
        self.task_number = task_number 
        main_2.Start_timesheet.create(username=self.username,
                            time_spent=int(self.time_spent),
                            notes=self.notes,
                            date=self.date,
                            task_name=self.task_name,
                            task_number=self.task_number) 
        return True 
           
    def if_error(self, time_spent=None):
        """checks for an error"""
        self.time_spent = time_spent    
        try:
            float(self.time_spent)
        except ValueError:
            print("{} is not an option.".format(self.time_spent))
            print("")
            return False
        else:
            return True 

    def if_error_2(self, message, err_2=None,):
        """checks for an error"""
        self.err_2 = err_2
        self.message = message
        if err_2:
            return True 
        else:
            print(self.message)
            print("")
            return False 

    def print_result(self, date_string=None, username=None, task_name=None, 
        time_spent=None, notes=None, task_number=None):
        """prints the result of creating a new entry"""
        self.date_string = date_string
        self.username = username 
        self.task_name = task_name 
        self.time_spent = time_spent 
        self.notes = notes 
        self.task_number = task_number 
        print("")
        print("")
        print("Date: {}".format(self.date_string))
        print("     Username: {}".format(self.username))
        print("     Task name: {}".format(self.task_name))
        print("     Time spent: {}".format(self.time_spent))
        print("     Notes: {}".format(self.notes))
        print("     Task number: {}".format(self.task_number))
        print("")
        print("")
        return True 

    def new_task_number(self):
        """finds the largest task number in our list, and +1 to it for a new 
        task number"""
        try:
            self.new_task_num = main_2.Start_timesheet.select().where(
                main_2.Start_timesheet.username == self.username).order_by(
                main_2.Start_timesheet.task_number.desc(
                    )).get()
        except DoesNotExist:
            self.new_task_num = 1
        else:
            self.new_task_num = self.new_task_num.task_number + 1
        return self.new_task_num 

    def get_input(self, message):
        """returns input"""
        self.message = message
        return input(self.message)

