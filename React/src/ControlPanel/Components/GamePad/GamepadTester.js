// GamepadTester.js

import React from 'react';
import ControllerSVG from './ControllerSVG'; // Import your ControllerSVG component
import GamepadController from './GamepadController'; // Import your GamepadController component
import './style.css'; // Import your CSS file

const GamepadTester = () => {
    return (
        <div style={{ padding: '20px', width:'50%' }}>
            <h3 className="center">Gamepad</h3>
            <div id="controller-not-connected-area" className="controller-status">
                <div className="loader"></div>
                <div>Controller not connected. Press any button to start.</div>
            </div>
            <div id="controller-connected-area">
                <div id="controller-connected" className="controller-status">Connected</div>
                <div id="rumble-on-button-press-area">
                    <input id="rumble-on-button-press" type="checkbox" />
                    <label htmlFor="rumble-on-button-press">Rumble on button press</label>
                </div>
                <div id="buttons"></div>
            </div>
            {/* Render ControllerSVG component */}
            <ControllerSVG />
            {/* Render GamepadController component */}
            <GamepadController />
        </div>
    );
};

export default GamepadTester;
