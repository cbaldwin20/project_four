import re
import datetime
import os
from peewee import *
import main_2


def clear_screen():
    """clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


class LookupEntry:
    """Gives option to lookup entry to edit or delete it"""
    def __init__(self, my_username):
        self.username = my_username

    def lookup_begin(self):
        """asks which option to look up an entry"""
        clear_screen()
        while True:
            self.look_beg_print()
            self.which_option = self.get_input(": ").strip().upper()
            self.which_option_result = self.which_return(self.which_option)
            if not self.which_option_result:
                continue 
            elif self.which_option_result == "quit":
                return None 
            else:
                self.which_option_result()
                return None 

    def look_beg_print(self):
        """prints the options"""
        print("")
        print("Enter 1 to find by date.")
        print("Enter 2 to find by time spent.")
        print("Enter 3 to find by search term.")
        print("Enter 4 to find by employee name.")
        print("Enter 5 if you know the task number and want to delete/"
            "edit.")
        print("Enter 6 if you want to quit to the main screen.")
        return True 

    def which_return(self, which_option):
        """filters through to decide which option was chosen"""
        self.which_option = which_option
        if self.which_option in ["1", "ONE", "DATE", "D"]:
            return self.find_by_date
            
        elif self.which_option in ["2", "TWO", "TIME", "TIME SPENT"]:
            return self.find_by_time_spent
            
        elif self.which_option in ["3", "THREE", "EXACT", "EXACT MATCH", 
                                    "MATCH", "E"]:
            return self.find_by_exact_match
            
        elif self.which_option in ["4", "FOUR", "NAME", "N"]:
            return self.find_by_name
            
        elif self.which_option in ["5", "FIVE",]:
            return self.del_or_edit
            
        elif self.which_option in ["6", "SIX", "QUIT", "Q"]:
            return "quit"
        else:
            print("{} was not an option.".format(self.which_option))
            print("")
            return False 

    def find_by_date(self):
        """can find an entry with a single date, or range of self.dates"""
        clear_screen()
        while True:
            self.date = self.get_input("Which date would you like to look at,"
                " ex: MM/DD/"
                "YYYY? Or you can find all self.dates including and between two"
                " self.dates, ex: MM/DD/YYYY - MM/DD/YYYY. Or Q to quit to the"
                " main screen.: ")
            self.between_answer = self.is_between_two(self.date)
            if self.between_answer == "quit":
                break 
            elif not self.between_answer:
                self.is_one_result = self.is_one_date(self.date)
                if not self.is_one_result:
                    print("")
                    print("{} is not an acceptable date.".format(self.date))
                    print("")
                    continue 
                else:
                    self.date_in_query, self.dates_to_print, 
                    self.date = self.is_one_result 
                    self.date_entries = main_2.Start_timesheet.select(
                        ).order_by(
                    main_2.Start_timesheet.date.desc()).where(
                    main_2.Start_timesheet.date.between(
                    self.date_in_query, self.date_in_query.replace(
                    hour=23, minute=59, second=59)) & (main_2.Start_timesheet.
                    username == self.username)) 
                    if not self.date_entries:
                        print("")
                        print("{} was not listed.".format(self.date))
                        print("")
                        continue 
                    else:
                        self.display_style(self.date_entries, 
                                        dates=self.dates_to_print)
                        self.del_or_edit()
                        break
            elif len(self.between_answer) == 3:
                self.date_one, self.date_two, 
                self.dates_to_print = self.between_answer
                #finds the self.dates that are in between the two 
                #entered self.dates.
                self.date_entries = main_2.Start_timesheet.select(
                ).order_by(main_2.Start_timesheet.date.desc(
                    )).where(main_2.Start_timesheet.date.between(self.date_one,
                 self.date_two.replace(hour=23, minute=59, second=59)) &
                  (main_2.Start_timesheet.username == self.username)) 
                #ex: datetime.datetime(2011, 1, 1)
                if len(self.date_entries) == 0:
                    print("{} was not listed.".format(self.date))
                    continue 
                elif len(self.date_entries) > 1:
                    self.multi_answer = self.is_multi_matches(self.date_entries,
                     self.date_one, self.date_two)
                    if self.multi_answer:
                        continue 
                    else: 
                        self.display_style(self.date_entries, 
                                        dates=self.dates_to_print)
                        self.del_or_edit()
                        break
                else:
                    self.display_style(self.date_entries, 
                                    dates=self.dates_to_print)
                    self.del_or_edit()
                    break
            #if user entered a single date, this option will be triggered
            
    def is_between_two(self, date):
        """checks to see if there are two dates to check between"""
        self.date = date 
        if self.date.strip().upper() in ["Q", "QUIT", "EXIT"]:
            return "quit"
            #if the user put a range of self.dates it will go into this option.
        elif re.search(r'[0-1][0-9]/[0-3][0-9]/[1-2][0-9]{3}\s?[-]\s?[0-1]'
                        '[0-9]/[0-3][0-9]/[1-2][0-9]{3}',self.date):
            self.date_one = re.search(r'([0-1][0-9]/[0-3][0-9]/[1-2]'
                                       '[0-9]{3})\s?[-]\s?',self.date)
            self.date_two = re.search(r'\s?[-]\s?([0-1][0-9]/[0-3][0-9]/'
                                       '[1-2][0-9]{3})', self.date)
            clear_screen() 
            self.dates_to_print = "Results for dates including and between"
            " {} - {}.".format(self.date_one.group(1), self.date_two.group(1))
            self.date_one = datetime.datetime.strptime(self.date_one.group(1),
                                                                 '%m/%d/%Y')
            self.date_two = datetime.datetime.strptime(self.date_two.group(1),
                                                                 '%m/%d/%Y')
            return (self.date_one, self.date_two, self.dates_to_print)
        else:
            return None 

    def is_one_date(self, date):
        """check to see if one date was entered"""
        self.date = date
        self.date = re.search(r'[0-1][0-9]/[0-3][0-9]/[1-2][0-9]{3}',self.date)
        if self.date:
            self.date = self.date.group()
            self.dates_to_print = "Results for the date {}.".format(
                                self.date)
            self.date_in_query = datetime.datetime.strptime(self.date,
                                                             '%m/%d/%Y')
            return self.date_in_query, self.dates_to_print, self.date  
        else:
            return False 
              
    def is_multi_matches(self, date_entries, date_one, date_two):
        """checks to see if there was many different dates between the dates"""
        self.date_entries = date_entries
        self.date_set = set()
        self.date_one = date_one
        self.date_two = date_two 
        for i in self.date_entries:
            self.date_set.add(i.date.strftime('%m/%d/%Y'))
        if len(self.date_set) > 1:
            print("")
            print("There are {} matches for the self.dates including and"
                " between '{} - {}'. Type in the MM/DD/YYYY of the one"
                " you want.".format(len(self.date_set), 
                    self.date_one.strftime('%m/%d/%Y'), 
                    self.date_two.strftime('%m/%d/%Y')))
            if self.is_multi_match_print(self.date_set):
                return True
        else:
            return False

    def is_multi_match_print(self, date_set):
        """prints out the multiple matches"""
        self.date_set = date_set
        print("")
        self.date_counter = 0
        for i in self.date_set:
            self.date_counter += 1
            print("{}) {}".format(self.date_counter, i))
            print("")
        return True  
        
    def find_by_time_spent(self):
        """can find an entry by the time spent"""
        while True:
            self.time_spent = self.get_input("Roughly what length of time did"
                " the task "
                "you are looking for take in minutes? Ex: 25. Or Q to quit to "
                "the main screen.: ").upper()
            self.find_ans = self.find_by_time_sp_error(self.time_spent)
            if self.find_ans == 1:
                break
            elif self.find_ans == 2:
                continue 
            if re.search(r'\d+', self.time_spent):
                #find all ones within 10 minutes of time spent
                self.time_spent_entries = main_2.Start_timesheet.select(
                    ).order_by(main_2.Start_timesheet.date.desc()).where(
                    main_2.Start_timesheet.time_spent.between(int(
                    self.time_spent)-10,int(self.time_spent)+10) & (
                    main_2.Start_timesheet.username == self.username))  
                if not self.time_spent_entries:
                    print("")
                    print("{} was not listed.".format(self.time_spent))
                    continue 
                else:
                    self.display_style(self.time_spent_entries)
                    self.del_or_edit()
                    break
    
    def find_by_time_sp_error(self, time_spent):
        """checks for an error entering time spent"""
        self.time_spent = time_spent 
        if self.time_spent in ["Q", "EXIT", "QUIT"]:
            return 1
        try:
            float(self.time_spent)
        except ValueError:
            print("{} is not a number.".format(self.time_spent))
            return 2
        else:
            return False 
                 
    def find_by_exact_match(self):
        """can enter a search keyword to find an entry"""
        while True:    
            self.task_name_search = self.get_input("What is the keyword/s you"
                " are looking"
                " for? Press Q to quit to the main screen: ").strip()
            if self.task_name_search.upper() in ["Q", "QUIT", "EXIT"]:
                return None 
            #find all ones has self.task_name_search in it
            self.find_by_exact = main_2.Start_timesheet.select().order_by(
            main_2.Start_timesheet.date.desc()).where((main_2.Start_timesheet.
            notes ** "%{}%".format(self.task_name_search)) | 
            (main_2.Start_timesheet.username ** "%{}%".
                format(self.task_name_search)) |
            (main_2.Start_timesheet.task_name ** "%{}%".
                format(self.task_name_search)) &
             (main_2.Start_timesheet.username == self.username))
            if not self.find_by_exact:
                print("There were no matches.")
            else:
                self.display_style(self.find_by_exact)
                break
        self.del_or_edit()
               
    def find_by_name(self):
        """can enter a regular expression to find an entry"""
        while True: 
            self.print_all_avail_names()
            print("")
            self.get_name = self.get_input("Enter the person's name. Press Q to"
                        " quit to the main screen: ")
            print("")
            if self.get_name.upper() in ["Q", "QUIT", "EXIT"]:
                return None
            #find all ones that have the same username as self.find_name
            self.find_name = main_2.Start_timesheet.select().order_by(main_2.
            Start_timesheet.date.desc()).where(main_2.Start_timesheet.
            username ** "%{}%".format(self.get_name)) 
            if not self.find_name:
                print("There were no matches.")
                continue 
            else:
                self.name_set = set()
                for i in self.find_name:
                    self.name_set.add(i.username)
                self.name_match_answer = self.name_matches(self.name_set, 
                    self.get_name)
                if self.name_match_answer == "1":
                    self.display_style(self.find_name)
                    break
                elif self.name_match_answer == "2":
                    self.get_name = self.get_input(": ")
                    self.find_name = main_2.Start_timesheet.select().order_by(
                        main_2.Start_timesheet.date.desc()).where(main_2.
                        Start_timesheet.username == self.get_name)
                    if not self.find_name:
                        print("There were no matches.")
                        continue 
                    else:
                        self.display_style(self.find_name)
                        break 
        self.del_or_edit()

    def name_matches(self, name_set, get_name):
        """checks to see if there are matching names to the one entered"""
        self.name_set = name_set
        self.get_name = get_name
        if len(self.name_set) == 1:
            return "1" 
        else:
            print("")
            print("There are {} matches for '{}'. Type in the full name"
                " of the correct one.".format(len(self.name_set), 
                    self.get_name))
            print("")
            self.counter = 0
            for i in self.name_set:
                self.counter += 1
                print("{}) {}".format(self.counter, i))
            return "2"
        
    def print_all_avail_names(self):  
        """prints the name matches"""  
        #prints out every name in the database
        self.all_names = main_2.Start_timesheet.select().order_by(
            main_2.Start_timesheet.username.desc())
        self.name_set = set()
        for i in self.all_names:
            self.name_set.add(i.username)
        self.name_num = 0
        for i in self.name_set:
            self.name_num += 1
            print("{}) {}".format(self.name_num, i))
    
    def del_or_edit(self):
        """gives the option to either delete or edit an entry"""
        while True:    
            print("")
            #asking the user explicitly for the task number of desired entry to 
            #edit or delete, then seeing if it exists in our list.
            self.current_task_num = self.get_input("Type in the task number of"
                " the entry"
                " if you want to edit or delete the entry. Or press Q to quit "
                "to main screen.: ").upper()
            self.del_err_ans = self.del_or_edit_err(self.current_task_num)
            if self.del_err_ans == 1:
                return None
            elif self.del_err_ans == 2:
                continue 
            else:
                try:
                    #find the row with the matching task number
                    self.current_row = main_2.Start_timesheet.get((main_2.
                    Start_timesheet.task_number == int(self.current_task_num)) &
                     (main_2.Start_timesheet.username == self.username)) 
                except DoesNotExist:
                    print("{} task number had no "
                        "matches.".format(self.current_task_num))
                    continue
                else:
                    self.username = self.current_row.username
                    self.task_name = self.current_row.task_name
                    self.time_spent = self.current_row.time_spent
                    self.notes = self.current_row.notes
                    self.date = self.current_row.date
                    self.task_number = self.current_row.task_number
                    self.display_simple() 
                    self.is_correct = self.get_input("Is this the correct entry"
                        " you were"
                        " looking for? Y for yes, N for no.: ").strip().upper()
                    if self.is_correct in ["NO", "N"]:
                        continue 
                    else:
                        break 
        while True:
            #User has enterd the task they want to edit/delete by this point,
            #and it has been confirmed the entry exists.
            print("")
            self.modify = self.get_input("Press E to edit entry, press D to "
                                "delete entry,"
                                " or press Q to quit to main screen: ")
            print("")
            self.modify =self.modify.strip().upper()
            if self.modify in ["Q", "QUIT"]:
                break 
            elif self.modify not in ["D", "DELETE", "E", "EDIT"]:
                print("{} was not an option.".format(self.modify))
                continue  
            #user has chosen the delete option.
            elif self.modify in ["D", "DELETE"]:
                #delete the row with the task number that matches 
                #"self.current_task_num"
                self.current_row.delete_instance() 
                print("")
                print("You have deleted the entry with the task number "
                    "{}.".format(self.current_task_num))
                self.get_input("Press enter to continue.")
                return None
            #user has chosen the edit option
            elif self.modify in ["E", "EDIT"]:
                self.how_to_edit = self.get_input("Press 1 to edit the date,"
                    " press 2 to "
                    "edit the task name, press 3 to edit the time spent, press "
                    "4 to edit the notes: ").strip().upper()
                #user has chosen to edit the date
                if self.how_to_edit in ["1", "ONE", "D", "DATE"]:
                    while True:   
                        print("The date currently reported is {}. What would you"
                            " like to change it to? (Must be in "
                            "MM/DD/YYYY HH:MM)".format(self.date))
                        self.changed_date = self.get_input(": ")
                        print("")
                        self.date = self.changed_date 
                        if self.is_acceptable(self.changed_date):
                            break
                        else:
                            print("{} is not an acceptable "
                                  "input.".format(self.changed_date))

                    #find the row with the same 
                    #"self.current_task_num" and change its date to 
                    #self.changed_date
                    self.current_row.date = datetime.datetime.strptime(self.
                    changed_date, '%m/%d/%Y %H:%M')
                    self.current_row.save()
                    print("")
                    self.display_simple()
                    self.get_input("This is the final result. Press enter to"
                        " continue.")
                    return None
                #user has chosen to edit the task name
                elif self.how_to_edit in ["2", "TWO", "TASK NAME", "TASK"]:
                    print("The task name currently reported is {}. What would "
                          "you like to change it to?".format(self.task_name))
                    changed_task = self.get_input(": ")
                    print("")
                    self.task_name = changed_task
                    #find the row with the same "self.current_task_num" 
                    #and change its task name to self.task_name
                    self.current_row.task_name = self.task_name 
                    self.current_row.save()
                    print("")
                    self.display_simple()
                    self.get_input("This is the final result. Press enter to"
                        " continue.")
                    return None
                #user has chosen to edit the time spent
                elif self.how_to_edit in ["3", "THREE", "TIME SPENT"]:
                    while True:
                        print("The time spent currently reported is {}. What "
                              "would you like to change it "
                              "to?".format(self.time_spent))
                        self.changed_time_spent = self.get_input(": ")
                        self.time_spent = self.changed_time_spent
                        try:
                            float(self.changed_time_spent)
                        except ValueError:
                            print("{} is not a "
                                "number.".format(self.changed_time_spent))
                        else:
                            break 
                    #find the row with the same "self.current_task_num" 
                    #and change its time to self.time_spent
                    self.current_row.time_spent = self.time_spent 
                    self.current_row.save()
                    self.display_simple()
                    self.get_input("This is the final result. Press enter to"
                        " continue.")
                    return None
                #user has chosen to edit the notes
                elif self.how_to_edit in ["4", "FOUR", "N", "NOTES"]:
                    print("The note currently reported is {}. What would you "
                        "like to change it to?".format(self.notes))
                    changed_notes = self.get_input(": ")
                    self.notes = changed_notes
                    #find the row with the same "self.current_task_num" 
                    #and change its notes to self.notes
                    self.current_row.notes = self.notes 
                    self.current_row.save() 
                    self.display_simple()
                    self.get_input("This is the final result. Press enter to"
                        " continue.")
                    print("")
                    return None
                #user did not give a valid option, and will go back over the
                #loop from the beginning
                else:
                    print("{} is not an acceptable "
                        "answer.".format(self.how_to_edit))
                    continue 
             
    def del_or_edit_err(self, current_task_num):
        """checks to see if current_task_num is legit"""
        self.current_task_num = current_task_num
        print("")
        if self.current_task_num in ["Q", "QUIT"]:
            return 1
        try:
            float(self.current_task_num)
        except ValueError:
            print("{} is not a number.".format(self.current_task_num))
            return 2 
        else:
            return 3

    def is_acceptable(self, changed_date):
        """checks to see if changed_date was entered correcty"""
        self.changed_date = changed_date
        if re.search(r'[0-1][0-9]/[0-3][0-9]/[1-2][0-9][0-9]'
            '[0-9]\s[0-2][0-9]:[0-5][0-9]',self.changed_date):
            return True
        else:
            return False    

    def dis_simp_print(self, date, username, task_name, time_spent, notes, 
        task_number):
        """prints out the simple print"""
        self.date = date
        self.username = username
        self.task_name = task_name
        self.time_spent = time_spent
        self.notes = notes
        self.task_number = task_number
        print("") 
        print("Date: {}".format(self.date))
        print("     Username: {}".format(self.username))
        print("     Task name: {}".format(self.task_name))
        print("     Time spent: {} minutes".format(self.time_spent))
        print("     Notes: {}".format(self.notes))
        print("     Task number: {}".format(self.task_number))
        print("")
        return True

    def display_simple(self):
        """displays the outcome of an edited entry"""
        if type(self.date) == datetime.datetime:
            self.date = self.date.strftime('%m/%d/%Y %H:%M')
        self.dis_simp_print(self.date, self.username, self.task_name, 
            self.time_spent, self.notes, self.task_number)
   
    def display_style(self, list, dates=None): 
        """takes in a list of matching entries, and displays them"""
        self.dates = dates 
        self.list = []
        for d in list:
            self.list.append(d)
        self.num = 0
        while True:
            i = self.list[self.num]
            clear_screen()
            if self.dates:
                print(self.dates)
            print("")
            print("Display match {}/{}".format(self.num + 1, len(self.list)))
            print("") 
            print("Date: {}".format(i.date.strftime('%m/%d/%Y %H:%M')))
            print("     Username: {}".format(i.username))
            print("     Task name: {}".format(i.task_name))
            print("     Time spent: {} minutes".format(i.time_spent))
            print("     Notes: {}".format(i.notes))
            print("     Task number: {}".format(i.task_number))
            print("")
            #works out the 'next, previous' portion to let the
            #user shuffle through matching entries one at a time.
            while True:
                if len(self.list) == 1:
                    print("")
                    self.get_input("Press any button to continue.: ").strip(
                        ).upper()
                    print("")
                    return None
                elif self.num + 1 == len(self.list):
                    print("")
                    self.which_category = 1
                    self.what_choice = self.get_input("Press P for previous"
                                            " match, L for"
                                            " the full list, or Q"
                                            " to quit to the main screen or edit"
                                            " an entry.: ").strip().upper()
                    self.disp_resp = self.disp_style_op(self.what_choice, 
                        self.num, self.dates, self.which_category)
                    if self.disp_resp in [1, 2]:
                        break
                    elif self.disp_resp == 3:
                        clear_screen()
                        if self.dates:
                            print(self.dates)
                        self.print_full_list(self.dates)
                        print("")
                        self.get_input("Press enter to quit to the main screen"
                            " or edit an entry")
                        print("")
                        return None 
                    elif self.disp_resp == 4:
                        return None 
                    elif self.disp_resp == 5:
                        print("{} was not an option.".format(self.what_choice))
                        continue 
                elif self.num == 0:
                    self.which_category = 2
                    print("")
                    self.what_choice = self.get_input("Press N for next match"
                                            ", L for the"
                                             " full list, or Q to"
                                             " quit to the main screen or edit"
                                             " an entry.: ").strip().upper()
                    print("")
                    self.disp_resp = self.disp_style_op(self.what_choice, 
                        self.num, self.dates, self.which_category)
                    if self.disp_resp in [1, 2]:
                        break
                    elif self.disp_resp == 3:
                        clear_screen()
                        if self.dates:
                            print(self.dates)
                        self.print_full_list(self.dates)
                        print("")
                        self.get_input("Press enter to quit to the main screen or edit"
                            " an entry")
                        print("")
                        return None 
                    elif self.disp_resp == 4:
                        return None 
                    elif self.disp_resp == 5:
                        print("{} was not an option.".format(self.what_choice))
                        continue 
                else:
                    self.which_category = 3
                    print("")
                    self.what_choice = self.get_input("Press N for next match,"
                        " P for"
                        " previous match, L for the full list, "
                        ",or Q to quit to the main screen or"
                        " edit an entry.: ").strip().upper()
                    self.disp_resp = self.disp_style_op(self.what_choice, 
                        self.num, self.dates, self.which_category)
                    if self.disp_resp in [1, 2]:
                        break
                    elif self.disp_resp == 3:
                        clear_screen()
                        if self.dates:
                            print(self.dates)
                        self.print_full_list(self.dates)
                        print("")
                        self.get_input("Press enter to quit to the main "
                            "screen or edit"
                            " an entry")
                        print("")
                        return None 
                    elif self.disp_resp == 4:
                        return None 
                    elif self.disp_resp == 5:
                        print("{} was not an option.".format(self.what_choice))
                        continue 

    def disp_style_op(self, what_choice, num, dates, which_category):
        """filters through to decide which options for navigating results"""
        self.what_choice = what_choice
        self.num = num
        self.which_category = which_category

        if self.which_category == 1:
            if self.what_choice in ["P", "PREVIOUS"]:
                self.num -= 1
                return 2
            elif self.what_choice in ["L", "LIST"]:
                return 3
            elif self.what_choice in ["Q", "QUIT"]:
                return 4
            else:
                return 5 
        elif self.which_category == 2:
            if self.what_choice in ["N", "NEXT"]:
                self.num += 1
                return 1 
            elif self.what_choice in ["L", "LIST"]:
                return 3
            elif self.what_choice in ["Q", "QUIT"]:
                return 4
            else:
                return 5 
        elif self.which_category == 3:
            if self.what_choice in ["N", "NEXT"]:
                self.num += 1
                return 1  
            elif self.what_choice in ["P", "PREVIOUS"]:
                self.num -= 1
                return 2 
            elif self.what_choice in ["L", "LIST"]:
                return 3
            elif self.what_choice in ["Q", "QUIT"]:
                return 4
            else:
                return 5

    def print_full_list(self, dates):
        """prints the full list"""
        for i in self.list:
            print("")
            print("Date: {}".format(i.date.strftime('%m/%d/%Y %H:%M')))
            print("     Username: {}".format(i.username))
            print("     Task name: {}".format(i.task_name))
            print("     Time spent: {} minutes".format(i.time_spent))
            print("     Notes: {}".format(i.notes))
            print("     Task number: {}".format(i.task_number))
            print("")

    def get_input(self, message):
        """returns input"""
        self.message = message
        return input(self.message)