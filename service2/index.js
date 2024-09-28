const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 8200;

function getContainerIP() {
    return new Promise((resolve, reject) => {
        exec(`hostname -I`, (error, stdout, stderr) => {
            if (error) {
                reject(`Error retrieving IP address: ${stderr}`);
                return;
            }
            const ipAddress = stdout.split(' ')[0].trim();
            resolve(ipAddress);
        });
    });
}

function getRunningProcesses() {
    return new Promise((resolve, reject) => {
        exec('ps -ax', (error, stdout, stderr) => {
            if (error) {
                reject(`Error retrieving running processes: ${stderr}`);
                return;
            }
            resolve(stdout);
        });
    });
}

function getDiskSpace() {
    return new Promise((resolve, reject) => {
        exec('df -h /', (error, stdout, stderr) => {
            if (error) {
                reject(`Error retrieving disk space: ${stderr}`);
                return;
            }
            const lines = stdout.split('\n');
            const diskSpaceInfo = lines[1];
            resolve(diskSpaceInfo);
        });
    });
}

function getUptime() {
    return new Promise((resolve, reject) => {
        exec('uptime -p', (error, stdout, stderr) => {
            if (error) {
                reject(`Error retrieving uptime: ${stderr}`);
                return;
            }
            resolve(stdout.trim());
        });
    });
}

app.get('/', async (req, res) => {
    try {
        const ipAddress = await getContainerIP();
        const processes = await getRunningProcesses();
        const diskSpace = await getDiskSpace();
        const uptime = await getUptime();

        const service_info = {
            "IP Address Information": ipAddress,
            "List of Running Processes": processes,
            "Available Disk Space": diskSpace,
            "Time Since Last Boot": uptime,
        };

        res.json(service_info);
    } catch (error) {
            console.error("An error occurred while retrieving service info:", error);
            res.status(500).json({ Error: `An error occurred: ${error.message || error}` });
        }
});

app.listen(port, () => {
    console.log(`Service2 is running internally on http://service2:${port}`);
});
