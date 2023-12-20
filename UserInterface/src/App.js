import React, { useEffect, useState } from 'react';

import ControlPanel from './ControlPanel/ControlPanel';
import MessageLog from './FlaskMessenger/MessageLog';
import ThreeJSCanvas from './ThreeJSCanvas/ThreeJSCanvas';
import io from 'socket.io-client';

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Connect to Socket.IO server
    const newSocket = io('http://127.0.0.1:4000');

    newSocket.on('connect', () => {
      console.log('Connected to Socket.IO server');
    });

    newSocket.on('message', (data) => {
      console.log('Message from server:', data);
      setMessage(data);
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  const sendMessage = (msg) => {
    socket.emit('message', msg);
  };

  return (
    <div className="App">
      <div className="flex-container">
        <div className="flex-child1">
          <ThreeJSCanvas />
        </div>
        <div className="flex-child2">
          <ControlPanel sendMessage={sendMessage}/>
          <MessageLog messages={messages} />
        </div>
      </div>
    </div>
  );
}

export default App;
