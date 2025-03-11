import tkinter as tk
import pymysql
import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database Configuration
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "SoundVisualizerDB"

# Establish MySQL Connection
def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

# Function to store data in MySQL
def save_to_db(frequency, amplitude, shape):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO SoundShapes (frequency, amplitude, shape) VALUES (%s, %s, %s)"
    cursor.execute(sql, (frequency, amplitude, shape))
    conn.commit()
    conn.close()

# Function to get shape based on frequency and amplitude
def get_shape(frequency, amplitude):
    if frequency < 500:
        return "Circle"
    elif frequency < 1000:
        return "Square"
    else:
        return "Triangle"

# Function to process audio and visualize
def visualize_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()

    def update():
        data = stream.read(CHUNK, exception_on_overflow=False)
        data_int = struct.unpack(str(CHUNK) + 'h', data)
        amplitude = np.abs(np.max(data_int))
        frequency = np.fft.fftfreq(len(data_int), d=1/RATE)[np.argmax(np.abs(np.fft.fft(data_int)))]
        
        shape = get_shape(frequency, amplitude)
        save_to_db(frequency, amplitude, shape)

        ax.clear()
        if shape == "Circle":
            circle = plt.Circle((0, 0), 1, fill=True)
            ax.add_patch(circle)
        elif shape == "Square":
            ax.add_patch(plt.Rectangle((-1, -1), 2, 2, fill=True))
        else:
            triangle = plt.Polygon([(-1, -1), (1, -1), (0, 1)], closed=True)
            ax.add_patch(triangle)

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        canvas.draw()
        window.after(1000, update)

    update()

# Tkinter UI
window = tk.Tk()
window.title("Sound-to-Shape Visualizer")
window.geometry("600x600")

start_button = tk.Button(window, text="Start Visualization", command=visualize_audio)
start_button.pack()

window.mainloop()