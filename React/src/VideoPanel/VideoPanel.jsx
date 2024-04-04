// Video Panel
// - Streaming Window for Video Feed from Raspi
// - Connects to Raspi server endpoint

import './VideoPanel.css';

import React, { useEffect, useRef, useState } from 'react';

import Tooltip from '../Widgets/Tooltip';

const VideoPanel = () => {
  // API Connections
  const video_endpoint = "http://192.168.1.2:4000/video_feed";
  const video_settings_endpoint = "http://192.168.1.2:4000/update_settings"
  const bitrate_endpoint = "http://192.168.1.2:4000/get_bitrate";

  // Video Quality Config (Client-Side)
  const [bitrate, setBitrate] = useState('Fetching bitrate...'); // Stored as String
  const [resolutionWidth, setResolutionWidth] = useState(320);
  const [resolutionHeight, setResolutionHeight] = useState(240);
  const [quality, setQuality] = useState(40);
  const [frameRate, setFrameRate] = useState(60);
  // For Updating Settings
  const [shouldSaveSettings, setShouldSaveSettings] = useState(false);
  const [imageUrl, setImageUrl] = useState(`${video_endpoint}?${Date.now()}`);

  // Render Window Controls
  const [windowHeight, setWindowHeight] = useState('480px'); // Default height
  const [prevHeight, setPrevHeight] = useState('480px'); // To remember the height before minimizing
  const [isMinimized, setIsMinimized] = useState(false);
  const videoContainerRef = useRef(null);

  // API Requests
  // ----------------------------------------------------------------
  // POST video stream settings updates to Raspi API endpoint
  const saveSettings = async () => {
    try {
      await fetch(video_settings_endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ resolution: [resolutionWidth, resolutionHeight], jpeg_quality: quality, frame_rate: frameRate }),
      });
    } catch (error) {
      console.error('Error saving settings:', error);
    }
    setImageUrl(`${video_endpoint}?${Date.now()}`);
  };

  // // GET bitrate measurement from Raspi API endpoint
  // const fetchBitrate = async () => {
  //   try {
  //     const response = await fetch(bitrate_endpoint);
  //     const data = await response.json();
  //     if (data.avg_bitrate) {
  //       setBitrate(`${Math.floor(data.avg_bitrate/1000)} kbps`);
  //     } else {
  //       setBitrate("Fetching bitrate...");
  //     }
  //   } catch (error) {
  //     console.error('Error fetching bitrate:', error);
  //     setBitrate("Fetching bitrate...");
  //   }
  // };

  // // UseEffect to periodically fetch bitrate
  // useEffect(() => {
  //   fetchBitrate();
  //   const intervalId = setInterval(fetchBitrate, 10000); // Fetch bitrate every 10 seconds

  //   return () => clearInterval(intervalId); // Cleanup interval on component unmount
  // }, []);

  // UseEffect to hook into batch settings changes
  useEffect(() => {
    if (shouldSaveSettings) {
      saveSettings();
      setShouldSaveSettings(false); // Reset flag
    }
  }, [resolutionWidth, resolutionHeight, quality, frameRate, shouldSaveSettings]);


  // Front-End
  // ----------------------------------------------------------------
  // Panel Window Interaction
  // Drag functionality
  const dragStartX = useRef(0);
  const dragStartY = useRef(0);
  const onStartDrag = (e) => {
    dragStartX.current = e.clientX - videoContainerRef.current.offsetLeft;
    dragStartY.current = e.clientY - videoContainerRef.current.offsetTop;
    document.addEventListener('mousemove', onDrag);
    document.addEventListener('mouseup', onStopDrag);
  };

  const onDrag = (e) => {
    videoContainerRef.current.style.left = `${e.clientX - dragStartX.current}px`;
    videoContainerRef.current.style.top = `${e.clientY - dragStartY.current}px`;
  };

  const onStopDrag = () => {
    document.removeEventListener('mousemove', onDrag);
    document.removeEventListener('mouseup', onStopDrag);
  };

  // ToggleMinimize
  const toggleMinimize = () => {
    if (!isMinimized) {
      // Save current height before minimizing
      setPrevHeight(windowHeight);
      console.log(prevHeight);
      // Minimize the window
      setWindowHeight('90px');
    } else {
      // Restore the window to its previous height
      setWindowHeight(prevHeight);
    }
    setIsMinimized(!isMinimized);
  };

  // Resize Observer
  useEffect(() => {
    const videoContainer = videoContainerRef.current;
  
    if (videoContainer) {
      const resizeObserver = new ResizeObserver(entries => {
        for (let entry of entries) {
          // Assuming you want to track the height, specifically
          const newHeight = entry.contentRect.height;
          setWindowHeight(`${newHeight}px`);
        }
      });
  
      resizeObserver.observe(videoContainer);
  
      // Clean up
      return () => {
        resizeObserver.unobserve(videoContainer);
      };
    }
  }, [windowHeight]); 

  // Quick Settings Button Config
  const setLowQuality = () => {
    setResolutionWidth(160);
    setResolutionHeight(120);
    setQuality(60);
    setFrameRate(5);
    setShouldSaveSettings(true);
  };

  const setMediumQuality = () => {
    setResolutionWidth(320);
    setResolutionHeight(240);
    setQuality(40);
    setFrameRate(60);
    setShouldSaveSettings(true);
  };

  const setHighQuality = () => {
    setResolutionWidth(640);
    setResolutionHeight(480);
    setQuality(85);
    setFrameRate(60);
    setShouldSaveSettings(true);
  };

  // Handle Front End Input Field Changes...
  const handleResolutionChangeHeight = (e) => setResolutionHeight(parseInt(e.target.value));
  const handleResolutionChangeWidth = (e) => setResolutionWidth(parseInt(e.target.value));
  const handleQualityChange = (e) => setQuality(parseInt(e.target.value));
  const handleFrameRateChange = (e) => setFrameRate(parseInt(e.target.value));

  // Component Render
  // ----------------------------------------------------------------
  return (
    <div
      className={`video-container ${isMinimized ? 'minimized' : ''}`}
      ref={videoContainerRef}
      style={{ width: isMinimized ? '640px' : '640px', height: windowHeight }}
    >
      <div className="title-bar" onMouseDown={onStartDrag}>
        <span id="bitrateMonitor" className="bitrate-monitor">{bitrate}</span>
        <input type="number" className="quality_settings_field" name="width" value={resolutionWidth} onChange={handleResolutionChangeWidth} />
        <input type="number" className="quality_settings_field" name="height" value={resolutionHeight} onChange={handleResolutionChangeHeight} />
        <Tooltip text="jpeg quality">
          <input type="number" className="quality_settings_field" value={quality} onChange={handleQualityChange} />
        </Tooltip>
        <Tooltip text="fps">
          <input type="number" className="quality_settings_field" value={frameRate} onChange={handleFrameRateChange} />
        </Tooltip>
        <button onClick={setLowQuality}>L</button>
        <button onClick={setMediumQuality}>M</button>
        <button onClick={setHighQuality}>H</button>
        <button onClick={saveSettings}>Save</button>
        <button onClick={toggleMinimize}>{isMinimized ? '[ ]' : '-'}</button>
      </div>
      {!isMinimized && (
         <img className="MainCam" src={imageUrl} alt="Remote Video Feed" width="100%" height="100%" />
      )}
    </div>
  );
};

export default VideoPanel;
