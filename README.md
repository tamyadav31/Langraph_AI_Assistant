# Langraph_AI_Assistant

## Overview

Langraph_AI_Assistant is an AI-powered conversational assistant built with the Langgraph framework. It uses modern language models through Langchain and OpenAI APIs to provide a flexible, state-graph-based chatbot experience. The project features a modular backend architecture combined with a Streamlit web-based frontend supporting multi-threaded chat sessions with persistent state management.

This repository demonstrates how to build a conversational AI assistant that tracks context and manages multiple chat threads in a clean, scalable way.

## Features

- **State Graph Architecture:** Implements the chatbot backend as a state graph using the Langgraph library, enabling flexible and composable conversation flows.
- **OpenAI Language Models:** Powers the chatbot with OpenAI models accessed via the Langchain framework.
- **Multi-threaded Conversations:** Supports multiple simultaneous chat sessions (threads) with unique IDs, allowing users to manage ongoing conversations independently.
- **State Persistence:** In-memory checkpointing saves conversation states so users can resume threads seamlessly.
- **Streamlit Frontend:** User-friendly interactive web interface with thread creation, renaming, and deletion capabilities.
- **Session Management:** Robust session state handling for storing message history and managing thread metadata.
- **Configurable & Extensible:** Easily extendable backend chat logic and adaptable frontend UI.

## Technology Stack

- Python 3.x
- [Langgraph](https://github.com/langgraph/langgraph) for state graph conversation modeling
- [Langchain](https://github.com/hwchase17/langchain) and [langchain-openai](https://github.com/hwchase17/langchain) for language model integration
- OpenAI GPT language models (via Langchain OpenAI wrapper)
- Streamlit for frontend UI
- Python-dotenv for environment configuration

## Installation

1. Clone the repository:

git clone https://github.com/tamyadav31/Langraph_AI_Assistant.git
cd Langraph_AI_Assistant

text

2. Create and activate a Python virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

text

3. Install dependencies:

pip install -r requirements.txt

text

4. Configure environment variables:

Create a `.env` file in the root directory and add your OpenAI API credentials and any other required configuration variables.

## Usage

### Run the backend and frontend

The backend logic is encapsulated in `langgraph_backend.py`. The main user interface runs in Streamlit via `streamlit_frontend_threading.py`.

To launch the chatbot frontend:

streamlit run streamlit_frontend_threading.py

text

Open the URL provided by Streamlit in your web browser to interact with the assistant.

### Functionality

- **New Conversations:** Create new chat threads with unique IDs.
- **Switch Threads:** Load and continue previous conversations.
- **Rename and Delete Threads:** Manage chat sessions effectively.
- **State Persistence:** Conversations are saved during the session via in-memory checkpointing.

## Code Structure

- `langgraph_backend.py` — Defines the chatbot state graph, integrates the OpenAI model, and manages message processing.
- `streamlit_frontend_threading.py` — Provides the Streamlit web app interface and chat thread management.
- `requirements.txt` — Lists Python dependencies for the project environment.

## Contributing

Contributions are welcome! Please open issues or pull requests for bug fixes, enhancements, or new features.

## License

This project is open source and available under the MIT License.

---

Built with ❤️ using Langgraph, Langchain, OpenAI, and Streamlit.  
For questions or support, please contact the repository owner.
