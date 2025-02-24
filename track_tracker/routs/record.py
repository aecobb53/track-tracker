from fastapi import APIRouter, HTTPException, Request, Response, Depends

from handlers import AthleteHandler, ResultHandler, parse_query_params, DuplicateRecordsException, MissingRecordException
from models import AthleteData, AthleteApiCreate, AthleteFilter, ResultFilter, ContextSingleton, RestHeaders

context = ContextSingleton()

router = APIRouter(
    prefix='/record',
    tags=['record'],
)


@router.get('/', status_code=200)
async def filter_team(request: Request):
    try:
        # athlete_filter = parse_query_params(request=request, query_class=AthleteFilter)
        # ah = AthleteHandler()
        # athletes = await ah.filter_athletes(AthleteFilter())
        mh = ResultHandler()
        offset = 0
        checking = True
        size = ResultFilter().limit
        results = []
        while checking:
            results_l = await mh.filter_results(ResultFilter(offset=offset))
            results.extend(results_l)
            if len(results_l) < 1000:
                checking = False
            offset += size

        # APPLY A FILTER TO ONLY GET ACTIVE TEAM MEMEBRS
        # DISPLAY HOW MANY STUDENTS ARE IN EACH GRADE?

        event_details = {}
        for result in results:
            if result.event not in event_details:
                event_details[result.event] = result
            else:
                if result.result > event_details[result.event].result:
                    # New record
                    event_details[result.event] = result

        return {'records': event_details}
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.get('/display', status_code=200)
async def filter_athlete(request: Request):
    try:
        athlete_filter = parse_query_params(request=request, query_class=AthleteFilter)
        ah = AthleteHandler()
        athletes = await ah.filter_athletes(athlete_filter=AthleteFilter(team=athlete_filter.team))
        offset = athlete_filter.offset
        limit = athlete_filter.limit
        start_index = offset
        stop_index = start_index + limit

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
        query_max_count = len(teams)
        response = {
            'teams': teams[start_index:stop_index],
            'query_max_count': query_max_count,
        }
        return response
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
