import cv2
import cv2.aruco as aruco

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

        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)
            for i, corner in zip(ids, corners):
                print(f"Detected marker ID: {i[0]}")
                points = corner[0]

        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.imshow("ArUco Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()