import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function App() {
  const [user, setUser] = useState("user1");
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get(`${API_URL}/history/${user}`).then(res => {
      setHistory(res.data.history);
    });
  }, [user]);

  const sendMessage = async (e) => {
    e.preventDefault();
    setLoading(true);
    console.log("wow")
    const res = await axios.post(`${API_URL}/chat`, { user, message });
    setHistory([...history, { user, message }, { user: "bot", message: res.data.response }]);
    setMessage("");
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>LLM Chatbot</h2>
      <div style={{ border: "1px solid #ccc", padding: 20, minHeight: 300, marginBottom: 20 }}>
        {history.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.user === user ? "right" : "left" }}>
            <b>{msg.user}:</b> {msg.message}
          </div>
        ))}
        {loading && <div>Bot is typing...</div>}
      </div>
      <form onSubmit={sendMessage} style={{ display: "flex", gap: 8 }}>
        <input
          value={message}
          onChange={e => setMessage(e.target.value)}
          placeholder="Type your message..."
          style={{ flex: 1 }}
        />
        <button type="submit" disabled={!message || loading}>Send</button>
      </form>
    </div>
  );
}

export default App; 