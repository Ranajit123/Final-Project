from dash import Dash, dcc, html, Input, Output, callback, ctx
import pyaudio
import wave
import numpy as np

app = Dash(__name__)


def Start_Recording():
    FRAMES_PER_BUFFER = 3200


    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 16000

    pa = pyaudio.PyAudio()

    stream = pa.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    print('start recording')
    seconds = 5
    frames = []
    second_tracking = 0
    second_count = 0
    for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
        second_tracking += 1
        if second_tracking == RATE/FRAMES_PER_BUFFER:
            second_count += 1
            second_tracking = 0
            print(f'Time Left: {seconds - second_count} seconds')


    stream.stop_stream()
    stream.close()
    pa.terminate()

    obj = wave.open('lemaster_tech.wav', 'wb')
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(pa.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b''.join(frames))
    obj.close()


    file = wave.open('lemaster_tech.wav', 'rb')

    sample_freq = file.getframerate()
    frames = file.getnframes()
    signal_wave = file.readframes(-1)

    file.close()


    time = frames / sample_freq


    # # if one channel use int16, if 2 use int32
    audio_array = np.frombuffer(signal_wave, dtype='float32')

    times = np.linspace(0, time, num=frames)

    return times, audio_array


app.layout = html.Div([
    html.Button(id='sRec', children='Start Recording'),
    html.Button(id='result', children='Show Result'),
    html.P(id="out")
])


@callback(
    Output('out', 'children'),
    Input('sRec', 'n_clicks'),
    Input('result', 'n_clicks')
)
def show_factors(sRec, btn2):
    msg = "No Button Clicked Yet"
    if 'sRec' == ctx.triggered_id:
        msg = "Start Recording button clicked"
        audio_arr = Start_Recording()
        print(audio_arr)
    elif 'result' == ctx.triggered_id:
        msg = "Show Rexult Button Clicked"
    return msg


if __name__ == '__main__':
    app.run(debug=True)
