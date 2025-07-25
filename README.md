# AI-powered Insights Platform

A simple AI insights platform that allows users to upload files, extract text, and generate insights using DeepSeek Model via Openrouter.ai.

## Gallery

<img width="1050" height="716" alt="Screenshot from 2025-07-25 01-00-48" src="https://github.com/user-attachments/assets/2bbc3474-a857-4d7c-a3bf-00f62ee80ee4" />


<img width="1050" height="716" alt="Screenshot from 2025-07-25 01-01-01" src="https://github.com/user-attachments/assets/395d8a75-eb92-4bb4-b107-a93f7d2ce072" />

<img width="1050" height="716" alt="Screenshot from 2025-07-25 01-01-10" src="https://github.com/user-attachments/assets/0109c5f6-f21a-4cc9-8b8c-fe2fc59ba1db" />

<img width="1045" height="732" alt="Screenshot from 2025-07-25 01-01-29" src="https://github.com/user-attachments/assets/3585c499-4fbd-4304-b8d5-0142852af796" />

<img width="1045" height="732" alt="Screenshot from 2025-07-25 01-02-25" src="https://github.com/user-attachments/assets/aed7c4c5-931e-471c-9123-872be061d4c1" />


## Features

- Document upload and text extraction
- AI-powered insights generation
- User-friendly interface (Flutter Web)
- Backend built with FastAPI

## Architectural Decisions

For a detailed overview of the architectural decisions made during the development of this project, please refer to the [Architectural Decisions](docs/architectural_decisions.md) document.
However, here are some key decisions taken into consideration of this project:

- **FastAPI**: Chosen for its performance and ease of use in building APIs.
- **Flutter Web**: Used for the frontend to provide a responsive and interactive user interface.
- **MCP Server/Client**: The platform is connected to a MCP server via Openrouter.ai, ensuring LLM (Large Language Model) capabilities are available for generating insights.
- **File Upload and Processing**: Implemented using FastAPI's file handling capabilities, allowing users to upload various document formats.
- **Text Extraction**: Text extraction is done via python-docx for Word Docuemnt files, and custom functions for TXT files, ensuring compatibility with different document types.

> Aside: Added support for Word Docuement files (.docx) and TXT files for text extraction, to stress-test the platform's capabilities with different file formats.

## Installation

> At the moment, It is highly recommended to run the project locally,
> within each project folders (`web` and `backend`). Ensure all dependencies are installed by following the instructions below.
>
> cd into `web`, and run:
>
> ```bash
> flutter pub get    # to install Flutter dependencies
> flutter build web    # to build the Flutter web app
> flutter run -d chrome    # to run the Flutter web app in Chrome
> ```
>
> cd into `backend`, and run:
>
> ```bash
> pip install -U pip    # to upgrade pip
> python3 -m venv .venv
> source .venv/bin/activate    # to activate the virtual environment
> pip install -r requirements.txt    # to install Python dependencies
> ```
>
> then still within `backend`, run:
>
> ```bash
> cd src
> uvicorn main:app --reload
> ```

For local development, you can set up the project using Docker and Docker Compose. This will allow you to run both the Flutter web app and the FastAPI backend seamlessly.

-

Clone the repository and run:

```bash
make web    # to build the Flutter web app
make backend    # to start the FastAPI backend
```

### Prerequisites

Docker

### Deployment

Please ensure you have Docker installed and running before deploying the application. Follow these steps to deploy the application:

Run the following commands to build and start the Docker containers:

```bash
docker-compose build    # to build the Docker images
docker-compose up -d    # on your server or VM
```

## Contributing

We welcome contributions to this project! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear messages.
4. Push your changes to your forked repository.
5. Create a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
