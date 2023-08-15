import os
import time
import threading
import signal
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
    memory_count = psutil.virtual_memory().total
    total_memory_gb = memory_count / (1024 ** 3)
    memory_usage = round(psutil.virtual_memory().used / (1024 * 1024), 2)
    storage_data = psutil.disk_usage('/')

    storage_metrics = {
        "total": round(storage_data.total / (1024 * 1024 * 1024), 2),
        "used": round(storage_data.used / (1024 * 1024 * 1024), 2),
        "free": round(storage_data.free / (1024 * 1024 * 1024), 2)
    }

    return {
        "cpu_count_cores": cpu_count,
        "cpu_usage": str(cpu_usage) + "%",
        "ram_count_gb":  round(total_memory_gb, 2),
        "ram_usage_gb": memory_usage,
        "storage_metrics_gb": storage_metrics
    }


def stop_stress_ng_processes():
    global stress_ng_process
    any_stopped = False

    for process in psutil.process_iter(attrs=['pid', 'name']):
        if 'stress-ng' in process.info['name'].lower():
            try:
                os.kill(process.info['pid'], signal.SIGTERM)
                print(f"Terminated stress-ng process with PID: {process.info['pid']}")
                any_stopped = True
            except Exception as e:
                print(f"Error terminating process with PID {process.info['pid']}: {e}")

    return any_stopped



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
    global stress_ng_process
    try:
        stopped = stop_stress_ng_processes()
        if stopped:
            return "All stress-ng processes stopped", 200
        else:
            return "No stress-ng processes were running", 200
    except Exception as e:
        return f"Error stopping stress-ng processes: {e}", 500


@app.route('/stress-ng/system-metrics', methods=['GET'])
def system_metrics():
    metrics = get_system_metrics()
    return jsonify(metrics), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
