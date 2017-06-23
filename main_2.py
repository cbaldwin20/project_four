import os
from peewee import *
import datetime
import make_new_2 
import look_up_2

db = SqliteDatabase('practice.db')


class Start_timesheet(Model):
    """creates the database attributes"""
    username = CharField(max_length=255)
    task_name = TextField()
    time_spent = IntegerField(default=0)
    notes = TextField()
    date = DateTimeField(default=datetime.datetime.now)
    task_number = IntegerField()


    class Meta:
        """creates the database"""
        database = db


def clear_screen():
    """clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """connects to the database"""
    db.connect()
    db.create_tables([Start_timesheet], safe=True)


class Start:
    """Starts off the program, giving options, then finishes the program
    by writing the results to the csv file"""
    def pick_one(self, choice, username):
        """Asks which option to make new entry or lookup old one"""
        while True:
            self.username = username 
            self.choice = choice 
            if self.choice.upper() in ["1", "ONE", "NEW ENTRY", "NEW"]:
                return make_new_2.NewEntry(self.username).make_new
            elif self.choice.upper() in ["2", "TWO", "LOOKUP", "EDIT"]:
                return look_up_2.LookupEntry(self.username).lookup_begin
            elif self.choice.upper() in ["3", "THREE", "QUIT", "Q"]:
                print("")
                print("Goodbye.")  
                return exit
            else:
                print("")
                print("{} is not an option.".format(self.choice))
                print("")

    def to_continue(self, if_continue):
        """results of if want to continue or not"""
        self.if_continue = if_continue
        if self.if_continue in ["N", "NO", "QUIT", "Q", "EXIT"]:
            print("Goodbye.")
            #if theres nothing in the list, then it will write nothing.
            return True 
        else:
            return False 
        
    def run(self):
        """After completing a task, asks if wants to do more,
        if no, then writes to the csv file the results """
        clear_screen()
        self.username = self.get_input("What is your first and last name?: ")
        print("Welcome {}.".format(self.username))
        while True:
            clear_screen()
            self.choice = self.get_input("Press 1 to add a new entry.\n"
                            "Press 2 to lookup and/or edit previous entries.\n"
                            "Press 3 to quit.\n"
                            ": ").upper().strip()
            self.which_module = self.pick_one(self.choice, self.username)
            self.which_module()
            print("")
            self.if_continue = self.get_input("Do you want to do some more?"
                " Enter N for no,"
                                " or Y for yes: ").upper().strip()
            if self.to_continue(self.if_continue):
                break 

    def get_input(self, message):
        """returns input"""
        self.message = message
        return input(self.message)

if __name__ == '__main__':
    initialize()
    Start().run()
