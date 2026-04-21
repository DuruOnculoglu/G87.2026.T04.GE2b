"""Module """
import hashlib
import os
import json
import re

from datetime import datetime
from .enterprise_management_exception import EnterpriseManagementException
from .project_document import ProjectDocument


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    def register_document(self, file_path):
        if not os.path.exists(file_path):
            raise EnterpriseManagementException("Input file not found.")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except EnterpriseManagementException:
            raise EnterpriseManagementException("This file is not JSON formatted.")


        file_name = data.get("FILENAME")
        name_without_ext = os.path.splitext(file_name)[0]
        ext = os.path.splitext(file_name)[1]

        if not re.fullmatch(r"[A-Za-z0-9]{8}", name_without_ext):
            raise EnterpriseManagementException("JSON data has no valid values.")

        project_id = data.get("PROJECT_ID")
        if project_id is None:
            raise EnterpriseManagementException("JSON data has no valid values.")

        if not re.fullmatch(r"[0-9a-fA-F]{32}", project_id):
            raise EnterpriseManagementException("JSON data has no valid values.")

        if ext not in [".pdf", ".docx", ".xlsx"]:
            raise EnterpriseManagementException("JSON data has no valid values.")

        if "PROJECT_ID" not in data or "FILENAME" not in data:
            raise EnterpriseManagementException("JSON does not have the expected structure.")

        if not isinstance(project_id, str) or not isinstance(file_name, str):
            raise EnterpriseManagementException("JSON does not have the expected structure.")


        # expected_md5 = hashlib.md5(name_without_ext.encode()).hexdigest()
        # if project_id != expected_md5:
        #     raise EnterpriseManagementException("Invalid project ID")

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
                    documents = []  # corrupted file → start fresh
        else:
            documents = []

        documents.append(project.to_json())

        # Save back to file
        with open(storage_file, "w", encoding="utf-8") as f:
            json.dump(documents, f, indent=4)

        return project.document_signature
