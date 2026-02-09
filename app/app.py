from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        ciudad = request.form.get('ciudad', '')
        
        # Buscar gasolineras en la ciudad especificada
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"gasolinera {ciudad}",
            "format": "json",
            "limit": 10,  # Buscar varias gasolineras
            "addressdetails": 1
        }
        headers = {
            "User-Agent": "Flask-Gas-Station-Finder"
        }
        
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if data:
            # Procesar todas las gasolineras encontradas
            gasolineras = []
            for item in data:
                gasolineras.append({
                    'nombre': item.get('display_name', 'Gasolinera'),
                    'lat': float(item['lat']),
                    'lon': float(item['lon']),
                    'direccion': item.get('display_name', '')
                })
            
            # Centro del mapa (primera gasolinera)
            centro_lat = gasolineras[0]['lat']
            centro_lon = gasolineras[0]['lon']
            
            return render_template(
                'map.html',
                gasolineras=gasolineras,
                centro_lat=centro_lat,
                centro_lon=centro_lon,
                ciudad=ciudad,
                total=len(gasolineras)
            )
        
        return render_template('map.html', error=True, ciudad=ciudad)
    
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)