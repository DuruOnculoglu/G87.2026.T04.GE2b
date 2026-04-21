"""class for testing the register_order method"""
import unittest
from datetime import datetime

from freezegun import freeze_time
from uc3m_consulting import EnterpriseManager
from uc3m_consulting import EnterpriseManagementException


class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""

    @freeze_time("2026/01/01")
    def test_tc1(self):
        """ VALID CASE 1 """
        manager = EnterpriseManager()
        obj = manager.register_project("A58818501","PRO01", "valid text",
        "HR", "01/01/2027", 50000.00)
        self.assertIsInstance(obj, str, "return should be string")
        self.assertEqual(len(obj), 32, "should be length of 32")
        self.assertTrue(obj.isalnum(), "should not have special characters")
        self.assertTrue(obj, "27e6024bf39af523a08276bfea060e5b")

    def test_tc2(self):
        """ VALID CASE 2 """
        manager = EnterpriseManager()
        obj = manager.register_project("A58818501","890478", "valid texts",
        "Finance", str(datetime.today().strftime("%d/%m/%Y")), 50000.01)
        self.assertIsInstance(obj, str, "return should be string")
        self.assertEqual(len(obj), 32, "should be length of 32")
        self.assertTrue(obj.isalnum(), "should not have special characters")
        self.assertTrue(obj,"c75640be4868e346b517e77411015119")

    def test_tc3(self):
        """ VALID CASE 3 """
        manager = EnterpriseManager()
        obj = manager.register_project("A58818501","PR0000002", "valid textvalid textvalid tex",
        "Legal", "31/12/2027", 999999.99)
        self.assertIsInstance(obj, str, "return should be string")
        self.assertEqual(len(obj), 32, "should be length of 32")
        self.assertTrue(obj.isalnum(), "should not have special characters")
        self.assertTrue(obj, "e08189f040ea53ad816137a5f44d20a0")


    def test_tc4(self):
        """" VALID CASE 4 """
        manager = EnterpriseManager()
        obj = manager.register_project("A58818501","PRCF538FG0", "valid textvalid textvalid text",
        "Logistics", "31/12/2026", 1000000.00)
        self.assertIsInstance(obj, str, "return should be string")
        self.assertEqual(len(obj), 32, "should be length of 32")
        self.assertTrue(obj.isalnum(), "should not have special characters")
        self.assertTrue(obj, "78de716662805a591a789e4c940d51d7")

    # INVALID TEST CASES
    # ECNV5
    def test_tc5(self):
        """" INVALID CIF """
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project, 123456789,
                          "PR001", "valid texts", "HR", "1/1/2027", 50000.00)

    # ECNV3, BLNV1
    def test_tc6(self):
        """" INVALID CIF : CIF_length = 8 """
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project,"A5881850",
                          "PR0000002", "valid texts", "Legal", "31/12/2026", 75000.00)

    # ECNV4, BLNV2
    def test_tc7(self):
        """" INVALID CIF : CIF_length = 10 """
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project,"A588185010",
                          "PR001", "valid texts", "Legal", "31/12/2026", 75000.00)

    # ECNV5
    def test_tc8(self):
        """" INVALID CIF : First char is not a letter"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException,manager.register_project,"158818501",
                          "PR001", "valid texts", "Legal", "31/12/2026", 50000.00)

    #ECNV6
    def test_tc9(self):
        """" INVALID PROJECT_ACHRONYM: DATATYPE (INT)"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException,manager.register_project,"A58818501",
                          123456, "valid texts", "HR", "31/12/2026", 50000.00)

    # ECNV7, BLNV3
    def test_tc10(self):
        """" INVALID PROJECT_ACHRONYM: length = 4"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException,manager.register_project,"A58818501",
                          "PR07", "valid texts", "HR", "31/12/2026", 50000.00)

    # ECNV8, BLNV4
    def test_tc11(self):
        """" INVALID PROJECT_ACHRONYM: length = 11"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project,"A58818501",
                          "PRCF538FG07", "valid texts", "HR", "31/12/2026", 50000.00)

    #ECNV9
    def test_tc12(self):
        """" INVALID PROJECT_ACHRONYM: has characters other than specified"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project,"A58818501",
                          "PR_F538FG0", "valid texts",
                                       "Logistics", "1/1/2027", 50000.00)

    #ECNV10
    def test_tc13(self):
        """" INVALID PROJECT_DESCRIPTION: DATA_TYPE"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project,"A58818501",
                          "PR001", 12345678976, "Logistics", "1/1/2027", 50000.00)

    #ECNV11, BLNV5
    def test_tc14(self):
        """" INVALID PROJECT_DESCRIPTION: char length (length < 10) (BVNV = 9)"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project,"A58818501",
                          "PR001", "not valid", "HR", "31/12/2026", 50000.00)

    #ECNV12, BLNV6
    def test_tc15(self):
        """" INVALID PROJECT_DESCRIPTION: char length (length > 30) (BVNV = 31)"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project,"A58818501",
                          "PR001", "Real-time neural signal systems", "HR", "31/12/2026", 50000.00)

    #ECNV13
    def test_tc16(self):
        """" INVALID DEPARTMENT: TYPE"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project,"A58818501",
                          "PR001", "valid texts", 13579 , "31/12/2026", 50000.00)

    #ECNV14
    def test_tc17(self):
        """" INVALID DEPARTMENT: WRONG VALUE"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project,"A58818501",
                          "PR001", "valid texts", "Communications" , "1/1/2027", 50000.00)

    # ECNV15
    def test_tc18(self):
        """" INVALID DATE: DATA_TYPE"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project, "A58818501",
                          "PR001", "valid texts", "HR", 12122025, 50000.00)

    # ECNV16
    def test_tc19(self):
        """" INVALID DATE: Invalid format for the date"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project, "A58818501",
                          "PR001", "valid texts", "Logistics", "10/14/2025", 50000.00)

    # ECNV17 - BLNV7
    def test_tc20(self):
        """" INVALID DATE: Invalid year value (year < 2025)"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project, "A58818501",
                          "PR001", "valid texts", "HR", "1/1/2024", 50000.00)

    # ECNV18 - BLNV8
    def test_tc21(self):
        """" INVALID DATE: Invalid year value (year > 2027)"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project, "A58818501",
                          "PR001", "valid texts", "Finance", "12/12/2028", 50000.00)

    # ECNV19
    def test_tc22(self):
        """" INVALID BUDGET_TYPE"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project, "A58818501",
                          "PR001", "valid texts", "Legal", "12/12/2026", "50000.50")

    # ECNV20-BLNV9
    def test_tc23(self):
        """" INVALID BUDGET: Invalid budget value - budget value < 50000.00"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project, "A58818501",
                          "PR001", "valid texts", "Logistics", "31/12/2026", 49999.99)

    # ECNV21-BLNV10
    def test_tc24(self):
        """" INVALID BUDGET: Invalid budget value - budget value > 100000.00 """
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project, "A58818501",
                          "PR001", "valid texts", "Logistics", "31/12/2026", 1000000.01)

    # ECNV19
    def test_tc25(self):
        """" INVALID BUDGET: Invalid budget value - one decimal value"""
        manager = EnterpriseManager()
        self.assertRaises(EnterpriseManagementException, manager.register_project, "A58818501",
                              "PR001", "valid texts", "Logistics", "31/12/2026", 1000000.1)

    # ECNV22
    # @patch("uc3m_consulting.enterprise_project.hashlib.md5")
    # def test_tc26(self, mock_md5):
    #     """" INVALID OUTPUT: String not returned through MD5"""
    #     mock_md5.side_effect = Exception("MD5 failure")
    #
    #     manager = EnterpriseManager()
    #
    #     with self.assertRaises(EnterpriseManagementException):
    #         manager.register_project("A58818501", "PRO01", "valid texts",
    #                                  "HR", "31/12/2026", 50000.00)
    #
    # # ECNV23
    # @patch("builtins.open")
    # def test_tc27(self, mock_open):
    #     """" INVALID OUTPUT: Data not saved in JSON File"""
    #     mock_open.side_effect = OSError("JSON Write Error")
    #
    #     manager = EnterpriseManager()
    #
    #     with self.assertRaises(EnterpriseManagementException):
    #         manager.register_project("A58818501", "PRO01", "valid texts",
    #                                    "Finance", "31/12/2026", 50000.00)

if __name__ == '__main__':
    unittest.main()
