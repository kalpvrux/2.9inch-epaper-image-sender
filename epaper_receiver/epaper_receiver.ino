#include "DEV_Config.h"
#include "EPD.h"
#include "GUI_Paint.h"
#include "imagedata.h"
#include <stdlib.h>

UBYTE *BlackImage;
UWORD Imagesize;
UWORD GrayImagesize;  
bool imageReceived = false;
bool grayImageReceived = false; 
String receivedData = "";

void setup()
{
    Serial.begin(115200);
    printf("EPD_2IN9_V2 Serial Image Receiver\r\n");
    DEV_Module_Init();

    printf("e-Paper Init and Clear...\r\n");
    EPD_2IN9_V2_Init();
    EPD_2IN9_V2_Clear();
    DEV_Delay_ms(500);

    
    Imagesize = ((EPD_2IN9_V2_WIDTH % 8 == 0)? (EPD_2IN9_V2_WIDTH / 8 ): (EPD_2IN9_V2_WIDTH / 8 + 1)) * EPD_2IN9_V2_HEIGHT;
    GrayImagesize = ((EPD_2IN9_V2_WIDTH % 4 == 0)? (EPD_2IN9_V2_WIDTH / 4 ): (EPD_2IN9_V2_WIDTH / 4 + 1)) * EPD_2IN9_V2_HEIGHT;
    
    if((BlackImage = (UBYTE *)malloc(max(Imagesize, GrayImagesize))) == NULL) {
        printf("Failed to apply for black memory...\r\n");
        while(1);
    }
    printf("Paint_NewImage\r\n");
    Paint_NewImage(BlackImage, EPD_2IN9_V2_WIDTH, EPD_2IN9_V2_HEIGHT, 0, WHITE);  
    
    Serial.println("Ready to receive image data...");
    Serial.println("Commands:");
    Serial.println("- Send B&W image: START_IMAGE,hex_data,END_IMAGE");
    Serial.println("- Send 4Gray image: START_GRAY,hex_data,END_GRAY"); 
    Serial.print("B&W data size: ");
    Serial.print(Imagesize);
    Serial.println(" bytes");
    Serial.print("4Gray data size: ");
    Serial.print(GrayImagesize);
    Serial.println(" bytes");
}

bool parseHexData(String hexData, bool isGray = false) {
    hexData.replace(" ", "");
    hexData.replace(",", "");
    hexData.replace("0X", "");
    hexData.replace("0x", "");
    hexData.toUpperCase();
    
    UWORD expectedSize = isGray ? GrayImagesize : Imagesize;
    
    if (hexData.length() != expectedSize * 2) {
        Serial.print("Error: Expected ");
        Serial.print(expectedSize * 2);
        Serial.print(" hex characters, got ");
        Serial.println(hexData.length());
        return false;
    }
    
    for (int i = 0; i < expectedSize; i++) {
        String byteString = hexData.substring(i * 2, i * 2 + 2);
        BlackImage[i] = (UBYTE)strtol(byteString.c_str(), NULL, 16);
    }
    
    return true;
}

void displayImage(bool isGray = false) {
    if (isGray) {
        printf("Displaying received 4Gray image...\r\n");
        EPD_2IN9_V2_Gray4_Init(); 
        Paint_NewImage(BlackImage, EPD_2IN9_V2_WIDTH, EPD_2IN9_V2_HEIGHT, 0, WHITE);
        Paint_SetScale(4);
        EPD_2IN9_V2_4GrayDisplay(BlackImage);
        printf("4Gray image displayed successfully!\r\n");
    } else {
        printf("Displaying received B&W image...\r\n");
        EPD_2IN9_V2_Init();
        Paint_NewImage(BlackImage, EPD_2IN9_V2_WIDTH, EPD_2IN9_V2_HEIGHT, 0, WHITE);
        Paint_SelectImage(BlackImage);
        EPD_2IN9_V2_Display(BlackImage);
        printf("B&W image displayed successfully!\r\n");
    }
}

void processSerialData() {
    if (receivedData.startsWith("START_IMAGE")) {
        int startIndex = receivedData.indexOf(',') + 1;
        int endIndex = receivedData.indexOf(",END_IMAGE");
        
        if (startIndex > 0 && endIndex > startIndex) {
            String hexData = receivedData.substring(startIndex, endIndex);
            Serial.println("Processing B&W image data...");
            
            if (parseHexData(hexData, false)) {
                Serial.println("B&W image data parsed successfully!");
                displayImage(false);
                Serial.println("DISPLAY_SUCCESS");
            } else {
                Serial.println("DISPLAY_ERROR: Failed to parse B&W image data");
            }
        } else {
            Serial.println("DISPLAY_ERROR: Invalid B&W data format");
        }
        
        receivedData = "";
        imageReceived = false;
    }
    
    if (receivedData.startsWith("START_GRAY")) {
        int startIndex = receivedData.indexOf(',') + 1;
        int endIndex = receivedData.indexOf(",END_GRAY");
        
        if (startIndex > 0 && endIndex > startIndex) {
            String hexData = receivedData.substring(startIndex, endIndex);
            Serial.println("Processing 4Gray image data...");
            
            if (parseHexData(hexData, true)) {
                Serial.println("4Gray image data parsed successfully!");
                displayImage(true);
                Serial.println("DISPLAY_SUCCESS");
            } else {
                Serial.println("DISPLAY_ERROR: Failed to parse 4Gray image data");
            }
        } else {
            Serial.println("DISPLAY_ERROR: Invalid 4Gray data format");
        }
        
        receivedData = "";
        grayImageReceived = false;
    }
}

void loop()
{
    while (Serial.available()) {
        char c = Serial.read();
        receivedData += c;
        
        if (receivedData.endsWith("END_IMAGE")) {
            imageReceived = true;
        } else if (receivedData.endsWith("END_GRAY")) {
            grayImageReceived = true;
        }
    }
    
    if (imageReceived || grayImageReceived) {
        processSerialData();
    }
    
    if (receivedData.equals("CLEAR\n") || receivedData.equals("CLEAR\r\n")) {
        Serial.println("Clearing display...");
        EPD_2IN9_V2_Init();  
        EPD_2IN9_V2_Clear();
        Serial.println("CLEAR_SUCCESS");
        receivedData = "";
    }
    
    
    if (receivedData.equals("STATUS\n") || receivedData.equals("STATUS\r\n")) {
        Serial.println("STATUS_READY");
        receivedData = "";
    }
    
    delay(10);
}