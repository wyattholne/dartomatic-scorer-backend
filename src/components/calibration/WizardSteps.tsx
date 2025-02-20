
import { Camera, Play, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { useRef, useState } from "react";
import { useToast } from "@/components/ui/use-toast";

export const WIZARD_STEPS = [
  "Camera Identification",
  "Intrinsic Calibration",
  "Extrinsic Calibration",
  "Dartboard Registration",
  "Verification",
  "Save/Load",
] as const;

export const CHECKERBOARD_SIZE = { width: 8, height: 6 };
export const MIN_CAPTURES_REQUIRED = 15;

interface StepIndicatorProps {
  currentStep: number;
}

export const StepIndicator = ({ currentStep }: StepIndicatorProps) => {
  return (
    <div className="flex items-center justify-between mb-8 relative">
      <div className="absolute top-1/2 left-0 w-full h-0.5 bg-neutral-200 -z-10" />
      {WIZARD_STEPS.map((step, index) => (
        <div
          key={step}
          className="flex flex-col items-center gap-2"
        >
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: index * 0.1 }}
            className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium border-2 ${
              index + 1 === currentStep
                ? "border-purple-500 bg-purple-500 text-white"
                : "border-neutral-300 bg-white text-neutral-500"
            }`}
          >
            {index + 1}
          </motion.div>
          <span
            className={`text-xs whitespace-nowrap ${
              index + 1 === currentStep
                ? "text-purple-500 font-medium"
                : "text-neutral-500"
            }`}
          >
            {step}
          </span>
        </div>
      ))}
    </div>
  );
};
