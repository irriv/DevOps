import subprocess
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import time
import docker
import socket

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
        connection = http.client.HTTPConnection("service2", 8200)  # Port 8200
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


class ServiceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/stop":
            client = docker.from_env()
            current_container = client.containers.get(socket.gethostname())
            current_container_id = current_container.id
            for container in client.containers.list():
                if container.id != current_container_id:
                    container.stop()
            if current_container_id:
                current_container.stop()
        else:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            service_info = {
                "Service": {
                    "IP Address Information": get_container_ip(),
                    "List of Running Processes": get_running_processes(),
                    "Available Disk Space": get_disk_space(),
                    "Time Since Last Boot": get_uptime()
                },
                "Service2": get_service2_info()
            }

            self.wfile.write(json.dumps(service_info, indent=4).encode("utf-8"))
            time.sleep(2)


def run(server_class=HTTPServer, handler_class=ServiceHandler, port=8199):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
