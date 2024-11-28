#!/bin/bash

# Base URL for the API gateway
BASE_URL="http://localhost:8197"

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
curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/state" | grep -q "200"
log_test $? "GET /state should return HTTP 200"

# Test 2: GET /run-log
echo "Testing GET /run-log..."
curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/run-log" | grep -q "200"
log_test $? "GET /run-log should return HTTP 200"

# Log in here

# Test 3: PUT /state (PAUSED)
echo "Testing PUT /state with 'PAUSED'..."
curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: text/plain" --data "PAUSED" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'PAUSED' should return HTTP 200"

# Test 4: PUT /state (RUNNING)
echo "Testing PUT /state with 'RUNNING'..."
curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: text/plain" --data "RUNNING" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'RUNNING' should return HTTP 200"

# Test 5: GET /request
echo "Testing GET /request..."
curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/request" | grep -q "200"
log_test $? "GET /request should return HTTP 200"

# Test 6: PUT /state (INIT)
echo "Testing PUT /state with 'INIT'..."
curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: text/plain" --data "INIT" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'INIT' should return HTTP 200"

# Log in here again

# Test 7: PUT /state (SHUTDOWN)
echo "Testing PUT /state with 'SHUTDOWN'..."
curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: text/plain" --data "SHUTDOWN" "${BASE_URL}/state" | grep -q "200"
log_test $? "PUT /state with 'SHUTDOWN' should return HTTP 200"

echo "All tests ran successfully!"
