from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageEnhance
import base64, io

app = Flask(__name__)
CORS(app)

def enhance_iphone16pro_s25(img):
    # S25 + iPhone 16 Pro style enhance - real AI er moto
    # 1. Sharpness
    img = ImageEnhance.Sharpness(img).enhance(1.8)
    # 2. Color - iPhone natural
    img = ImageEnhance.Color(img).enhance(1.25)
    # 3. Contrast - S25 Super HDR
    img = ImageEnhance.Contrast(img).enhance(1.15)
    # 4. Brightness
    img = ImageEnhance.Brightness(img).enhance(1.05)
    # 5. Upscale 2x - 12MP to 48MP
    w, h = img.size
    img = img.resize((w*2, h*2), Image.LANCZOS)
    return img

@app.route('/')
def home():
    return "M S Camera Cloud AI - S25 + iPhone 16 Pro Ready!"

@app.route('/enhance', methods=['POST'])
def enhance():
    try:
        data = request.json
        base64_img = data['image']
        mode = data.get('mode', 's25_iphone16pro')
        
        # Decode
        img_bytes = base64.b64decode(base64_img)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        
        # AI Enhance
        enhanced = enhance_iphone16pro_s25(img)
        
        # Encode back
        buf = io.BytesIO()
        enhanced.save(buf, format='JPEG', quality=95)
        out_base64 = base64.b64encode(buf.getvalue()).decode()
        
        return jsonify({
            "status": "success",
            "enhanced": out_base64,
            "mode": mode,
            "resolution": f"{enhanced.width}x{enhanced.height}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)