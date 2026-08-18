from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_flight_data():
    try:
        url = "https://opensky-network.org/api/states/all"
        response = requests.get(url, timeout=10)
        data = response.json()
        states = data.get('states', [])
        flights = []
        for s in states[:30]:
            if s[5] and s[6]:
                flights.append({
                    "id": s[0], 
                    "callsign": s[1].strip() if s[1] else "Bilinmiyor",
                    "airline": "Bilinmiyor", 
                    "lat": s[6], 
                    "lon": s[5],
                    "speed": round(s[9]*3.6) if s[9] else 0, 
                    "alt": round(s[7]*3.28) if s[7] else 0,
                    "route": "Aktif"
                })
        return jsonify(flights)
    except:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
  
