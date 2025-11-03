import cv2
import cv2.aruco as aruco
import numpy as np

print(cv2.__version__)

def main():
    cap = cv2.VideoCapture(0)

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters()

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

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
                        #floor_points[i[0] - 1] = [int(floor_points[i][0][0]), int(floor_points[i][0][1])]
                    else:
                        floor_points[i[0] - 1] = [int(points[0][0]), int(points[0][1])]

        #for fpnum in range(4):
            #if not fpnum == 3:
                #cv2.line(frame, (floor_points[fpnum][0], floor_points[fpnum][1]), (floor_points[fpnum + 1][0], floor_points[fpnum + 1][1]), (0, 255, 0), 3)
            #else:
                #cv2.line(frame, (floor_points[fpnum][0], floor_points[fpnum][1]), (floor_points[0][0], floor_points[0][1]), (0, 255, 0), 3)
                
        pts = np.array(floor_points, dtype=np.int32)
        noCamFrame = np.zeros((720, 1280, 3), dtype=np.uint8)
        cv2.fillPoly(frame, [pts], (0, 255, 0))


        cv2.imshow("ArUco Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()