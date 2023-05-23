from flask import Flask, render_template, request
import math
import os

app = Flask(__name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers

    # Convert latitude and longitude to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c

    return distance

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        my_lat = float(request.form['my_lat'])
        my_lon = float(request.form['my_lon'])
        coordinates = request.form['coordinates']
        coordinates_list = coordinates.split('\n')

        distances = []
        for coordinate in coordinates_list:
            lat, lon = coordinate.split(',')
            lat = float(lat.strip())
            lon = float(lon.strip())
            distance = calculate_distance(my_lat, my_lon, lat, lon)
            distances.append(((lat, lon), distance))

        return render_template('result.html', distances=distances)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
