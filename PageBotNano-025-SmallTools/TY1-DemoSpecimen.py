#
#    Generate waterfall for a number of installed fonts
#    selected by a pattern in the name.
#
#    Run this is DrawBotApp - drawbot.com
#
W = 595 # Width of the page in points. 595 is equivalent of A4 210mm
H = 842 # Height of the page in points, equivalent of A4 297mm
M = 60 # Margin in points
FS = 24 # Size of the font name title
LEADING = 1.2 # Leading factor of font size
TEXT = 'Hamburgonstiv' # Same
namePattern = 'Verdana' # Your own font name pattern here

for name in installedFonts(): # Test all fonts in the system
    if namePattern in name: # If the search pattern is in this font name
        print('Making page for', name)
        y = H - M # Top of the page
        newPage(W, H) # Create a new page for each found font
        font(name) # Set the font to the selection of this page
        fontSize(FS ) # Set to title size.
        text(name, (M, y)) # Draw the name of the font as font.
        y -= FS # Move vertical position down
        for fs in range(8, 100): # For this range of font sizes
            fontSize(fs) # Set the font size
            text(TEXT + ' '+ str(fs) + 'pt', (M, y)) # Add size to sample text
            y -= fs * LEADING # Move next vertical position down
            if y < M: # Position still above bottom margin?
                break # Otherwise stop the waterfall for this font

# Construct export file name for this search pattern
fileName = 'TY1-DemoSpecimen-%s.pdf' % namePattern
print('Saving file', fileName)
saveImage(fileName)
