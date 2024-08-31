from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image, ImageDraw, ImageFont
import io

from telegram.ext import ContextTypes

from utils.templates import TEMPLATES
from utils.text_outline import draw_text_with_outline
from utils.wrap_text import wrap_text


def generate_meme(template_info: dict, texts: list[str]):
    template_path = template_info['path']
    color = template_info['color']
    font_size = template_info['font_size']
    text_boxes = template_info['text_boxes']

    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype('fonts/arial.ttf', font_size)

    for i, text in enumerate(texts):
        if i >= len(text_boxes):
            break

        box = text_boxes[i]
        position = box['position']
        size = box['size']

        lines = wrap_text(text, font, size[0], draw)
        text_height = sum(
            draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines
        )

        y = position[1] + (size[1] - text_height) // 2

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = position[0] + (size[0] - text_width) // 2
            draw_text_with_outline(
                draw,
                (x, y),
                line,
                font=font,
                text_color=color,
                outline_color="black",
                outline_width=3
            )
            y += bbox[3] - bbox[1]

    img_byte_arr = io.BytesIO()
    template.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    return img_byte_arr


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(value.get("name"), callback_data=key)] for key, value in TEMPLATES.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Изберете шаблон за вашето меме:', reply_markup=reply_markup)


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    template_choice = query.data
    template_info = TEMPLATES.get(template_choice, 'template1')
    expected_words = len(template_info['text_boxes'])

    await query.message.edit_text(f'Моля, въведете {expected_words} текста, разделени с "|".')

    context.user_data['template'] = template_choice
