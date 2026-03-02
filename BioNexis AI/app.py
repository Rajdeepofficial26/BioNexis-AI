from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
import numpy as np
import io
import logging
import warnings
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


app = Flask(__name__)

logging.getLogger("grpc").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

print("✅ AeroBioForensic AI Backend Initialized (Offline Mode)")



def analyze_stain(original_image, mask):

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_area = 0
    shape_labels = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        total_area += area

        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue

        circularity = 4 * np.pi * (area / (perimeter * perimeter))

        if circularity > 0.75:
            shape_labels.append("Circular Drop")
        elif circularity > 0.4:
            shape_labels.append("Elongated Drip")
        else:
            shape_labels.append("Irregular Splash")

    red_channel = original_image[:, :, 2]
    similarity_score = 0

    if np.any(mask > 0):
        similarity_score = int((np.mean(red_channel[mask > 0]) / 255) * 100)

    if total_area > 20000:
        risk = "HIGH"
    elif total_area > 8000:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "area": int(total_area),
        "count": len(contours),
        "shapes": list(set(shape_labels)),
        "similarity": similarity_score,
        "risk": risk
    }


def detect_stain(image_path):

    original_image = cv2.imread(image_path)

    if original_image is None:
        raise Exception("Image could not be loaded.")

    hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)

    analytics = analyze_stain(original_image, mask)
    evidence_id = f"EVID-{np.random.randint(1000,9999)}"

    return analytics, evidence_id



def generate_ai_report(analytics, evidence_id):

    area = analytics["area"]
    count = analytics["count"]
    shapes = ", ".join(analytics["shapes"])
    similarity = analytics["similarity"]
    risk = analytics["risk"]

    # Question 1
    q1 = f"I observe {count} stain formations covering approximately {area} square pixels."

    # Question 2
    if similarity > 60:
        q2 = "Yes, it strongly resembles a blood-like stain based on color similarity."
    elif similarity > 40:
        q2 = "It moderately resembles a blood-like stain."
    else:
        q2 = "The similarity is low, so confirmation requires further testing."

    # Question 3
    shape_explanation = []
    if "Circular Drop" in analytics["shapes"]:
        shape_explanation.append("circular drops suggest passive dripping")
    if "Elongated Drip" in analytics["shapes"]:
        shape_explanation.append("elongated shapes suggest directional movement")
    if "Irregular Splash" in analytics["shapes"]:
        shape_explanation.append("irregular splashes suggest impact force")

    if shape_explanation:
        q3 = "The stain shapes suggest " + ", ".join(shape_explanation) + "."
    else:
        q3 = "No clear shape pattern detected."

    # Question 4
    q4 = f"The similarity score of {similarity}% indicates how closely the detected color matches typical blood-like coloration."

    # Question 5
    if risk == "HIGH":
        conclusion = "The pattern suggests a significant blood event."
    elif risk == "MEDIUM":
        conclusion = "The pattern suggests a moderate bleeding event."
    else:
        conclusion = "The pattern suggests a minor or controlled bleeding event."

    report = f"""

System Data:
Evidence ID: {evidence_id}
Total Area: {area}
Stain Count: {count}
Shape Types: {shapes}
Similarity Score: {similarity}%
Risk Level: {risk}

1. What do you see?
{q1}

2. Does it look like a blood-like stain?
{q2}

3. What do the stain shapes suggest?
{q3}

4. What does the similarity score mean?
{q4}

5. Final conclusion (short and direct).
{conclusion}
"""

    return report.strip()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    upload_path = "uploaded_image.jpg"
    file.save(upload_path)

    try:
        analytics, evidence_id = detect_stain(upload_path)
        ai_report = generate_ai_report(analytics, evidence_id)

        os.remove(upload_path)

        return jsonify({
            "analytics": analytics,
            "evidence_id": evidence_id,
            "ai_report": ai_report
        })

    except Exception as e:
        print("ANALYSIS ERROR:", e)
        return jsonify({"error": "Image analysis failed"}), 500



@app.route("/export_pdf", methods=["POST"])
def export_pdf():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    
    normal_style = styles["Normal"]
    normal_style.spaceAfter = 8

    elements.append(Paragraph("AeroBioForensic AI Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Evidence ID: {data.get('evidence_id','N/A')}", normal_style))
    elements.append(Paragraph(f"Risk Level: {data.get('risk','N/A')}", normal_style))
    elements.append(Paragraph(f"Similarity: {data.get('similarity','N/A')}%", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Full Forensic Analysis:", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Preserve formatting
    for line in data.get("ai_report", "").split("\n"):
        elements.append(Paragraph(line.strip(), normal_style))

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="AeroBioForensic_Report.pdf",
        mimetype="application/pdf"
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)