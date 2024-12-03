#!/bin/bash

# Base URL for the API gateway
BASE_URL="http://localhost:8197"

# Credentials
USERNAME="vbox"
PASSWORD="123"

# Track overall test failures
TEST_FAILURES=0

# Helper function for logging test results
log_test() {
    if [ "$1" -eq 0 ]; then
        echo "[PASS] $2"
    else
        echo "[FAIL] $2"
        TEST_FAILURES=$((TEST_FAILURES + 1))
    fi
}



# Test 1: GET /state
echo "Testing GET /state..."
curl -s -o /dev/null -w "%{http_code}" -H ”Accept: text/plain” "${BASE_URL}/state" | grep -q "200"
log_test $? "GET /state should return HTTP 200"

# Test 2: GET /run-log
echo "Testing GET /run-log..."
curl -s -o /dev/null -w "%{http_code}" -H ”Accept: text/plain” "${BASE_URL}/run-log" | grep -q "200"
log_test $? "GET /run-log should return HTTP 200"

# Test 3: PUT /state (RUNNING) 1/3
echo "Testing PUT /state with 'RUNNING'... (1/3)"
curl -s -o /dev/null -w "%{http_code}" -u "$USERNAME:$PASSWORD" -X PUT -H "Content-Type: text/plain" -H ”Accept: text/plain” --data "RUNNING" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'RUNNING' should return HTTP 200"

# Test 4: PUT /state (PAUSED)
echo "Testing PUT /state with 'PAUSED'..."
curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: text/plain" -H ”Accept: text/plain” --data "PAUSED" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'PAUSED' should return HTTP 200"

# Test 5: PUT /state (RUNNING) 2/3
echo "Testing PUT /state with 'RUNNING'... (2/3)"
curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: text/plain" -H ”Accept: text/plain” --data "RUNNING" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'RUNNING' when state is 'PAUSED' should return HTTP 200"

# Test 6: GET /request
echo "Testing GET /request..."
curl -s -o /dev/null -w "%{http_code}" -H ”Accept: text/plain” "${BASE_URL}/request" | grep -q "200"
log_test $? "GET /request should return HTTP 200"

# Test 7: PUT /state (INIT)
echo "Testing PUT /state with 'INIT'..."
curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: text/plain" -H ”Accept: text/plain” --data "INIT" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'INIT' should return HTTP 200"

# Test 8: PUT /state (RUNNING) 3/3
echo "Testing PUT /state with 'RUNNING'... (3/3)"
curl -s -o /dev/null -w "%{http_code}" -u "$USERNAME:$PASSWORD" -X PUT -H "Content-Type: text/plain" -H ”Accept: text/plain” --data "RUNNING" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'RUNNING' after reset to state 'INIT' should return HTTP 200"

# Test 9: PUT /state (SHUTDOWN)
echo "Testing PUT /state with 'SHUTDOWN'..."
curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: text/plain" -H ”Accept: text/plain” --data "SHUTDOWN" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'SHUTDOWN' should return HTTP 200"



# Summary of results
if [ "$TEST_FAILURES" -eq 0 ]; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "$TEST_FAILURES test(s) failed."
    exit 1
fi
