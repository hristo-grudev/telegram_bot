def draw_text_with_outline(draw, position, text, font, text_color="white", outline_color="black", outline_width=2):
    # Draw outline
    x, y = position
    draw.text((x - outline_width, y - outline_width), text, font=font, fill=outline_color)
    draw.text((x + outline_width, y - outline_width), text, font=font, fill=outline_color)
    draw.text((x - outline_width, y + outline_width), text, font=font, fill=outline_color)
    draw.text((x + outline_width, y + outline_width), text, font=font, fill=outline_color)
    draw.text((x - outline_width, y), text, font=font, fill=outline_color)
    draw.text((x + outline_width, y), text, font=font, fill=outline_color)
    draw.text((x, y - outline_width), text, font=font, fill=outline_color)
    draw.text((x, y + outline_width), text, font=font, fill=outline_color)

    # Draw main text
    draw.text(position, text, font=font, fill=text_color)