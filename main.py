import numpy as np
from PIL import Image
import gradio as gr
import io

def expand_with_noise_and_crop_gradio(img, shift_pct=0.3, noise_strength=0.1, direction='bottom'):
    img = img.convert('RGB')
    w, h = img.size
    shift_w = int(w * shift_pct)
    shift_h = int(h * shift_pct)

    if direction == 'bottom':
        new_img = Image.new('RGB', (w, h + shift_h), color=(0, 0, 0))
        new_img.paste(img, (0, 0))
        noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(shift_h, w, 3))
        noise = np.clip(noise, 0, 255).astype(np.uint8)
        new_img.paste(Image.fromarray(noise, 'RGB'), (0, h))
        cropped = new_img.crop((0, shift_h, w, shift_h + h))

    elif direction == 'top':
        new_img = Image.new('RGB', (w, h + shift_h), color=(0, 0, 0))
        new_img.paste(img, (0, shift_h))
        noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(shift_h, w, 3))
        noise = np.clip(noise, 0, 255).astype(np.uint8)
        new_img.paste(Image.fromarray(noise, 'RGB'), (0, 0))
        cropped = new_img.crop((0, 0, w, h))

    elif direction == 'right':
        new_img = Image.new('RGB', (w + shift_w, h), color=(0, 0, 0))
        new_img.paste(img, (0, 0))
        noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(h, shift_w, 3))
        noise = np.clip(noise, 0, 255).astype(np.uint8)
        new_img.paste(Image.fromarray(noise, 'RGB'), (w, 0))
        cropped = new_img.crop((shift_w, 0, shift_w + w, h))

    elif direction == 'left':
        new_img = Image.new('RGB', (w + shift_w, h), color=(0, 0, 0))
        new_img.paste(img, (shift_w, 0))
        noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(h, shift_w, 3))
        noise = np.clip(noise, 0, 255).astype(np.uint8)
        new_img.paste(Image.fromarray(noise, 'RGB'), (0, 0))
        cropped = new_img.crop((0, 0, w, h))

    else:
        raise ValueError(f"Invalid direction: {direction}. Must be one of top, bottom, left, right.")

    return cropped

# Gradio インターフェース定義
demo = gr.Interface(
    fn=expand_with_noise_and_crop_gradio,
    inputs=[
        gr.Image(type="pil"),
        gr.Slider(0.0, 0.5, value=0.3, label="Shift Percentage"),
        gr.Slider(0.0, 1.0, value=0.1, label="Noise Strength"),
        gr.Radio(["top", "bottom", "left", "right"], value="bottom", label="Direction")
    ],
    outputs=gr.Image(type="pil"),
    title="Expand Image with Noise and Crop",
    description="Upload an image and apply noise-based expansion and cropping in the selected direction.",
    # flagを完全に無効化
    flagging_mode="never"
)

if __name__ == "__main__":
    demo.launch()
