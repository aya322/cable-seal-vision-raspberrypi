[README.md](https://github.com/user-attachments/files/34819040/README.md)
# Cable Seal Inspection with Raspberry Pi and OpenCV

A vision system that checks a cable seal with a camera and decides **OK** or **NOK**. It was designed during my second-year internship  as a replacement for the existing color-sensor station.

## The problem

The existing station checks the color of the seal with a color sensor and a PLC. It is sensitive to lighting and to the position of the part, and it only checks color.

## The proposed solution

A **Raspberry Pi 4** with a camera module and LED ring lighting. The program checks the color **and the shape** of the seal.

## How the program works

1. Captures an image from the camera.
2. Reduces noise with a Gaussian filter (5x5).
3. Converts the image from BGR to HSV.
4. Keeps only the reference color (blue) with `cv2.inRange`.
5. Finds the contours and keeps the biggest one.
6. Computes its area and its circularity.
7. Decision: **OK** if the area and circularity are high enough, otherwise **NOK**.
8. Lights the green LED for OK or the red LED for NOK, and shows the result on screen.

## Key parameters (in `seal_inspection.py`)

| Parameter | Value |
|---|---|
| HSV range (blue) | min `[100, 80, 50]`, max `[130, 255, 255]` |
| Minimum colored pixels | 500 |
| Minimum contour area | 3000 |
| Minimum circularity | 0.80 |
| Green LED | GPIO 17 (BCM) |
| Red LED | GPIO 27 (BCM) |

Circularity is `4 x pi x area / perimeter^2`. It is close to 1 for a perfect circle, so a deformed seal gets a lower value.

## Hardware

- Raspberry Pi 4
- Camera (USB webcam or Pi camera, read through `cv2.VideoCapture(0)`)
- One green and one red LED with resistors, on GPIO 17 and 27
- LED ring lighting (for stable lighting)

## How to run

On the Raspberry Pi:

```bash
pip install opencv-python numpy
python3 seal_inspection.py
```

`RPi.GPIO` is already installed on Raspberry Pi OS. Press `q` in the camera window to stop.

## Status and limits

This is a **prototype program** written for my internship report. It has not been tested on the real production line yet, and the HSV range and thresholds must be calibrated for the real seals and lighting.

## Future work

- Test and calibrate it under real production conditions.
- Add texture and surface-defect detection.
- Save each result in a log file for quality tracking.
- Try machine learning to improve accuracy.

## Author

**Aya Ben Haj Ali**, electronics engineering student at ISET Sousse, Tunisia.
Contact: ayabenhajali399@gmail.com
