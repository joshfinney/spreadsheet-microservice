from app import create_app
import argparse
import logging
from app.utilities.logging_config import setup_logging

setup_logging()

parser = argparse.ArgumentParser(description='Start the SC microservice with specified storage repository.')
parser.add_argument('-r', '--repository', type=str, choices=['sqlite', 'firebase'], required=True,
                    help='Specify the storage repository: "sqlite" for on-premises or "firebase" for cloud storage.')
args = parser.parse_args()

# Inject the storage method into the application config
if args.repository == 'firebase':
    config_class = 'app.config.FirebaseConfig'
else:
    config_class = 'app.config.Config'

app = create_app(config_class)

if __name__ == '__main__':
    app.run(debug=True, port=3000)