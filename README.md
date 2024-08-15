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

### Installation
* To clone this repo:
  ```bash
  git clone https://github.com/meghanaraobn/retrieval-augmented-generation_llama3.git
  cd retrieval-augmented-generation_llama3
  ```
* For pip users, please type the command `pip install -r requirements.txt`.
* For conda users, you can create a new conda environment using `conda env create -f environment.yml`.
### Docker Support
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
