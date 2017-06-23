
#******when running this test, if it pauses just press enter until it finishes******


import unittest
import main_2
import make_new_2
import look_up_2 
import datetime

#can't do main_2.Start.run 

class StartTest(unittest.TestCase):
	def setUp(self):
		self.username = "Chris"
	def test_pick_one(self):
		self.assertTrue(main_2.Start().pick_one("1", "Chris"))
		self.assertTrue(main_2.Start().pick_one("2", "Chris"))
		self.assertEqual(main_2.Start().pick_one("3", "Chris"), exit)

	def test_to_continue(self):
		self.assertTrue(main_2.Start().to_continue("N"))
		self.assertFalse(main_2.Start().to_continue("Y"))

	def test_get_input(self):
		self.assertFalse(main_2.Start().get_input("N"))





class NewEntryTest(unittest.TestCase):
	def setUp(self):
		self.date = datetime.datetime.now()
		self.date_string = self.date.strftime('%m/%d/%Y %H:%M')
		self.username = "Chris"
		self.task_name = "Working on paperwork."
		self.time_spent = "25"
		self.notes = "Everything went well."
		#******you may have to change the task number to get it to work
		self.task_number = 5

	def test_if_error(self):
		self.assertTrue(make_new_2.NewEntry(self.username).if_error(3))
		self.assertFalse(make_new_2.NewEntry(self.username).if_error("a"))

	def test_if_error_2(self):
		self.assertTrue(make_new_2.NewEntry(self.username).if_error_2("alsdkjf",3))
		self.assertFalse(make_new_2.NewEntry(self.username).if_error_2("aalkdj"))

	def test_print_result(self):
		self.assertTrue(make_new_2.NewEntry(self.username).print_result(
			self.date_string, self.username, self.task_name, self.time_spent,
			self.notes, self.task_number))

	def test_get_input(self):
		self.assertFalse(make_new_2.NewEntry("Chris").get_input("N"))

	

class LookupEntryTest(unittest.TestCase):
	def setUp(self):
		self.date = datetime.datetime.now()
		self.date_string = self.date.strftime('%m/%d/%Y %H:%M')
		self.username = "Chris"
		self.task_name = "Working on paperwork."
		self.time_spent = "25"
		self.notes = "Everything went well."
		#******you may have to change the task number to get it to work
		self.task_number = 5

	def test_look_beg_print(self):
		self.assertTrue(look_up_2.LookupEntry("Chris").look_beg_print())

	def test_which_return(self):
		self.assertTrue(look_up_2.LookupEntry("Chris").which_return("1"))
		self.assertTrue(look_up_2.LookupEntry("Chris").which_return("2"))
		self.assertTrue(look_up_2.LookupEntry("Chris").which_return("3"))
		self.assertTrue(look_up_2.LookupEntry("Chris").which_return("4"))
		self.assertTrue(look_up_2.LookupEntry("Chris").which_return("5"))
		self.assertTrue(look_up_2.LookupEntry("Chris").which_return("6"))
		self.assertFalse(look_up_2.LookupEntry("Chris").which_return("7"))

	def test_is_between_two(self):
		self.assertEqual(look_up_2.LookupEntry("Chris").is_between_two("q"), "quit")
		self.assertTrue(look_up_2.LookupEntry("Chris").is_between_two("01/01/1990-01/01/2020"))
		self.assertFalse(look_up_2.LookupEntry("Chris").is_between_two("11/3/2017"))

	def test_is_multi_match_print(self):
		self.assertTrue(look_up_2.LookupEntry("Chris").is_multi_match_print(["d1", "d2"]))
		
	def test_find_by_time_sp_error(self):
		self.assertTrue(look_up_2.LookupEntry("Chris").find_by_time_sp_error("Q"))
		self.assertFalse(look_up_2.LookupEntry("Chris").find_by_time_sp_error(2))
		self.assertTrue(look_up_2.LookupEntry("Chris").find_by_time_sp_error("A"))

	def test_name_matches(self):
		self.assertEqual(look_up_2.LookupEntry("Chris").name_matches(["n1", "n2"], "Joel"), "2")
		self.assertEqual(look_up_2.LookupEntry("Chris").name_matches(["n1"], "Joe"), "1")

	def test_del_or_edit_err(self):
		self.assertEqual(look_up_2.LookupEntry("Chris").del_or_edit_err("Q"), 1)
		self.assertEqual(look_up_2.LookupEntry("Chris").del_or_edit_err("A"), 2)
		self.assertEqual(look_up_2.LookupEntry("Chris").del_or_edit_err(2), 3)



	def test_is_one_date(self):
		self.assertEqual(look_up_2.LookupEntry("Chris").is_one_date("01/01/1990"), 
			(datetime.datetime(1990, 1, 1, 0, 0), 'Results for the date 01/01/1990.',
			 '01/01/1990'))
		self.assertFalse(look_up_2.LookupEntry("Chris").is_one_date("1/03/1990"))

	def test_del_or_edit(self):
		self.assertTrue(look_up_2.LookupEntry("Chris").is_acceptable("01/01/1990 01:01"))
		self.assertFalse(look_up_2.LookupEntry("Chris").is_acceptable("01/01/199 01:01"))

	def test_display_simp_print(self):
		self.assertTrue(look_up_2.LookupEntry("Chris").dis_simp_print("1", "2", "3", "4", "5", "6"))
		
	def test_disp_style_op(self):
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("P", 2, "d1", 1), 2)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("L", 2, "d1", 1), 3)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("Q", 2, "d1", 1), 4)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("Z", 2, "d1", 1), 5)

		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("N", 2, "d1", 2), 1)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("L", 2, ["d1", "d2", "d3"], 2), 3)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("Q", 2, ["d1", "d2", "d3"], 2), 4)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("Z", 2, ["d1", "d2", "d3"], 2), 5)

		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("N", 2, ["d1", "d2", "d3"], 3), 1)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("P", 2, ["d1", "d2", "d3"], 3), 2)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("L", 2, ["d1", "d2", "d3"], 3), 3)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("Q", 2, ["d1", "d2", "d3"], 3), 4)
		self.assertEqual(look_up_2.LookupEntry("Chris").disp_style_op("Z", 2, ["d1", "d2", "d3"], 3), 5)

	def test_get_input(self):
		self.assertFalse(look_up_2.LookupEntry("Chris").get_input("N"))





if __name__ == '__main__':
	unittest.main()