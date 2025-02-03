# AI-Powered Q&A Agent

## Overview
The **AI-Powered Q&A Agent** is a web application that allows users to interact with an AI model to ask questions and receive intelligent responses. The application maintains a conversation history for better context and provides a smooth user experience.

## Features
- User-friendly chat interface with dynamic updates.
- AI-driven responses using OpenAI GPT or other LLM models.
- Maintains conversation history for context-aware replies.
- Backend API built with **FastAPI** (or Flask/Django/Node.js as needed).
- Frontend built with **React.js** for a responsive UI.
- Error handling for invalid inputs or API failures.

## Tech Stack
### Frontend
- **React.js** (with Hooks and Axios for API calls)
- **CSS** (or TailwindCSS for styling)

### Backend
- **FastAPI** (or Flask/Django/Node.js for API handling)
- **OpenAI API** (or another LLM model for AI responses)
- **In-memory storage** (Python dictionary/JavaScript object for session history)

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- **Node.js** (for frontend)
- **Python 3.8+** (for backend)
- **pip** (Python package manager)
- **virtualenv** (recommended for Python dependencies)

### Backend Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/ai-qa-agent.git
   cd ai-qa-agent/backend
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Add Your OpenAI Key in .env   
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Start the backend server:
   ```sh
   uvicorn main:app --reload
   ```
   The backend will run on `http://localhost:8000`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```sh
   cd ../frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the frontend server:
   ```sh
   npm start
   ```
   The frontend will run on `http://localhost:3000`.

## API Endpoints
### `POST /ask`
- **Description:** Accepts user queries and returns AI-generated responses.
- **Request Body:**
  ```json
  {
    "query": "What is machine learning?",
    "session_id": "abc123"
  }
  ```
- **Response:**
  ```json
  {
    "session_id": "abc123",
    "history": [
      { "role": "user", "content": "What is machine learning?" },
      { "role": "ai", "content": "Machine learning is a branch of AI..." }
    ]
  }
  ```

## Project Structure
```
├── backend/
│   ├── main.py  # FastAPI app
│   ├── requirements.txt  # Backend dependencies
│   ├── utils.py  # Helper functions
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat.js  # Chat interface component
│   │   ├── App.js  # Main app file
│   │   ├── index.js  # React entry point
│   ├── package.json  # Frontend dependencies
├── README.md  # Project documentation
```


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


