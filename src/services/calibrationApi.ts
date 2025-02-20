
interface CalibrationStatus {
  status: 'idle' | 'detecting' | 'calibrating' | 'complete' | 'error';
  progress: number;
  message: string;
  intrinsicMatrix?: any;
  distortionCoeffs?: any;
  reprojectionError?: number;
}

class CalibrationApi {
  private baseUrl: string = '/api';  // Keep using relative URL

  private async makeRequest<T>(url: string, options: RequestInit): Promise<T> {
    console.log('Making request to:', url, 'with options:', options);
    
    try {
      const response = await fetch(url, {
        ...options,
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, ${errorText}`);
      }

      const data = await response.json();
      console.log('Response data:', data); // Debug log
      return data;
    } catch (error) {
      console.error('Request failed:', error);
      throw error;
    }
  }

  async startCalibration(imageData?: string): Promise<{ success: boolean, detected?: boolean, message?: string }> {
    try {
      if (!imageData) {
        console.error('No image data provided');
        throw new Error('No image data provided');
      }

      const url = `${this.baseUrl}/capture_checkerboard_image`;
      console.log('Making request to:', url);
      
      return this.makeRequest(url, {
        method: 'POST',
        body: JSON.stringify({ 
          image_data: imageData,
          camera_index: 0
        }),
      });
    } catch (error) {
      console.error('Failed to start calibration:', error);
      throw error;
    }
  }

  async getCalibrationStatus(): Promise<CalibrationStatus> {
    try {
      return this.makeRequest(`${this.baseUrl}/capture_checkerboard_image/status`, {
        method: 'GET',
      });
    } catch (error) {
      console.error('Failed to get calibration status:', error);
      throw error;
    }
  }

  async stopCalibration(): Promise<{ success: boolean }> {
    try {
      return this.makeRequest(`${this.baseUrl}/capture_checkerboard_image/stop`, {
        method: 'POST',
      });
    } catch (error) {
      console.error('Failed to stop calibration:', error);
      throw error;
    }
  }
}

export const calibrationApi = new CalibrationApi();
