import ButtonPanel1 from './Components/ButtonPanel1/ButtonPanel1';
import ButtonPanel2 from './Components/ButtonPanel2/ButtonPanel2';
import React from 'react';

const ControlPanel = ({sendMessage}) => {
  return (
    <div style={{ display: 'absolute', top:'0' }}>
      <h1>Control Panel</h1>
      <ButtonPanel1 sendMessage={sendMessage} />
      <ButtonPanel2 sendMessage={sendMessage} />
    </div>
  );
};

export default ControlPanel;
