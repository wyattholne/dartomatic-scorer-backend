// src/services/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const api = {
  calibration: {
    async startCalibration() {
      return axios.post(`${API_BASE_URL}/api/calibration/start`);
    },
    async processFrame(frameData: string) {
      return axios.post(`${API_BASE_URL}/api/calibration/process`, { frame: frameData });
    }
  },
  scoring: {
    async processThrow(throwData: any) {
      return axios.post(`${API_BASE_URL}/api/scoring/process-throw`, throwData);
    },
    async getScore() {
      return axios.get(`${API_BASE_URL}/api/scoring/current`);
    }
  }
};