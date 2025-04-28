import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")  # Set di Cloud Run atau .env

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/geocode', methods=['POST'])
def geocode():
    location = request.form.get('location')
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_API_KEY}'
    response = requests.get(url)
    result = response.json()
    if result['status'] == 'OK':
        latlng = result['results'][0]['geometry']['location']
        formatted_address = result['results'][0]['formatted_address']
        return render_template('index.html', lat=latlng['lat'], lng=latlng['lng'], location=location, address=formatted_address)
    else:
        return render_template('index.html', error="Lokasi tidak ditemukan.")

@app.route('/reverse_geocode', methods=['POST'])
def reverse_geocode():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_API_KEY}'
    response = requests.get(url)
    result = response.json()
    if result['status'] == 'OK':
        formatted_address = result['results'][0]['formatted_address']
        return jsonify({
            'success': True,
            'lat': lat,
            'lng': lng,
            'address': formatted_address
        })
    else:
        return jsonify({'success': False, 'error': 'Lokasi tidak ditemukan.'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
