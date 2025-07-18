import PIL
import av
import argparse
import numpy as np
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('filepath')
args = parser.parse_args()

# Create a video container and add a video stream
container = av.open(args.filepath)
for frame in container.decode(video=0):
    img = frame.to_image()
    break

output_container = av.open("video.mp4", mode="w")
video_stream = output_container.add_stream("libx264", rate=30)  # H.264 codec
video_stream.width = img.size[0]  # Set resolution (match your frames)
video_stream.height = img.size[1]
video_stream.pix_fmt = "yuv420p"  # Required for MP4 compatibility

container = av.open(args.filepath)
for frame in tqdm(container.decode(video=0)):
    img = frame.to_image()
    frame = np.array(img.convert("L"))
    av_frame = av.VideoFrame.from_ndarray(frame, format="gray8")
    for packet in video_stream.encode(av_frame):
        output_container.mux(packet)

# Flush remaining packets
for packet in video_stream.encode():
    output_container.mux(packet)

output_container.close()

audio_stream = next(s for s in container.streams if s.type == "audio")  
with open("audio.mp3", "wb") as f:
    for packet in container.demux(audio_stream):  
        f.write(packet)

# Open video and audio files
video_container = av.open("video.mp4")
audio_container = av.open("audio.mp3")

# Create output container with combined streams
output_container = av.open(f"{args.filepath.split('/')[-1].split('.')[0]}_baw.mp4", mode="w")
video_stream = output_container.add_stream("copy")  # Copy video stream
audio_stream = output_container.add_stream("aac", rate=48000)  # Encode audio (AAC for MP4)
audio_stream.channels = 2
audio_stream.channel_layout = "stereo"

# Copy video packets
for packet in video_container.demux():
    if packet.stream.type == "video":
        output_container.mux(packet)

# Decode and re-encode audio packets (required for AAC in MP4)
audio_packets = []
for packet in audio_container.demux():
    if packet.stream.type == "audio":
        for frame in packet.decode():
            for encoded_packet in audio_stream.encode(frame):
                output_container.mux(encoded_packet)

# Flush remaining audio packets
for encoded_packet in audio_stream.encode():
    output_container.mux(encoded_packet)

# Close containers
video_container.close()
audio_container.close()
output_container.close()

# Delete temporary files
os.remove('audio.mp3')
os.remove('video.mp4')
