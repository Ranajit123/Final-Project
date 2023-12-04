from dash import Dash, html, Input, Output, callback, ctx


app = Dash(__name__)

app.layout = html.Div([
    html.Button('REC', id='rec'),
    html.Button('PLOT', id='plot'),
    html.Div(id='recording_button_div'),
    # html.Div(id='ploting_button_div')
])

@callback(
    Output('recording_button_div', 'children'),
    Input('rec', 'n_clicks')
)
def callback1(btn1):
    msg = "No Button is clicked"

    if 'rec' in ctx.triggered_id:
        msg = "rec button pressed"
    return html.Div(msg)

# @callback(
#     Output('ploting_button_div', 'children'),
#     Input('plot', 'n_clicks')
# )

# def callback2(rbtn2):
#     msg = "No Button is clicked"

#     if 'plot' in ctx.triggered_id:
#         msg = "plot button pressed"
#     return html.Div(msg)


if __name__ == '__main__':
    app.run(debug=True)
