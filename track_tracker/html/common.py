import yaml
import json

import os

path = os.path.join(os.getcwd(), 'html', 'common')

# Home Page
with open(os.path.join(path, 'home_page_content.yml')) as yf:
    home_page_content_file = yaml.safe_load(yf)
HOME_PAGE_LINK_CONTENT = home_page_content_file


# Mark Filter Params
with open(os.path.join(path, 'mark.yml')) as yf:
    mark_file = yaml.safe_load(yf)
MARK_FILTER_PARAMS = mark_file['filter']
MARK_DISPLAY_PARAMS = mark_file['display']
