import React, { useEffect, useState } from 'react';

const TestParam = ({ sendMessage }) => {
  const [sliderValue1, setSliderValue1] = useState(50); // Assuming a range of 0-100
  const [sliderValue2, setSliderValue2] = useState(50); // Adjust initial values as needed

  // This function remains unchanged, it maps specific slider values to the desired range
  const mapSliderValueToRange = (sliderValue) => {
    if (sliderValue === 50) return 0;
    else if (sliderValue === 0) return -3600;
    else if (sliderValue === 10) return -2900;
    else if (sliderValue === 20) return -2200;
    else if (sliderValue === 30) return -1500;
    else if (sliderValue === 40) return -800;
    else if (sliderValue === 60) return 800;
    else if (sliderValue === 70) return 1500;
    else if (sliderValue === 80) return 2200;
    else if (sliderValue === 90) return 2900;
    else if (sliderValue === 100) return 3600;
    return null; // It's good practice to return a default value
  };

  // Modify handleSliderChange to use transformed values for sending message
  const handleSliderChange = (value1, value2) => {
    const transformedValue1 = mapSliderValueToRange(parseInt(value1, 10));
    const transformedValue2 = mapSliderValueToRange(parseInt(value2, 10));

    setSliderValue1(parseInt(value1, 10)); // Update state with original (untransformed) value
    setSliderValue2(parseInt(value2, 10)); // Update state with original (untransformed) value

    // Send message with transformed values
    sendMessage(`${transformedValue1} ${transformedValue2}`);
  };

  useEffect(() => {
    const handleKeyPress = (e) => {
      switch (e.key) {
        case 'w':
          setSliderValue1((prev) => Math.min(100, prev + 10));
          break;
        case 's':
          setSliderValue1((prev) => Math.max(0, prev - 10));
          break;
        case 'ArrowUp':
          setSliderValue2((prev) => Math.min(100, prev + 10));
          break;
        case 'ArrowDown':
          setSliderValue2((prev) => Math.max(0, prev - 10));
          break;
        default:
          break;
      }
    };

    // Add event listener
    window.addEventListener('keydown', handleKeyPress);

    // Remove event listener on cleanup
    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, []);

  useEffect(() => {
    // Transform the current slider values
    const transformedValue1 = mapSliderValueToRange(sliderValue1);
    const transformedValue2 = mapSliderValueToRange(sliderValue2);
  
    // Send the transformed values
    sendMessage(`${transformedValue1} ${transformedValue2}`);
  }, [sliderValue1, sliderValue2]); // Depend on the original slider values



  return (
    <div style={{ padding: '10px' }}>
      <p style={{ margin: '0', marginLeft: '200px' }}>{TestParam.title}</p>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <input
          type="range"
          min="0"
          max="100"
          value={sliderValue1}
          onChange={(e) => handleSliderChange(e.target.value, sliderValue2)}
          className="vertical-slider"
          style={{ transform: 'rotate(-90deg)' }}
        />
        <input
          type="range"
          min="0"
          max="100"
          value={sliderValue2}
          onChange={(e) => handleSliderChange(sliderValue1, e.target.value)}
          className="vertical-slider"
          style={{ transform: 'rotate(-90deg)', marginLeft: '100px', marginTop: '-18px'}}
        />
      </div>
    </div>
  );
};

export default TestParam;
