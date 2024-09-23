import pyttsx3
import sounddevice as sd
import numpy as np
import serial
import time
import speech_recognition as sr
import cohere

# Initialize Cohere client
cohere_api_key = "Cohere_API_Key"  # Replace with your actual Cohere API key
co = cohere.Client(cohere_api_key)

# Initialize pyttsx3
engine = pyttsx3.init()

# Talking Rate  
engine.setProperty('rate', 120) 
# Set volume 
engine.setProperty('volume', 1.0) 

# Using female voice 
voice_id = "com.apple.voice.compact.en-IE.Moira"
engine.setProperty('voice', voice_id) 

# Initialize serial communication with Arduino
ser = serial.Serial('/dev/tty.usbmodem1101', 9600)  # Update with your port name

# Constants for servo movement range
SERVO_MIN_ANGLE = 90
SERVO_MAX_ANGLE = 180
MOVING_AVERAGE_WINDOW = 15

# Buffer for smoothing
amplitude_buffer = []

# Map amplitude to servo position
def amplitude_to_servo(amplitude):
    scaled_amplitude = SERVO_MIN_ANGLE + (amplitude * (SERVO_MAX_ANGLE - SERVO_MIN_ANGLE))
    servo_position = int(np.clip(scaled_amplitude, SERVO_MIN_ANGLE, SERVO_MAX_ANGLE))
    return servo_position

# Process audio in real-time
def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio callback status: {status}")
    try:
        audio_data = np.abs(indata[:, 0])
        rms_amplitude = np.sqrt(np.mean(audio_data ** 2))
        amplitude_buffer.append(rms_amplitude)
        if len(amplitude_buffer) > MOVING_AVERAGE_WINDOW:
            amplitude_buffer.pop(0)
        smoothed_amplitude = np.mean(amplitude_buffer)
        normalized_amplitude = smoothed_amplitude / np.max(amplitude_buffer) if np.max(amplitude_buffer) > 0 else 0
        servo_position = amplitude_to_servo(normalized_amplitude)
        print(f"Servo Position: {servo_position}")
        ser.write(f"{servo_position}\n".encode())
    except Exception as e:
        print(f"Error in audio processing: {e}")

# Speak text and process audio simultaneously
def speak_text(text):
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100, blocksize=1024):
        engine.say(text)
        engine.runAndWait()

# Initialize speech recognition
recognizer = sr.Recognizer()

def listen_for_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return ""

def ai_response(command):
    try:
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=f"Human: {command}\nAI:",
            max_tokens=100,
            temperature=0.7,
            stop_sequences=["Human:", "AI:"]
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "I'm sorry, I encountered an error while processing your request."

def main():
    intro_message = "Hello! I'm Veronica, your AI assistant. I'm equipped with facial recognition. I can track human faces and engage in natural conversations. How can I assist you today?"
    print("Welcome to the interactive AI assistant. Say 'quit' to exit.")
    speak_text(intro_message)
    
    while True:
        command = listen_for_command()
        if command == "quit":
            speak_text("Goodbye! Thank you for talking with me.")
            break
        response = ai_response(command)
        speak_text(response)

if __name__ == "__main__":
    main()

# Close serial connection
ser.close()
