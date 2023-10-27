import pyaudio
import numpy as np
from scipy.signal import find_peaks
import wave
import matplotlib.pyplot as plt

# Parameters for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10  # Adjust this as needed
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"

# Create a PyAudio object
audio = pyaudio.PyAudio()

# Open a new audio stream for recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# Record audio for the specified duration
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop and close the audio stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded audio to a WAV file
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

# Load the recorded audio for further analysis
recorded_audio = wave.open(WAVE_OUTPUT_FILENAME, 'rb')

# Read audio data and convert it to a NumPy array
audio_signal = np.frombuffer(recorded_audio.readframes(-1), dtype=np.int16)

# Find the indices of the two highest peaks in the audio signal
peaks, _ = find_peaks(audio_signal, height=0)  # You may need to adjust the "height" parameter

# Sort the peaks by amplitude to get the highest two
highest_peaks = sorted(peaks, key=lambda x: audio_signal[x], reverse=True)[:2]

# Calculate the time difference between the two highest peaks in seconds
time_difference = abs(highest_peaks[0] - highest_peaks[1]) / RATE

print(f"Time difference between the two highest peaks: {time_difference:.2f} seconds")



# Create a PyAudio object
audio = pyaudio.PyAudio()


time = np.arange(0, len(audio_signal)) / RATE

# Plot the audio signal
plt.figure(figsize=(10, 6))
plt.plot(time, audio_signal, label='Audio Signal')
plt.scatter(time[highest_peaks], audio_signal[highest_peaks], color='red', marker='x', label='Highest Peaks')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Recorded Audio Signal with Highest Peaks')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
