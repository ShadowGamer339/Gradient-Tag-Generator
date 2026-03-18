# GRADIENT_TAG_GENERATOR

Made by **ShadowGamer**  
Discord ID: `1shadowgamer1`

A Python tool to generate multi-color wave tags. Converts HEX colors to smooth gradients or shiny wave animations and provides a preview in the terminal.  

---

## Features

- Smooth gradient generation between multiple colors  
- Shiny wave gradient with highlights and depth  
- Animation preview in terminal  
- Custom key naming for generated gradient tags  

---

## Knowledge Required

- Basic understanding of Python  
- Familiarity with terminal/command line usage  
- (Optional) Knowledge of color codes (HEX)  

---

## Installation

1. Download the repository using the **Download** button on GitHub  
2. Run `GRADIENT_TAG_GENERATOR.py` using any Python runner or coding application such as:  
   - Pydroid
   - Visual Studio Code  
   - Termux

Make sure you have **Python 3.x** installed.

---

## Usage

1. Run the script:  
```bash
python GRADIENT_TAG_GENERATOR.py
```
2.Follow the prompts to select:
• Number of steps (8–32)
• Mode: Smooth Gradient or Shiny Wave Gradient
• Base or multiple colors
• Key name for the gradient
3.Preview the generated colors in your terminal
## License
This project is licensed under the MIT License. 
## Example
```
Enter steps(8–32)(recommended 16): 16
Choose mode: 1
Enter color (or 'done'): red
Enter color (or 'done'): blue
Enter color (or 'done'): done
Enter key (e.g. WAVE_1): WAVE_1

Generated:

WAVE_1 = [
    (1.0, 0.0, 0.0),
    (0.937, 0.0, 0.062),
    ...
]
```
Preview available in Terminal Animation
