import os
import json

from fastapi import FastAPI, Query, Request, HTTPException, Body
from fastapi.responses import HTMLResponse, ORJSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from models import (
    ResponseTypes,
    RestHeaders,
    ContextSingleton)
from handlers import DatabaseHandler, init_logger
from html import project_home_page, unimplemented_page, unimplemented_dev_page






from html import (
    project_base_page,
    project_home_page,
    project_about,
    unimplemented_page,
    filter_results_html_page,
    filter_athletes_html_page, find_athletes_html_page,
    filter_teams_html_page, find_team_html_page,
    filter_records_html_page,
)








from routs import (
    result_router,
    athlete_router,
    team_router,
    record_router,
    # result_html_router,
    # athlete_html_router,
    # team_html_router,
    # record_html_router,
    unimplemented_html_router,
    # dev_html_router,
    workout_router,
    # workout_html_router,
    # group_html_router,
    html_routs_main_router,
    meetday_router,
)

# Can delete after done testing rest calls from different sources
from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from html import project_base_page


# Service Info
with open(os.path.join(os.path.dirname(os.getcwd()), 'info.json'), 'r') as jf:
    app_info = json.load(jf)
FAVICON_PATH = 'favicon.ico'
ROBOTS_PATH = 'robots.txt'

app = FastAPI(
    title=app_info['service_name'],
    description=app_info['description'],
    version=app_info['version'],
)

# Setting up CORS and who can access the API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(result_router)
app.include_router(athlete_router)
app.include_router(team_router)
app.include_router(record_router)
app.include_router(workout_router)
app.include_router(meetday_router)
# app.include_router(result_html_router)
# app.include_router(athlete_html_router)
# app.include_router(team_html_router)
# app.include_router(record_html_router)
# app.include_router(workout_html_router)
# app.include_router(group_html_router)
app.include_router(unimplemented_html_router)
# app.include_router(dev_html_router)
app.include_router(html_routs_main_router)



@app.on_event("startup")
async def startup_event():
    db = DatabaseHandler()
    db.create_tables()
    context = ContextSingleton()
    context.database = db
    context.logger = init_logger()





# Root
@app.get('/ht', status_code=200)
async def root(request: Request):
    """HTML PAGE TESTING"""
    project_page = await filter_athletes_html_page()
    return HTMLResponse(content=project_page)






# Root
@app.get('/', status_code=200)
@app.get('/home', status_code=200)
@app.get('/html/home', status_code=200)
@app.get('/html/home', status_code=200)
async def root(request: Request):
    header_details = RestHeaders(request=request)
    if header_details.response_type == ResponseTypes.HTML:
        project_page = await project_home_page()
        return HTMLResponse(content=project_page)
    elif header_details.response_type == ResponseTypes.JSON:
        return {'Hello': 'WORLD!'}

# Favicon
@app.get('/static/favicon.ico', include_in_schema=False)
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(FAVICON_PATH)

# Robots
@app.get('/static/robots.txt', include_in_schema=False)
@app.get('/robots.txt', include_in_schema=False)
async def favicon():
    return FileResponse(ROBOTS_PATH)

# About
@app.get('/about', status_code=200)
async def root(request: Request):
    about_page_content = await project_about()
    return HTMLResponse(content=about_page_content)


# @app.get('/test', status_code=200)
# async def root(request: Request):
#     context = ContextSingleton()
#     context.logger.info(f'Request: {request}')
#     context.logger.info(f'Request Headers: {request.headers}')
#     header_details = RestHeaders(request=request)
#     context.logger.info(f'Header Details: {header_details}')
#     response_type = header_details.response_type
#     context.logger.info(f'Response Type: {response_type}')

#     a = str(request.headers)[8:-1].replace('"', '\\"').replace("'", '"')
#     json_parsed_header = json.loads(a)

#     page_content = Div().add_style({'display': 'block', 'color': '#949ba4'})


#     page_content.add_element(
#         Header(level=1, internal='Request Header:')
#     )
#     header_json_element = Paragraph()
#     a = json.dumps(json_parsed_header, indent=4)
#     for i in a.split('\n'):
#         header_json_element.add_element(Paragraph(internal=i))
#     page_content.add_element(header_json_element)


#     page_content.add_element(
#         Header(level=1, internal='Rest Object:')
#     )
#     page_content.add_element(Paragraph(internal=f"host: {header_details.host}"))
#     page_content.add_element(Paragraph(internal=f"connection: {header_details.connection}"))
#     page_content.add_element(Paragraph(internal=f"accept: {header_details.accept}"))
#     page_content.add_element(Paragraph(internal=f"accept_encoding: {header_details.accept_encoding}"))


#     page_content.add_element(
#         Header(level=1, internal='Rest Object:')
#     )
#     page_content.add_element(Paragraph(internal=f"Response Type: {header_details.response_type}"))


#     base_doc = await project_base_page()
#     base_doc.body_content.body_content.append(page_content)
#     return HTMLResponse(content=base_doc.return_document)



# @app.get('/service-info', status_code=200)
# @app.get('/html/service-info', status_code=200)
# async def service_info(request: Request):
#     service_info_page = await unimplemented_dev_page()
#     return HTMLResponse(content=service_info_page)
#     # logger.debug('GET on /service-info')
#     file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'info.json')
#     header_details = RestHeaders(request=request)
#     with open(file_path, 'r') as f:
#         service_info = json.load(f)
#     if header_details.response_type == ResponseTypes.HTML:
#         navigation_content = NavigationContent(webpage_name="Game Process Calculator")
#         body_content = BodyContent(body_content=[service_info])
#         footer_content = FooterContent(
#             footer_content=[Header(level=3, internal='Game Process Calculator').add_style(
#                 Style(style_details={'margin': '0', 'padding': '0'}))],)
#         new_formated_doc = MyBaseDocument(
#             navigation_content=navigation_content,
#             body_content=body_content,
#             footer_content=footer_content,
#         )
#         return HTMLResponse(content=new_formated_doc.return_document, status_code=200)
#     elif header_details.response_type == ResponseTypes.JSON:
#         return service_info
