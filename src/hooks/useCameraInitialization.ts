
import { RefObject, useEffect, useCallback, useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { useCameraState } from "./useCameraState";
import { cleanupCameraStreams, getVideoDevices, initializeCameraStream } from "@/utils/cameraUtils";

export const useCameraInitialization = (
  videoRefs: RefObject<HTMLVideoElement>[],
  currentStep?: number
) => {
  const { toast } = useToast();
  const {
    cameraDevices,
    setCameraDevices,
    cameraStreams,
    setCameraStreams,
    isBrowser
  } = useCameraState();
  
  const [isInitializing, setIsInitializing] = useState(false);

  const initializeCameras = useCallback(async () => {
    if (!isBrowser || isInitializing) {
      return;
    }

    setIsInitializing(true);
    
    try {
      // First get devices
      const videoDevices = await getVideoDevices(toast);
      if (!videoDevices) {
        setIsInitializing(false);
        return;
      }
      
      setCameraDevices(videoDevices);

      if (videoDevices.length === 0) {
        toast({
          title: "No Cameras Found",
          description: "Please connect a camera and try again.",
          variant: "destructive",
        });
        setIsInitializing(false);
        return;
      }

      // Clean up existing streams before initializing new ones
      await cleanupCameraStreams(isBrowser, cameraStreams, videoRefs, setCameraStreams);

      // Wait a moment for cleanup to complete
      await new Promise(resolve => setTimeout(resolve, 100));

      const requiredCameras = currentStep === 3 ? [0, 2] : [...Array(Math.min(3, videoDevices.length)).keys()];
      const newStreams: MediaStream[] = [];

      // Initialize cameras sequentially to prevent conflicts
      for (const cameraIndex of requiredCameras) {
        try {
          const stream = await initializeCameraStream(videoDevices[cameraIndex], videoRefs[cameraIndex]);
          if (stream) {
            newStreams[cameraIndex] = stream;
          }
          // Add small delay between initializations
          await new Promise(resolve => setTimeout(resolve, 100));
        } catch (err) {
          console.error(`Failed to initialize camera ${cameraIndex}:`, err);
        }
      }

      const validStreams = newStreams.filter(Boolean);
      if (validStreams.length > 0) {
        setCameraStreams(validStreams);
        toast({
          title: "Cameras Initialized",
          description: `Successfully initialized ${validStreams.length} camera(s).`,
        });
      }
    } catch (error) {
      console.error("Camera initialization error:", error);
      toast({
        title: "Camera Error",
        description: "Failed to access cameras. Please check permissions and try again.",
        variant: "destructive",
      });
    } finally {
      setIsInitializing(false);
    }
  }, [isBrowser, cameraStreams, videoRefs, toast, currentStep, isInitializing]);

  useEffect(() => {
    if (!isBrowser) return;

    let mounted = true;

    const initialize = async () => {
      if (!mounted) return;
      if (currentStep !== undefined && (currentStep < 1 || currentStep > 3)) return;

      // Add delay before initial initialization
      await new Promise(resolve => setTimeout(resolve, 500));
      if (mounted) {
        await initializeCameras();
      }
    };

    initialize();

    return () => {
      mounted = false;
      cleanupCameraStreams(isBrowser, cameraStreams, videoRefs, setCameraStreams);
    };
  }, [currentStep, isBrowser, initializeCameras]);

  return { cameraDevices, cameraStreams, initializeCameras, isInitializing };
};

export default useCameraInitialization;
