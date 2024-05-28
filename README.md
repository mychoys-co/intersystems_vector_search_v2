# Vector Search with LLM in InterSystems IRIS

## Overview
This project demonstrates a Vector Search application using Large Language Models (LLMs) integrated with InterSystems IRIS. The application is built using Streamlit and leverages OpenAI's API for natural language processing tasks.

## Project Structure
```
├── app
│   ├── app.py
│   ├── Dockerfile
│   ├── initialise_database.py
│   ├── requirements.txt
│   └── streamlit_app
│       ├── config
│       │   ├── constants.py
│       │   └── __init__.py
│       ├── core
│       │   ├── caching.py
│       │   ├── chunking.py
│       │   ├── embedding.py
│       │   ├── file_parsing.py
│       │   ├── __init__.py
│       │   ├── intersystemsdb.py
│       │   ├── llm.py
│       │   ├── prompts.py
│       │   ├── qa.py
│       │   └── vectorstore.py
│       ├── __init__.py
│       ├── media
│       │   └── img_2.png
│       └── ui_elements
│           ├── __init__.py
│           ├── show_references.py
│           ├── sidebar.py
│           ├── suggested_prompts.py
│           └── ui_helper.py
├── app.env
├── docker-compose.yaml
├── notebooks
│   └── intersystems_vector_search.ipynb
├── README.md
└── sample_documents
    ├── example_Imatinib_Teva.pdf
    ├── large_document.txt
    └── small_data.txt
```

## Prerequisites
Ensure you have the following installed on your local machine:
- Docker
- Docker Compose

## Getting Started
- Clone the Repository
- git clone https://github.com/mychoys-co/intersystems_vector_search_v2
- cd intersystems_vector_search_v2

## Set Up Environment Variables
Fill in variables in app.env file in the root directory of your project and add the following environment variables:
```
IRIS_USERNAME=demo
IRIS_PASSWORD=demo
IRIS_HOSTNAME=intersystems
IRIS_NAMESPACE=USER
IRIS_PORT=1972
IRIS_TABLE_NAME=intersystems_table
OPENAI_API_KEY=<your-openai-api-key>
LLM_MODEL=gpt-4o
EMBEDDING_MODEL=all-MiniLM-L6-v2
MINIMUM_MATCH_SCORE=0.10
```

## Build and Run the Application

### If Using the app through docker and UI
Run the following command to build and start the services:
```
docker compose up --build
```

If encounter docker timeout issue do
```
docker compose down
docker compose up --build
```

### If want to use the app through jupyter notebook

Run Intersystems DB
```
docker run --name iris-comm -p 1972:1972 -p 52773:52773 -e IRIS_PASSWORD=demo -e IRIS_USERNAME=demo intersystemsdc/iris-community:latest
```

Run jupyter notebook
```
cd notebooks
jupyter notebook
```

## This will start two services:
- InterSystems IRIS: Runs on ports 1972 and 52773.
- Streamlit App: Runs on ports 8501 and 8502.

## Access the Application if using through docker
Once the services are up and running, you can access the Streamlit application by navigating to:
`
http://localhost:8501
`

## Usage

### Uploading Files
You can upload a .pdf or .txt file through the Streamlit interface.
The file content will be processed and inserted into the InterSystems IRIS database.

### Asking Questions
Enter your question in the provided input box and click the Submit button.
The application will generate a response to your question using OpenAI's API and display relevant search results from the InterSystems IRIS database.

## Closing app

### If using though docker compose
Simply do Ctrl+C from the terminal
```
docker compose down
```

### If using jupyter notebook
- Close notebooks
- Close Intersystems, do Ctrl+C
```
docker rm iris-comm
```

## Notes
Ensure that the InterSystems IRIS container is fully up and running before attempting to use the Streamlit application.
The sleep 40 command in the Docker configuration ensures that the IRIS service has enough time to start before the application attempts to connect.

## Troubleshooting
If you encounter any issues, check the logs of both containers using the following command:
`
docker-compose logs
`
