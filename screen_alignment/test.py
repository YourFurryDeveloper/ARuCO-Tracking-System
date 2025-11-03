import mss

with mss.mss() as sct:
    monitor = sct.monitors[2]
    
    while True:
        frame = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        h, w = frame.shape[:2]

        # Original corners (top-left, top-right, bottom-right, bottom-left)
        src_pts = np.float32([[0, 0],
                            [w, 0],
                            [w, h],
                            [0, h]])

        # Destination corners (skewed)
        dst_pts = np.float32([[100, 100],       # top-left moves right/down
                            [w - 200, 50],    # top-right moves left/up
                            [w - 100, h - 50],# bottom-right moves slightly up
                            [150, h - 100]])  # bottom-left moves right/up
            
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(frame, M, (w, h))

        cv2.imshow("PyProjectFix V1.0", warped)
        
        if cv2.waitKey(1) == 27:  # ESC to quit
            break