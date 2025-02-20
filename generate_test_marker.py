import cv2
import numpy as np

# Use same dictionary as detection code
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Settings for good detection
marker_size = 200  # Made smaller to fit 4 on page
border_size = 20
spacing = 40  # Space between markers

# Create a page (A4 paper ratio approximately)
page_width = marker_size * 2 + spacing * 3 + border_size * 4
page_height = page_width * 1.414  # A4 ratio
page = np.full((int(page_height), int(page_width)), 255, dtype=np.uint8)

# Generate 4 markers in a 2x2 grid
for row in range(2):
    for col in range(2):
        marker_id = row * 2 + col
        marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
        
        # Calculate position
        x = col * (marker_size + spacing + border_size * 2) + border_size
        y = row * (marker_size + spacing + border_size * 2) + border_size
        
        # Place marker on page
        page[y:y+marker_size, x:x+marker_size] = marker_image
        
        # Add marker ID text
        cv2.putText(page, f"ID: {marker_id}", (x, y-5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)

# Save the page
cv2.imwrite('all_markers.png', page)
print("Generated page with all 4 markers")
