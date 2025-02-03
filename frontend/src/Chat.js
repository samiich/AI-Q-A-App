import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState([]);
  const [sessionId, setSessionId] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      const response = await axios.post('http://localhost:8000/ask', {
        query: input,
        session_id: sessionId
      });

      setSessionId(response.data.session_id);
      setHistory(response.data.history);
      setInput('');
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to get response. Please try again.');
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {history.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="bubble">{msg.content}</div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chat;
