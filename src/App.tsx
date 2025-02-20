venv\Scripts\activateimport { useState } from 'react'
import './App.css'

function App() {
  const [calibrationStatus, setCalibrationStatus] = useState('Not calibrated')
  const [lastThrow, setLastThrow] = useState(null)

  const startCalibration = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/calibrate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ markers: [] }),
      })
      const data = await response.json()
      setCalibrationStatus(data.message)
    } catch (error) {
      console.error('Calibration failed:', error)
      setCalibrationStatus('Calibration failed')
    }
  }

  return (
    <div className="container">
      <h1>Dart Scorer</h1>
      
      <div className="card">
        <h2>System Status</h2>
        <p>Calibration: {calibrationStatus}</p>
        <button onClick={startCalibration}>
          Start Calibration
        </button>
      </div>

      <div className="card">
        <h2>Last Throw</h2>
        <p>{lastThrow ? JSON.stringify(lastThrow) : 'No throws recorded'}</p>
      </div>
    </div>
  )
}

export default App