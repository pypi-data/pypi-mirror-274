import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import random
import os

def fit_text_in_box(font, bounding_box, text):
    x, y, w, h = bounding_box
    best_font_size = 1
    best_num_lines = float('inf')
    best_text_lines = []
    vertical_offset = 0
    for font_size in range(1, h):
        current_font = ImageFont.truetype(font, font_size)
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        text_width, text_height = draw.textbbox((0, 0), text, font=current_font)[2:]
        lines = []
        line = ''
        for word in text.split():
            if draw.textbbox((0, 0), line + word, font=current_font)[2] <= w:
                line += word + ' '
            else:
                lines.append(line.strip())
                line = word + ' '
        if line:
            lines.append(line.strip())
        num_lines = len(lines)
        total_text_height = text_height * num_lines
        if total_text_height <= h and (num_lines < best_num_lines or (num_lines == best_num_lines and font_size > best_font_size)):
            best_font_size = font_size
            best_num_lines = num_lines
            best_text_lines = lines
            vertical_offset = (h - total_text_height) // 2
    return best_font_size, best_text_lines, vertical_offset

def create_watermark_from_text(text, font_path, image_width, image_height):
    pil_img = Image.new('RGB', (image_width, image_height), (0, 0, 0))
    draw = ImageDraw.Draw(pil_img)
    font_size, lines, vertical_offset = fit_text_in_box(font_path, (0, 0, image_width, image_height), text)
    font = ImageFont.truetype(font_path, font_size)
    y = vertical_offset
    for line in lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        x = (image_width - text_width) // 2
        draw.text((x, y), line, font=font, fill=(255, 255, 255))
        y += text_height
    return np.array(pil_img)

def insert_watermark_pass(img, watermark):
    return img

def insert_watermark_simple(img, watermark):
    watermark = cv2.cvtColor(watermark, cv2.COLOR_RGB2BGR)
    mask = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)
    mask = cv2.bitwise_not(mask)
    mask = cv2.merge([mask, mask, mask])
    img = cv2.bitwise_and(img, mask)
    img = cv2.add(img, watermark)
    return img

def insert_watermark_simple_adaptive(img, watermark):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2RGB)
    h_img, w_img, _ = img.shape
    ht, wd, cc = watermark.shape
    watermark_padded = np.full((h_img, w_img, cc), (255, 255, 255), dtype=np.uint8)
    xx, yy = (w_img - wd) // 2, (h_img - ht) // 2
    watermark_padded[yy:yy+ht, xx:xx+wd] = watermark
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    weber = np.abs(gray_img - 128) / 128.0
    H = np.zeros_like(gray_img, dtype=float)
    for row in range(h_img):
        for col in range(w_img):
            Lx, Ux = max(0, col-2), min(w_img, col+2)
            Ly, Uy = max(0, row-2), min(h_img, row+2)
            local_region = gray_img[Ly:Uy, Lx:Ux].flatten()
            probabilities = np.bincount(local_region) / local_region.size
            probabilities = probabilities[probabilities > 0]
            H[row, col] = -np.sum(probabilities * np.log2(probabilities))
    J = weber * H
    a, b, c, d = 0.7, 0.8, 0.25, 0.1160
    alpha = (b - a) * (J - J.min()) / (J.max() - J.min()) + a
    beta = (d - c) * (J - J.min()) / (J.max() - J.min()) + c
    final_image = alpha[..., None] * img + beta[..., None] * watermark_padded
    final_image = final_image.clip(0, 255).astype(np.uint8)
    return cv2.cvtColor(final_image, cv2.COLOR_RGB2BGR)

if __name__ == '__main__':
    font = os.path.join('fonts', random.choice(os.listdir('fonts')))
    img = cv2.imread('example.jpg')
    watermark = create_watermark_from_text('Lorem ipsum', font, img.shape[1], img.shape[0])
    img1 = insert_watermark_pass(img, watermark)
    img2 = insert_watermark_simple(img, watermark)
    img3 = insert_watermark_simple_adaptive(img, watermark)
    cv2.imshow('watermark', np.array(watermark))
    cv2.imshow('insert_watermark_pass', img1)
    cv2.imshow('insert_watermark_simple', img2)
    cv2.imshow('insert_watermark_simple_adaptive', img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()