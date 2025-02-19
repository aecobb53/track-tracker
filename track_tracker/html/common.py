import yaml
import json

import os

path = os.path.join(os.getcwd(), 'html', 'common')

# calculation_parameters_path = os.path.join(os.getcwd(), "common", "calculation_parameters.yml")
# if not os.path.exists(calculation_parameters_path):
#     calculation_parameters_path = os.path.join(os.getcwd(), "millionaire", "common", "calculation_parameters.yml")

with open(os.path.join(path, 'mark.yml')) as yf:
    mark_file = yaml.safe_load(yf)
MARK_FILTER_PARAMS = mark_file['filter']
MARK_DISPLAY_PARAMS = mark_file['display']
