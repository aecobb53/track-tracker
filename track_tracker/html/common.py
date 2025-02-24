import yaml
import json

import os

path = os.path.join(os.getcwd(), 'html', 'common')

# Home Page
with open(os.path.join(path, 'home_page_content.yml')) as yf:
    home_page_content_file = yaml.safe_load(yf)
HOME_PAGE_LINK_CONTENT = home_page_content_file


# Result Filter Params
with open(os.path.join(path, 'result.yml')) as yf:
    result_file = yaml.safe_load(yf)
MARK_FILTER_PARAMS = result_file['filter']
MARK_ARRANGE_PARAMS = result_file['arrange']
MARK_DISPLAY_PARAMS = result_file['display']


# Athlete Filter Params
with open(os.path.join(path, 'athlete.yml')) as yf:
    athlete_file = yaml.safe_load(yf)
ATHLETE_FILTER_PARAMS = athlete_file['filter']
ATHLETE_ARRANGE_PARAMS = athlete_file['arrange']
ATHLETE_DISPLAY_PARAMS = athlete_file['display']

# Team Filter Params
with open(os.path.join(path, 'team.yml')) as yf:
    team_file = yaml.safe_load(yf)
TEAM_FILTER_PARAMS = team_file['filter']
TEAM_ARRANGE_PARAMS = team_file['arrange']
TEAM_DISPLAY_PARAMS = team_file['display']

def display_date(date):
    return date.strftime('%m/%d/%y')
