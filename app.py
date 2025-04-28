from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # atau langsung hardcode buat testing

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', lat=None, lng=None)

@app.route('/geocode', methods=['POST'])
def geocode():
    location = request.form.get('location')
    if location:
        endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_API_KEY}'
        response = requests.get(endpoint)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'OK':
                lat = result['results'][0]['geometry']['location']['lat']
                lng = result['results'][0]['geometry']['location']['lng']
                formatted_address = result['results'][0]['formatted_address']  # 🔥 ini dia
                return render_template('index.html', lat=lat, lng=lng, location=location, address=formatted_address)
            else:
                error = f"Lokasi tidak ditemukan: {result['status']}"
                return render_template('index.html', error=error)
        else:
            error = "Gagal mengambil data dari Google Maps API."
            return render_template('index.html', error=error)
    else:
        error = "Silakan masukkan nama lokasi."
        return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
