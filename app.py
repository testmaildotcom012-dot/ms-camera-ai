from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageEnhance, ImageFilter
import base64
import io

app = Flask(__name__)
CORS(app)

def enhance_iphone16pro_s25_8k(img):
    # 1. Original size save
    w, h = img.size
    
    # 2. iPhone 16 Pro Color Science - Vibrant but natural
    # Color 1.35 = iPhone vivid
    img = ImageEnhance.Color(img).enhance(1.35)
    # Contrast 1.25 = Deep HDR
    img = ImageEnhance.Contrast(img).enhance(1.25)
    # Brightness 1.08 = S24/S25 bright night
    img = ImageEnhance.Brightness(img).enhance(1.08)
    
    # 3. Super Sharpness - Unsharp Mask like DSLR
    # Sharpen + Detail Enhance
    img = img.filter(ImageFilter.UnsharpMask(radius=2.5, percent=180, threshold=2))
    img = ImageEnhance.Sharpness(img).enhance(2.2)
    
    # 4. Noise Clean - S25 Night Mode
    img = img.filter(ImageFilter.MedianFilter(size=3))
    
    # 5. 8K Upscale - Progressive Super Resolution
    # Target: 8K = 7680px long edge, but keep ratio
    # For mobile speed: max 4K if normal, 8K if requested
    mode = "4K"
    try:
        # Check if request wants 8K
        if hasattr(enhance_iphone16pro_s25_8k, 'target_8k') and enhance_iphone16pro_s25_8k.target_8k:
            target = 7680
            mode = "8K"
        else:
            target = 3840
    except:
        target = 3840
    
    # Only upscale if smaller than target
    if max(w, h) < target:
        scale = target / max(w, h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        # LANCZOS = best quality for photo (like iPhone)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        # Second sharpen after upscale for 50x clear zoom
        img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=1))
    
    return img

@app.route('/')
def home():
    return "M S Camera Cloud AI V2 - 8K Ready! iPhone 16 Pro + S25 Ultra Engine Active!"

@app.route('/enhance', methods=['POST'])
def enhance():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"error": "No image"}), 400
        
        # Check 8K mode from request
        is_8k = data.get('mode', '4k') == '8k'
        enhance_iphone16pro_s25_8k.target_8k = is_8k
        
        # Decode base64
        img_data = base64.b64decode(data['image'])
        img = Image.open(io.BytesIO(img_data)).convert("RGB")
        
        # Enhance
        enhanced = enhance_iphone16pro_s25_8k(img)
        
        # Encode back
        buffered = io.BytesIO()
        enhanced.save(buffered, format="JPEG", quality=95, optimize=True)
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            "enhanced_image": img_str,
            "status": "success",
            "mode": "8K" if is_8k else "4K",
            "engine": "iPhone16Pro+S25Ultra V2"
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)