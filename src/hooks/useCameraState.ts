
import { useState } from "react";

interface CameraState {
  cameraDevices: MediaDeviceInfo[];
  setCameraDevices: (devices: MediaDeviceInfo[]) => void;
  cameraStreams: MediaStream[];
  setCameraStreams: (streams: MediaStream[]) => void;
  isBrowser: boolean;
}

export const useCameraState = (): CameraState => {
  const [cameraDevices, setCameraDevices] = useState<MediaDeviceInfo[]>([]);
  const [cameraStreams, setCameraStreams] = useState<MediaStream[]>([]);
  const [isBrowser] = useState(typeof window !== 'undefined');

  return {
    cameraDevices,
    setCameraDevices,
    cameraStreams,
    setCameraStreams,
    isBrowser
  };
};

export default useCameraState;
