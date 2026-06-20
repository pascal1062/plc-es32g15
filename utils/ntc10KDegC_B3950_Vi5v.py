'''
    Analog Input Configuration. (ntc Thermistor 10K B3950 Amazon, 10Kohms @ 25 DegC)
    Sensor is connected betwenn Vcc-5V and Terminla VI1 (0-10V input, but use 0-5V)
    Equivalent circuit is 5V --> RNTC --> R43K --> R10K --> internal op amp of es32g15 (3 resistors in series)
    Those inputs has voltage divider 43K/10K result of 0-1.8V final on ADC
    volts vs Celsius
'''

SCALE_RANGE = (
    (0.15142, -40),
    (0.18904, -35),
    (0.23787, -30),
    (0.29481, -25),
    (0.35605, -20),
    (0.41694, -15),
    (0.47701, -10),
    (0.53505, -5),
    (0.58983, 0),
    (0.64152, 5),
    (0.68795, 10),
    (0.72865, 15),
    (0.76371, 20),
    (0.79365, 25),
    (0.81881, 30),
    (0.8398, 35),
    (0.85724, 40),
    (0.87164, 45),
    (0.88352, 50),
    (0.8933, 55),
    (0.90136, 60),
    (0.908, 65),
    (0.91349, 70),
    (0.91802, 75),
    (0.92178, 80),
    (0.92492, 85),
    (0.9275, 90),
    (0.92969, 95),
    (0.93154, 100),
    (0.93308, 105)
)
