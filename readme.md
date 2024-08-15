# Search Microservice
Part of Video Search Engine Project

This repository contains a Flask-based web service for searching videos in a MySQL database. The service accepts search queries and returns the matching video information.

## Features

- Search videos in a MySQL database by category.
- Return video file paths, file name, and associated categories.
- REST API endpoints for checking service status and searching videos.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/iam-VK/search_service
   cd search_service
2. Install the required dependencies:

    ```bash
    ./setup.sh
## Usage
1. Run the Flask application:

    ```bash
    ./run.sh
2. The service will be available at http://0.0.0.0:5003

## Endpoints
- ### Service Status
    - URL: /
    - Method: GET or POST
    - Response:
    ```json
    {
        "status": "Alive",
        "endpoints": {
            "/search": {
                "method": "[POST]",
                "parameters": {
                    "search_query": "video tag / search query"
                }
            }
        }
    }
- ### Video Search

    - URL: /search
    - Method: POST
    - Request: Form data with search query (search_query)
    - Response:
    ```json
    {
        "status": "SUCCESS",
        "total_results": <number_of_results>,
        "results": [
            {
                "file_path": "<file_path>",
                "file_name": "<file_name>",
                "category_list": "<category_list>"
            },
            ...
        ]
    }
## Project Structure
```bash
    search_service/
    ├── API_SERVER.py         # Flask application
    ├── mysql_DB.py           # MySQL database interactions
    ├── requirements.txt      # List of dependencies
    ├── README.md             # Project README
    ├── setup.sh              # Setup virtual env and install dependencies
    └── run.sh                # Starts the microservice  