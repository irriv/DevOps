# About
This program collects information from the Docker container:
- IP address information
- List of running processes
- Available disk space
- Time since last boot

This information comes from both service1 and service2 in json format. There are 3 instances of service1. Only the Nginx service is accessible from the outside.
# How to run
1. Clone repository ```git clone -b exercise4 https://github.com/irriv/DevOps.git```
2. Navigate to repository in terminal ```cd DevOps```
3. Run the command ```docker compose up --build``` OR ```docker-compose up --build``` depending on your Docker installation (docker-compose is deprecated)
4. Open ```localhost:8198``` in browser
5. Login with the credentials in ```login.txt```
6. Press the ```REQUEST``` button to fetch information.
7. Press the ```STOP``` button to stop all the containers.
