# Drowsiness Detection System

This project is a web-based system designed to detect drowsiness and prevent drowsy driving using YOLO. It monitors the driver’s face and eye movements in real-time and provides warnings when drowsiness is detected.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This project analyzes the driver’s face and eye movements to detect drowsiness in real-time. It uses the YOLO model to detect facial features and identifies signs of drowsiness, providing warnings to prevent accidents caused by drowsy driving. The system aims to enhance road safety by alerting drivers before they fall asleep at the wheel.

## Features

- **Real-Time Drowsiness Detection**: Monitors and analyzes the driver’s face and eyes in real-time.
- **Warning System**: Provides visual or auditory warnings when drowsiness is detected.
- **Web Interface**: Offers an intuitive web UI for easy usage.
- **Data Logging**: Logs detected drowsiness events for future analysis.

## Installation

### Prerequisites

- Python 3.x
- Flask
- OpenCV
- YOLOv10-N model fine-tuned weights (Please check my other repository)

Please refer to the `requirements.txt` file for additional environment setup.

### Setup Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/drowsiness-detection.git
    cd drowsiness-detection
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate  # On Windows
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Download the YOLO model weights and place them in the project folder.

5. Start the Flask server:
    ```bash
    flask run
    ```

## Usage

1. Open your web browser and go to `http://localhost:5000` or `http://localhost:8080`.
2. Set up the camera to monitor the driver’s face.
3. The system will alert you if drowsiness is detected.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Model**: YOLO (You Only Look Once), OpenCV

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions about the project, feel free to reach out via [email](mailto:agy91521947@gmail.com).
