//GamepadController.js

import React, { useEffect, useRef, useState } from 'react';

const GamepadController = () => {
    const controllerIndexRef = useRef(null);
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        const handleConnectDisconnect = (event, isConnected) => {
            const controllerAreaNotConnected = document.getElementById('controller-not-connected-area');
            const controllerAreaConnected = document.getElementById('controller-connected-area');
            const gamepad = event.gamepad;

            if (isConnected) {
                controllerIndexRef.current = gamepad.index;
                controllerAreaNotConnected.style.display = 'none';
                //controllerAreaConnected.style.display = 'block';
                createButtonLayout(gamepad.buttons);
                createAxesLayout(gamepad.axes);
            } else {
                controllerIndexRef.current = null;
                controllerAreaConnected.style.display = 'none';
                controllerAreaNotConnected.style.display = 'block';
            }
            setConnected(isConnected);
        };

        const handleConnect = (event) => {
            handleConnectDisconnect(event, true);
        };

        const handleDisconnect = (event) => {
            handleConnectDisconnect(event, false);
        };

        window.addEventListener('gamepadconnected', handleConnect);
        window.addEventListener('gamepaddisconnected', handleDisconnect);

        return () => {
            window.removeEventListener('gamepadconnected', handleConnect);
            window.removeEventListener('gamepaddisconnected', handleDisconnect);
        };
    }, []);

    useEffect(() => {
        const gameLoop = () => {
            if (controllerIndexRef.current !== null) {
                const gamepad = navigator.getGamepads()[controllerIndexRef.current];
                handleButtons(gamepad.buttons);
                handleSticks(gamepad.axes);
                handleRumble(gamepad);
            }
            requestAnimationFrame(gameLoop);
        };

        if (connected) {
            gameLoop();
        }
    }, [connected]);

    const createAxesLayout = (axes) => {
        const buttonsArea = document.getElementById('buttons');
        for (let i = 0; i < axes.length; i++) {
            buttonsArea.innerHTML += `<div id=axis-${i} class='axis'>
                <div class='axis-name'>AXIS ${i}</div>
                <div class='axis-value'>${axes[i].toFixed(4)}</div>
            </div> `;
        }
    };

    const createButtonLayout = (buttons) => {
        const buttonArea = document.getElementById('buttons');
        buttonArea.innerHTML = '';
        for (let i = 0; i < buttons.length; i++) {
            buttonArea.innerHTML += createButtonHtml(i, 0);
        }
    };

    const createButtonHtml = (index, value) => {
        return `<div class="button" id="button-${index}">
            <svg width="10px" height="30px">
                <rect width="10px" height="30px" fill="grey"></rect>
                <rect
                    class="button-meter"
                    width="10px"
                    x="0"
                    y="50"
                    data-original-y-position="50"
                    height="30px"
                    fill="rgb(60, 61, 60)"
                ></rect>
            </svg>
            <div class='button-text-area'>
                <div class="button-name">B${index}</div>
                <div class="button-value">${value.toFixed(2)}</div>
            </div>
        </div>`;
    };

    const updateButtonOnGrid = (index, value) => {
        const buttonArea = document.getElementById(`button-${index}`);
        const buttonValue = buttonArea.querySelector('.button-value');
        buttonValue.innerHTML = value.toFixed(2);

        const buttonMeter = buttonArea.querySelector('.button-meter');
        const meterHeight = Number(buttonMeter.dataset.originalYPosition);
        const meterPosition = meterHeight - (meterHeight / 100) * (value * 100);
        buttonMeter.setAttribute('y', meterPosition);
    };

    const handleButtons = (buttons) => {
        for (let i = 0; i < buttons.length; i++) {
            const buttonValue = buttons[i].value;
            updateButtonOnGrid(i, buttonValue);
            updateControllerButton(i, buttonValue);
        }
    };

    const handleSticks = (axes) => {
        updateAxesGrid(axes);
        updateStick('controller-b10', axes[0], axes[1]);
        updateStick('controller-b11', axes[2], axes[3]);
    };

    const updateAxesGrid = (axes) => {
        for (let i = 0; i < axes.length; i++) {
            const axis = document.querySelector(`#axis-${i} .axis-value`);
            const value = axes[i];
            if (value > 0.06 || value < -0.06) {
                axis.innerHTML = value.toFixed(4);
            }
        }
    };

    const updateStick = (elementId, leftRightAxis, upDownAxis) => {
        const multiplier = 25;
        const stickLeftRight = leftRightAxis * multiplier;
        const stickUpDown = upDownAxis * multiplier;

        const stick = document.getElementById(elementId);
        const x = Number(stick.dataset.originalXPosition);
        const y = Number(stick.dataset.originalYPosition);

        stick.setAttribute('cx', x + stickLeftRight);
        stick.setAttribute('cy', y + stickUpDown);
    };

    const updateControllerButton = (index, value) => {
        const button = document.getElementById(`controller-b${index}`);
        const selectedButtonClass = 'selected-button';

        if (button) {
            if (value > 0) {
                button.classList.add(selectedButtonClass);
                button.style.filter = `contrast(${value * 200}%)`;
            } else {
                button.classList.remove(selectedButtonClass);
                button.style.filter = `contrast(100%)`;
            }
        }
    };

    const handleRumble = (gamepad) => {
        const rumbleOnButtonPress = document.getElementById('rumble-on-button-press');

        if (rumbleOnButtonPress.checked) {
            if (gamepad.buttons.some((button) => button.value > 0)) {
                gamepad.vibrationActuator.playEffect('dual-rumble', {
                    startDelay: 0,
                    duration: 25, //Milliseconds
                    weakMagnitude: 1.0,
                    strongMagnitude: 1.0,
                });
            }
        }
    };

    return (
        <div>
            {/* Your JSX for the gamepad UI */}
        </div>
    );
};

export default GamepadController;
