
#!/bin/bash

# Print a message to indicate the script is running
echo "Running collectstatic..."

# Install dependencies
pip install -r requirements.txt

# Run Django's collectstatic command
python3 manage.py collectstatic --noinput
