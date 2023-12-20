import React from 'react';

const MessageLog = ({ messages }) => {
  return (
    <div style={styles.logContainer}>
        <p>Message Log</p>
      {messages.map((message, index) => (
        <div key={index} style={styles.message}>
          {message}
        </div>
      ))}
    </div>
  );
};

const styles = {
  logContainer: {
    maxHeight: '200px', // Adjust the height as needed
    overflowY: 'auto',
    backgroundColor: '#f0f0f0', // Light grey background
    padding: '10px',
    border: '1px solid #ccc',
    marginTop: '10px',
  },
  message: {
    padding: '5px',
    borderBottom: '1px solid #ddd',
  }
};

export default MessageLog;
