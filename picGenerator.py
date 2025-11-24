from PIL import Image, ImageDraw, ImageFont
import io

def make_counter_png(count, width=192, height=108):
    img = Image.new('RGB', (width, height), color=(255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(20)
    text = f"Visits: {count}"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    position = ((width - text_w) // 2, (height - text_h) // 2)
    draw.text(position, text, fill=(0, 0, 0), font=font)

    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output


