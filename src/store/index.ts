import { configureStore } from '@reduxjs/toolkit';
import calibrationReducer from './slices/calibrationSlice';
import scoringReducer from './slices/scoringSlice';

export const store = configureStore({
  reducer: {
    calibration: calibrationReducer,
    scoring: scoringReducer
  }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;