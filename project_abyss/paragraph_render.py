from settings import *

def render_paragraph(text, font, max_width, colour=(0, 0, 0)):
    words = text.split()
    line = ""
    paragraph = ""
    i = 0
    lines = []

    while i < len(words):
        word = words[i]

        if line == "": extended_line = word
        else: extended_line = line + " " + word

        if font.size(extended_line)[0] <= max_width:
            line = extended_line #extended line does not excede max width. extend the line by one word
            i += 1
        else: #extended line is too long. start new line
            lines.append(line)
            paragraph += line + "\n"
            line = ""
            extended_line = ""
    
    paragraph += line #add the final line, as it is not added in the loop
    
    return font.render(paragraph, True, colour)