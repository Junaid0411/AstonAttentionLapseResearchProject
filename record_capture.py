import zmq
import msgpack as serializer
import subprocess
import threading
import time
import os

def record_video():
    # Path to k4arecorder
    k4a_recorder_path = r"C:\Program Files\Azure Kinect SDK v1.4.1\tools\k4arecorder.exe"

    # Command arguments for k4arecorder
    duration = 300
    output_path = "master1.mkv"

    # Construct the command, commented out due to error
    #if os.path.exists("C:\Users\scrim\OneDrive - Aston University\Documents\Work\Research Associate\pupil\pupil_src\master1.mkv"):
    #    print('Master1.mkv already exists')
    #    exit()
    
    command = f'"{k4a_recorder_path}" --external-sync master -l {duration} {output_path}'

    # Call k4arecorder command to record video
    subprocess.call(command, shell=True)

def record_sound():
    # Path to Python interpreter and sound recording script
    python_command = r"C:\Users\scrim\AppData\Local\Programs\Python\Python311\python.exe"
    sound_recording_script = "sound_recording.py"

    # Command arguments for sound recording script
    duration = 300
    output_file = "sound_recording.wav"

    # Construct the command
    command = [python_command, sound_recording_script, "--duration", str(duration), "--output", output_file]

    # Call sound recording script
    subprocess.call(command)

if __name__ == "__main__":
    # Create separate threads for audio and video recordings
    
    video_thread = threading.Thread(target=record_video)
    audio_thread = threading.Thread(target=record_sound)

    # Start the threads
    video_thread.start()
    audio_thread.start()
    
    # Setup zmq context and remote helper
    ctx = zmq.Context()
    socket = zmq.Socket(ctx, zmq.REQ)
    socket.connect("tcp://127.0.0.1:50020")

    # Measure round trip delay
    t = time.time()
    socket.send_string("t")
    print(socket.recv_string())
    print("Round trip command delay:", time.time() - t)

    # Set current Pupil time to 0.0
    socket.send_string("T 0.0")
    print(socket.recv_string())

    # Start recording
    time.sleep(0.91)
    socket.send_string("R")
    print(socket.recv_string())
    
    # Wait for both threads to complete
    video_thread.join()
    audio_thread.join()

    # Send notification:
    def notify(notification):
        """Sends ``notification`` to Pupil Remote"""
        topic = "notify." + notification["subject"]
        payload = serializer.dumps(notification, use_bin_type=True)
        socket.send_string(topic, flags=zmq.SNDMORE)
        socket.send(payload)
        return socket.recv_string()
