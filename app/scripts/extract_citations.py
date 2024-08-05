import re
import fitz

class CitationsExtractor:
    def __init__(self):
        """
        Class to extract citations from text
        """

    def extract_citations(self, text):
        """
        Extracts author names and citation numbers from the provided text.

        Args:
            text (str): The text from which to extract references.

        Returns:
            results (dict): A dictionary containing 'author_names' and 'citation_numbers' lists.
        """
        results = {
            'author_names': [],
            'citation_numbers': []
        }
        
        unique_authors = set()
        # Pattern to match authors followed by "et al."
        author_et_al_pattern = re.compile(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)? et al\.?\b')
        author_et_al_matches = author_et_al_pattern.findall(text)
        if author_et_al_matches:
            unique_authors.update(author_et_al_matches) 

        # Pattern to match authors separated by "and" or comma and a year in various formats
        author_and_year_pattern = re.compile(
            r'\b([A-Z][a-z]+)\b(?:\s+and\s+[A-Z][a-z]+|\s*,\s*[A-Z][a-z]+)?\s*(?:\(\d{4}\)|,\s*\d{4}|\.?\s*\d{4})',
            re.UNICODE)
        author_and_year_matches = author_and_year_pattern.findall(text)
        for primary_author in author_and_year_matches:
            unique_authors.add(f"{primary_author} et al")

        results['author_names'] = list(unique_authors)

        # Pattern to match citation numbers
        citation_pattern = re.compile(r'\[\s*(\d+(?:\s*,\s*\d+)*)\s*\]')
        citation_matches = citation_pattern.findall(text)
        if citation_matches:
            # Extract citation numbers from the matches
            citation_numbers = re.findall(r'\d+', ','.join(citation_matches))
            results['citation_numbers'] = list(set(citation_numbers)) 

        return results

    def extract_reference_section_text(self, document_path):
        """
        Extracts the text of the "References" section from the document.

        Args:
            document_path (str): The path of document from which to extract reference section.

        Returns:
            ref_section (str): The text of the "References" section.
        """
        
        ref_section = ''
        
        try:
            document = fitz.open(document_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at path {document_path} was not found.")
        
        found_references = False
        
        for page_num in range(len(document)):
            page = document.load_page(page_num) 
            text = page.get_text()
            if text:
                if not found_references:
                    # Find text starting with variations of "References" and "\n" afterwards
                    match = re.search(r'(?:References|REFERENCES|Bibliographical References)\s*\n(.*)', text, re.DOTALL)
                    if match:
                        ref_section += match.group(1)
                        found_references = True
                else:
                    ref_section += text

        return ref_section

    def extract_author_from_document_references(self, citation_number, document_path):
        """
        Extracts the first author’s name from the reference section for the given citation number.

        Args:
            citation_number (str): The citation number to look up in the references.
            document_path (str): The path of document from which to extract author.

        Returns:
            author (str): The first author's name.
        """

        ref_section = self.extract_reference_section_text(document_path)
        if not ref_section:
            return None
        
        pattern = re.compile(r'\[\s*' + re.escape(citation_number) + r'\]\s*(.*)')
        match = pattern.search(ref_section)

        if match:
            ref_text = match.group(1)
            authors_pattern = re.compile(r'^([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)(?:,|\s)')
            author_match = authors_pattern.match(ref_text)

            if author_match:
                return f"{author_match.group(1)} et al"
        return None

    def get_authors_list(self, text, document_path):
        """
        Get the list of authors cited in text.

        Args:
            text (str): The text to process for extracting references.
            document_path (str): The path of the document to fetch author names.

        Returns:
            final_authors_list (list): A list containing a list of author names.
        """
        references = self.extract_citations(text)

        combined_authors = set()

        # Add authors directly extracted from text
        if 'author_names' in references:
            combined_authors.update(references['author_names'])

        # Add authors linked with citation numbers
        if 'citation_numbers' in references and document_path:
            for citation_number in references['citation_numbers']:
                author_names = self.extract_author_from_document_references(citation_number, document_path)
                if author_names:
                    combined_authors.add(author_names)

        # Convert set to list 
        final_authors_list = list(combined_authors)

        return final_authors_list
