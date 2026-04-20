"""class for testing the regsiter_order method"""
import unittest
import os
import json

from openpyxl import load_workbook

from uc3m_consulting import EnterpriseManager, EnterpriseManagementException


def create_temp_json(file_name, content):
    file_path = os.path.join("/tmp", file_name)

    content = json.loads(content)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)

    return file_path


class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""
    def test_something( self ):
        """dummy test"""
        self.assertEqual(True, False)

    def test_valid_cases_from_excel(self):

        excel_file = "docs/Syntax Analysis Tree.pdf"

        wb = load_workbook(excel_file)
        sheet = wb.active

        headers = [cell.value for cell in sheet[1]]

        mngr = EnterpriseManager()

        for row in sheet.iter_rows(min_row=2, values_only=True):

            row_dict = dict(zip(headers, row))

            test_id = row_dict["ID TEST"]
            test_type = row_dict["TYPE (DUPLICATION / DELETION / MODIFICATION / VALID)"]
            file_path = create_temp_json(
                row_dict["FILE PATH"],
                row_dict["FILE CONTENT"])
            expected = row_dict["EXPECTED RESULT"]

            # Only run VALID cases (same idea as your CSV example)
            if test_type == "VALID":
                with self.subTest(test_id=test_id):
                    result = mngr.register_document(file_path)
                    self.assertEqual(expected, result)

        def test_valid_cases_from_excel(self):

            excel_file = "docs/Syntax Analysis Tree.pdf"

            wb = load_workbook(excel_file)
            sheet = wb.active

            headers = [cell.value for cell in sheet[1]]

            mngr = EnterpriseManager()

            for row in sheet.iter_rows(min_row=2, values_only=True):

                row_dict = dict(zip(headers, row))

                test_id = row_dict["ID TEST"]
                test_type = row_dict["TYPE (DUPLICATION / DELETION / MODIFICATION / VALID)"]
                file_path = create_temp_json(
                    row_dict["FILE PATH"],
                    row_dict["FILE CONTENT"])
                expected = row_dict["EXPECTED RESULT"]

                # Only run VALID cases (same idea as your CSV example)
                if test_type == "VALID":
                    with self.subTest(test_id=test_id):
                        result = mngr.register_document(file_path)
                        self.assertEqual(expected, result)

        def test_invalid_cases_from_excel(self):

            excel_file = "docs/Syntax Analysis Tree.pdf"

            wb = load_workbook(excel_file)
            sheet = wb.active

            headers = [cell.value for cell in sheet[1]]

            mngr = EnterpriseManager()

            for row in sheet.iter_rows(min_row=2, values_only=True):

                row_dict = dict(zip(headers, row))

                test_id = row_dict["ID TEST"]

                content = row_dict["FILE CONTENT"]
                if isinstance(content, str):
                    content = json.loads(content)

                file_path = create_temp_json(row_dict["FILE PATH"], content)

                expected_message = row_dict["EXPECTED RESULT"]

                with self.subTest(test_id=test_id):

                    with self.assertRaises(EnterpriseManagementException) as context:
                        mngr.register_document(file_path)

                    actual_message = str(context.exception)

                    self.assertEqual(expected_message, actual_message)

if __name__ == '__main__':
    unittest.main()
