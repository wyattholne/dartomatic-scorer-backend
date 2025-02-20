
import { RefObject } from "react";
import { Button } from "@/components/ui/button";
import { RefreshCw } from "lucide-react";
import { motion } from "framer-motion";

interface ExtrinsicCalibrationCameraProps {
  videoRef: RefObject<HTMLVideoElement>;
  index: number;
  isCalibrating: boolean;
  calibrationStatus: 'detecting' | string;
  initializeCameras: () => Promise<void>;
}

export const ExtrinsicCalibrationCamera = ({
  videoRef,
  index,
  isCalibrating,
  calibrationStatus,
  initializeCameras,
}: ExtrinsicCalibrationCameraProps) => {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.1 }}
      className="aspect-video bg-black rounded-lg overflow-hidden relative group"
    >
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="w-full h-full object-cover"
      />
      <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/50 opacity-0 group-hover:opacity-100 transition-opacity" />
      <div className="absolute top-2 left-2 bg-black/50 text-white px-2 py-1 rounded text-sm">
        Camera {index + 1}
      </div>
      <Button
        onClick={initializeCameras}
        className="absolute bottom-4 right-4 bg-white hover:bg-gray-100 text-black shadow-lg"
        size="default"
      >
        <RefreshCw className="w-4 h-4 mr-2" />
        Refresh Camera
      </Button>
      {isCalibrating && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="absolute bottom-2 left-2 right-2 bg-black/50 text-white px-2 py-1 rounded text-sm"
        >
          {calibrationStatus === 'detecting' ? 'Detecting pattern...' : 'Processing...'}
        </motion.div>
      )}
    </motion.div>
  );
};
