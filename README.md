## Prerequisites
* Linux or macOS (recommended)
* Python 3
* NVIDIA GPU + CUDA CuDNN

## Code Structure
The project is organized into the following directories and files:
- `docs/`: Contains information documents related to the project.
- `data/`: Contains input.txt file with sample text for testing purpose.
- `src/`: Includes the main source code files.
    - `models/`: Directory for model-related functionalities.
        - `model_handler.py`: Script to load and save a model
        - `topic_generation_model.py`: Script to train dynamic topic generation model.
    - `scripts/`: Directory for additional scripts and utilities.
        - `data_format.py`: Script to handle data formatting.
    - `inference.py`: Script for model inference.
    - `train.py`: Script for model training.
- `dockerignore`: To exclude unnecessary files from the docker build context.
- `gitignore`: To ignore certain files from version control.
- `Dockerfile`: To build the project's docker image.
- `docker-compose.yml`: Configuration file for docker compose.
- `environment.yml`: Defines the conda environment for the project.
- `requirements.txt`: Lists python dependencies required for the project.
- `task.txt`: Task-related information.
  
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
* To enter into the container (topic-generation-container):
  ```bash
  docker exec -it topic-generation-container bash
  ```
* To stop the container:
  ```bash
  docker-compose down
  ```
