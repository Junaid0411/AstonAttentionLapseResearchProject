import argparse
import tempfile
import queue
import sys
from os.path import join
import time
timestr = time.strftime("%Y%m%d-%H%M%S")


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-dev', '--device', type=int_or_str, default=6,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, default=48000, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-o', '--output', type=str, default=join('/home/franka/Videos/', timestr+'.wav'),
    help='audio file to store recording to')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
parser.add_argument(
    '-dur', '--duration', type=float, default=300.0, help='duration of the recording in seconds')
args = parser.parse_args()

try:
    import sounddevice as sd
    import soundfile as sf

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])
    if args.output is None:
        args.output = tempfile.mktemp(prefix='rec_unlimited_',
                                        suffix='.wav', dir='')
    q = queue.Queue()
    duration_frames = int(args.samplerate * args.duration)
    recorded_frames = [0]  # Mutable object to store the recorded frames

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())
        recorded_frames[0] += len(indata)

    # Make sure the file is opened before recording anything:
    with sf.SoundFile(args.output, mode='x', samplerate=args.samplerate,
                      channels=args.channels, subtype=args.subtype) as file:
        with sd.InputStream(samplerate=args.samplerate, device=args.device,
                            channels=args.channels, callback=callback):
            print('#' * 80)
            print('Recording for {} seconds...'.format(args.duration))
            print('#' * 80)
            while recorded_frames[0] < duration_frames:
                file.write(q.get())

except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(args.output))
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
