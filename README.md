# Depth-Pong 3D

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Current Status](#current-status)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

**Depth-Pong 3D** is an experimental study project that integrates **computer vision** and **3D physics** to create an interactive Pong-like game. Utilizing **MediaPipe** for hand detection and **Panda3D** for rendering a 3D environment, this project demonstrates the basics of real-time hand tracking and physics simulation within a virtual 3D space.

## Features

- **Real-Time Hand Detection**: Uses MediaPipe to track hand movements via webcam.
- **3D Pong Game**: A Pong-inspired game rendered in a 3D environment where players control paddles using hand gestures.
- **Physics Simulation**: Implements basic physics to allow the ball to bounce realistically within the 3D space.
- **Interactive Control**: Move the paddles using hand gestures or fallback keyboard controls.
- **Mini Camera View**: Displays a live feed from the webcam within the application window.

## Technologies Used

- **Python 3.10**
- **Panda3D**: 3D game engine for rendering and scene management.
- **MediaPipe**: Framework for building multimodal applied machine learning pipelines (used here for hand detection).
- **OpenCV**: Library for computer vision tasks.
- **Torch (PyTorch)**: For depth estimation using MiDaS.

## Installation

### Prerequisites

- **Python 3.10** (Ensure you have Python 3.10 installed as MediaPipe may not fully support newer versions)
- **Git** (optional, for cloning the repository)

### Steps

1. **Clone the Repository**
   
   ```bash
   git clone https://github.com/yourusername/Depth-Pong-3D.git
   cd Depth-Pong-3D
   ```

2. **Create a Virtual Environment**

   ```bash
   python3.10 -m venv venv3.10
   ```

3. **Activate the Virtual Environment**

   - **Windows (Command Prompt):**
     
     ```bash
     venv3.10\Scripts\activate.bat
     ```

   - **Windows (PowerShell):**
     
     ```powershell
     .\venv3.10\Scripts\Activate.ps1
     ```
     
     *If you encounter an execution policy error, run:*
     
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
     ```

4. **Install Required Packages**

   ```bash
   pip install --upgrade pip
   pip install mediapipe opencv-python panda3d torch torchvision torchaudio
   ```

5. **Download Additional Dependencies**

   - **Visual C++ Redistributables**: Ensure you have the latest [Visual C++ Redistributable for Visual Studio](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist) installed.

## Usage

1. **Activate the Virtual Environment** (if not already active)

   - **Windows (Command Prompt):**
     
     ```bash
     venv3.10\Scripts\activate.bat
     ```

   - **Windows (PowerShell):**
     
     ```powershell
     .\venv3.10\Scripts\Activate.ps1
     ```

2. **Run the Application**

   ```bash
   python main.py
   ```
   
   - A Panda3D window should open displaying a 3D Pong game with a bouncing ball and interactive paddles.
   - Use your hand gestures to move the paddles via webcam or fallback to arrow keys + W/S for manual control.

## Current Status

🚧 **Under Development** 🚧

**Depth-Pong 3D** is a **work-in-progress** project intended for **educational and study purposes**. Features are actively being developed and refined. Contributions and feedback are welcome!

### Known Issues

- **Compatibility with Python 3.12**: MediaPipe currently has limited support for Python versions beyond 3.10 on Windows, leading to DLL load errors.
- **Hand Detection Accuracy**: The current implementation uses a stub for hand detection. Integrating full MediaPipe and MiDaS functionality is ongoing.
- **Performance Optimization**: Running MediaPipe and MiDaS simultaneously may impact real-time performance. Optimizations are being explored.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork the Project**
2. **Create Your Feature Branch**
   
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Commit Your Changes**
   
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```

4. **Push to the Branch**
   
   ```bash
   git push origin feature/AmazingFeature
   ```

5. **Open a Pull Request**

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [Panda3D](https://www.panda3d.org/) - For the 3D game engine.
- [MediaPipe](https://mediapipe.dev/) - For the hand detection framework.
- [OpenCV](https://opencv.org/) - For computer vision tasks.
- [MiDaS](https://github.com/intel-isl/MiDaS) - For depth estimation.
- [Python](https://www.python.org/) - The programming language used.
