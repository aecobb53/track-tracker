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
    )
# from .common import WORKOUT_FILTER_PARAMS, WORKOUT_ARRANGE_PARAMS, WORKOUT_DISPLAY_PARAMS
from models import Result



async def filter_workouts_html_page(workouts: list):
    base_doc = await project_base_page()

    # Body
    page_content = Div().add_class('page-content')


    # # Filter Form
    # filter_form_div = Div()
    # filter_form_div.add_element(Header(level=1, internal='Workouts'))
    # # filter_form_div.add_element(Paragraph(internal='''
    # # Workouts are the workouts of a race, jump, or throw. I use workout to avoid overloading other common phrases. You can use 
    # # this page to filter criteria. The filters are partial as in you can query for the Team "Fairview" to get all 
    # # Fairview High School workouts. Some have additional dropdowns. For example, you can filter for Heats <= 3. 
    # # Table columns can be toggled with the checkboxes to make viewing easier.
    # # '''))
    # # filter_form_div.add_element(Paragraph(
    # #     internal='For multiple items separate with a comma. Ex "Fairview, Boulder"'))
    # filter_form = Form(action=f"/workout", method='get').add_class('filter-form')
    # filter_groupings = {}
    # for grouping in WORKOUT_FILTER_PARAMS.keys():
    #     if grouping not in filter_groupings:
    #         filter_groupings[grouping] = []
    #     for details in WORKOUT_FILTER_PARAMS[grouping].values():
    #         filter_groupings[grouping].append(details)
    # for grouping in filter_groupings.keys():
    #     params = filter_groupings[grouping]
    #     grouping_div = Div()
    #     grouping_div.add_element(Header(level=3, internal=grouping))
    #     for param in params:
    #         id_base = param['variable'].replace(' ', '-').lower()
    #         input_kwargs = {
    #             'id': f"{id_base}-input",
    #             'name': param['display'],
    #             'value': param['default_value'],
    #         }
    #         if param.get('datatype'):
    #             input_kwargs['type'] = param['datatype']
    #         if param.get('size'):
    #             input_kwargs['size'] = param['size']
    #         box = [
    #             Span(
    #                 for_=f"{id_base}-input", internal=param['display']
    #             ).add_class('filter-checkbox-input'),
    #         ]
    #         if param.get('options'):
    #             options = []
    #             for option in param['options']:
    #                 options.append(Option(internal=option, id=f"{id_base}-input-select"))
    #             box.append(Select(internal=options, id=f"{id_base}-input-select"))
    #         if not param.get('no_text_field'):
    #             box.append(Input(**input_kwargs).add_class('filter-select'))
    #         else:
    #             box[-1].add_class('filter-select').add_class('standalone-select')

    #         grouping_div.add_element(
    #             Label(
    #                 for_=f"{id_base}-input", internal=box, title=param['description']
    #             ).add_class('checkbox-label').add_class('filter-label'))
    #     filter_form.add_element(grouping_div)
    # filter_form_div.add_element(filter_form)
    # page_content.add_element(filter_form_div)

    # # Arrange
    # arrange_div = Div()
    # # arrange_div.add_element(Header(level=1, internal='Filter Workouts'))
    # arrange_form = Form(action=f"/workout", method='get').add_class('arrange-form')
    # arrange_groupings = {}
    # for grouping in WORKOUT_ARRANGE_PARAMS.keys():
    #     if grouping not in arrange_groupings:
    #         arrange_groupings[grouping] = []
    #     for details in WORKOUT_ARRANGE_PARAMS[grouping].values():
    #         arrange_groupings[grouping].append(details)
    # for grouping in arrange_groupings.keys():
    #     params = arrange_groupings[grouping]
    #     grouping_div = Div()
    #     grouping_div.add_element(Header(level=3, internal=grouping))
    #     for param in params:
    #         id_base = param['variable'].replace(' ', '-').lower()
    #         input_kwargs = {
    #             'id': f"{id_base}-input",
    #             'name': param['display'],
    #             'value': param.get('default_value'),
    #         }
    #         if param.get('datatype'):
    #             input_kwargs['type'] = param['datatype']
    #         if param.get('size'):
    #             input_kwargs['size'] = param['size']
    #         # if param.get('required'):
    #         #     input_kwargs['required'] = True

    #         box = [
    #             Span(
    #                 for_=f"{id_base}-input", internal=param['display']
    #             ).add_class('arrange-checkbox-input'),
    #         ]
    #         if param.get('options'):
    #             options = []
    #             for option in param['options']:
    #                 options.append(Option(internal=option, id=f"{id_base}-input-select"))
    #             box.append(Select(internal=options, id=f"{id_base}-input-select"))
    #         if not param.get('no_text_field'):
    #             box.append(Input(**input_kwargs).add_class('arrange-select'))
    #         else:
    #             box[-1].add_class('arrange-select').add_class('standalone-select')

    #         grouping_div.add_element(
    #             Label(
    #                 for_=f"{id_base}-input", internal=box, title=param['description']
    #             ).add_class('checkbox-label').add_class('arrange-label'))
    #     arrange_form.add_element(grouping_div)
    # arrange_div.add_element(arrange_form)
    # page_content.add_element(arrange_div)

    # Display Form
    # display_form_div = Div()
    # display_form_div.add_element(Header(level=1, internal='Table Columns'))
    # display_form = Form(action=f"/workout", method='get').add_class('display-form')
    # display_groupings = {}
    # for grouping in WORKOUT_DISPLAY_PARAMS.keys():
    #     if grouping not in display_groupings:
    #         display_groupings[grouping] = []
    #     for details in WORKOUT_DISPLAY_PARAMS[grouping].values():
    #         display_groupings[grouping].append(details)
    # for grouping in display_groupings.keys():
    #     params = display_groupings[grouping]
    #     grouping_div = Div()
    #     grouping_div.add_element(Header(level=3, internal=grouping))
    #     for param in params:
    #         id_base = param['variable'].replace(' ', '-').lower()
    #         input_kwargs = {
    #             'type': 'checkbox',
    #             'id': f"{id_base}-input",
    #             'name': param['display'],
    #         }
    #         if param['html_display_filtering']['checked']:
    #             input_kwargs['checked'] = True
    #         input_tag = Input(
    #                 **input_kwargs
    #             ).add_class('display-checkbox-input')
    #         for group_class in param['html_display_filtering']['grouping_classes']:
    #             input_tag.add_class(group_class)
    #         box = [
    #             input_tag,
    #             Span(internal=param['display']),
    #         ]
    #         grouping_div.add_element(
    #             Label(
    #                 internal=box, id=f"{id_base}-label", title=param['html_display_filtering']['description'], for_=f"{id_base}-input"
    #             ).add_class('checkbox-label'))
    #     display_form.add_element(grouping_div)

    # display_form.add_element(
    #     Button(internal='Toggle all checkboxes', title='Toggle all checkboxes', type='button', onclick='toggleCheckboxesAll()').add_class('small-button'))
    # display_form_div.add_element(display_form)
    # page_content.add_element(display_form_div)

    # page_content.add_element(
    #     Button(internal='Request Data', type='button', onclick='applyFilterForm()').add_class('big-button').add_class('submit-button'))

    # page_content.add_element(
    #     Button(internal='Apply Column Checkboxes', type='button', onclick='applyDisplayFilters()').add_class('big-button'))

    # Workout Content
    # Workout Dates
    # page_content_workout = Div().add_class('display-item')
    workouts_dict = {}
    for workout in workouts:
        workout_datetime = datetime.strftime(workout.workout_date, "%a %b %d")
        workout_name = workout.workout
        if workout_datetime not in workouts_dict:
            workouts_dict[workout_datetime] = {}
        if workout_name not in workouts_dict[workout_datetime]:
            workouts_dict[workout_datetime][workout_name] = []
        workouts_dict[workout_datetime][workout_name].append(workout)

    workout_dates_div = Div().add_class('workout-dates-div')
    for date , workout_details in workouts_dict.items():
        for workout_name, workout_list in workout_details.items():
            column_names = ['First', 'Last'] + [k for k in workout_list[0].results.keys()]
            workout_div = Div().add_class('workout-div')

            workout_div.add_element(Header(level=3, internal=f"{date} - {workout_name}"))
            workout_dates_table = Table().add_class('workout-dates-table')
            workout_dates_table.add_element(TableRow(
                internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
            ))
            for index, workout in enumerate(workout_list):
                if index % 2:
                    workout_table_row = TableRow().add_class('odd-row')
                else:
                    workout_table_row = TableRow().add_class('even-row')
                workout_table_row.add_element(
                    TableData(internal=f"{workout.athlete.first_name}").add_class('event-table-data'))
                workout_table_row.add_element(
                    TableData(internal=f"{workout.athlete.last_name}").add_class('event-table-data'))
                for result in workout.results.values():
                    if isinstance(result, Result):
                        value = result.format_smaller_value
                    else:
                        value = result
                    workout_table_row.add_element(
                        TableData(internal=f"{value}").add_class('event-table-data'))
                workout_dates_table.add_element(workout_table_row)

            workout_div.add_element(workout_dates_table)
        workout_dates_div.add_element(workout_div)
    page_content.add_element(workout_dates_div)


    # # Table
    # table_div = Div(id='table-div')
    # page_content.add_element(table_div)

    # # Pagination
    # pagination_div = Div().add_class('pagination-div')
    # page_content.add_element(pagination_div)

    # # JS Files
    # js_files = [
    #     os.path.join('workout', 'applyFilterForm.js'),
    #     os.path.join('workout', 'GETFilterWorkout.js'),
    #     os.path.join('workout', 'populateWorkoutTable.js'),
    #     os.path.join('workout', 'applyDisplayFilters.js'),
    #     os.path.join('workout', 'toggleCheckboxes.js'),
    #     os.path.join('common', 'pagination.js'),
    # ]
    # for fl in js_files:
    #     with open(os.path.join('html', fl), 'r') as jf:
    #         # line = line.replace('SERVICE_URL', service_url)
    #         js_lines = jf.readlines()
    #         js_lines[-1] += '\n'  # In case there is not a newline at the end of the file
    #         # js_script = [l[:-1] for l in js_lines]
    #         # js_script = []
    #         # for line in [l[:-1] for l in js_lines]:
    #         #     line = line.replace('ROW_BACKGROUND_COLOR_1', 'black')
    #         #     line = line.replace('ROW_BACKGROUND_COLOR_2', 'red')
    #         #     js_script.append(line)
    #         page_content.add_element(
    #             Script(internal=[l[:-1] for l in js_lines])
    #         )
    #         # page_content.add_element(
    #         #     Script(internal=js_script)
    #         # )
    body_content = BodyContent(body_content=[page_content])

    # Styles
    for style in PAGE_STYLES:
        body_content.add_body_styles(style)
    for style in FILTER_STYLES:
        body_content.add_body_styles(style)
    for style in TABLE_STYLES:
        body_content.add_body_styles(style)

    base_doc.body_content = body_content
    return base_doc.return_document

"""
https://www.w3schools.com/css/css3_pagination.asp
"""
