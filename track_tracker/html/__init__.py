from .base_page import SEASON_YEAR, project_base_page, project_home_page, project_about
from .unimplemented_page import unimplemented_page
from .html_result import filter_results_html_page
from .html_athlete import filter_athletes_html_page, find_athletes_html_page
from .html_team import filter_teams_html_page, find_team_html_page
from .html_record import filter_records_html_page
from .html_workout import filter_workouts_html_page
from .common import (
    HOME_PAGE_LINK_CONTENT,
    RESULT_FILTER_PARAMS,
    RESULT_DISPLAY_PARAMS,
    ATHLETE_FILTER_PARAMS,
    ATHLETE_ARRANGE_PARAMS,
    ATHLETE_DISPLAY_PARAMS,
    TEAM_FILTER_PARAMS,
    TEAM_ARRANGE_PARAMS,
    TEAM_DISPLAY_PARAMS,
    display_date,
)
from .html_group import sprint_html_page, hurlde_html_page, points_html_page
