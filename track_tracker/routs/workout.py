from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Response, Depends

# from models import Workout, WorkoutFilter
# # from handlers import WorkoutHandler
from handlers import ResultHandler, AthleteHandler, WorkoutHandler, parse_query_params, DuplicateRecordsException, MissingRecordException
# # from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
# from models import WorkoutData, WorkoutApiCreate, WorkoutFilter
from models import WorkoutData, WorkoutApiCreate, WorkoutFilter, AthleteFilter
from models import ContextSingleton


context = ContextSingleton()

router = APIRouter(
    prefix='/workout',
    tags=['workout'],
)


@router.post('/', status_code=201)
async def create_workout(workout: WorkoutApiCreate):
    try:
        ah = AthleteHandler()
        athlete = await ah.find_athlete(AthleteFilter(
                first_name=[workout.athlete_first_name],
                last_name=[workout.athlete_last_name],
                team=["Fairview High School"],
            ))
        workout.athlete = athlete
        workout_data = workout.cast_data_object()
        wh = WorkoutHandler()
        existing_workout_filter = WorkoutFilter(
            workout=[workout.workout],
            workout_date=[
                f"After{datetime.strftime(workout_data.workout_date, '%Y-%m-%d')}",
                f"Before{datetime.strftime(workout_data.workout_date, '%Y-%m-%d')}",
            ],
            athlete_uid=[workout.athlete.uid],
        )
        existing_workout = await wh.find_workouts(workout_filter=existing_workout_filter, silence_missing=True)
        if existing_workout:
            # Verify the record doesnt already exist
            raise DuplicateRecordsException(f"workout={workout_data.workout}, workout_date={workout_data.workout_date}")
        created_workout = await wh.create_workout(workout_data)
        return created_workout.put
    except MissingRecordException as err:
        message = f"No record found: [{err}]"
        context.logger.error(message)
        raise HTTPException(status_code=404, detail=message)
    except DuplicateRecordsException as err:
        message = f"Duplicate records found: [{err}]"
        context.logger.error(message)
        raise HTTPException(status_code=409, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.get('/', status_code=200)
async def filter_workout(request: Request):
    try:
        workout_filter = parse_query_params(request=request, query_class=WorkoutFilter)
        mh = WorkoutHandler()
        workouts = await mh.filter_workouts(workout_filter=workout_filter)
        ah = AthleteHandler()
        for workout in workouts:
            athlete = await ah.find_athlete(AthleteFilter(uid=[workout.athlete_uid]))
            workout.athlete = athlete
        return {'workouts': workouts}
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


# @router.put('/', status_code=200)
# async def update_workout(workout: WorkoutData):
#     try:
#         mh = AthleteHandler()
#         created_workout = await mh.update_workout(workout=workout)
#         return created_workout.put
#     except DuplicateRecordsException as err:
#         message = f"Dupe record attempt: {err}"
#         context.logger.warning(message)
#         raise HTTPException(status_code=409, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')


# @router.get('/display', status_code=200)
# async def filter_workout(request: Request):
#     try:
#         workout_filter = parse_query_params(request=request, query_class=WorkoutFilter)
#         mh = WorkoutHandler()
#         workouts, query_max_count = await mh.filter_workouts_display(workout_filter=workout_filter)
#         ah = AthleteHandler()
#         for workout in workouts:
#             athlete = await ah.find_athlete(AthleteFilter(uid=[workout['Athlete']]))
#             workout['Athlete'] = f"{athlete.first_name} {athlete.last_name}"
#             workout['Class'] = class_formatter(athlete.graduation_year)[1]
#         response = {
#             'workouts': workouts,
#             'query_max_count': query_max_count,
#         }
#         return response
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
