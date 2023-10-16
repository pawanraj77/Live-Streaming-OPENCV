import cv2
import zmq
import numpy as np
import pygame
import json

context = zmq.Context()

# Create a socket to receive video frames
video_socket = context.socket(zmq.SUB)
video_socket.connect("tcp://192.168.29.208:5555")
video_socket.setsockopt_string(zmq.SUBSCRIBE, "")

# Create a socket to receive telemetry data
telemetry_socket = context.socket(zmq.SUB)
telemetry_socket.connect("tcp://192.168.29.208:5556")
telemetry_socket.setsockopt_string(zmq.SUBSCRIBE, "")

pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Remote Stream")

# Initialize Pygame font for displaying telemetry data
font = pygame.font.Font(None, 24)
font_color = (255, 255, 255)  # White text color

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cv2.destroyAllWindows()
            exit()

    try:
        # Receive and decode video frame
        frame_data = video_socket.recv()
        if not frame_data:
            continue  # Skip empty frames

        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

        if frame is None:
            continue  # Skip frames that could not be decoded

        # Resize the frame to fit the screen
        frame = cv2.resize(frame, (screen_width, screen_height))  # Swap dimensions
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate 90 degrees clockwise

        # Display the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)
        screen.blit(frame_surface, (0, 0))

    except zmq.ZMQError as e:
        print(f"ZMQ Error: {e}")
    except cv2.error as e:
        print(f"OpenCV Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        # Receive and parse telemetry data
        telemetry_data = telemetry_socket.recv().decode('utf-8')
        telemetry_data_dict = json.loads(telemetry_data)

        # Render and display telemetry data
        text_y = screen_height - 150
        for key, value in telemetry_data_dict.items():
            telemetry_text = f"{key}: {value}"
            text_surface = font.render(telemetry_text, True, font_color)
            text_position = (10, text_y)
            screen.blit(text_surface, text_position)
            text_y += 30  # Adjust the vertical spacing

    except zmq.ZMQError as e:
        print(f"ZMQ Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    pygame.display.update()

# Release resources
pygame.quit()
cv2.destroyAllWindows()
