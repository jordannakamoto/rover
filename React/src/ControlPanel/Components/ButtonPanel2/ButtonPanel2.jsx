import React from 'react';
import buttonConfig from './buttonConfig.json'; // Adjust the path based on your file structure

const SquareButton = ({ label, onClick }) => (
  <button
    style={{
      width: '100px',
      height: '100px',
      margin: '10px',
      flexShrink: 0,
    }}
    onClick={onClick}
  >
    {label}
  </button>
);

const ButtonPanel2 = ({ sendMessage }) => (
  <div style={{padding: '10px'}}>
    <p style={{ margin: '0', marginLeft:'200px'}}>{buttonConfig.title}</p>
    <div style={{ display: 'flex', flexWrap: 'wrap' }}>
      {buttonConfig.buttons.map((button, index) => (
        <SquareButton
          key={index}
          label={button.label}
          onClick={() => sendMessage(button.message, button.data)}
        />
      ))}
    </div>
  </div>
);

export default ButtonPanel2;
