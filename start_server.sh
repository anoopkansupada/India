#!/bin/bash

# Simple local web server for testing the India trip website
# This allows you to test with proper HTTP referrer restrictions

PORT=8000

echo "🚀 Starting local web server..."
echo ""
echo "📍 Open your browser and visit:"
echo "   http://localhost:$PORT/index.html"
echo ""
echo "🗺️  To test the map specifically:"
echo "   http://localhost:$PORT/test_map_final.html"
echo ""
echo "⚠️  Make sure your Google Maps API key has this referrer allowed:"
echo "   http://localhost:*/*"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 -m http.server $PORT
