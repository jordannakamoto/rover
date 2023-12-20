import './App.css'; // Adjust the path if your file structure is different

import React, { useEffect, useState } from 'react';

import ControlPanel from './ControlPanel/ControlPanel';
import MessageLog from './Components/MessageLog/MessageLog';
import ThreeJSCanvas from './ThreeJSCanvas/ThreeJSCanvas';

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [websocket, setWebsocket] = useState(null);

  const addMessage = (newMessage) => {
    setMessages(prevMessages => [...prevMessages, newMessage]);
  };


  useEffect(() => {
    // Create WebSocket connection
    const socket = new WebSocket('ws://localhost:4000'); // Replace with your Flask server URL

    // Connection opened
    socket.addEventListener('open', (event) => {
      console.log('Connected to WS Server');
    });

    // Listen for messages
    socket.addEventListener('message', (event) => {
      console.log('Message from server ', event.data);
      setMessage(event.data);
    });

    // Update WebSocket in the state
    setWebsocket(socket);

    // Cleanup on unmount
    return () => {
      socket.close();
    };
  }, []);

  const sendMessage = () => {
    if (websocket) {
      websocket.send('Hello from React');
    }
  };

  return (
    <div className="App">
      <div className="flex-container">
        <div className="flex-child1">
          <ThreeJSCanvas/>
        </div>
        <div className="flex-child2">
          <ControlPanel/>
          <MessageLog messages={messages} />
        </div>
      </div>
    </div>
  );
}

export default App;
