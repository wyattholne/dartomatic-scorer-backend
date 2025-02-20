import { useState, useCallback, useRef } from 'react';

export const useWebcam = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const startStream = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsStreaming(true);
      }
    } catch (error) {
      console.error('Failed to start webcam:', error);
    }
  }, []);

  return { videoRef, isStreaming, startStream };
};