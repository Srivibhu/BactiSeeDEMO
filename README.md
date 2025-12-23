# BactiSee
TRY IT HERE: bacti-see-demo.vercel.app
A functional full-stack prototype for BactiSee, a smartphone-based application for rapid bacterial contamination detection. This project integrates a Python (Flask) image-processing backend with a Node.js/JavaScript frontend to deliver real-time contamination assessment through a graphical gauge.

Core FeaturesAdaptive Thresholding Algorithm: Implements a dynamic statistical filter ($Mean + k \cdot \sigma$) to extract contamination data while accounting for variable ambient lighting.Saturation-Based Glare Guard: A noise-reduction filter that identifies and ignores high-saturation specular reflections (glare) to ensure accurate quantification logic.Real-Time Contamination Gauge: A responsive UI that translates raw pixel data into a visual "Safe/Warning/Danger" assessment for the user.

Full-Stack Integration: A smooth workflow connecting a web-based frontend to a serverless Python backend via REST API.
Technical StackBackend: Python 3.10, Flask (API), Pillow (Image Processing).Frontend: Vanilla JavaScript, CSS3 (Flexbox/Grid), HTML5.
Deployment: Vercel (Serverless Functions).

The "Why" Behind the Logic: I built this prototype to address a specific challenge in mobile contamination detection: Ambient Noise. 1.  Extraction: By utilizing a grayscale conversion, the script extracts light intensity data.2.  Comparison: The adaptive threshold ensures that "brightness" is measured relative to the specific surface being scanned, functioning as a virtual baseline comparison tool.3.  Optimization: The glare guard prevents false positives caused by shiny surfaces in a lab environment.
