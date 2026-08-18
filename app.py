import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Havayolu markaları, kodları ve kurumsal renkleri (Koyuluk dengesine göre seçilmiştir)
AIRLINE_BRANDS = {
    "THY": {
        "name": "Turkish Airlines",
        "color": "#C8102E",
    },  # Türk Hava Yolları Kırmızısı
    "PGT": {"name": "Pegasus Airlines", "color": "#FFCC00"},  # Pegasus Sarısı
    "DLH": {"name": "Lufthansa", "color": "#051C2C"},  # Lufthansa Koyu Lacivert
    "BAW": {"name": "British Airways", "color": "#07519E"},  # British Mavisi
    "AFR": {"name": "Air France", "color": "#002157"},  # Air France Koyu Mavi
    "KLM": {"name": "KLM Royal Dutch", "color": "#00A1DE"},  # KLM Açık Mavi
    "RYR": {"name": "Ryanair", "color": "#003399"},  # Ryanair Mavi
    "EZY": {"name": "easyJet", "color": "#FF6600"},  # easyJet Turuncu
    "UAE": {"name": "Emirates", "color": "#D71921"},  # Emirates Kırmızısı
    "QTR": {"name": "Qatar Airways", "color": "#5C0632"},  # Katar Bordo/Mor
}


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/data")
def get_flight_data():
  try:
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
      data = response.json()
      states = data.get("states", [])
      flights = []

      for s in states[:250]:  # Yoğun trafik için limit artırıldı
        if s[5] and s[6] and s[1]:
          callsign = s[1].strip()
          if callsign:
            prefix = callsign[:3].upper()

            # Havayolu markasını ve rengini belirle
            airline_info = AIRLINE_BRANDS.get(
                prefix,
                {"name": s[2].strip() if s[2] else "Global Airline", "color": "#4A5568"} # Varsayılan koyu gri/mavi
            )

            speed_kmh = int(s[9] * 3.6) if s[9] else 750
            alt_ft = int(s[13] * 3.28084) if s[13] else 35000
            heading = s[10] if s[10] else 0

            flights.append({
                "id": s[0],
                "callsign": callsign,
                "airlineName": airline_info["name"],
                "brandColor": airline_info["color"],
                "route": "Active Route",
                "speed": speed_kmh,
                "alt": alt_ft,
                "progress": 50,
                "lat": s[6],
                "lon": s[5],
                "heading": heading,
            })
      return jsonify(flights)
  except Exception as e:
    print("API Hatası:", e)

  return jsonify([])


if __name__ == "__main__":
  app.run(debug=True)
  
