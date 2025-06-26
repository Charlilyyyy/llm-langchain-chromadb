import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";
const ALLOWED_USERS = ["admin", "alice"];

function App() {
  const [user, setUser] = useState("");
  const [inputUser, setInputUser] = useState("");
  const [inputPass, setInputPass] = useState("");
  const [loginError, setLoginError] = useState("");
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      axios.get(`${API_URL}/history/${user}`).then(res => {
        setHistory(res.data.history);
      });
    }
  }, [user]);

  const sendMessage = async (e) => {
    e.preventDefault();
    setLoading(true);
    const res = await axios.post(`${API_URL}/chat`, { user, message });
    setHistory([...history, { user, message }, { user: "bot", message: res.data.response }]);
    setMessage("");
    setLoading(false);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError("");
    if (!ALLOWED_USERS.includes(inputUser)) {
      setLoginError("Only 'admin' and 'alice' can login.");
      return;
    }
    try {
      const res = await axios.post(`${API_URL}/login`, { username: inputUser, password: inputPass });
      if (res.data.success) {
        setUser(res.data.username);
      }
    } catch (err) {
      setLoginError("Invalid username or password");
    }
  };

  if (!user) {
    return (
      <div style={{ maxWidth: 400, margin: "100px auto", fontFamily: "sans-serif" }}>
        <h2>Login to Chatbot</h2>
        <form onSubmit={handleLogin} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <input
            value={inputUser}
            onChange={e => setInputUser(e.target.value)}
            placeholder="Enter your username"
            autoFocus
          />
          <input
            type="password"
            value={inputPass}
            onChange={e => setInputPass(e.target.value)}
            placeholder="Enter your password"
          />
          <button type="submit" disabled={!inputUser.trim() || !inputPass.trim()}>Login</button>
          {loginError && <div style={{ color: "red" }}>{loginError}</div>}
        </form>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>LLM Chatbot</h2>
      <div style={{ marginBottom: 16 }}>
        <span>Logged in as <b>{user}</b></span>
        <button style={{ marginLeft: 16 }} onClick={() => { setUser(""); setInputUser(""); setInputPass(""); setHistory([]); }}>Logout</button>
      </div>
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