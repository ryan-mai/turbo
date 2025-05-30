from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import BikeRide
from .extensions import db
import requests, os, csv, json
from io import TextIOWrapper
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    rides = BikeRide.query.filter_by(user_id=current_user.id).order_by(BikeRide.date.desc()).all()
    return render_template('dashboard.html', rides=rides)

@main_bp.route('/weather')
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    api_key = os.getenv('OPENWEATHER_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    temp = data.get("main", {}).get("temp")
    return jsonify({"temp": temp})

@main_bp.route('/import_rides', methods=['POST'])
@login_required
def import_rides():
    file = request.files.get('ridefile')
    if not file:
        flash('No file uploaded.', 'danger')
        return redirect(url_for('main.dashboard'))
    try:
        filename = file.filename.lower()
        imported = 0
        skipped = 0

        if filename.endswith('.json'):
            data = json.load(file)
            for row in data:
                ride_date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M')
                distance = float(row['distance_km'])
                duration = float(row['duration_min'])
                exists = BikeRide.query.filter_by(
                    user_id=current_user.id,
                    date=ride_date,
                    distance_km=distance
                ).first()
                if exists:
                    skipped += 1
                    continue
                ride = BikeRide(
                    user_id=current_user.id,
                    date=ride_date,
                    distance_km=distance,
                    duration_min=duration
                )
                db.session.add(ride)
                imported += 1
        else:
            stream = TextIOWrapper(file.stream, encoding='utf-8')
            if filename.endswith('.tsv'):
                reader = csv.DictReader(stream, delimiter='\t')
            else:
                reader = csv.DictReader(stream)
            for row in reader:
                ride_date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M')
                distance = float(row['distance_km'])
                duration = float(row['duration_min'])
                exists = BikeRide.query.filter_by(
                    user_id=current_user.id,
                    date=ride_date,
                    distance_km=distance
                ).first()
                if exists:
                    skipped += 1
                    continue
                ride = BikeRide(
                    user_id=current_user.id,
                    date=ride_date,
                    distance_km=distance,
                    duration_min=duration
                )
                db.session.add(ride)
                imported += 1

        db.session.commit()
        if skipped > 0:
            flash(f'ERROR: Found Duplicate Log', 'duplicate')
        if imported > 0:
            flash(f'Rides imported: {imported}.', 'success')
    except Exception as e:
        flash(f'Import failed: {e}', 'danger')
    return redirect(url_for('main.dashboard'))