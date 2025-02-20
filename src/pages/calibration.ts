export interface CalibrationData {
  matrix: number[][];
  cameraPositions: {
    [cameraId: string]: {
      position: [number, number, number];
      rotation: [number, number, number];
    };
  };
  confidence: number;
}

export interface MarkerDetectionResult {
  id: number;
  corners: number[][];
  tvec?: number[];
  rvec?: number[];
  confidence: number;
}

export type CalibrationStatus = 'idle' | 'detecting' | 'calibrating' | 'complete' | 'error';

export interface CalibrationProgress {
  status: CalibrationStatus;
  progress: number;
  message: string;
}
