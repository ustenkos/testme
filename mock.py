import os
import time
import threading
import subprocess
import psutil
from flask import Flask, request, jsonify

app = Flask(__name__)

def simulate_cpu_stress():
    # Simulate CPU stress by consuming CPU cycles
    while True:
        pass

def run_stress_ng(cpu, mem, storage, duration):
    # Simulate running the stress-ng test (You would replace this with the actual stress-ng command)
    # stress_ng_cmd = f"stress-ng -c 100 -l {cpu[: -1]} -m 1 --vm-bytes {mem} --hdd {storage} --timeout {duration}"
    stress_ng_cmd = f"stress-ng --cpu {cpu} --vm 1 --vm-bytes {mem} --hdd 100 --hdd-bytes {storage} --timeout {duration}"
    print(f"Running stress-ng command: {stress_ng_cmd}")
    subprocess.run(stress_ng_cmd, shell=True)

def get_system_metrics():
    # Get real system metrics using psutil
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = round(psutil.virtual_memory().used / (1024 * 1024), 2)
    storage_data = psutil.disk_usage('/')

    return cpu_usage, memory_usage, {
        "total": round(storage_data.total / (1024 * 1024 * 1024), 2),
        "used": round(storage_data.used / (1024 * 1024 * 1024), 2),
        "free": round(storage_data.free / (1024 * 1024 * 1024), 2)
    }

@app.route('/stress-ng', methods=['POST'])
def stress_ng_mock():
    if not request.is_json:
        return "Invalid JSON data", 400

    data = request.get_json()
    cpu_percentage = data.get('cpu')
    mem_percentage = data.get('mem')  # Default to 50% memory usage
    storage = data.get('storage')
    duration = data.get('duration')

    try:
        # Run the stress-ng test
        run_stress_ng(cpu_percentage, mem_percentage, storage, duration)

        # # Get system metrics after the stress-ng test
        # cpu_usage, memory_usage, storage_data = get_system_metrics()

        response_msg = f"Test finished execution with params: CPU={cpu_percentage}, MEM={mem_percentage}, HDD={storage}, DURATION={duration}"
        response_code = 200
        
    return response_msg, response_code

@app.route('/system-metrics', methods=['GET'])
def system_metrics():
    # Get real-time system metrics
    cpu_usage, memory_usage, storage_data = get_system_metrics()

    return jsonify({
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "storage_data": storage_data
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
