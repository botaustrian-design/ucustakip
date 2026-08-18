import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/data")
def get_flight_data():
  try:
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
      data = response.json()
      states = data.get("states", [])
      flights = []

      for s in states[:60]:
        if s[5] and s[6] and s[1]:
          callsign = s[1].strip()
          if callsign:
            speed_kmh = int(s[9] * 3.6) if s[9] else 750
            alt_ft = int(s[13] * 3.28084) if s[13] else 35000

            flights.append({
                "id": s[0],
                "callsign": callsign,
                "airlineName": s[2] if s[2] else "International Flight",
                "route": "Live Tracking",
                "speed": speed_kmh,
                "alt": alt_ft,
                "progress": 50,
                "lat": s[6],
                "lon": s[5],
            })
      return jsonify(flights)
  except Exception as e:
    print("API Hatası:", e)

  return jsonify([])


if __name__ == "__main__":
  app.run(debug=True)
    
