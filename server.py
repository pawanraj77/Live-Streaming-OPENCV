import cv2
import numpy as np
import zmq
import psutil

context = zmq.Context()
video_socket = context.socket(zmq.PUB)
video_socket.bind("tcp://192.168.29.208:5555")

telemetry_socket = context.socket(zmq.PUB)
telemetry_socket.bind("tcp://192.168.29.208:5556")

cap1 = cv2.VideoCapture(0)

while True:
    ret1, frame1 = cap1.read()

    if not ret1:
        break

    _, frame1 = cv2.imencode('.JPEG', frame1)

    video_socket.send_multipart([b'frame1', frame1])

    telemetry_data = {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "network_bytes_sent": psutil.net_io_counters().bytes_sent,
        "network_bytes_received": psutil.net_io_counters().bytes_recv
    }

    telemetry_socket.send_json(telemetry_data)

cap1.release()
