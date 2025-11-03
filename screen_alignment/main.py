import cv2
import cv2.aruco as aruco
import numpy as np
import mss

print(cv2.__version__)

def main():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        
        cap = cv2.VideoCapture(0)
        
        cv2.namedWindow("PyProjectFix", cv2.WINDOW_NORMAL)
        #cv2.setWindowProperty("PyProjectFix", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        parameters = aruco.DetectorParameters()

        print("Press 'f' to fimish calibration. Press 'q' to quit.")
        
        calibFinished = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.resize(frame, (monitor["width"], monitor["height"]), interpolation=cv2.INTER_LINEAR)
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
            
            frame = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            h, w = frame.shape[:2]
            
            src_pts = np.float32([[0, 0],
                                [w, 0],
                                [w, h],
                                [0, h]])
            
            if not calibFinished:
                dst_pts = np.float32([[floor_points[1][0], floor_points[1][1]],       # top-left
                                    [floor_points[2][0], floor_points[2][1]],    # top-right
                                    [floor_points[3][0], floor_points[3][1]],# bottom-right
                                    [floor_points[0][0], floor_points[0][1]]])  # bottom-left
                
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(frame, M, (w, h))
            
            cv2.imshow("PyProjectFix V1.0", warped)
            
            if cv2.waitKey(1) & 0xFF == ord("f"):
                calibFinished = True
                print("Sucsessfully stored skew data!")
            elif cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()