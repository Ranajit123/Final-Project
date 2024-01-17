# Import packages
from dash import Dash, html, dcc, Input, Output, callback, ctx
import plotly.graph_objs as go
import pandas as pd
import pyaudio
import wave
import numpy as np

# Function to start recording and return audio data and time
def start_recording():
    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 1600

    pa = pyaudio.PyAudio()

    stream = pa.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    print("Start recording..")
    seconds = 5
    frames = []
    seconds_tracking = 0

    for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
        seconds_tracking += 1

    stream.stop_stream()
    stream.close()
    pa.terminate()

    file = wave.open('lemaster_tech.wav', 'rb')
    sample_freq = file.getframerate()
    frames = file.getnframes()
    signal_wave = file.readframes(-1)
    file.close()

    audio_arr = np.frombuffer(signal_wave, dtype=np.int16)
    time = frames / sample_freq

    return audio_arr, time

# create Dash constructor
app = Dash(__name__)

# Create app layout
app.layout = html.Div([
    html.Button(id='sRec', children='Start Recording'),
    html.Button(id='result', children='Show Result'),
    html.Div(id='container-button-basic'),
    dcc.Graph(id='graph')
])



@callback(Output(component_id='container-button-basic', component_property='children'),
        Output('graph', 'figure'),
        Input('sRec', 'n_clicks'),
        Input('result', 'n_clicks'))

def update_output(btn1, btn2):
    msg = "No Button is clicked"
    
    if 'sRec' == ctx.triggered_id:
        msg = 'Start Recording button is clicked'
        audio_arr, time = start_recording()
        print(audio_arr)
    elif 'result' == ctx.triggered_id:    
        msg = 'Show result Button is clicked'
        df = pd.DataFrame({
            "Audio_value": audio_arr,
            "Time": time
        })
        if not df.empty:
            fig = go.Figure(data=go.Scatter(x=df['Time'], y=df['Audio_value']))
            fig.update_layout(
                title="Audio Data",
                xaxis_title="Time",
                yaxis_title="Audio Value"
            )

    return html.Div(msg), fig

if __name__== '__main__':

    app.run(debug=True)
