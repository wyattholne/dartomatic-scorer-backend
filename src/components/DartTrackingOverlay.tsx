import { useEffect, useRef } from 'react';
import { CalibrationData, MarkerDetectionResult } from '@/types/calibration';
import { cn } from '@/lib/utils';

interface DartTrackingOverlayProps {
  calibrationData?: CalibrationData;
  markers?: MarkerDetectionResult[];
  className?: string;
}

export const DartTrackingOverlay = ({
  calibrationData,
  markers,
  className
}: DartTrackingOverlayProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current || !calibrationData || !markers) return;

    const ctx = canvasRef.current.getContext('2d');
    if (!ctx) return;

    // Clear previous frame
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);

    // Draw markers
    markers.forEach(marker => {
      drawMarker(ctx, marker, calibrationData);
    });

    // Draw scoring zones
    drawScoringZones(ctx, calibrationData);
  }, [calibrationData, markers]);

  return (
    <div className={cn(
      "absolute inset-0 pointer-events-none",
      "animate-fade-in",
      className
    )}>
      <canvas 
        ref={canvasRef}
        className="w-full h-full"
        style={{
          background: 'transparent',
          mixBlendMode: 'overlay'
        }}
      />
      
      {/* Status Overlay */}
      <div className="absolute top-4 right-4 bg-background/80 p-4 rounded-lg">
        <div className="space-y-2 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-accent" />
            <span>System Calibrated</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-primary animate-marker-pulse" />
            <span>Tracking Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};