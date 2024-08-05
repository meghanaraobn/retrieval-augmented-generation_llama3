import fitz
from llama_index import Document

class IndexManager:
    def __init__(self, index_service_context_loader):
        """
        Initialize the IndexManager with IndexServiceContextLoader.
        """
        self.index_service_context_loader = index_service_context_loader

    def extract_text_from_document(self, document_path):
        """
        Extract entire text from the document.

        Args:
            document_path (str): The path of the document.
        
        Returns:
            text (str): Entire document text.
        """
        text = ""
        document = fitz.open(document_path)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text() 
        return text
    
    def create_document_index(self, document_path):
        """
        Create an index for a given document.

        Args:
            document_path (str): The path of the document to be indexed.
        """
        try:
            # Extract text from the document
            document_text = self.extract_text_from_document(document_path)
            # Create a Document instance
            li_document = Document(text=document_text, metadata={"file_path": document_path})
            # Create index
            self.index_service_context_loader.create_index(li_document)

        except Exception as e:
            raise RuntimeError(f"Failed to create document index: {e}")

    def delete_document_index(self, ref_document_id):
        """
        Delete an index for a given document

        Args:
            ref_doc_id (str): Reference document id of the document to be removed from index.
        """
        try:
            # Delete index
            self.index_service_context_loader.delete_index(ref_document_id)
        except Exception as e:
            raise RuntimeError(f"Failed to delete document index: {e}")
