🚀 BioNexis AI
AI-Powered Bloodstain Pattern Analysis System

🧠 Overview
BioNexis AI is a computer vision–based forensic analysis system designed to detect, analyze, and interpret blood-like stain patterns from images.

This project combines image processing, contour analytics, and structured reasoning to generate explainable forensic reports.

It simulates a tactical forensic HUD interface inspired by drone-based field deployment systems.

The system runs fully offline using OpenCV and Flask.

No paid APIs. No cloud dependency. Pure analytical logic.

🎯 Problem Statement
Bloodstain pattern analysis plays a critical role in forensic investigations.

Traditional analysis relies heavily on manual observation.

This can introduce subjectivity and inconsistency.

There is a need for structured, computational assistance.

BioNexis AI addresses this gap.

⚙️ How It Works
User uploads an image.
System detects red-spectrum regions using HSV masking.
Contours are extracted.
Surface area is calculated.
Stain shapes are classified.
Similarity score is computed.
Risk level is determined.
A structured forensic report is generated.
A professional PDF report can be exported.
All analysis is logic-based and explainable.

🧪 Core Analytics
Total stained area (in square pixels)

Stain count

Morphological classification:

Circular Drop
Elongated Drip
Irregular Splash
Chromatic similarity index

Risk classification (LOW / MEDIUM / HIGH)

🖥️ Interface Features
Tactical forensic HUD design
Drone telemetry simulation
Real-time altitude animation
Recording timer
Zoom controls
GPS-style location panel
PDF report generation
Risk glow indicators
Structured AI summary section
📊 Forensic Report Structure
The system generates a clear report answering:

What is observed?
Does it resemble a blood-like stain?
What do the shapes suggest?
What does the similarity score imply?
Final conclusion.
The report is structured and legally readable.

🛠️ Tech Stack
Backend:

Python
Flask
OpenCV
NumPy
ReportLab
Frontend:

HTML
CSS
JavaScript
Architecture: Input Layer → Detection Engine → Analytics Module → Reasoning Engine → PDF Generator

📌 Use Cases
Academic forensic demonstrations
Computer vision projects
Research prototypes
Structured evidence documentation
AI explainability showcase
🚀 Future Scope
Real-time camera streaming
Machine learning stain classifier
Heatmap overlay visualization
Case database integration
GPS coordinate logging
Multi-image batch processing
👥 Team
Developed by The BackEnd Boys