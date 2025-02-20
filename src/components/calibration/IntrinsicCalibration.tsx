
import React, { type RefObject } from 'react';
import { Button } from "@/components/ui/button";
import { Camera, RefreshCw } from "lucide-react";
import { motion } from "framer-motion";

interface IntrinsicCalibrationProps {
    videoRefs: RefObject<HTMLVideoElement>[];
    canvasRef: RefObject<HTMLCanvasElement>;
    cameraDevices: MediaDeviceInfo[];
    initializeCameras?: () => Promise<void>;
    handleCameraSwitch: (index: number) => void;
    cameraIndex: number;
    captureCount?: number;
    onCapture?: () => void;
    isCapturing?: boolean;
}

const IntrinsicCalibration: React.FC<IntrinsicCalibrationProps> = ({
    videoRefs,
    canvasRef,
    cameraDevices = [],
    initializeCameras,
    handleCameraSwitch,
    cameraIndex,
    captureCount = 0,
    onCapture,
    isCapturing = false,
}) => {
    const totalRequiredImages = 15;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
        >
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-medium text-neutral-800">
                    Step 2: Intrinsic Calibration - Camera {cameraIndex + 1}
                </h2>
                <Button
                    variant="outline"
                    onClick={initializeCameras}
                    className="flex items-center gap-2"
                >
                    <RefreshCw className="h-4 w-4" />
                    Refresh Feeds
                </Button>
            </div>
            <div className="p-6 bg-neutral-50 rounded-lg border border-neutral-200">
                <h3 className="text-lg font-medium text-neutral-700 mb-4">Instructions:</h3>
                <ol className="list-decimal list-inside space-y-3 text-neutral-600">
                    <li>Position the 8x6 checkerboard pattern in front of Camera {cameraIndex + 1}</li>
                    <li>Hold the pattern approximately 30-40cm from the camera lens</li>
                    <li>Capture at least 15 different pattern positions:
                        <ul className="list-disc list-inside ml-6 mt-2 space-y-2">
                            <li>Tilt the pattern at various angles (approximately ±45°)</li>
                            <li>Move it to different parts of the camera's field of view</li>
                            <li>Rotate the pattern to capture different orientations</li>
                        </ul>
                    </li>
                </ol>
            </div>

            <div className="flex gap-4 mt-6 mb-6">
                {[0, 1, 2].map((index) => (
                    <Button
                        key={index}
                        onClick={() => handleCameraSwitch(index)}
                        variant={cameraIndex === index ? "default" : "outline"}
                        className={`flex-1 ${cameraIndex === index ? 'bg-blue-500 hover:bg-blue-700' : 'hover:bg-blue-50'}`}
                    >
                        Camera {index + 1}
                    </Button>
                ))}
            </div>

            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="aspect-video bg-black rounded-lg overflow-hidden relative">
                    <video
                        ref={videoRefs[cameraIndex]}
                        autoPlay
                        playsInline
                        muted
                        className="w-full h-full object-cover"
                    />
                    <canvas
                        ref={canvasRef}
                        className="hidden"
                    />
                    <div className="absolute top-2 left-2 bg-black/50 text-white px-2 py-1 rounded text-sm">
                        Camera {cameraIndex + 1} Feed
                    </div>
                    <Button 
                        className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-blue-500 hover:bg-blue-700"
                        onClick={onCapture}
                        disabled={isCapturing}
                        size="lg"
                    >
                        <Camera className="mr-2 h-5 w-5" />
                        {isCapturing ? 'Capturing...' : 'Capture Image'}
                    </Button>
                </div>

                <div className="space-y-4">
                    <div className="p-4 bg-neutral-50 rounded-lg border border-neutral-200">
                        <h4 className="font-medium text-neutral-700 mb-2">Calibration Progress</h4>
                        <p className="text-neutral-600">Images captured: {captureCount}/{totalRequiredImages}</p>
                        {captureCount >= totalRequiredImages && (
                            <p className="text-green-600 mt-2 font-medium">✓ Required images captured</p>
                        )}
                    </div>
                    <Button
                        onClick={initializeCameras}
                        className="w-full bg-blue-500 hover:bg-blue-700 text-white"
                        size="lg"
                    >
                        <RefreshCw className="mr-2 h-5 w-5" />
                        Refresh Camera Feed
                    </Button>
                </div>
            </div>
        </motion.div>
    );
};

export default IntrinsicCalibration;
