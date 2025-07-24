# AI-powered Insights Platform

A simple AI insights platform that allows users to upload files, extract text, and generate insights using OpenAI's GPT-3.5-turbo model.

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
- **MCP Server**: The platform is hosted on a MCP server, ensuring scalability and reliability.
- **OpenAI GPT-3.5-turbo**: Selected for its advanced natural language processing capabilities to generate insights from text.
- **File Upload and Processing**: Implemented using FastAPI's file handling capabilities, allowing users to upload various document formats.
- **Text Extraction**: Utilized libraries like PyMuPDF and pdfminer.six for extracting text from PDF files, ensuring compatibility with different document types.

## Installation

### Prerequisites

### Deployment Checklist

### Deployment

## Contributing

## License
