import cv2
import numpy as np
import os
import math
import time

# Parameters
width = 1920
height = 1080
fps = 60
duration = 60  # 1 minute
total_frames = fps * duration
circle_count = 20
circle_width = 5

# Video setup
epoch_time = int(time.time())
output_folder = 'render'
os.makedirs(output_folder, exist_ok=True)
output_filename = f'{output_folder}/animation_{epoch_time}.mp4'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

# Circle class similar to the JavaScript version
class Circle:
    def __init__(self):
        self.t = np.random.randint(0, 4)
        self.r = 0
        self.a1 = np.random.random() * np.pi * 2
        self.a2 = self.a1 + np.random.random() * np.pi * 2
        self.v = (np.random.random() - 0.5)
    
    def update(self, time_step):
        self.v += (np.random.random() - 0.5) * 0.001
        self.a1 += np.cos(time_step * 0.01) * 0.001 + np.sin(self.v) * 0.01
        self.a2 += np.sin(time_step * 0.01) * 0.001 + np.sin(self.v) * 0.01

# Create circles
circles = [Circle() for _ in range(circle_count)]
for i, circle in enumerate(circles):
    circle.r = i * circle_width + 30

# Drawing loop
start_time = time.time()
for frame_number in range(total_frames):
    # Create a black frame
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    for circle in circles:
        circle.update(frame_number)

        if circle.t == 0:
            cv2.ellipse(frame, (width//2, height//2), (circle.r, circle.r), 0, 
                        np.degrees(circle.a1), np.degrees(circle.a2), 
                        (0, 0, 0), circle_width)
        elif circle.t == 1:
            pts = np.array([[width//2, height//2],
                            [width//2 + int(circle.r * np.cos(circle.a1)), 
                             height//2 + int(circle.r * np.sin(circle.a1))],
                            [width//2 + int(circle.r * np.cos(circle.a2)), 
                             height//2 + int(circle.r * np.sin(circle.a2))]], 
                           np.int32)
            cv2.fillPoly(frame, [pts], (0, 0, 0))
        elif circle.t == 2:
            for j in np.arange(circle.a1, circle.a2, 0.05):
                cv2.ellipse(frame, (width//2, height//2), (circle.r, circle.r), 0, 
                            np.degrees(j), np.degrees(j + 0.02), 
                            (0, 0, 0), circle_width)
            cv2.ellipse(frame, (width//2, height//2), (circle.r, circle.r), 0, 
                        np.degrees(circle.a1), np.degrees(circle.a1 + 0.02), 
                        (0, 0, 0), circle_width + 10)
            cv2.ellipse(frame, (width//2, height//2), (circle.r, circle.r), 0, 
                        np.degrees(circle.a2), np.degrees(circle.a2 + 0.02), 
                        (0, 0, 0), circle_width + 10)
        elif circle.t == 3:
            cv2.ellipse(frame, (width//2, height//2), (circle.r, circle.r), 0, 
                        np.degrees(circle.a1), np.degrees(circle.a2), 
                        (0, 0, 0), 1)
            cv2.circle(frame, (width//2 + int(circle.r * np.cos(circle.a1)), 
                               height//2 + int(circle.r * np.sin(circle.a1))), 
                       3, (0, 0, 0), -1)
            cv2.circle(frame, (width//2 + int(circle.r * np.cos(circle.a2)), 
                               height//2 + int(circle.r * np.sin(circle.a2))), 
                       3, (0, 0, 0), -1)

    # Write frame to video
    out.write(frame)

    # Show statistics
    if frame_number % fps == 0:
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / (frame_number + 1)) * total_frames
        remaining_time = estimated_total_time - elapsed_time
        completion = (frame_number + 1) / total_frames * 100

        print(f'Frame: {frame_number + 1}/{total_frames}, '
              f'Time Passed: {elapsed_time:.2f}s, '
              f'Time Remaining: {remaining_time:.2f}s, '
              f'Estimated Finish: {estimated_total_time:.2f}s, '
              f'Completion: {completion:.2f}%')

# Finalize the video
out.release()
print(f'Video saved to {output_filename}')
