import cv2
import numpy as np
from PIL import Image

cap = cv2.VideoCapture("test.mkv")


# Get video properties (e.g., frame count and frame width)
# frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get total number of frames in the video
# fps = cap.get(cv2.CAP_PROP_FPS)  
# print(f"Total frames: {frame_count}, FPS: {fps}")
 
# # Read and display each frame of the video
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("End of video or error occurred.")
#         break
 
#     # Display the frame
#     cv2.imshow("Video Frame", frame)
 
#     # Wait for 1ms for key press to continue or exit if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


 
# Open the video file
cap = cv2.VideoCapture("test.mkv")
fps = cap.get(cv2.CAP_PROP_FPS) # Get frames per second (FPS)

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()
 
# Get frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
 
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, fps, (frame_width, frame_height))
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or error occurred.")
        break
 
    frame = Image.fromarray(frame)
    frame = np.array(frame.convert("L").convert('RGB'))
    # Write the frame to the output video file
    out.write(frame)
 
    # # Display the frame
    # cv2.imshow("Frame", frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
 
# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()

import subprocess

subprocess.run("ffmpeg -i test.mkv -ab 160k -ac 2 -ar 44100 -vn audio.wav", shell=True)

videoSource = "output.avi"
audioSource = "audio.wav"
savePath = "output_final.avi"
def addAudio(audioSource, videoSource, savePath):
    subprocess.run(f'ffmpeg -y -i "{videoSource}" -i "{audioSource}" -c copy "{savePath}"', shell=True)

addAudio(audioSource, videoSource, savePath)