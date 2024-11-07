# Project Veronica

A humanoid AI assistant that combines natural language processing with facial tracking and mechatronic expressions to create an interactive, embodied AI experience.

## Overview

Veronica is an AI-powered humanoid assistant that uses the Cohere API for natural language processing and understanding. The system features mechanical eyes and mouth that move in response to user interactions, creating a more engaging and lifelike experience. The eyes track user movement through facial detection, while the mouth movements are synchronized with Veronica's speech output.

## Features

- **Natural Language Processing**
  - Powered by Cohere API
  - Real-time conversation capabilities
  - Context-aware responses
  - Memory of conversation history

- **Facial Tracking**
  - Real-time face detection
  - Dynamic eye movement tracking
  - Maintains "eye contact" with users

- **Mechatronic Expressions**
  - Arduino-controlled servo motors
  - Synchronized mouth movements with speech
  - Smooth eye tracking movement
  - Natural-looking expressions

## Technical Architecture

### Software Components
- Face detection system
- Cohere API integration
- Serial communication with Arduino
- Speech-to-mouth movement mapping
- Main control system

### Hardware Components
- Arduino microcontroller
- Servo motors for eyes (2x)
- Servo motor for mouth
- Camera for facial detection
- Display/speaker for output

## Prerequisites

- Python 3.8+
- Arduino IDE
- OpenCV
- Cohere API key
- Required Python packages:
  ```
  cohere
  opencv-python
  pyserial
  numpy
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/agneya-1402/veronica.git
   cd veronica
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Upload Arduino sketch:
   - Open `arduino/veronica_control/veronica_control.ino` in Arduino IDE
   - Upload to your Arduino board

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your Cohere API key
   ```

## Usage

1. Connect the Arduino and ensure all servo motors are properly wired
2. Run the main program:
   ```bash
   python main.py
   ```
3. Position yourself in front of the camera
4. Start interacting with Veronica through voice or text input

## Configuration

### Servo Mapping
- Eyes X-axis: 0-180 degrees
- Eyes Y-axis: 0-180 degrees
- Mouth movement: 0-90 degrees

### Face Detection Parameters
- Detection confidence threshold: 0.8
- Maximum detection distance: 2 meters
- Frame processing rate: 30 FPS

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Cohere API for natural language processing
- OpenCV for face detection capabilities
- Arduino community for servo control examples
- [Add any other acknowledgments]
