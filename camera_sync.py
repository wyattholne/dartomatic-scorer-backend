from dataclasses import dataclass
from threading import Lock, Event
from typing import Dict, List, Optional
import time
import cv2
import numpy as np

@dataclass
class SyncedFrame:
    timestamp: float
    frames: Dict[str, np.ndarray]
    metadata: Dict[str, any]

class CameraSynchronizer:
    def __init__(self, camera_ids: List[str], sync_threshold_ms: float = 16.67):
        self.camera_ids = camera_ids
        self.sync_threshold = sync_threshold_ms / 1000.0
        self.frame_buffers: Dict[str, List[SyncedFrame]] = {
            cam_id: [] for cam_id in camera_ids
        }
        self.locks: Dict[str, Lock] = {
            cam_id: Lock() for cam_id in camera_ids
        }
        self.sync_event = Event()
        self.last_sync_time = time.time()

    def add_frame(self, camera_id: str, frame: np.ndarray, timestamp: Optional[float] = None):
        if camera_id not in self.camera_ids:
            raise ValueError(f"Unknown camera ID: {camera_id}")

        timestamp = timestamp or time.time()
        
        with self.locks[camera_id]:
            self.frame_buffers[camera_id].append(SyncedFrame(
                timestamp=timestamp,
                frames={camera_id: frame},
                metadata={}
            ))
            
            # Clean old frames
            self._cleanup_old_frames(camera_id)

        # Check if we can sync frames
        self._try_sync()

    def get_synced_frames(self) -> Optional[SyncedFrame]:
        """
        Get the most recent set of synchronized frames
        """
        if not self.sync_event.is_set():
            return None

        synced_frames = {}
        synced_metadata = {}
        sync_timestamp = None

        for camera_id in self.camera_ids:
            with self.locks[camera_id]:
                if not self.frame_buffers[camera_id]:
                    return None
                
                frame_data = self.frame_buffers[camera_id][-1]
                synced_frames.update(frame_data.frames)
                synced_metadata.update(frame_data.metadata)
                
                if sync_timestamp is None:
                    sync_timestamp = frame_data.timestamp

        return SyncedFrame(
            timestamp=sync_timestamp,
            frames=synced_frames,
            metadata=synced_metadata
        )

    def _try_sync(self):
        """
        Attempt to synchronize frames from all cameras
        """
        timestamps = []
        
        for camera_id in self.camera_ids:
            with self.locks[camera_id]:
                if not self.frame_buffers[camera_id]:
                    return
                timestamps.append(self.frame_buffers[camera_id][-1].timestamp)

        if max(timestamps) - min(timestamps) <= self.sync_threshold:
            self.sync_event.set()
            self.last_sync_time = time.time()
        else:
            self.sync_event.clear()

    def _cleanup_old_frames(self, camera_id: str, max_age: float = 1.0):
        """
        Remove frames older than max_age seconds
        """
        current_time = time.time()
        self.frame_buffers[camera_id] = [
            frame for frame in self.frame_buffers[camera_id]
            if current_time - frame.timestamp <= max_age
        ]