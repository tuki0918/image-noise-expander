import numpy as np
from PIL import Image
import gradio as gr

def expand_with_noise_and_crop_gradio(img, mode='outside', shift_pct=30, direction='bottom'):
    img = img.convert('RGB')
    w, h = img.size
    shift_pct_decimal = shift_pct / 100.0
    shift_w = int(w * shift_pct_decimal)
    shift_h = int(h * shift_pct_decimal)
    noise_strength = 0.1

    if mode == 'inside':
        # 画像を内側に処理する場合
        img_array = np.array(img)
        
        if direction == 'bottom':
            noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(shift_h, w, 3))
            noise = np.clip(noise, 0, 255).astype(np.uint8)
            img_array[h-shift_h:h] = noise
            
            # 内側処理領域のマスク作成（処理領域=白、元画像=黒）
            mask = Image.new('L', (w, h), color=0)
            mask_array = np.array(mask)
            mask_array[h-shift_h:h] = 255
            mask = Image.fromarray(mask_array)
            
        elif direction == 'top':
            noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(shift_h, w, 3))
            noise = np.clip(noise, 0, 255).astype(np.uint8)
            img_array[0:shift_h] = noise
            
            # 内側処理領域のマスク作成（処理領域=白、元画像=黒）
            mask = Image.new('L', (w, h), color=0)
            mask_array = np.array(mask)
            mask_array[0:shift_h] = 255
            mask = Image.fromarray(mask_array)
            
        elif direction == 'right':
            noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(h, shift_w, 3))
            noise = np.clip(noise, 0, 255).astype(np.uint8)
            img_array[:, w-shift_w:w] = noise
            
            # 内側処理領域のマスク作成（処理領域=白、元画像=黒）
            mask = Image.new('L', (w, h), color=0)
            mask_array = np.array(mask)
            mask_array[:, w-shift_w:w] = 255
            mask = Image.fromarray(mask_array)
            
        elif direction == 'left':
            noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(h, shift_w, 3))
            noise = np.clip(noise, 0, 255).astype(np.uint8)
            img_array[:, 0:shift_w] = noise
            
            # 内側処理領域のマスク作成（処理領域=白、元画像=黒）
            mask = Image.new('L', (w, h), color=0)
            mask_array = np.array(mask)
            mask_array[:, 0:shift_w] = 255
            mask = Image.fromarray(mask_array)
            
        else:
            raise ValueError(f"Invalid direction: {direction}. Must be one of top, bottom, left, right.")
            
        return Image.fromarray(img_array), mask

    if direction == 'bottom':
        new_img = Image.new('RGB', (w, h + shift_h), color=(0, 0, 0))
        new_img.paste(img, (0, 0))
        noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(shift_h, w, 3))
        noise = np.clip(noise, 0, 255).astype(np.uint8)
        new_img.paste(Image.fromarray(noise), (0, h))
        cropped = new_img.crop((0, shift_h, w, shift_h + h))
        
        # 拡張領域のマスク作成（拡張領域=白、元画像=黒）
        mask = Image.new('L', (w, h), color=0)
        mask_array = np.array(mask)
        mask_array[h-shift_h:h] = 255
        mask = Image.fromarray(mask_array)

    elif direction == 'top':
        new_img = Image.new('RGB', (w, h + shift_h), color=(0, 0, 0))
        new_img.paste(img, (0, shift_h))
        noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(shift_h, w, 3))
        noise = np.clip(noise, 0, 255).astype(np.uint8)
        new_img.paste(Image.fromarray(noise), (0, 0))
        cropped = new_img.crop((0, 0, w, h))
        
        # 拡張領域のマスク作成（拡張領域=白、元画像=黒）
        mask = Image.new('L', (w, h), color=0)
        mask_array = np.array(mask)
        mask_array[0:shift_h] = 255
        mask = Image.fromarray(mask_array)

    elif direction == 'right':
        new_img = Image.new('RGB', (w + shift_w, h), color=(0, 0, 0))
        new_img.paste(img, (0, 0))
        noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(h, shift_w, 3))
        noise = np.clip(noise, 0, 255).astype(np.uint8)
        new_img.paste(Image.fromarray(noise), (w, 0))
        cropped = new_img.crop((shift_w, 0, shift_w + w, h))
        
        # 拡張領域のマスク作成（拡張領域=白、元画像=黒）
        mask = Image.new('L', (w, h), color=0)
        mask_array = np.array(mask)
        mask_array[:, w-shift_w:w] = 255
        mask = Image.fromarray(mask_array)

    elif direction == 'left':
        new_img = Image.new('RGB', (w + shift_w, h), color=(0, 0, 0))
        new_img.paste(img, (shift_w, 0))
        noise = np.random.normal(loc=127, scale=255 * noise_strength, size=(h, shift_w, 3))
        noise = np.clip(noise, 0, 255).astype(np.uint8)
        new_img.paste(Image.fromarray(noise), (0, 0))
        cropped = new_img.crop((0, 0, w, h))
        
        # 拡張領域のマスク作成（拡張領域=白、元画像=黒）
        mask = Image.new('L', (w, h), color=0)
        mask_array = np.array(mask)
        mask_array[:, 0:shift_w] = 255
        mask = Image.fromarray(mask_array)

    else:
        raise ValueError(f"Invalid direction: {direction}. Must be one of top, bottom, left, right.")

    return cropped, mask

def create_gradio_interface():
    demo = gr.Interface(
        fn=expand_with_noise_and_crop_gradio,
        inputs=[
            gr.Image(type="pil"),
            gr.Radio(["outside", "inside"], value="outside", label="Mode"),
            gr.Slider(0, 50, value=30, step=1, label="Shift Percentage (%)"),
            gr.Radio(["top", "bottom", "left", "right"], value="bottom", label="Direction")
        ],
        outputs=[
            gr.Image(type="pil", label="Output Image", format="png"),
            gr.Image(type="pil", label="Mask", format="png")
        ],
        title="Expand Image with Noise and Crop + Mask",
        description="Upload an image and apply noise-based expansion and cropping in the selected direction. Also generates an expansion area mask for the extended regions.",
        flagging_mode="never"
    )
    
    return demo


if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch()
