# simulate_post.py
import requests
import json

url = 'http://127.0.0.1:8000/api/data-entry/'

# Sample data to be posted
data = {
    'device_id': '12345',
    'acceleration_x': 0.1,
    'acceleration_y': 0.2,
    'acceleration_z': 0.3,
    'gyro_x': 0.01,
    'gyro_y': 0.02,
    'gyro_z': 0.03,
    'temperature': 22.5,
    'battery': 95.0
}

response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

print(response.status_code)
print(response.json())
