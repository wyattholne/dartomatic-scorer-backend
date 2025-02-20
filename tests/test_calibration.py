// filepath: tests/test_calibration.py
import pytest
from app.services.calibration import CalibrationService

def test_calibration_process():
    service = CalibrationService()
    result = service.process_frame(mock_frame_data)
    assert result['status'] == 'success'
    assert 'markers' in result
```

#### 3.2 Frontend Tests

Create a new file `CalibrationView.test.tsx` in the `src/__tests__` directory:

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { CalibrationView } from '../components/CalibrationView';

test('starts calibration process', async () => {
  render(<CalibrationView />);
  const startButton = screen.getByText('Start Calibration');
  fireEvent.click(startButton);
  expect(await screen.findByText('Calibrating...')).toBeInTheDocument();
});
```

### Step 4: Development Environment

#### 4.1 Add Docker support

Create a new `Dockerfile` in the root directory:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

#### 4.2 Add docker-compose

Create a new `docker-compose.yml` in the root directory:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
    environment:
      - FLASK_ENV=development
      
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
```

By following these steps one by one, you can gradually implement the improvements without feeling overwhelmed. Let me know if you need help with any specific part!// filepath: tests/test_calibration.py
import pytest
from app.services.calibration import CalibrationService

def test_calibration_process():
    service = CalibrationService()
    result = service.process_frame(mock_frame_data)
    assert result['status'] == 'success'
    assert 'markers' in result
```

#### 3.2 Frontend Tests

Create a new file `CalibrationView.test.tsx` in the `src/__tests__` directory:

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { CalibrationView } from '../components/CalibrationView';

test('starts calibration process', async () => {
  render(<CalibrationView />);
  const startButton = screen.getByText('Start Calibration');
  fireEvent.click(startButton);
  expect(await screen.findByText('Calibrating...')).toBeInTheDocument();
});
```

### Step 4: Development Environment

#### 4.1 Add Docker support

Create a new `Dockerfile` in the root directory:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

#### 4.2 Add docker-compose

Create a new `docker-compose.yml` in the root directory:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
    environment:
      - FLASK_ENV=development
      
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
```

By following these steps one by one, you can gradually implement the improvements without feeling overwhelmed. Let me know if you need help with any specific part!