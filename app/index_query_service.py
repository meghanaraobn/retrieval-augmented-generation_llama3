from app.scripts.extract_citations import CitationsExtractor

class IndexQueryService:
    def __init__(self, index_service_context_loader):
        """
        Initialize the IndexQueryService with an IndexServiceContextLoader and CitationsExtractor.
        """
        self.index_service_context_loader = index_service_context_loader
        self.citations_extractor = CitationsExtractor()
    

    def extract_detailed_response(self, response_obj):
        """
        Extracts query response, source text, document path, and authors from the response object.

        Args:
            response_obj (obj): The response object containing source nodes with metadata.

        Returns:
            details (dict): A dictionary containing query response, source text, document path, and authors
        """
        details = {
            "query_response": response_obj.response if hasattr(response_obj, 'response') else '',
            "other": []
        }

        if hasattr(response_obj, 'source_nodes'):
            for node_with_score in response_obj.source_nodes:
                node = node_with_score.node
                source_text = node.text if hasattr(node, 'text') and node.text else ''
                document_path = ''
                authors_list = []

                if hasattr(node, 'metadata'):
                    metadata = node.metadata
                    document_path = metadata.get('file_path', '')

                    # Extract authors from the source text using the document path
                    if source_text and document_path:
                        authors_list = self.citations_extractor.get_authors_list(source_text, document_path)
                    else:
                        authors_list = []

                details["other"].append({
                    "source_text": source_text if source_text else 'No source text available',
                    "document_path": document_path if document_path else 'No document path available',
                    "authors": authors_list if authors_list else ['No authors found']
                })

        return details

    def query_documents(self, request):
        """
        Query the indexed documents with specified query string.

        Args:
            request (str): The query string to search in the indexed documents.

        Returns:
            response (dict): A dictionary containing the query response and associated source text details.
        """
        try:
            response_obj = self.index_service_context_loader.get_index().as_query_engine().query(request)
            response = self.extract_detailed_response(response_obj)
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to query documents: {e}")

