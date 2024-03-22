import React, { useState, useRef } from 'react';
import ReactDOM from 'react-dom';

const Tooltip = ({ children, text }) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const childRef = useRef(); // To reference the child component

  const renderTooltip = () => {
    const tooltipStyle = {
      position: 'fixed', // Positioned relative to the viewport
      top: `${childRef.current.getBoundingClientRect().top + window.scrollY - 30}px`, // Above the element
      left: `${childRef.current.getBoundingClientRect().left + window.scrollX + (childRef.current.offsetWidth / 2)}px`, // Centered
      transform: 'translateX(-50%)',
      backgroundColor: 'black',
      color: 'white',
      padding: '5px',
      borderRadius: '4px',
      whiteSpace: 'nowrap',
      display: 'block',
      fontSize: '12px',
      zIndex: 1000, // Ensure the tooltip is above other content
    };

    return ReactDOM.createPortal(
      <div style={tooltipStyle}>{text}</div>,
      document.body // Appends the tooltip to the body element
    );
  };

  // Clone the child element to attach the ref and event handlers
  const child = React.cloneElement(children, {
    ref: childRef,
    onMouseEnter: () => setShowTooltip(true),
    onMouseLeave: () => setShowTooltip(false),
  });

  return (
    <>
      {child}
      {showTooltip && renderTooltip()}
    </>
  );
};

export default Tooltip;
