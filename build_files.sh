
#!/bin/bash

# Print a message to indicate the script is running
echo "Running collectstatic..."

# Run Django's collectstatic command
python3 manage.py collectstatic --noinput
