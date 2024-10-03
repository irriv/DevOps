# About
This program collects information from the Docker container:
- IP address information
- List of running processes
- Available disk space
- Time since last boot

This information comes from both service1 and service2 in json format. Service2 is only accessible within the Docker composition.
# How to run
1. Clone repository ```git clone -b exercise1 https://github.com/irriv/DevOps.git```
2. Navigate to repository in terminal ```cd DevOps```
3. Run the command ```docker compose up --build``` OR ```docker-compose up --build``` depending on your Docker installation (docker-compose is deprecated)
4. Either open ```localhost:8199``` in browser or run the command ```curl localhost:8199``` in another terminal window to see the output
