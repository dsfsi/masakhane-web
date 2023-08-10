#!/bin/bash

# Wait for 5 minutes (300 seconds)
sleep 60

# curl --connect-timeout 1800 --max-time 1800 --request GET 'http://127.0.0.1:5000/update'

npm run develop

# Now, execute the original command for the service
exec "$@"
