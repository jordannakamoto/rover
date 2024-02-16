import ButtonPanel1 from './Components/ButtonPanel1/ButtonPanel1';
import ButtonPanel2 from './Components/ButtonPanel2/ButtonPanel2';
import GamePadGUI from './Components/GamePad/GamePadGUI';
import React from 'react';

const ControlPanel = ({sendMessage}) => {
  return (
    <div style={{ display: 'absolute', top:'0' }}>
      <h1>Control Panel</h1>
      <GamePadGUI/>
    </div>
  );
};

export default ControlPanel;
