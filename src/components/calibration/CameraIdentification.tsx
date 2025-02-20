
import { Camera } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { RefObject, useState } from "react";
import { useToast } from "@/hooks/use-toast";

interface CameraIdentificationProps {
  videoRefs: RefObject<HTMLVideoElement>[];
  initializeCameras: () => Promise<void>;
  cameraDevices: MediaDeviceInfo[];
}

export const CameraIdentification = ({
  videoRefs,
  initializeCameras,
  cameraDevices = [],
}: CameraIdentificationProps) => {
  const [debugOutput, setDebugOutput] = useState<string>("");
  const { toast } = useToast();

  const handleRefreshCameras = async () => {
    console.log("Refresh Camera Feeds Button Clicked");
    await initializeCameras();
  };

  const handleDebugListCameras = () => {
    const cameraList = cameraDevices.map((device, index) => 
      `Camera ${index}: ${device.label} (${device.deviceId})`
    ).join('\n');
    
    setDebugOutput(cameraList || "No cameras detected");
    console.log("Available cameras:", cameraDevices);
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <h2 className="text-2xl font-medium text-neutral-800 mb-2">
          Step 1: Camera Identification
        </h2>
        <p className="text-neutral-600 leading-relaxed mb-4">
          Please verify the three cameras below are working correctly. Each camera should show a live feed.
        </p>
        
        {(!cameraDevices || cameraDevices.length === 0) && (
          <div className="bg-yellow-50 p-4 rounded-lg mb-6 text-yellow-800 border border-yellow-200">
            No cameras detected. Please ensure your cameras are connected and you have granted camera permissions.
          </div>
        )}
      </motion.div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {videoRefs.map((videoRef, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + index * 0.1 }}
            className="relative aspect-video bg-neutral-900 rounded-lg overflow-hidden"
          >
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover"
            />
            <div className="absolute top-2 left-2 bg-black/50 text-white px-2 py-1 rounded text-sm">
              Camera {index}
            </div>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="flex flex-col items-center gap-4"
      >
        <div className="flex gap-4">
          <Button
            onClick={handleRefreshCameras}
            className="bg-blue-500 hover:bg-blue-600"
          >
            <Camera className="mr-2" />
            Refresh Camera Feeds
          </Button>
          <Button
            onClick={handleDebugListCameras}
            variant="outline"
          >
            Debug: List Cameras
          </Button>
        </div>

        {debugOutput && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            className="w-full mt-4 p-4 bg-neutral-100 rounded-lg border border-neutral-200"
          >
            <h3 className="text-sm font-medium text-neutral-800 mb-2">Camera List Output (Debug)</h3>
            <pre className="text-sm text-neutral-600 whitespace-pre-wrap">{debugOutput}</pre>
          </motion.div>
        )}
      </motion.div>
    </>
  );
};
