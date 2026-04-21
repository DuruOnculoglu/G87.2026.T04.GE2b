"""Module """

import os
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
            raise EnterpriseManagementException("Input file not found")

        doc = ProjectDocument(file_path)

        return doc.document_signature
