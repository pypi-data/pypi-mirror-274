"""Testing the module with the python internal unittest module."""

import unittest

from addimportdir import importdir,removedir

importdir()

import src.pycutroh as pycutroh

testlist = ["Carplot;Highway;17:25;03.11.2021",
            "17:25;01.08.2022;Admin;WS19Srv",
            "17:30;01.08.2022;Administrator;WS16Srv;41589",
            "PowerShellisthebest",
            "PowerShell is the best cli to manage all kinds of servers.",
            "Everything      we want     is PowerShell!",
            "421943194948i12948348913",
            "fadsfafjaeifjadjfaiefiaf",
            "_:;)=(/()=?[]}}\¬}{][",
            "IT-administrators@github.com"]

def check_list_len(testlist: list, reslist: list):
    if len(testlist) != len(reslist):
        raise Exception("Testlist and result list need the same length.")

# Testing prerequistes
class TestPrerequistes(unittest.TestCase):
    def setUp(self) -> None:
        self.testlist = testlist

    def test_testlist_len_not_null(self):
        if len(testlist) == 0:
            raise Exception("No tests in testlist.")

# Testing helper functions
class TestPycutrohHelperFunctions(unittest.TestCase):
    def setUp(self):
        self.content = "This is a demonstration string."

    def test_pos_handling(self):
        self.assertEqual(pycutroh._pos_handling(1), 0)
        self.assertEqual(pycutroh._pos_handling(0), 0)
        self.assertEqual(pycutroh._pos_handling(2), 1)
    
    def test_remove_leading_separator(self):
        self.assertEqual(pycutroh._remove_leading_separator(self.content, self.content[0]), self.content[1:])

    def test_replace_separator(self):
        self.assertEqual(pycutroh._replace_separator(self.content, " ", "|"), self.content.replace(" ", "|"))

    def test_calc_separator_pos(self):
        self.assertEqual(pycutroh._calc_separator_pos(self.content," "),[0,4,7,9,23,len(self.content)])
        teststring1 = "19.10.2023"
        self.assertEqual(pycutroh._calc_separator_pos(teststring1,"."),[0,2,5,len(teststring1)])

    def test_calc_fields(self):
        self.assertEqual(pycutroh._calc_fields((0,3),[0,4,7,9,23,len(self.content)]),[(0,4),(9,14)])
        teststring1 = "19.10.2023"
        self.assertEqual(pycutroh._calc_fields((0,2),[0,2,5,len(teststring1)]),[(0,2),(5,len(teststring1) -5 )])

# Testing the main functions. 
class TestPycutrohMainFunctions(unittest.TestCase):
    def setUp(self):
        self.content = "This is a demonstration string."
        self.testlist = testlist

    def test_get_letter_on_pos(self):
        self.reslist = ["C","1","1","P","P","E","4","f","_","I"]
        self.pos = 0
        # Check if lists have equal length if not break.
        check_list_len(self.testlist, self.reslist)
        self.assertEqual(pycutroh.get_letter_on_pos(self.content, self.pos), "T")
        # Test list of values against startlist.
        for i in range(len(self.testlist)):
            self.assertEqual(pycutroh.get_letter_on_pos(self.testlist[i], self.pos), self.reslist[i])
    
    def test_get_letters_from_pos_to_pos(self):
        self.assertEqual(pycutroh.get_letters_from_pos_to_pos(self.content, (0, 25)), self.content[0:25])
        self.assertEqual(pycutroh.get_letters_from_pos_to_pos(self.content, (0, 9)), self.content[0:9])
        self.assertEqual(pycutroh.get_letters_from_pos_to_pos(self.content, (0, 10)), self.content[0:10])
        self.assertEqual(pycutroh.get_letters_from_pos_to_pos(self.content, (0, 20)), self.content[0:20])

    def test_get_fields(self):
        self.assertEqual(pycutroh.get_fields(self.content, (0, 3), " "),"This demonstration")
        self.assertEqual(pycutroh.get_fields(self.content, (0, 3, 1, 2, 4), " "),"This demonstration is a string.")

    def test_get_fields_new_separator(self):
        self.assertEqual(pycutroh.get_fields_new_separator(self.content, (0, 3), " ", "|"),"This|demonstration")
        self.assertEqual(pycutroh.get_fields_new_separator(self.content,(0,3,1,2,4)," ","|"),"This|demonstration|is|a|string.")
        # Specifiying just one field is currently not supported. 
        # self.assertEqual(pycutroh.get_fields_new_separator(self.content,(0,)," ","|"),"This|")
    
    def test_get_letters_before_sign(self):
        self.reslist = ["Carplot",
            "17:25",
            "17:30;01.08.2022;Administrator;",
            "Power",
            "PowerShell",
            "Everything      we want     is PowerShell",
            "421",
            "fadsfaf",
            "_:;",
            "IT-administrators"]
        self.signs = [";", ";", "WS16Srv", "S", " ", "!", "9", "j", ")", "@"]
        self.assertEqual(pycutroh.get_letters_before_sign(self.content, " "), "This")
        # Test list of values against startlist.
        for i in range(len(self.testlist)):
            self.assertEqual(pycutroh.get_letters_before_sign(self.testlist[i], self.signs[i]), self.reslist[i])

    def test_get_letters_after_sign(self):
            self.reslist = ["Highway;17:25;03.11.2021",
            "01.08.2022;Admin;WS19Srv",
            "S16Srv;41589",
            "hellisthebest",
            "is the best cli to manage all kinds of servers.",
            "",
            "43194948i12948348913",
            "aeifjadjfaiefiaf",
            "=(/()=?[]}}\¬}{][",
            "github.com"]
            check_list_len(self.testlist, self.reslist)
            self.signs = [";", ";", "W", "S", " ", "!", "9", "j", ")", "@"]
            self.assertEqual(pycutroh.get_letters_after_sign(self.content, " "), "is a demonstration string.")
            with self.assertRaises(ValueError):
                pycutroh.get_letters_after_sign(self.content, "This")
            # Test list of values against startlist.
            for i in range(len(self.testlist)):
                self.assertEqual(pycutroh.get_letters_after_sign(self.testlist[i], self.signs[i]), self.reslist[i])

    def test_get_letters_between_signs(self):
        self.reslist = ["arplot",
            "01.08.2022",
            "",
            "ower",
            "is",
            "verything      we want     is PowerShell",
            "431",
            "aeif",
            "",
            "administrators"]
        check_list_len(self.testlist, self.reslist)
        self.signlist = [("C", ";"), (";", ";"), ("A", ";"), ("P", "S"), (" ", " "), ("E", "!"), ("9", "9"), ("j", "j"), ("[","]"), ("-","@")]
        self.assertEqual(pycutroh.get_letters_between_signs(self.content, " ", " "), "is")
        self.assertEqual(pycutroh.get_letters_between_signs(self.content, "T", " "), "his")
        with self.assertRaises(ValueError):
            pycutroh.get_letters_between_signs(self.content, "This", " ")
        # Test list of values against startlist.
        for i in range(len(self.testlist)):
            self.assertEqual(pycutroh.get_letters_between_signs(self.testlist[i], self.signlist[i][0], self.signlist[i][1]), self.reslist[i])

if __name__ == '__main__':
    # Verbose unittests.
    unittest.main(verbosity=2)
    removedir()