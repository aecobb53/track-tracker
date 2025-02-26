from fastapi import APIRouter, HTTPException, Request, Response, Depends

from handlers import AthleteHandler, ResultHandler, parse_query_params, DuplicateRecordsException, MissingRecordException
from models import AthleteData, AthleteApiCreate, AthleteFilter, ResultFilter, ContextSingleton, RestHeaders

from typing import Annotated

context = ContextSingleton()

router = APIRouter(
    prefix='/team',
    tags=['team'],
)


@router.get('/', status_code=200)
async def filter_team(request: Request):
    try:
        athlete_filter = parse_query_params(request=request, query_class=AthleteFilter)
        ah = AthleteHandler()
        athletes = await ah.filter_athletes(athlete_filter=athlete_filter)

        # APPLY A FILTER TO ONLY GET ACTIVE TEAM MEMEBRS
        # DISPLAY HOW MANY STUDENTS ARE IN EACH GRADE?

        team_details = {}
        for athlete in athletes:
            team = athlete.team
            if team not in team_details:
                team_details[team] = {
                    'team': team,
                    'athlete_count': 0
                }
            team_details[team]['athlete_count'] += 1
        teams = [team for team in team_details.values()]
        return {'teams': teams}
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.get('/display', status_code=200)
async def filter_athlete(request: Request):
    try:
        athlete_filter = parse_query_params(request=request, query_class=AthleteFilter)
        params = parse_query_params(request=request)
        ah = AthleteHandler()
        athletes = await ah.filter_athletes(athlete_filter=AthleteFilter(team=athlete_filter.team))
        offset = athlete_filter.offset
        limit = athlete_filter.limit
        start_index = offset
        stop_index = start_index + limit


        # I believe this needs to be able to pull all athletes or better yet just have this data loaded into mem


        # APPLY A FILTER TO ONLY GET ACTIVE TEAM MEMEBRS
        # DISPLAY HOW MANY STUDENTS ARE IN EACH GRADE?

        team_details = {}
        for athlete in athletes:
            team = athlete.team
            if team not in team_details:
                team_details[team] = {
                    'Team': team,
                    'Athlete Count': 0
                }
            team_details[team]['Athlete Count'] += 1
        team_keys = list(team_details.keys())
        team_keys.sort()
        teams = [team_details[key] for key in team_keys]


        # if params.get('min_athlete_count'):
        #     teams = [t for t in teams if t['Athlete Count'] >= int(params['min_athlete_count'][0])]




        query_max_count = len(teams)
        response = {
            'teams': teams[start_index:stop_index],
            'query_max_count': query_max_count,
        }
        return response
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
