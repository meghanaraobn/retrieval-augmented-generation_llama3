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
#### Other setup
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
  
  
