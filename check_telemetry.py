import cv2
import numpy as np

# Create a NumPy array to store the telemetry data
capture = cv2.VideoCapture(0)
while True:
    image = capture.read()[1]
    telemetry_data = np.array([25, 50, 75])

    # Use the `cv2.putText()` function to display the telemetry data on the screen
    cv2.putText(image, "Temperature: {} degrees Celsius".format(telemetry_data[0]), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

    # Display the image using the `cv2.imshow()` function
    cv2.imshow("Telemetry", image)

    if cv2.waitKey(1) == ord('q'):
        break

# Keep the window open until the user presses a key
capture.release()
# Release the image
cv2.destroyAllWindows()