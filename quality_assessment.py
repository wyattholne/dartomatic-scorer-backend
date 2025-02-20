import numpy as np

class QualityAssessor:
    def __init__(self):
        self.min_markers = 4
        self.scores_history = []

    def assess_detection_quality(self, corners, ids) -> float:
        """Assess the quality of ArUco marker detection"""
        if ids is None or len(ids) == 0:
            return 0.0

        num_markers = len(ids)
        if num_markers < self.min_markers:
            return num_markers / self.min_markers

        # Assess marker distribution in the image
        centers = np.mean(corners[0], axis=1)
        std_dev = np.std(centers, axis=0)
        distribution_score = min(1.0, np.mean(std_dev) / 100.0)

        self.scores_history.append(distribution_score)
        if len(self.scores_history) > 10:
            self.scores_history.pop(0)

        return distribution_score

    def get_latest_scores(self):
        """Get the most recent quality scores"""
        return self.scores_history[-5:] if self.scores_history else []