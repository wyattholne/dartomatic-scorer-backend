
import { motion } from "framer-motion";

export const WizardHeader = () => {
  return (
    <div className="px-6 py-4 border-b border-neutral-200">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-medium text-neutral-800">
          Artificial Intelligence Calibration Wizard
        </h1>
        <div className="flex gap-2">
          <button
            className="w-3 h-3 rounded-full bg-neutral-200 hover:bg-yellow-400 transition-colors"
            aria-label="minimize"
          />
          <button
            className="w-3 h-3 rounded-full bg-neutral-200 hover:bg-green-400 transition-colors"
            aria-label="maximize"
          />
          <button
            className="w-3 h-3 rounded-full bg-neutral-200 hover:bg-red-400 transition-colors"
            aria-label="close"
          />
        </div>
      </div>
    </div>
  );
};

