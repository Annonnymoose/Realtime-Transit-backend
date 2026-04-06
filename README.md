# 🚌 Real-Time Transit Spatial API

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-REST_Framework-092E20.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-336791.svg)
![Leaflet](https://img.shields.io/badge/Frontend-Leaflet.js-199900.svg)

An enterprise-grade transit backend that ingests massive General Transit Feed Specification (GTFS) datasets, calculates spatial geographic queries, and serves real-time bus departures to a live interactive map.

## ✨ Key Features

* **Custom ETL Pipeline:** Automated Python scripts to extract, clean, and load hundreds of thousands of raw GTFS records (Routes, Trips, Stops, StopTimes) into a relational database.
* **Spatial Geography Engine:** Leverages PostgreSQL and PostGIS to convert raw latitude/longitude coordinates into complex spatial geometries.
* **"Near Me" Filtering:** Highly optimized spatial API endpoints that use PostGIS `DWithin` math to instantly find transit stops within a specified radius of a user's GPS coordinates.
* **N+1 Query Prevention:** Advanced Django ORM architecture utilizing `select_related` to execute complex SQL JOINs, delivering "Next Departure" times without crashing the server.
* **Interactive Frontend:** A decoupled HTML/JS frontend utilizing Leaflet.js to plot GeoJSON endpoints on a live map with dynamic, lazy-loaded arrival boards.

## 🛠️ Tech Stack

* **Backend Framework:** Django & Django REST Framework (DRF)
* **Spatial API Engine:** DRF-GIS & Django-Filter
* **Database:** PostgreSQL with PostGIS extension
* **Frontend Visualization:** Standard HTML/JS & Leaflet.js

## 🚀 API Endpoints

The RESTful API serves universally readable GeoJSON, allowing easy integration with any frontend mapping library.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/stops/` | Returns a paginated GeoJSON list of all bus stops. |
| `GET` | `/api/stops/?dist=3000&point=77.21,28.63` | **Spatial Filter:** Returns stops within a 3km radius of a specific Long/Lat coordinate. |
| `GET` | `/api/stops/<id>/departures/` | **Live Board:** Returns the next 10 upcoming buses, route names, and arrival times for a specific stop. |

## 🏗️ Local Installation & Setup



```bash
git clone https://github.com/YOUR-USERNAME/realtime-transit-api.git
cd realtime-transit-api

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py load_gtfs

python manage.py runserver