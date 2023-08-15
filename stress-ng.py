import os
import time
import threading
import subprocess
import psutil
from flask import Flask, request, jsonify

app = Flask(__name__)
stress_ng_process = None  # To store the stress-ng process


def simulate_cpu_stress():
    # Simulate CPU stress by consuming CPU cycles
    while True:
        pass


def run_stress_ng(cpu_cores, cpu_perc, mem, storage, duration):
    global stress_ng_process
    cpu_perc = str(cpu_perc).replace('%', '')
    stress_ng_cmd = f"stress-ng --cpu {cpu_cores} --cpu-load {cpu_perc} --vm 1 --vm-bytes {mem} --hdd 1 --hdd-bytes {storage} --timeout {duration}"
    print(f"Running stress-ng command: {stress_ng_cmd}")

    stress_ng_process = subprocess.Popen(stress_ng_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = stress_ng_process.communicate()

    response = {
        "stdout": stdout.decode("utf-8"),
        "stderr": stderr.decode("utf-8")
    }

    stress_ng_process = None
    return response


def get_system_metrics():
    # Get real system metrics using psutil
    cpu_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = round(psutil.virtual_memory().used / (1024 * 1024), 2)
    storage_data = psutil.disk_usage('/')

    storage_metrics = {
        "total": round(storage_data.total / (1024 * 1024 * 1024), 2),
        "used": round(storage_data.used / (1024 * 1024 * 1024), 2),
        "free": round(storage_data.free / (1024 * 1024 * 1024), 2)
    }

    return {
        "cpu_count": cpu_count,
        "cpu_usage": str(cpu_usage) + "%",
        "memory_usage": memory_usage,
        "storage_metrics": storage_metrics
    }



@app.route('/stress-ng/start', methods=['POST'])
def start_stress_ng():
    global stress_ng_process

    if not request.is_json:
        return "Invalid JSON data", 400

    data = request.get_json()
    cpu_cores = data.get('cpu_cores')
    cpu_perc = data.get('cpu_perc')
    mem_percentage = data.get('mem')  # Default to 50% memory usage
    storage = data.get('storage')
    duration = data.get('duration')

    if not stress_ng_process:
        # Run the stress-ng test if process isn't already running
        response = run_stress_ng(cpu_cores, cpu_perc, mem_percentage, storage, duration)
        return jsonify(response), 200
    else:
        return "Stress-ng process is already running", 400


@app.route('/stress-ng/stop', methods=['POST'])
def stop_stress_ng():
    try:
        subprocess.run(['pkill', 'stress-ng'], check=True)
        return "Stopping stress-ng processes", 200
    except subprocess.CalledProcessError as e:
        return f"Error stopping stress-ng processes: {e}", 500


@app.route('/stress-ng/system-metrics', methods=['GET'])
def system_metrics():
    metrics = get_system_metrics()
    return jsonify(metrics), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
