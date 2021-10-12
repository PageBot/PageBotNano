#
#    Generate waterfall for all .ttf and .otf fonts in the
#    current directory for this scrpts.
#
#    Run this is DrawBotApp - drawbot.com
#
import os # Standard library to access the file system

W = 595 # Width of the page in points. 595 is equivalent of A4 210mm
H = 842 # Height of the page in points, equivalent of A4 297mm
M = 60 # Margin in points
FS = 16# Size of the font name title
LEADING = 1.2 # Leading factor of font size
TEXT = 'Hamburgonstiv' # Sample of the waterfall lines
fontPath = './' # Take current folder of this script

for fileName in os.listdir(fontPath): # Look through all files in this directory
    if not fileName.lower().endswith('.ttf') and not fileName.lower().endswith('.otf'):
        continue # This is not a font name, continue the search
    
    print('Making page for', fileName)
    y = H - M # Top of the page
    newPage(W, H) # Create a new page for each found font
    font(fileName) # Set the font to the selection of this page
    fontSize(FS ) # Set to title size.
    text(fileName, (M, y)) # Draw the name of the font as font.
    y -= FS # Move vertical position down

    for fs in range(8, 100): # For this range of font sizes
        fString = FormattedString(TEXT, font=fileName, fontSize=fs)
        # Add small string to the line with the pointsize in fixed size
        fString += FormattedString(' '+ str(fs) + 'pt', font=fileName, fontSize=FS/2)
        text(fString, (M, y)) # Draw the waterfall line
        y -= fs * LEADING # Move next vertical position down
        if y < M: # Position still above bottom margin?
            break # Otherwise stop the waterfall for this font

# Construct export file name for this search pattern
filePath = fontPath + 'TY1-DemoSpecimen-TTF-OTF.pdf' 
print('Saving file', filePath)
saveImage(filePath)
