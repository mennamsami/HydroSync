import serial
import Adafruit_DHT
from gpiozero import DistanceSensor
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_daq as daq

ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the serial port as needed
ultrasonic = DistanceSensor(echo=17, trigger=4)  # GPIO pins for ultrasonic sensor

app = Dash(__name__)

app.layout = html.Div(
    style={'backgroundColor': '#642C2C', 'height': '100%', 'color': '#A9E1FB'},
    children=[
        html.H1("Sensor Readings", style={'textAlign': 'center'}),
        # Water Tank Level Gauge
        html.Div([
            html.H3("Water Tank Level"),
            daq.Gauge(
                showCurrentValue=True,
                id='water-tank-gauge',
                color={"gradient": True, "ranges": {"red": [0, 50], "yellow": [50, 65], "green": [65, 100]}},
                value=5,
                label='Water Tank Level (%)',
                max=100,
                min=0
            ),
        ]),
        # Temperature Gauge
        html.Div([
            html.H3("Temperature"),
            daq.Gauge(
                showCurrentValue=True,
                id='temperature-gauge',
                color={"gradient": True, "ranges": {"green": [0, 24], "yellow": [24, 35], "red": [35, 50]}},
                value=8,
                label='Temperature (°C)',
                max=50,
                min=0,
            ),
        ]),
        # Humidity Gauge
        html.Div([
            html.H3("Humidity"),
            daq.Gauge(
                showCurrentValue=True,
                id='humidity-gauge',
                color={"gradient": True, "ranges": {"green": [0, 50], "yellow": [50, 80], "red": [80, 100]}},
                value=2,
                label='Humidity (%)',
                max=100,
                min=0
            ),
        ]),
        # Hydrogen Level Gauge
        html.Div([
            html.H3("Hydrogen Level"),
            daq.Gauge(
                showCurrentValue=True,
                id='hydrogen-gauge',
                color={"gradient": True, "ranges": {"red": [0, 600], "yellow": [600, 700], "green": [700, 1000]}},
                value=5,
                label='Hydrogen Sensor Reading',
                max=1000,
                min=0
            ),
        ]),
        dcc.Interval(
            id='interval-component',
            interval=0.6*1000,
            n_intervals=0
        )
    ]
)


@app.callback(
    [Output('water-tank-gauge', 'value'),
     Output('temperature-gauge', 'value'),
     Output('humidity-gauge', 'value'),
     Output('hydrogen-gauge', 'value')],
    [Input('interval-component', 'n_intervals')]
)
def update_gauges(n_intervals):
    distance = ultrasonic.distance * 100
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 2)  # GPIO pin for DHT11 sensor
    ser.write(b'read_mq8\n')
    hydrogen_level = int(ser.readline().decode().strip().split()[-1])
    
    # Calculate water tank percentage based on distance (adjust 2.5 and 5 as needed)
    water_tank_percentage = 100 - ((distance - 2.5) / (5 - 2.5)) * 100
    return water_tank_percentage, temperature if temperature is not None else 0, humidity if humidity is not None else 0, hydrogen_level


if __name__ == '__main__':
    app.run_server(debug=True)
