import cv2
import cv2.aruco as aruco
import numpy as np

print(cv2.__version__)

def main():
    cap = cv2.VideoCapture(0)

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters()

    print("Press 'q' to quit.")
    
    windowWidth, windowHeight = 1280, 720
    cv2.namedWindow("image_window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image_window", windowWidth, windowHeight)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        displayframe = np.zeros((windowHeight, windowWidth, 3), dtype=np.uint8)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        
        floor_points = [[0,0],[0,0],[0,0],[0,0]]
        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)
            for i, corner in zip(ids, corners):
                if i[0] == 1 or i[0] == 2 or i[0] == 3 or i[0] == 4:
                    points = corner[0]
                    x = int(points[0][0])
                    y = int(points[0][1])
                    if x == 0 and y == 0:
                        pass
                    else:
                        floor_points[i[0] - 1] = [int(points[0][0]), int(points[0][1])]
                        
        camX = floor_points[1][0] - 15
        camY = floor_points[1][1] - 15
        
        tracker_pts = np.array([[15,15], [75,15], [75, 75], [15,75]], dtype=np.int32)
        cv2.fillPoly(displayframe, [tracker_pts], (0, 255, 0))
        
        cam_pts = np.array([[camX + 15,camY + 15], [camX + 75, camY + 15], [camX + 75, camY + 75], [camX + 15, camY + 75]], dtype=np.int32)
        cv2.fillPoly(displayframe, [cam_pts], (0, 255, 0))
        
        cv2.imshow("image_window", displayframe)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()