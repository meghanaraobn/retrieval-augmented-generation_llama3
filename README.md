# Retrieval Augmented Generation using Llama 3
Retrieval-Augmented Generation (RAG) is an advanced natural language processing technique that combines retrieval-based and generative models to enhance response quality and accuracy. The retrieval component searches a large database for relevant documents or text snippets based on a query, providing the generative model with specific context or information. The generative model then uses this retrieved content to produce a coherent and contextually appropriate response. By integrating both components, RAG excels in tasks like question answering and content creation, delivering responses that are accurate, fluent, and factually grounded.

### Why Llama 3 Instruct? 
[Llama 3 Instruct](https://ai.meta.com/blog/meta-llama-3/), a LLM, is used for Retrieval-Augmented Generation (RAG) because it is specifically designed to generate highly relevant, context-aware responses based on detailed instructions or prompts. Its architecture is optimized for understanding complex queries and effectively utilizing external information retrieved by the RAG system. This makes it ideal for tasks that require not only accurate information retrieval but also the generation of coherent and contextually appropriate text. Llama 3 Instruct's ability to follow instructions closely and generate precise responses enhances the overall effectiveness of RAG, particularly in applications like question answering and content generation where nuanced understanding and accuracy are critical.

### Objective
The objective of this project is create a backend application to answer questions about set of scientific papers using RAG technique.

## Datasets
A dataset consisting of 100 different scientific papers covering various topics.

## Models and API
* API used: ``` FastAPI ```
* LLM used: ```Meta-Llama-3-8B-Instruct ```
* Embed model used: ``` all-mpnet-base-v2 ```
* For indexing: ``` llama_index ```

#### Endpoints
* Root Endpoint: 'GET /'
* Create Document Index: 'POST /create_index' (parameter - document_path)
* Delete Document Index: 'DELETE /delete_index/{ref_document_id}' (parameter - ref_document_id)
* Query Documents: 'POST /query_documents' (parameter - query_string)
  
## Prerequisites
* Linux or macOS (recommended)
* Python 3
* NVIDIA GPU + CUDA CuDNN

## Code Structure
The project is organized into the following directories and files:

    ├── app    
    │   ├── main.py   
    │   ├── index_manager.py
    │   ├── index_query_service.py
    │   ├── index_service_context_loader.py
    │   ├── scripts
    │   │   └── extract_citations.py
    ├── docs
    │   └── index
    │   └── scientific_papers
    ├── environment.yml
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── .env
    └── instructions.txt
  
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

#### Installation
* To clone this repo:
  ```bash
  git clone https://github.com/meghanaraobn/retrieval-augmented-generation_llama3.git
  cd retrieval-augmented-generation_llama3
  ```
* For pip users, please type the command `pip install -r requirements.txt`.
* For conda users, you can create a new conda environment using `conda env create -f environment.yml`.
#### Docker Support
This project includes docker support for easy setup with configurations provided in `docker-compose.yml` and `Dockerfile`. To enable GPU support within Docker containers, ensure the NVIDIA Container Toolkit is installed on the system. Detailed installation instructions can be found [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

For managing the setup:
* Build the docker image:
  ```bash
  docker-compose build
  ```
* To spin the container:
  ```bash
  docker-compose up -d
  ```
* To enter into the container (rag-container):
  ```bash
  docker exec -it rag-container bash
  ```
* To stop the container:
  ```bash
  docker-compose down
  ```
* Set up hugging face token in .env file
  ```bash
   HF_TOKEN=huggingface_token
  ```
#### Other Setup
* Place all the documents (.pdf files) in the directory: ``` /docs/scientific_papers ```
* If you have a persisted index, place it in the directory: ``` /docs/index ```
* Start the FastAPI application
  ```bash
  uvicorn app.main:app --reload
  ```
* Navigate to swagger UI
  ```bash
  http://127.0.0.1:8000/docs
  ```
### Process Flow
* Startup
* Load environment variables
* Hugging face login
* Service context set up (configured with LLM, embedding model)
* Initially index all documents present in '/docs/scientific_papers' (if persisted index is present, load the index present in '/docs/index')
* Create index/Delete index/Query documents.

### Further Improvements
* Improve index management to handle large volumes of documents more efficiently.
* Fine-tune the Meta-Llama-3-8B-Instruct model.
* Create a broader range of prompts to cover more use cases which improve the LLM's ability to handle different queries.
* Improve techniques for citation extraction from the retrieved source text.
  
  
