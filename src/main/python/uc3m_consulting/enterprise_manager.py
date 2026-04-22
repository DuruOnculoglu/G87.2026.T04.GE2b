"""Module """
import hashlib
import os
import json
import re

from datetime import datetime
from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject
from .project_document import ProjectDocument


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self, company_cif: str, project_achronym: str, project_description: str,
                         department: str, date: str, budget: float):
        """ This method registers a new enterprise project based on the required inputs and is
        added into a JSON File for reference"""
        # CIF Check
        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("Invalid Company Cif")
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("Invalid Company Cif")

        # Project_acronym Check
        if not isinstance(project_achronym, str):
            raise EnterpriseManagementException("Invalid Project Acronym")
        if not 5 <= len(project_achronym) <= 10:
            raise EnterpriseManagementException("Invalid Project Acronym")

        # isalnum() checks for a-z, A-Z, 0-9
        if not project_achronym.isalnum():
            raise EnterpriseManagementException("Invalid Project Acronym Characters")

        # Project_description check
        if not isinstance(project_description, str):
            raise EnterpriseManagementException("Invalid Project Description")
        if not 10 <= len(project_description) <= 30:
            raise EnterpriseManagementException("Invalid Project Description Length")

        # department check
        if not isinstance(department, str):
            raise EnterpriseManagementException("Invalid Department")
        if department not in ("HR", "Finance", "Legal", "Logistics"):
            raise EnterpriseManagementException("Invalid Department")

        # date check
        if not isinstance(date, str):
            raise EnterpriseManagementException("Invalid Date")
        try:
            date_valid = datetime.strptime(date, "%d/%m/%Y").date()
            year = date_valid.year

            if date_valid < datetime.today().date():
                raise ValueError
            if not 2025 <= year <= 2027:
                raise ValueError
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid Date") from exc

        # budget check
        try:
            if not isinstance(budget, float):
                raise ValueError

            s = f"{budget:.2f}"
            if '.' not in s or len(s.split('.')[1]) != 2:
                raise ValueError("Invalid Budget")

            if not 50000.00 <= budget <= 1000000.00:
                raise ValueError

        except ValueError as exc:
            raise EnterpriseManagementException("Invalid Budget") from exc

        storage_file = "corporate_operations.json"

        if os.path.exists(storage_file):
            with open(storage_file, "r", encoding="utf-8") as file:
                try:
                    projects = json.load(file)
                    if not isinstance(projects, list):
                        projects = []
                except Exception:
                    projects = []
        else:
            projects = []

        for p in projects:
            if p.get("company_cif") == company_cif and p.get("project_achronym") == project_achronym:
                raise EnterpriseManagementException("Project already exists for this CIF")

        obj_project = EnterpriseProject(company_cif, project_achronym, project_description,
                                       department, date, budget)
        try:
            project_id = obj_project.project_id
        except Exception as exc:
            raise EnterpriseManagementException("MD5 String Error") from exc

        projects.append(obj_project.to_json())

        try:
            with open(storage_file, "w", encoding="utf-8") as file:
                json.dump(projects, file, indent=4)
        except OSError as exc:
            raise EnterpriseManagementException("Error Writing to JSON File") from exc

        return project_id

    def register_document(self, file_path):
        if not os.path.exists(file_path):
            raise EnterpriseManagementException("Input file not found.")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            raise EnterpriseManagementException("This file is not JSON formatted.")


        if not isinstance(data, dict):
            raise EnterpriseManagementException("JSON does not have the expected structure.")

        if "PROJECT_ID" not in data or "FILENAME" not in data:
            raise EnterpriseManagementException("JSON does not have the expected structure.")

        project_id = data["PROJECT_ID"]
        file_name = data["FILENAME"]

        if not isinstance(project_id, str) or not isinstance(file_name, str):
            raise EnterpriseManagementException("JSON does not have the expected structure.")

        name_without_ext = os.path.splitext(file_name)[0]
        ext = os.path.splitext(file_name)[1]

        if not re.fullmatch(r"[A-Za-z0-9]{8}", name_without_ext):
            raise EnterpriseManagementException("JSON data has no valid values.")
        if not re.fullmatch(r"[0-9a-fA-F]{32}", project_id):
            raise EnterpriseManagementException("JSON data has no valid values.")
        if ext not in [".pdf", ".docx", ".xlsx"]:
            raise EnterpriseManagementException("JSON data has no valid values.")

        # Validate PROJECT_ID exists in registered projects
        corp_file = "corporate_operations.json"
        if not os.path.exists(corp_file):
            raise EnterpriseManagementException("JSON data has no valid values.")

        with open(corp_file, "r", encoding="utf-8") as f:
            try:
                projects = json.load(f)
                if not isinstance(projects, list):
                    projects = []
            except Exception:
                raise EnterpriseManagementException("JSON data has no valid values.")

        if not any(p.get("project_id") == project_id for p in projects):
            raise EnterpriseManagementException("JSON data has no valid values.")

        try:
            project = ProjectDocument(project_id, file_name)
        except Exception:
            raise EnterpriseManagementException(
                "Internal processing error when getting the file_signature.")

        # Storage file path
        storage_file = "src/main/python/uc3m_consulting/" + "all_documents.json"

        # Load existing documents if file exists
        if os.path.exists(storage_file):
            with open(storage_file, "r", encoding="utf-8") as f:
                try:
                    documents = json.load(f)
                except Exception:
                    documents = []
        else:
            documents = []

        documents.append(project.to_json())

        # Save back to file
        with open(storage_file, "w", encoding="utf-8") as f:
            json.dump(documents, f, indent=4)

        return project.document_signature

    @staticmethod
    def validate_cif(cif: str):
        """RETURNS TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE OTHERWISE"""

        control_map = {0: "J", 1: "A", 2: "B", 3: "C", 4: "D",
                       5: "E", 6: "F", 7: "G", 8: "H", 9: "I"}
        letter_val = cif[0]
        step_one = int(cif[2]) + int(cif[4]) + int(cif[6])
        step_two = 0

        for j in range(1, 9, 2):
            num = int(cif[j]) * 2
            if num > 9:
                num = (num % 10) + (num // 10)
            step_two += num

        step_sum = step_one + step_two
        unit = step_sum % 10
        base_digit = 0 if unit == 0 else 10 - unit

        if letter_val in ["A", "B", "E", "H"]:
            control_char = base_digit
        elif letter_val in ["K", "P", "Q", "S"]:
            control_char = control_map[base_digit]
        else:
            return False
        # NESTED IF_ELSE AUTOMATICALLY CHECKS IF FIRST CHAR IS LETTER

        if not len(cif) == 9:
            return False

        return str(control_char) == cif[8]
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE OTHERWISE

