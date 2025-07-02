# E-Paper Image Sender

A Python GUI application for sending images to 2.9-inch E-Paper displays via serial communication with ESP32. Supports both Black & White and 4-level grayscale display modes with color inversion options.

## 📸 Application Preview

### Main Interface
![Main Interface](https://github.com/kalpvrux/2.9inch-epaper-image-sender/blob/main/app.png)
*Main application window showing serial connection, image processing options, and controls*

## Features

- **Dual Display Modes**: Black & White and 4-level grayscale support
- **Color Inversion**: Option to invert colors (white↔black)
- **Real-time Preview**: See processed image before sending
- **Progress Tracking**: Detailed progress indicators for processing and transmission
- **Serial Communication**: Robust serial connection with ESP32
- **Image Processing**: Automatic resize and format conversion
- **User-friendly GUI**: Clean, modern interface with progress feedback
- **Multiple Format Support**: PNG, JPG, JPEG, BMP, GIF, TIFF

## Hardware Requirements

- **E-Paper Display**: 2.9-inch E-Paper display (128×296 pixels)
- **Microcontroller**: ESP32 or compatible board
- **Connection**: USB/Serial connection between computer and ESP32

## Software Requirements

### Python Dependencies

```bash
pip install tkinter pillow pyserial
```

### Required Libraries

- `tkinter` - GUI framework
- `PIL` (Pillow) - Image processing
- `pyserial` - Serial communication
- `threading` - Background processing

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kalpvrux/2.9inch-epaper-image-sender.git
   cd 2.9inch-epaper-image-sender
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Flash the ESP32 code**:
   - Open `epaper_receiver.ino` in Arduino IDE
   - Install required E-Paper display libraries
   - Upload to your ESP32

## Usage

### 1. Hardware Setup
- Connect your 2.9-inch E-Paper display to ESP32
- Connect ESP32 to computer via USB

### 2. Run the Application
```bash
python epaper_image_sender.py
```

### 3. Using the GUI

1. **Serial Connection**:
   - Select COM port from dropdown
   - Choose baud rate (default: 115200)
   - Click "Connect"

2. **Processing Options**:
   - Choose display mode: "Black & White" or "4-Level Grayscale" 
   - Optionally enable "Invert Colors"

3. **Image Selection**:
   - Click "Browse Image" to select your image file
   - Supported formats: PNG, JPG, JPEG, BMP, GIF, TIFF

4. **Process and Send**:
   - Click "Process Image" to resize and convert
   - Preview appears on the left
   - Click "Send to E-Paper" to transmit to display
   - Use "Clear Display" to clear the screen

## Display Modes

### Black & White Mode
- Pure monochrome display
- 1-bit per pixel
- Fastest processing and transmission
- Best for text and simple graphics

### 4-Level Grayscale Mode
- Four shades: Black, Dark Gray, Light Gray, White
- 2-bits per pixel
- Better for photographs and complex images
- Longer processing time

## Communication Protocol

The application communicates with ESP32 using a simple text-based protocol:

### Commands Sent to ESP32
- `START_IMAGE,hex_data,END_IMAGE` - Send B&W image
- `START_GRAY,hex_data,END_GRAY` - Send grayscale image
- `CLEAR` - Clear the display
- `STATUS` - Check device status

### Expected Responses
- `DISPLAY_SUCCESS` - Image displayed successfully
- `DISPLAY_ERROR` - Error occurred during display
- `CLEAR_SUCCESS` - Display cleared successfully
- `STATUS_READY` - Device ready

## File Structure

```
epaper-image-sender/
├── epaper_image_sender.py    # Main Python GUI application
├── epaper_receiver.ino       # Arduino/ESP32 receiver code
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── docs/
    ├── images/              # Screenshots and diagrams
    └── hardware_setup.md    # Hardware connection guide
```

## Technical Specifications

- **Display Resolution**: 128×296 pixels
- **Supported Image Formats**: PNG, JPG, JPEG, BMP, GIF, TIFF
- **Serial Communication**: 9600 or 115200 baud
- **Processing**: Automatic resize with Lanczos resampling
- **Data Format**: Hexadecimal strings for transmission

## Troubleshooting

### Common Issues

1. **Connection Problems**:
   - Ensure correct COM port is selected
   - Check baud rate matches ESP32 configuration
   - Verify USB cable supports data transfer

2. **Image Processing Errors**:
   - Verify image file is not corrupted
   - Try different image formats
   - Check available system memory

3. **Display Issues**:
   - Ensure E-Paper display is properly connected
   - Check power supply to ESP32
   - Verify ESP32 code is properly uploaded

### Debug Steps

1. Check serial monitor in Arduino IDE for ESP32 debug messages
2. Try different images and formats
3. Test with smaller images first
4. Verify hardware connections

## Development

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

### Code Structure

- **EPaperImageSender**: Main application class
- **Image Processing**: PIL-based image conversion and resizing
- **Serial Communication**: PySerial-based ESP32 communication
- **GUI**: Tkinter-based user interface with progress tracking

## Acknowledgments

- Waveshare Electronics for E-Paper display libraries
- Python community for excellent libraries (PIL, PySerial, Tkinter)
- ESP32 community for development support

## Version History

- **v1.0** - Initial release with B&W and grayscale support
- Color inversion feature
- Progress tracking and user feedback
- Robust error handling

## Support

For issues and questions:
1. Check the [Issues](https://github.com/kalpvrux/2.9inch-epaper-image-sender/issues) page
2. Create a new issue with detailed description
3. Include system information and error messages

---

**Developed by**: Kalp_D  
**Company**: Waveshare Electronics  
**Copyright**: © 2024 Waveshare Electronics
