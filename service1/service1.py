import subprocess
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import time
import docker
import socket
from datetime import datetime
import os
from threading import Thread

# Shared files
STATE_FILE = "/shared_data/state.txt"
LOG_FILE = "/shared_data/run-log.txt"

# State management variables
possible_states = ["INIT", "PAUSED", "RUNNING", "SHUTDOWN"]
possible_paths = ["/state", "/request", "/run-log"]

# Read the current state
def read_state():
    if not os.path.exists(STATE_FILE):
        return "INIT"  # Default state
    with open(STATE_FILE, "r") as f:
        return f.read().strip()

# Update the state
def write_state(new_state):
    with open(STATE_FILE, "w") as f:
        f.write(new_state)

# Update the run log
def log_state_change(old_state, new_state):
    timestamp = datetime.now().isoformat()
    log_entry = f"{timestamp}: {old_state} -> {new_state}\n"
    with open(LOG_FILE, "a+") as f:
        f.write(log_entry)

# Get the run log
def get_run_log():
    if not os.path.exists(LOG_FILE):
        return "No log entries found."
    with open(LOG_FILE, "r") as f:
        return f.read()

def set_state(new_state, auth_header):
    old_state = read_state()
    if old_state == "INIT" and new_state != "RUNNING":
        return "Login required to change state", 403
    if old_state == "INIT" and new_state == "RUNNING":
        if not auth_header or not auth_header.startswith("Basic "):
            return "Authentication required to change state", 401
    if old_state == "SHUTDOWN":
        return "System is shut down", 403
    if new_state == old_state:
        return "State unchanged", 200
    if not isinstance(new_state, str) or new_state not in possible_states:
        return "Invalid state payload", 400

    write_state(new_state)
    log_state_change(old_state, new_state)

    if new_state == "INIT":
        return "System reset to INIT. Please log in again.", 200
    elif new_state == "SHUTDOWN":
        return "System shutting down...", 200

    return f"State changed to {new_state}", 200

# Remove files from volume and stop all containers
def shutdown():
    remove_files()
    client = docker.from_env()
    current_container = client.containers.get(socket.gethostname())
    current_container_id = current_container.id
    for container in client.containers.list():
        if container.id != current_container_id:
            container.stop()
    current_container.stop()

def remove_files():
    # Remove the state and run-log files
    try:
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
    except Exception as e:
        print(f"Error removing state or log file: {str(e)}")

def logout():
    # Logout the user so credentials would be asked again. Not implemented!
    return

def get_container_ip():
    try:
        container_ip = subprocess.check_output(['hostname', '-I']).decode("utf-8").strip()
        return container_ip.split()[0]
    except subprocess.CalledProcessError as e:
        return {"Error": f"Error retrieving IP address: {str(e)}"}

def get_running_processes():
    try:
        processes = subprocess.check_output(["ps", "-ax"]).decode("utf-8").strip()
        return processes
    except subprocess.CalledProcessError as e:
        return {"Error": f"Error retrieving running processes: {str(e)}"}

def get_disk_space():
    try:
        disk_space = subprocess.check_output(["df", "-h", "/"]).decode("utf-8").strip()
        return disk_space
    except subprocess.CalledProcessError as e:
        return {"Error": f"Error retrieving disk space: {str(e)}"}

def get_uptime():
    try:
        uptime = subprocess.check_output(["uptime", "-p"]).decode("utf-8").strip()
        return uptime
    except subprocess.CalledProcessError as e:
        return {"Error": f"Error retrieving uptime: {str(e)}"}

def get_service2_info():
    connection = None
    try:
        connection = http.client.HTTPConnection("service2", 8200)
        connection.request("GET", "/")
        response = connection.getresponse()
        if response.status == 200:
            data = response.read().decode("utf-8")
            return json.loads(data)
        else:
            return {"Error": f"Failed to retrieve information from Service2. HTTP Status Code: {response.status}"}
    except Exception as e:
        return {"Error": f"Failed to connect to Service2: {str(e)}"}
    finally:
        if connection:
            connection.close()

def get_info():
    return {
        "Service": {
            "IP Address Information": get_container_ip(),
            "List of Running Processes": get_running_processes(),
            "Available Disk Space": get_disk_space(),
            "Time Since Last Boot": get_uptime()
        },
        "Service2": get_service2_info()
    }

class ServiceHandler(BaseHTTPRequestHandler):
    def send_response_with_message(self, status, message):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def do_GET(self):
        state = read_state()
        if self.path not in possible_paths:
            self.send_response_with_message(400, "Invalid request")
        elif self.path == "/request" and state == "PAUSED":
            self.send_response_with_message(403, "System is paused")
        elif self.path == "/state":
            self.send_response_with_message(200, state)
        elif self.path == "/request":
            info = get_info()
            info_str = "\n".join([f"{key}:\n{value}" for key, value in info.items()])
            self.send_response_with_message(200, info_str)
            time.sleep(2)
        elif self.path == "/run-log":
            log_str = get_run_log()
            self.send_response_with_message(200, log_str)

    def do_PUT(self):
        if self.path == "/state":
            try:
                content_length = int(self.headers['Content-Length'])
                new_state = self.rfile.read(content_length).decode("utf-8").strip()
                auth_header = self.headers.get("Authorization")
                msg, status = set_state(new_state, auth_header)
                self.send_response_with_message(status, msg)
                updated_state = read_state()
                if updated_state == "SHUTDOWN":
                    # Run shutdown in a separate thread so the response is sent first
                    Thread(target=shutdown).start()
                elif updated_state == "INIT":
                    logout()
            except Exception as e:
                self.send_response_with_message(400, f"Error processing request: {str(e)}")
        else:
            self.send_response_with_message(400, "Invalid request")

def run(server_class=HTTPServer, handler_class=ServiceHandler, port=8199):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
