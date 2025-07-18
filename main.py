import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import argparse
from tqdm import tqdm
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('filepath')
parser.add_argument('color', default='gray')
args = parser.parse_args()


assert args.color in ['gray','red','green','blue']

cap = cv2.VideoCapture(args.filepath)

# Open the video file
cap = cv2.VideoCapture("test.mkv")
fps = cap.get(cv2.CAP_PROP_FPS) # Get frames per second (FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

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
pbar = tqdm(frame_count)
with tqdm(total=frame_count) as pbar:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or error occurred.")
            break
     
        frame = Image.fromarray(frame)
        if args.color == 'gray':
            frame = np.array(frame.convert("L").convert('RGB'))
        elif args.color == 'red':
            # Step 1: Desaturate colors (reduce overall saturation)
            enhancer = ImageEnhance.Color(frame)
            img_desaturated = enhancer.enhance(0.5)  # Adjust value (0=black/white, 1=original)

            # Step 2: Increase contrast
            enhancer = ImageEnhance.Contrast(img_desaturated)
            img_higher_contrast = enhancer.enhance(1.5)  # Adjust value as needed

            # Step 3: Tint toward red (add a red overlay)
            red_tint = Image.new("RGB", frame.size, (0, 255, 0))
            img_redscale = Image.blend(img_higher_contrast, red_tint, alpha=0.2)  # Alpha controls intensity

            # Optional: Adjust individual channels for finer control
            r, g, b = img_redscale.split()
            # Reduce green and blue channels
            g = g.point(lambda x: x * 0.7)  # Adjust multipliers
            b = b.point(lambda x: x * 0.6)
            frame = np.array(Image.merge("RGB", (r, g, b)))

        # Write the frame to the output video file
        out.write(frame)
     
        pbar.update(1)
        pbar.refresh()
 
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

# Clean up temporary files
os.remove('output.avi')
os.remove('audio.wav')