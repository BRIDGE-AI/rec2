#!/usr/bin/env python
import pyaudio, wave, sys, datetime, time

_idx = 0
_t0 = None

def main():
    global _t0

    print("* Press Enter to stop")

    audio = pyaudio.PyAudio()

    wavefile = wave.open("a.wav", 'wb')
    wavefile.setnchannels(1)
    wavefile.setsampwidth(2)
    wavefile.setframerate(16000)

    def callback(in_data, frame_count, time_info, status):
        global _idx, _t0

        now = datetime.datetime.now()
        t1 = time.time()
        print("%3d chunk[%d]:%s, %0.2fms" % (_idx + 1, len(in_data), now.strftime("%Y-%m-%d %H:%M:%S.%f"), (t1 - _t0) * 1000))
        _t0 = t1

        wavefile.writeframes(in_data)
        _idx += 1
        return (in_data, pyaudio.paContinue)

    options = {
        "format":pyaudio.paInt16,
        "channels":1,
        "rate":16000,
        "input":True,
        "frames_per_buffer":int(16000 / 10),
        "stream_callback":callback,
    }

    stream = audio.open(**options)
    stream.start_stream()

    now = datetime.datetime.now()
    _t0 = time.time()
    print("stream started :%s" % (now.strftime("%Y-%m-%d %H:%M:%S.%f")))

    _ = sys.stdin.readline()

    stream.stop_stream()
    stream.close()
    audio.terminate()
    wavefile.close()

    print("finish")

if __name__ == '__main__':
    main()

