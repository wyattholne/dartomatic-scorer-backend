import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ProgressIndicator } from '@/components/ProgressIndicator';
import { CalibrationStep } from '@/components/CalibrationStep';
import { EnhancedCameraView } from '@/components/EnhancedCameraView';
import { DartTrackingOverlay } from '@/components/DartTrackingOverlay';
import { CalibrationData } from '@/types/calibration';

interface CalibrationWorkflowProps {
  onComplete: (data: CalibrationData) => void;
}

export const CalibrationWorkflow = ({ onComplete }: CalibrationWorkflowProps) => {
  const [step, setStep] = useState(0);
  const [calibrationData, setCalibrationData] = useState<CalibrationData>();

  const steps = [
    {
      title: "Camera Setup",
      description: "Position your cameras for optimal dart tracking",
      component: (
        <CalibrationStep
          title="Camera Positioning"
          description="Ensure both cameras have a clear view of the dartboard"
        >
          <div className="grid grid-cols-2 gap-4">
            <EnhancedCameraView className="rounded-lg overflow-hidden" />
            <EnhancedCameraView className="rounded-lg overflow-hidden" />
          </div>
        </CalibrationStep>
      )
    },
    // Add more steps...
  ];

  return (
    <div className="space-y-8">
      <ProgressIndicator 
        steps={steps.map(s => s.title)}
        currentStep={step}
        className="mb-8"
      />
      
      {steps[step].component}
      
      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={() => setStep(s => Math.max(0, s - 1))}
          disabled={step === 0}
        >
          Previous
        </Button>
        <Button
          onClick={() => {
            if (step === steps.length - 1) {
              onComplete(calibrationData!);
            } else {
              setStep(s => s + 1);
            }
          }}
        >
          {step === steps.length - 1 ? 'Complete' : 'Next'}
        </Button>
      </div>
    </div>
  );
};