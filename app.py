import os
import requests
from flask import Flask, render_template, request

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
        return render_template('index.html', lat=latlng['lat'], lng=latlng['lng'], location=location)
    else:
        return render_template('index.html', error="Lokasi tidak ditemukan.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)