import cv2
import cv2.aruco as aruco

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
marker_id = 1
marker_size = 200

markers_to_create = 4

for i in range(markers_to_create):
    marker_img = aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    cv2.imwrite(f"aruco_marker_{marker_id}.png", marker_img)
    print(f"Saved aruco_marker_{marker_id}.png")
    marker_id += 1