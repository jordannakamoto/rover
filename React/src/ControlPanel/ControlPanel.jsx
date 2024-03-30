import ButtonPanel1 from './Components/ButtonPanel1/ButtonPanel1';
import React from 'react';
// import ButtonPanel2 from './Components/ButtonPanel2/ButtonPanel2';
// import TestParam from './Components/TestParam/TestParam'

const ControlPanel = ({sendMessage}) => {
  return (
    <div style={{ display: 'absolute', top:'0' }}>
      <h3>Control Panel</h3>
      <ButtonPanel1 sendMessage={sendMessage}/>
    </div>
  );
};

export default ControlPanel;
