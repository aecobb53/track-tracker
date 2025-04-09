import os
from datetime import datetime
from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .base_page import (
    project_base_page,
    # BACKGROUND_COLOR,
    # SECONDARY_COLOR,
    # ACCENT_COLOR,
    # TEXT_COLOR_1,
    # TEXT_COLOR_2,
    # ROW_BACKGROUND_COLOR_1,
    # ROW_BACKGROUND_COLOR_2,
    PAGE_STYLES,
    FILTER_STYLES,
    TABLE_STYLES,
    CSV_STYLES,
    HOME_PAGE_STYLES,
    )
# from .common import WORKOUT_FILTER_PARAMS, WORKOUT_ARRANGE_PARAMS, WORKOUT_DISPLAY_PARAMS
from models import Result


# def generate_csv_item(default):
#     item = Input(type='text', value=default).add_class('csv-input')
#     return item

# def generate_csv_element(default_csv: list = []):
#     csv_div = Div().add_class('csv-div')
#     csv_table = Table().add_class('csv-table')
#     if default_csv:
#         # Header
#         header = default_csv.pop(0)
#         csv_row = TableRow().add_class('csv-row').add_class('csv-header')
#         for item in header:
#             csv_row.add_element(TableHeader(generate_csv_item(item)).add_class('csv-header-item'))
#         csv_table.add_element(csv_row)

#         # Data
#         csv_row = TableRow().add_class('csv-row').add_class('csv-header')
#         for index, row in enumerate(default_csv):
#             if index % 2:
#                 csv_row = TableRow().add_class('csv-row').add_class('odd-row')
#             else:
#                 csv_row = TableRow().add_class('csv-row').add_class('even-row')
#             for item in row:
#                 csv_row.add_element(TableData(generate_csv_item(item)).add_class('csv-data-item'))
#             csv_table.add_element(csv_row)
#     else:
#         print(f'NO DEFAULT CSV')
#     csv_div.add_element(csv_table)
#     return csv_div




async def find_meet_html_page(meet):
    # base_doc = await project_base_page()
    base_doc = await project_base_page(onload_function="runUpdate()")

    # Body
    page_content = Div().add_class('page-content')

    page_content.add_element(Header(level=1, internal=meet, id='page-identifier-meet-name'))
    page_content.add_element(Header(level=1, id='page-identifier-update-time', hidden=True))
    # page_content.add_element(Header(level=1, internal='EXAMPLE', id='page-identifier-update-time'))

    # page_content.add_element(
    #     Button(internal='Edit Mode', type='button', onclick='runUpdate()').add_class('big-button').add_class('submit-button'))


    # Table
    table_div = Div(id='meet-table')
    page_content.add_element(table_div)

    # JS Files
    js_files = [
        os.path.join('csv', 'runUpdate.js'),
        # os.path.join('csv', 'GETMeetCSV.js'),
        os.path.join('csv', 'updateMeetTable.js'),
        os.path.join('csv', 'populateCSV.js'),
        os.path.join('csv', 'createMeetUpdateBody.js'),
        os.path.join('csv', 'rowManipulation.js'),
    ]
    if os.environ.get('LOGICAL_ENV') == 'DEV':
        js_files.append(os.path.join('csv', 'GETMeetCSVDEV.js'))
    else:
        js_files.append(os.path.join('csv', 'GETMeetCSVPROD.js'))
    for fl in js_files:
        with open(os.path.join('html', fl), 'r') as jf:
            # line = line.replace('SERVICE_URL', service_url)
            js_lines = jf.readlines()
            js_lines[-1] += '\n'  # In case there is not a newline at the end of the file
            script = Script(internal=[l[:-1] for l in js_lines])
            script.attributes
            page_content.add_element(
                script
            )


    body_content = BodyContent(body_content=[page_content])

    # Styles
    for style in PAGE_STYLES:
        body_content.add_body_styles(style)
    for style in FILTER_STYLES:
        body_content.add_body_styles(style)
    for style in TABLE_STYLES:
        body_content.add_body_styles(style)
    for style in CSV_STYLES:
        body_content.add_body_styles(style)

    base_doc.body_content = body_content
    return base_doc.return_document

async def filter_meetdays_html_page(meets_dict):
    # base_doc = await project_base_page()
    base_doc = await project_base_page(onload_function="runUpdate()")

    # Body
    page_content = Div().add_class('page-content')

    meet_grouping_div = Div(Header(level=1, internal='Meets')).add_class('page-group-div')
    for meet_name, meet_details in meets_dict.items():
        content = [
            Div(internal=Header(level=2, internal=meet_name)).add_class('page-header'),
            # Div(internal=Paragraph(internal=details['description'])).add_class('page-paragraph'),
        ]
        page_link = Link(internal=content, href=f"/html/{meet_details['endpoint']}").add_class('page-link').add_class('page-div')
        meet_grouping_div.add_element(page_link)
    page_content.add_element(meet_grouping_div)


    body_content = BodyContent(body_content=[page_content])


    # Styles
    for style in PAGE_STYLES:
        body_content.add_body_styles(style)
    for style in FILTER_STYLES:
        body_content.add_body_styles(style)
    for style in TABLE_STYLES:
        body_content.add_body_styles(style)
    for style in CSV_STYLES:
        body_content.add_body_styles(style)
    for style in HOME_PAGE_STYLES:
        body_content.add_body_styles(style)

    base_doc.body_content = body_content
    return base_doc.return_document


# async def filter_meetdays_html_page():
#     base_doc = await project_base_page(onload_function="runUpdate()")

#     # Body
#     page_content = Div().add_class('page-content')

#     page_identifier_span = Span().add_class('page-identifier-span')
#     # Date
#     # date_div = Div().add_class('data-div')
#     # date_span = Span().add_class('data-span')
#     # date_label = Label(internal='Date: ', for_='date-input').add_class('data-label')
#     # date_span.add_element(date_label)
#     # date_input = Input(type='date', id='date-input').add_class('data-input')
#     # date_input.attributes['onchange'] = 'runUpdate()'
#     # date_span.add_element(date_input)
#     # date_div.add_element(date_span)
#     # page_identifier_span.add_element(date_div)

#     # # Name
#     # name_div = Div().add_class('data-div')
#     # name_span = Span().add_class('data-span')
#     # name_label = Label(internal='Name: ', for_='name-input').add_class('data-label')
#     # name_span.add_element(name_label)
#     # name_input = Input(type='name', id='name-input').add_class('data-input')
#     # name_input.attributes['onchange'] = 'runUpdate()'
#     # name_span.add_element(name_input)
#     # name_div.add_element(name_span)
#     # page_identifier_span.add_element(name_div)

#     date_div = Div().add_class('data-div')
#     date_div.add_element(Header(level=1, internal='Date: '))
#     date_div.add_element(Header(level=1, internal='3/15'))
#     page_identifier_span.add_element(date_div)

#     # Name
#     name_div = Div().add_class('data-div')
#     name_div.add_element(Header(level=1, internal='Name :'))
#     name_div.add_element(Header(level=1, internal='10x200'))
#     page_identifier_span.add_element(name_div)

#     page_content.add_element(page_identifier_span)



#     # default_csv = [
#     #     'First;Last;1 - 400m;2 - 400m;3 - 400m;4 - 400m',
#     #     'Justin;King;88.0;95.0;116.0;',
#     #     'Dashiell;Ecklund;70.0;87.0;78.0;76.0',
#     #     'Casey;Lamson;77.0;81.0;80.0;79.0',
#     #     'Wetera;Schlachter;81.0;74.0;71.0;59.0',
#     #     'Charles;Bonvillian;81.0;74.0;71.0;60.0',
#     #     'Tommy;Bauer;81.0;74.0;76.0;',
#     #     'Luke;Stickland;81.0;74.0;74.0;',
#     #     'Wyatt;Keegan;81.0;74.0;74.0;',
#     #     'Loyo;Abalu;81.0;74.0;74.0;',
#     #     'Ellie;Grandsaert;76.0;76.0;76.0;78.0',
#     #     'Bethany;Kim;90.0;93.0;92.0;92.0',
#     #     'Anna;Johnson;77.0;77.0;77.0;78.0',
#     #     'Ada;Kimmel;98.0;99.0;;',
#     #     'Max;Webb;81.0;74.0;75.0;74.0',
#     #     'Aubrie;Miller;91.0;96.0;99.0;102.0',
#     #     'Michelle;He;95.0;101.0;101.0;106.0',
#     #     'Alisa;Gao;93.0;93.0;90.0;87.0',
#     #     'Sienna;Strickland;120.0;;94.0;',
#     #     'Miles;Weber;73.0;85.0;72.0;77.0',
#     #     'Kieran;Meier;77.0;89.0;81.0;79.0',
#     #     'Piotr;Kestech;80.0;91.0;101.0;99.0',
#     #     'Jack;Muhier;74.0;;;',
#     #     'Jeremiah;Cole;75.0;83.0;74.0;62.0',
#     #     'Elan;Castillo-Veltman;72.0;84.0;100.0;98.0',
#     #     'Andrew;McCarty;74.0;84.0;;',
#     # ]
#     # default_csv = [row.split(';') for row in default_csv]
#     # page_content.add_element(generate_csv_element(default_csv=default_csv))

#     # Table
#     table_div = Div(id='table-div')
#     page_content.add_element(table_div)

#     # JS Files
#     js_files = [
#         os.path.join('csv', 'runUpdate.js'),
#         os.path.join('csv', 'GETCSV.js'),
#         os.path.join('csv', 'updateCSVTable.js'),
#         os.path.join('csv', 'populateCSV.js'),
#     ]
#     for fl in js_files:
#         with open(os.path.join('html', fl), 'r') as jf:
#             # line = line.replace('SERVICE_URL', service_url)
#             js_lines = jf.readlines()
#             js_lines[-1] += '\n'  # In case there is not a newline at the end of the file
#             script = Script(internal=[l[:-1] for l in js_lines])
#             script.attributes
#             page_content.add_element(
#                 script
#             )


#     body_content = BodyContent(body_content=[page_content])

#     # Styles
#     for style in PAGE_STYLES:
#         body_content.add_body_styles(style)
#     for style in FILTER_STYLES:
#         body_content.add_body_styles(style)
#     for style in TABLE_STYLES:
#         body_content.add_body_styles(style)
#     for style in CSV_STYLES:
#         body_content.add_body_styles(style)

#     base_doc.body_content = body_content
#     return base_doc.return_document
