@echo off
echo =========================================================================
echo   Starting NSUT Campus Navigator & Resource Optimizer
echo   Local Web Server running at: http://localhost:8000
echo   (Enables HTML5 Browser Geolocation, High-Accuracy GPS, and Live Tracking)
echo =========================================================================

start http://localhost:8000
python -m http.server 8000
