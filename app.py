import cv2
from pyzbar.pyzbar import decode

# Open the default camera
cap = cv2.VideoCapture(0)

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Decode barcodes in the frame
    codes = decode(frame)
    for code in codes:
        data = code.data.decode('utf-8')
        print("🔍 Detected:", data)

        # Draw a rectangle around the barcode
        points = code.polygon
        if len(points) > 4:
            hull = cv2.convexHull(points)
            points = hull.reshape(-1, 2)
        for i in range(len(points)):
            cv2.line(frame, tuple(points[i]), tuple(points[(i+1) % len(points)]), (0, 255, 0), 2)

        # Put the decoded data on screen
        x, y = code.rect.left, code.rect.top
        cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Show the video frame
    cv2.imshow('Barcode Scanner', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
