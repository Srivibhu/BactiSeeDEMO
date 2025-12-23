from flask import Flask, request, jsonify
from flask_cors import CORS  # Allows frontend to talk to backend
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
CORS(app) # Enables local testing across different ports

# 1. THE EXTRACTION LOGIC
# Adaptive threshold based on image brightness distribution.
ADAPTIVE_STD_MULTIPLIER = 0.8

# Glare guard tuning (lower saturation + low texture + very bright).
GLARE_BRIGHT_STD_MULTIPLIER = 1.5
GLARE_SATURATION_MAX = 20
GLARE_CONTRAST_MAX = 10

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Receives a single image, extracts bright pixel data, 
    and returns a contamination assessment.
    """
    try:
        # Check if the 'image' file was actually sent
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
            
        file = request.files['image'].read()
        
        # Open the image using Pillow (PIL)
        img = Image.open(io.BytesIO(file)).convert('RGB')
        arr = np.asarray(img, dtype=np.float32)

        # Grayscale luminance
        gray = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]

        # 2. THE QUANTIFICATION LOGIC
        # Adaptive threshold based on mean/std to reduce lighting bias.
        mean = float(gray.mean())
        std = float(gray.std())
        adaptive_threshold = mean + (ADAPTIVE_STD_MULTIPLIER * std)

        # Glare guard: very bright + low saturation + low texture.
        sat = arr.max(axis=2) - arr.min(axis=2)
        gx = np.abs(gray[:, 1:] - gray[:, :-1])
        gy = np.abs(gray[1:, :] - gray[:-1, :])
        gx = np.pad(gx, ((0, 0), (0, 1)), mode='edge')
        gy = np.pad(gy, ((0, 1), (0, 0)), mode='edge')
        contrast = gx + gy

        glare_mask = (
            (gray > (mean + (GLARE_BRIGHT_STD_MULTIPLIER * std)))
            & (sat < GLARE_SATURATION_MAX)
            & (contrast < GLARE_CONTRAST_MAX)
        )

        bacteria_mask = (gray > adaptive_threshold) & (~glare_mask)
        bacteria_count = int(bacteria_mask.sum())
        
        # 3. REAL-TIME ASSESSMENT
        # Determine safety status based on the count
        total_pixels = gray.size
        contamination_percent = (bacteria_count / total_pixels) * 100

        # In a real room, 1-5% brightness might be normal 'Safe' noise.
        # We only flag it as 'Danger' if it's very high.
        status = "Safe"
        if contamination_percent > 6:
            status = "Danger"
        elif contamination_percent > 2:
            status = "Warning"

        return jsonify({
            "status": "success",
            "bacteriaCount": bacteria_count,
            "percentage": round(contamination_percent, 2),
            "safetyLevel": status
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# 4. LOCAL RUNNER (For testing in VS Code)
if __name__ == "__main__":
    print("BactiSee Backend running locally at http://127.0.0.1:3000")
    app.run(debug=True, port=3000)
