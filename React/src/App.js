import React, { useEffect, useState } from 'react';

import ControlPanel from './ControlPanel/ControlPanel';
import GamePadGUI from './ControlPanel/Components/GamePad/GamepadTester';
import MessageLog from './FlaskMessenger/MessageLog';
// import ThreeJSCanvas from './ThreeJSCanvas/ThreeJSCanvas';
import VideoPanel from './VideoPanel/VideoPanel';
import VideoPanel2 from './VideoPanel/VideoPanel2';
import VideoPanel3 from './VideoPanel/VideoPanel3';
import io from 'socket.io-client';

function App() {
  const [messages, setMessages] = useState([]);
  const [socket, setSocket]     = useState(null);

  useEffect(() => {
    // DEVELOPMENT SOCKET
    // For use on localhost when - both React and Raspi servers run on the laptop
    // const newSocket = io('http://127.0.0.1:4000');
    
    // PRODUCTION SOCKET
    // When connected to Lab LAN Network 'microUAS' - static IP for Raspi
    const newSocket = io('http://192.168.1.2:4000');
  
    // 1. Verify Connection
    newSocket.on('connect', () => {
      console.log('Connected to Socket.IO server');
    });

    // Handler for Message Responses from Flask
    newSocket.on('response', (response) => {
      console.log('Response from server:', response.data);
      setMessages(prevMessages => [...prevMessages, response.data]);
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  // Send Message to Flak Server
  // (MessageType, MessageData)
  const sendMessage = (type, data) => {
    const msg = { type, data };   // Create a message object with type and data
    console.log(msg);             // Log the message for debugging
    socket?.emit('message', msg); // Emit the message to the Flask server
};

  return (
    <div className="App">
      <div className="flex-container">
        {/* DISABLED 3D VIEWER INDEFINITELY                    <ThreeJSCanvas sendMessage={sendMessage} /> */}
        <VideoPanel />
        <VideoPanel2/>
        <VideoPanel3/>
        <div className="flex-child2" style={{ position: 'absolute', top: 0, right: 0 }}>
          {/* <ControlPanel sendMessage={sendMessage} /> */}
          {/* <MessageLog messages={messages} /> */}
          
          {/* <GamePadGUI/> */}
        </div>
      </div>
    </div>
  );
}

export default App;
