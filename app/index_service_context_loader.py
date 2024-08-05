from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.prompts.prompts import SimpleInputPrompt
from llama_index.embeddings import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.llms import HuggingFaceLLM
from llama_index import load_index_from_storage, StorageContext
import torch

class IndexServiceContextLoader:
    def __init__(self, document_directory = "docs/scientific_papers",  index_directory = "docs/index",
                 model_name = "meta-llama/Meta-Llama-3-8B-Instruct", tokenizer_name = "meta-llama/Meta-Llama-3-8B-Instruct",
                 embed_model_name = "sentence-transformers/all-mpnet-base-v2"):
        """
        Initialize the IndexManager with document directory, index storage directory, models and tokenizer.

        Args:
            document_directory (str): Directory containing the documents to index.
            index_directory (str): Directory to store the index.
            model_name (str): Name of the LLM.
            tokenizer_name (str): Name of the tokenizer.
            embed_model_name (str): Name of the embedding model.
        """
        self.DOCUMENT_DIRECTORY = document_directory
        self.INDEX_DIRECTORY = index_directory
        self.model_context_window = 4096
        self.model_max_new_tokens = 256
        self.generate_kwargs={"temperature": 0.0, "do_sample": False}
        self.model_kwargs={"torch_dtype": torch.float16, "load_in_8bit": True}
        self.device_map="auto"
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.embed_model_name = embed_model_name
        # Set up the service context
        self.service_context = self.setup_service_context()    
        # Load or set up the index
        try:
            self.index = self.load_index()
        except:
            self.index = self.setup_index()
            self.persist_index()

    def setup_service_context(self):
        """
        Set up the service context with LLM, embedding model and tokenizer.

        Returns:
            service_context (ServiceContext): The configured service context.
        """
        system_prompt = """
        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.
        Your answers should not include any harmful, unethical or illegal content.
        Please ensure that your responses are socially unbiased and positive in nature.

        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
        If you don't know the answer to a question, please don't share false information.
        """
        query_wrapper_prompt = SimpleInputPrompt("{query_str}")

        # LLM
        llm = HuggingFaceLLM(
            context_window=self.model_context_window,
            max_new_tokens=self.model_max_new_tokens,
            generate_kwargs=self.generate_kwargs,
            system_prompt=system_prompt,
            query_wrapper_prompt=query_wrapper_prompt,
            tokenizer_name=self.tokenizer_name,
            model_name=self.model_name,
            device_map=self.device_map,
            model_kwargs=self.model_kwargs
        )
        
        # Embedding model
        embed_model = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name=self.embed_model_name)
        )

        # Service context
        service_context = ServiceContext.from_defaults(
            chunk_size=1024,
            llm=llm,
            embed_model=embed_model
        )
        return service_context

    def setup_index(self):
        """
        Set up document indexes initially using the service context.

        Returns:
            VectorStoreIndex: The document index.
        """
        documents = SimpleDirectoryReader(self.DOCUMENT_DIRECTORY).load_data()
        return VectorStoreIndex.from_documents(documents, service_context=self.service_context)

    def persist_index(self):
        """
        Persist the current state of the index to storage.
        """
        self.index.storage_context.persist(self.INDEX_DIRECTORY)
    
    def load_index(self):
        """
        Load index from persistent storage.
        """
        storage_context = StorageContext.from_defaults(persist_dir=self.INDEX_DIRECTORY)
        return load_index_from_storage(storage_context, service_context=self.service_context)
    
    def reload_index(self):
        """
        Reload the index from persistent storage.
        """
        self.index = self.load_index()
    
    def get_index(self):
        """
        Retrieve the current index.
        """
        return self.index
    
    def create_index(self, li_document):
        """
        Create document Index.
        """
        # Insert the document into the index
        self.index.insert(li_document)
        # Store the updated index
        self.persist_index()
        # Reload the index
        self.reload_index()
    
    def delete_index(self, ref_document_id):
        """
        Delete document Index.
        """
        # Delete the document index based on ref_doc_id
        self.index.delete_ref_doc(ref_doc_id=ref_document_id, delete_from_docstore=True)
        # Store the updated index
        self.persist_index()
        # Reload the index
        self.reload_index()


