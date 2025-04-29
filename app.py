import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Gunakan API Key dari environment (di Cloud Run atau lokal .env)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") # or 'ISI_API_KEY_KAMU'

@app.route('/')
def index():
    return render_template('index.html', GOOGLE_API_KEY=GOOGLE_API_KEY)

@app.route('/geocode', methods=['POST'])
def geocode():
    location = request.form.get('location')
    if not location:
        return render_template('index.html', error="Lokasi tidak boleh kosong.", GOOGLE_API_KEY=GOOGLE_API_KEY)

    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_API_KEY}'
    response = requests.get(url)
    result = response.json()

    if result['status'] == 'OK':
        latlng = result['results'][0]['geometry']['location']
        formatted_address = result['results'][0]['formatted_address']
        return render_template('index.html', 
                               lat=latlng['lat'], 
                               lng=latlng['lng'], 
                               location=location, 
                               address=formatted_address,
                               GOOGLE_API_KEY=GOOGLE_API_KEY)
    else:
        return render_template('index.html', error="Lokasi tidak ditemukan.", GOOGLE_API_KEY=GOOGLE_API_KEY)


# @app.route('/reverse_geocode', methods=['POST'])
# def reverse_geocode():
#     data = request.json
#     lat = data.get('lat')
#     lng = data.get('lng')

#     if not lat or not lng:
#         return jsonify({'success': False, 'error': 'Latitude dan Longitude wajib diisi.'})

#     url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_API_KEY}'
#     response = requests.get(url)
#     result = response.json()

#     if result['status'] == 'OK':
#         formatted_address = result['results'][0]['formatted_address']
#         return jsonify({
#             'success': True,
#             'lat': lat,
#             'lng': lng,
#             'address': formatted_address
#         })
#     else:
#         return jsonify({'success': False, 'error': 'Lokasi tidak ditemukan.'})

@app.route('/reverse-geocode', methods=['POST'])
def reverse_geocode():
    lat = request.form.get('lat')
    lng = request.form.get('lng')

    api_key = os.environ.get('GOOGLE_API_KEY')  # pastikan diset di Cloud Run atau .env

    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK' and len(data['results']) > 0:
        formatted_address = data['results'][0]['formatted_address']
        return render_template('index.html', location=formatted_address, lat=lat, lng=lng)
    else:
        return render_template('index.html', error="Gagal menemukan alamat dari koordinat.")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
