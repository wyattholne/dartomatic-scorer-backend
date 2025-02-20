
import React, { type RefObject, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { RefreshCw, Camera } from "lucide-react";
import { motion } from "framer-motion";
import { useToast } from "@/hooks/use-toast";
import { calibrationApi } from "@/services/calibrationApi";

interface ExtrinsicCalibrationProps {
    videoRefs: RefObject<HTMLVideoElement>[];
    canvasRef: RefObject<HTMLCanvasElement>;
    cameraDevices: any[];
    initializeCameras?: () => Promise<void>;
}

const ExtrinsicCalibration: React.FC<ExtrinsicCalibrationProps> = ({
    videoRefs,
    canvasRef,
    cameraDevices,
    initializeCameras
}) => {
    const { toast } = useToast();
    const selectedCameras = [0, 2]; // Only show cameras 0 and 2

    // Initialize cameras when component mounts
    useEffect(() => {
        if (initializeCameras) {
            console.log('ExtrinsicCalibration mounted, initializing cameras...');
            initializeCameras();
        }
    }, [initializeCameras]);

    const captureImage = async () => {
        try {
            // Log the video elements we're trying to capture from
            console.log('Video refs:', videoRefs);
            console.log('Video 0:', videoRefs[0]?.current);
            console.log('Video 2:', videoRefs[2]?.current);

            // Capture from both cameras and combine into one canvas
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            if (!ctx) {
                throw new Error('Could not get canvas context');
            }

            // Get video elements
            const video0 = videoRefs[0]?.current;
            const video2 = videoRefs[2]?.current;

            if (!video0 || !video2) {
                console.error('Missing video elements:', { video0, video2 });
                throw new Error('Camera feeds not available');
            }

            // Log video dimensions
            console.log('Video 0 dimensions:', video0.videoWidth, video0.videoHeight);
            console.log('Video 2 dimensions:', video2.videoWidth, video2.videoHeight);

            if (!video0.videoWidth || !video2.videoWidth) {
                throw new Error('Video feeds not ready - no dimensions available');
            }

            // Set canvas width to accommodate both videos side by side
            canvas.width = video0.videoWidth + video2.videoWidth;
            canvas.height = Math.max(video0.videoHeight, video2.videoHeight);

            // Draw both video feeds onto the canvas
            ctx.drawImage(video0, 0, 0);
            ctx.drawImage(video2, video0.videoWidth, 0);

            // Convert canvas to base64
            const imageData = canvas.toDataURL('image/jpeg');
            console.log('Generated image data length:', imageData.length);

            // Send to backend
            const result = await calibrationApi.startCalibration(imageData);
            console.log('Backend response:', result);

            if (result.success) {
                toast({
                    title: "Success",
                    description: result.message || "Image captured successfully",
                });
            } else if (result.detected === false) {
                toast({
                    title: "Warning",
                    description: "No checkerboard pattern detected. Please adjust the position.",
                    variant: "destructive",
                });
            } else {
                throw new Error(result.message || 'Failed to process image');
            }
        } catch (error) {
            console.error('Error capturing image:', error);
            toast({
                title: "Error",
                description: error instanceof Error ? error.message : "Failed to capture image",
                variant: "destructive",
            });
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
        >
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-medium text-neutral-800">
                    Step 3: Extrinsic Calibration
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
                    <li>Position the checkerboard so it's visible to both cameras you want to calibrate</li>
                    <li>Ensure good lighting and minimal reflections</li>
                    <li>Press 'Capture Frame' to capture the image from both cameras</li>
                    <li>Extrinsic Calibration will begin automatically when 15 images are captured</li>
                </ol>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {selectedCameras.map((cameraIndex, index) => (
                    <div key={index} className="relative aspect-video bg-black rounded-lg overflow-hidden">
                        <video
                            ref={videoRefs[cameraIndex]}
                            autoPlay
                            playsInline
                            muted
                            className="w-full h-full object-contain"
                        />
                        <div className="absolute top-2 left-2 bg-black/50 text-white px-2 py-1 rounded text-sm">
                            Camera {cameraIndex}
                        </div>
                    </div>
                ))}
            </div>
            <div className="flex justify-between items-center mt-4">
                <Button
                    onClick={initializeCameras}
                    variant="outline"
                    className="bg-white hover:bg-gray-100"
                >
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Refresh Cameras
                </Button>
                <Button
                    onClick={captureImage}
                    className="bg-blue-500 hover:bg-blue-600 text-white"
                >
                    <Camera className="mr-2 h-4 w-4" />
                    Capture Frame
                </Button>
            </div>
        </motion.div>
    );
};

export default ExtrinsicCalibration;
