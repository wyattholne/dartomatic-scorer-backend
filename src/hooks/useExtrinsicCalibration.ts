
import { useState, useEffect } from "react";
import { useToast } from "@/components/ui/use-toast";
import { calibrationApi } from "@/services/calibrationApi";

interface CalibrationProgress {
  status: 'idle' | 'detecting' | 'calibrating' | 'complete' | 'error';
  progress: number;
  message: string;
}

export const useExtrinsicCalibration = () => {
  const { toast } = useToast();
  const [isCalibrating, setIsCalibrating] = useState(false);
  const [calibrationProgress, setCalibrationProgress] = useState<CalibrationProgress>({
    status: 'idle',
    progress: 0,
    message: 'Ready to start calibration'
  });

  useEffect(() => {
    let statusInterval: NodeJS.Timeout;

    const pollStatus = async () => {
      try {
        const status = await calibrationApi.getCalibrationStatus();
        setCalibrationProgress(status);
        
        if (status.status === 'complete' || status.status === 'error') {
          setIsCalibrating(false);
          clearInterval(statusInterval);
          
          toast({
            title: status.status === 'complete' ? "Calibration Complete" : "Calibration Error",
            description: status.message,
            variant: status.status === 'complete' ? "default" : "destructive",
          });
        }
      } catch (error) {
        console.error('Failed to get calibration status:', error);
        toast({
          title: "Error",
          description: "Failed to get calibration status",
          variant: "destructive",
        });
      }
    };

    if (isCalibrating) {
      statusInterval = setInterval(pollStatus, 1000);
    }

    return () => {
      if (statusInterval) {
        clearInterval(statusInterval);
      }
    };
  }, [isCalibrating, toast]);

  const startCalibration = async () => {
    try {
      setIsCalibrating(true);
      setCalibrationProgress({
        status: 'detecting',
        progress: 0,
        message: 'Starting calibration...'
      });

      const result = await calibrationApi.startCalibration();
      
      if (!result.success) {
        throw new Error('Failed to start calibration');
      }

      toast({
        title: "Starting Extrinsic Calibration",
        description: "Place the checkerboard so it is visible to all cameras.",
      });
    } catch (error) {
      console.error('Failed to start calibration:', error);
      setIsCalibrating(false);
      setCalibrationProgress({
        status: 'error',
        progress: 0,
        message: 'Failed to start calibration'
      });
      
      toast({
        title: "Error",
        description: "Failed to start calibration",
        variant: "destructive",
      });
    }
  };

  const stopCalibration = async () => {
    try {
      await calibrationApi.stopCalibration();
      setIsCalibrating(false);
      setCalibrationProgress({
        status: 'idle',
        progress: 0,
        message: 'Calibration stopped'
      });
      
      toast({
        title: "Calibration Stopped",
        description: "Extrinsic calibration has been stopped.",
      });
    } catch (error) {
      console.error('Failed to stop calibration:', error);
      toast({
        title: "Error",
        description: "Failed to stop calibration",
        variant: "destructive",
      });
    }
  };

  return {
    isCalibrating,
    calibrationProgress,
    startCalibration,
    stopCalibration
  };
};
