
import { RefObject } from "react";
import { type Toast } from "@radix-ui/react-toast";

type ToastFunction = (props: { title: string; description: string; variant?: "default" | "destructive" }) => void;

export const cleanupCameraStreams = (
  isBrowser: boolean,
  cameraStreams: MediaStream[],
  videoRefs: RefObject<HTMLVideoElement>[],
  setCameraStreams: (streams: MediaStream[]) => void
) => {
  if (!isBrowser) return;
  
  console.log('Cleaning up camera streams...');
  
  cameraStreams.forEach(stream => {
    if (stream) {
      const tracks = stream.getTracks();
      tracks.forEach(track => {
        track.stop();
      });
    }
  });
  
  videoRefs.forEach(ref => {
    if (ref.current) {
      ref.current.srcObject = null;
    }
  });

  setCameraStreams([]);
};

export const getVideoDevices = async (showToast: ToastFunction) => {
  if (typeof navigator === 'undefined' || !navigator?.mediaDevices?.getUserMedia) {
    console.error('MediaDevices API not supported');
    showToast({
      title: "Camera Error",
      description: "Your browser doesn't support camera access",
      variant: "destructive",
    });
    return null;
  }

  try {
    await navigator.mediaDevices.getUserMedia({ video: true });
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(device => device.kind === 'videoinput');
    
    if (videoDevices.length === 0) {
      showToast({
        title: "No Cameras Found",
        description: "Please ensure you have at least one camera connected.",
        variant: "destructive",
      });
      return null;
    }

    return videoDevices;
  } catch (error) {
    console.error('Error accessing camera:', error);
    showToast({
      title: "Camera Access Error",
      description: "Unable to access camera. Please check permissions and try again.",
      variant: "destructive",
    });
    return null;
  }
};

export const initializeCameraStream = async (
  videoDevice: MediaDeviceInfo,
  videoRef: RefObject<HTMLVideoElement>
): Promise<MediaStream | null> => {
  if (!videoRef.current) {
    console.error('Video element not ready');
    return null;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: { exact: videoDevice.deviceId }
      }
    });
    
    if (videoRef.current) {
      videoRef.current.srcObject = stream;
      try {
        await videoRef.current.play();
        console.log('Successfully initialized camera with deviceId:', videoDevice.deviceId);
        return stream;
      } catch (playError) {
        console.error('Play failed, will try to recover:', playError);
        // Let's try one more time after a short delay
        await new Promise(resolve => setTimeout(resolve, 100));
        await videoRef.current.play();
        return stream;
      }
    }
    
    return null;
  } catch (err) {
    console.error('Error initializing camera stream:', err);
    try {
      // Try with basic constraints as fallback
      const fallbackStream = await navigator.mediaDevices.getUserMedia({
        video: true
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = fallbackStream;
        await videoRef.current.play();
        console.log('Successfully initialized camera with fallback constraints');
        return fallbackStream;
      }
    } catch (fallbackErr) {
      console.error('Fallback camera initialization failed:', fallbackErr);
    }
  }
  return null;
};
