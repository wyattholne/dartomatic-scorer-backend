
import { useState, useCallback } from 'react';
import { useToast } from "@/hooks/use-toast";
import { calibrationApi } from "@/services/calibrationApi";

const useCalibration = () => {
    const [currentCameraIndex, setCurrentCameraIndex] = useState<number>(0);
    const [captureCounts, setCaptureCounts] = useState<{ [key: number]: number }>({});
    const [isCalibrating, setIsCalibrating] = useState<boolean>(false);
    const [isExtrinsicCapturing, setIsExtrinsicCapturing] = useState<boolean>(false);
    const [extrinsicCalibrationResults, setExtrinsicCalibrationResults] = useState<any>(null);
    const { toast } = useToast();

    const handleCameraSwitch = (index: number) => {
        setCurrentCameraIndex(index);
    };

    const captureFrame = useCallback(async () => {
        const videos = document.querySelectorAll('video');
        const videoElement = videos[currentCameraIndex] as HTMLVideoElement;
        
        if (!videoElement || !videoElement.videoWidth) {
            toast({
                title: "Error",
                description: "Camera not ready or no video feed available",
                variant: "destructive",
            });
            return;
        }

        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const ctx = canvas.getContext('2d');
        
        if (!ctx) {
            toast({
                title: "Error",
                description: "Failed to create canvas context",
                variant: "destructive",
            });
            return;
        }

        ctx.drawImage(videoElement, 0, 0);
        const imageData = canvas.toDataURL('image/jpeg');

        try {
            console.log("Sending image data to backend...");
            const result = await calibrationApi.startCalibration(imageData);

            if (result.success) {
                const currentCount = captureCounts[currentCameraIndex] || 0;
                setCaptureCounts(prev => ({
                    ...prev,
                    [currentCameraIndex]: currentCount + 1
                }));

                toast({
                    title: "Success",
                    description: "Image captured successfully",
                });
            }
        } catch (error) {
            console.error("Error sending image:", error);
            toast({
                title: "Error",
                description: "Failed to send image to server",
                variant: "destructive",
            });
        }
    }, [currentCameraIndex, captureCounts, toast]);

    const captureExtrinsicFrame = useCallback(async () => {
        const videos = document.querySelectorAll('video');
        const videoElement = videos[currentCameraIndex] as HTMLVideoElement;
        
        if (!videoElement || !videoElement.videoWidth) {
            toast({
                title: "Error",
                description: "Camera not ready or no video feed available",
                variant: "destructive",
            });
            return;
        }

        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const ctx = canvas.getContext('2d');
        
        if (!ctx) {
            toast({
                title: "Error",
                description: "Failed to create canvas context",
                variant: "destructive",
            });
            return;
        }

        ctx.drawImage(videoElement, 0, 0);
        const imageData = canvas.toDataURL('image/jpeg');

        try {
            setIsExtrinsicCapturing(true);
            const response = await fetch('/api/calibration/extrinsic', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    imageData,
                    cameraIndices: [0, 1]
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            if (data.success) {
                setExtrinsicCalibrationResults(data);
                toast({
                    title: "Success",
                    description: data.message,
                });
            } else {
                toast({
                    title: "Error",
                    description: data.message || "Failed to process image",
                    variant: "destructive",
                });
            }
        } catch (error) {
            console.error("Error sending image:", error);
            toast({
                title: "Error",
                description: "Failed to send image to server",
                variant: "destructive",
            });
        } finally {
            setIsExtrinsicCapturing(false);
        }
    }, [currentCameraIndex, toast]);

    return {
        handleCameraSwitch,
        currentCameraIndex,
        captureFrame,
        captureExtrinsicFrame,
        captureCounts,
        isCalibrating,
        isExtrinsicCapturing,
        extrinsicCalibrationResults,
    };
};

export default useCalibration;
