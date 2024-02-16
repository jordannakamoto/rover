import React, { useEffect, useState } from 'react';

import ControlPanel from './ControlPanel/ControlPanel';
import MessageLog from './FlaskMessenger/MessageLog';
import ThreeJSCanvas from './ThreeJSCanvas/ThreeJSCanvas';
import io from 'socket.io-client';

function App() {
  const [messages, setMessages] = useState([]);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = io('http://127.0.0.1:4000');

    newSocket.on('connect', () => {
      console.log('Connected to Socket.IO server');
    });

    newSocket.on('response', (response) => {
      console.log('Response from server:', response.data);
      setMessages(prevMessages => [...prevMessages, response.data]);
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  const sendMessage = (msg) => {
    console.log(msg);
    socket?.emit('message', msg);
  };

  return (
    <div className="App">
      <div className="flex-container">
        {/* <ThreeJSCanvas sendMessage={sendMessage} /> */}
        <div className="flex-child2" style={{ position: 'absolute', top: 0, right: 0 }}>
          <ControlPanel sendMessage={sendMessage} />
          <MessageLog messages={messages} />
        </div>
      </div>
    </div>
  );
}

export default App;
