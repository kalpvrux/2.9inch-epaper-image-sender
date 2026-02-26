# 2.9inch E-Paper Image Sender

[![Platform](https://img.shields.io/badge/Platform-Python%20|%20ESP32-blue)](#getting-started)
[![License](https://img.shields.io/badge/License-Open%20Source-green)](#license)

## Overview
A Python-based GUI application designed for sending images directly to a **2.9-inch E-Paper Display (128×296 pixels)** via serial communication with an **ESP32** microcontroller. It supports both Black & White and 4-level Grayscale display modes, complete with on-the-fly image processing and color inversion.

## 📸 Application Preview

### Main Interface
![Main Interface](https://github.com/kalpvrux/2.9inch-epaper-image-sender/blob/main/app.png)
*Main application window showing serial connection, image processing options, and controls.*

---

## Features

- **Dual Display Modes:** Choose between pure Black & White (1-bit) or 4-level Grayscale (2-bit) for better image quality.
- **Color Inversion:** Easily invert colors (White ↔ Black) before sending.
- **Real-time Preview:** View the processed image in the GUI before transmission.
- **Progress Tracking:** Clear visual indicators for image processing and serial transmission.
- **Automatic Image Processing:** Automatically resizes and converts images (PNG, JPG, JPEG, BMP, GIF, TIFF) to the required hex format.
- **Robust Serial Communication:** Built-in tools to select COM ports, set baud rates, and manage the connection to the ESP32.

---

## Hardware Requirements

- **E-Paper Display:** 2.9-inch E-Paper display module (128×296 pixels).
- **Microcontroller:** ESP32 or a compatible development board.
- **Connection:** Standard USB cable for serial communication between the PC and ESP32.

---

## Repository Structure

```text
2.9inch-epaper-image-sender/
├── epaper_receiver/          # Arduino/ESP32 C++ code & Waveshare display libraries
│   ├── epaper_receiver.ino   # Main sketch to flash to ESP32
│   └── ...                   # Display drivers (DEV_Config, EPD_2in9_V2, etc.)
├── epaper_image_sender.py    # Main Python GUI application
├── requirements.txt          # Python dependencies
├── app.png                   # Application screenshot
└── README.md                 # This documentation
```

---

## Getting Started

### 1. Hardware & Microcontroller Setup

1. Connect your 2.9-inch E-Paper display to the ESP32 using the SPI interface pins (refer to `epaper_receiver/DEV_Config.h` for pin mappings).
2. Connect the ESP32 to your computer via USB.
3. Open the `epaper_receiver/epaper_receiver.ino` sketch in the **Arduino IDE**.
4. Ensure you have the required ESP32 board packages installed in the Arduino IDE.
5. Compile and **Upload** the sketch to your ESP32.

### 2. Software Installation (PC)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kalpvrux/2.9inch-epaper-image-sender.git
   cd 2.9inch-epaper-image-sender
   ```

2. **Install Python dependencies:**
   Make sure you have Python 3 installed. Run:
   ```bash
   pip install -r requirements.txt
   ```
   *(Installs `tkinter`, `Pillow`, and `pyserial`)*

### 3. Using the GUI Application

1. **Run the application:**
   ```bash
   python epaper_image_sender.py
   ```
2. **Serial Connection:**
   - Select your ESP32's COM port from the dropdown.
   - Choose the baud rate (default is usually `115200`).
   - Click **Connect**.
3. **Processing Options:**
   - Select the display mode: **Black & White** or **4-Level Grayscale**.
   - Enable **Invert Colors** if needed.
4. **Image Selection & Transmission:**
   - Click **Browse Image** to load an image.
   - Click **Process Image** to resize and format it. A preview will appear.
   - Click **Send to E-Paper** to transmit the image to the ESP32.
   - Use **Clear Display** if you want to wipe the E-Paper screen.

---

## Communication Protocol Details

The Python script communicates with the ESP32 using a straightforward text-based protocol over serial:

- **Commands Sent to ESP32:**
  - `START_IMAGE,hex_data,END_IMAGE` - Transmits a B&W image.
  - `START_GRAY,hex_data,END_GRAY` - Transmits a grayscale image.
  - `CLEAR` - Clears the display.
  - `STATUS` - Checks device readiness.
- **Expected Responses from ESP32:**
  - `DISPLAY_SUCCESS` / `DISPLAY_ERROR`
  - `CLEAR_SUCCESS`
  - `STATUS_READY`

---

## Troubleshooting

- **Connection Problems:** Double-check the COM port and baud rate. Verify that the USB cable supports data transfer (not just power).
- **Image Processing Errors:** Ensure the image is not corrupted. Try testing with a smaller image or a different format (PNG/JPG).
- **Display Issues:** Check the SPI wiring between the ESP32 and the E-Paper module. Open the Arduino Serial Monitor (at 115200 baud) to view ESP32 debug messages.

---

*Maintained by [Kalpvrux](https://github.com/kalpvrux)* | *© 2024 Waveshare Electronics*
