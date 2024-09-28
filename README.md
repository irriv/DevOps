# About
This program collects information from the Docker container:
- IP address information
- List of running processes
- Available disk space
- Time since last boot

This information comes from both service1 and service2 in json format. Service2 is only accessible within the Docker composition.
# How to run
1. Clone repository
2. Navigate to repository in terminal
3. Run the command 'sudo docker compose up --build'
4. Either open 'localhost:8199' in browser or run the command 'curl localhost:8199' in another terminal window to see the output
