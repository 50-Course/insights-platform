# AI-powered Insights Platform

A simple AI insights platform that allows users to upload files, extract text, and generate insights using DeepSeek Model via Openrouter.ai.

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
- **Text Extraction**: Utilized libraries like PyMuPDF and pdfminer.six for extracting text from PDF files, ensuring compatibility with different document types.

## Installation

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
