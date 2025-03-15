import os

from datetime import datetime, timezone
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
from .common import ATHLETE_FILTER_PARAMS, ATHLETE_ARRANGE_PARAMS, ATHLETE_DISPLAY_PARAMS, display_date, class_formatter

async def filter_athletes_html_page():
    base_doc = await project_base_page()

    page_content = Div().add_class('page-content')

    # Filter Form
    filter_form_div = Div()
    filter_form_div.add_element(Header(level=1, internal='Athlete Results'))
    # filter_form_div.add_element(Paragraph(internal='''
    # This page is for finding athletes by filtering criteria. You can use it to get headcounts of similar athletes or 
    # find similar athletes to compare. The filters are partial as in you can query for the Team "Fairview" to get all 
    # Fairview High School results. Some have additional dropdowns. For example, you can filter for Heats <= 3. 
    # Table columns can be toggled with the checkboxes to make viewing easier.
    # '''))
    # filter_form_div.add_element(Paragraph(
    #     internal='For multiple items separate with a comma. Ex "Fairview, Boulder"'))
    filter_form = Form(action=f"/athlete", method='get').add_class('filter-form')
    filter_groupings = {}
    for grouping in ATHLETE_FILTER_PARAMS.keys():
        if grouping not in filter_groupings:
            filter_groupings[grouping] = []
        for details in ATHLETE_FILTER_PARAMS[grouping].values():
            filter_groupings[grouping].append(details)
    for grouping in filter_groupings.keys():
        params = filter_groupings[grouping]
        grouping_div = Div()
        grouping_div.add_element(Header(level=3, internal=grouping))
        for param in params:
            id_base = param['variable'].replace(' ', '-').lower()
            input_kwargs = {
                'id': f"{id_base}-input",
                'name': param['display'],
                'value': param['default_value'],
            }
            if param.get('datatype'):
                input_kwargs['type'] = param['datatype']
            if param.get('size'):
                input_kwargs['size'] = param['size']

            box = [
                Span(
                    for_=f"{id_base}-input", internal=param['display']
                ).add_class('filter-checkbox-input'),
            ]
            if param.get('options'):
                options = []
                for option in param['options']:
                    options.append(Option(internal=option, id=f"{id_base}-input-select"))
                box.append(Select(internal=options, id=f"{id_base}-input-select"))
            if not param.get('no_text_field'):
                box.append(Input(**input_kwargs).add_class('filter-select'))
            else:
                box[-1].add_class('filter-select').add_class('standalone-select')

            grouping_div.add_element(
                Label(
                    for_=f"{id_base}-input", internal=box, title=param['description']
                ).add_class('checkbox-label').add_class('filter-label'))
        filter_form.add_element(grouping_div)
    filter_form_div.add_element(filter_form)
    page_content.add_element(filter_form_div)

    # Arrange
    arrange_div = Div()
    # arrange_div.add_element(Header(level=1, internal='Filter Results'))
    arrange_form = Form(action=f"/athlete", method='get').add_class('arrange-form')
    arrange_groupings = {}
    for grouping in ATHLETE_ARRANGE_PARAMS.keys():
        if grouping not in arrange_groupings:
            arrange_groupings[grouping] = []
        for details in ATHLETE_ARRANGE_PARAMS[grouping].values():
            arrange_groupings[grouping].append(details)
    for grouping in arrange_groupings.keys():
        params = arrange_groupings[grouping]
        grouping_div = Div()
        grouping_div.add_element(Header(level=3, internal=grouping))
        for param in params:
            id_base = param['variable'].replace(' ', '-').lower()
            input_kwargs = {
                'id': f"{id_base}-input",
                'name': param['display'],
                'value': param.get('default_value'),
            }
            if param.get('datatype'):
                input_kwargs['type'] = param['datatype']
            if param.get('size'):
                input_kwargs['size'] = param['size']
            # if param.get('required'):
            #     input_kwargs['required'] = True

            box = [
                Span(
                    for_=f"{id_base}-input", internal=param['display']
                ).add_class('arrange-checkbox-input'),
            ]
            if param.get('options'):
                options = []
                for option in param['options']:
                    options.append(Option(internal=option, id=f"{id_base}-input-select"))
                box.append(Select(internal=options, id=f"{id_base}-input-select"))
            if not param.get('no_text_field'):
                box.append(Input(**input_kwargs).add_class('arrange-select'))
            else:
                box[-1].add_class('arrange-select').add_class('standalone-select')

            grouping_div.add_element(
                Label(
                    for_=f"{id_base}-input", internal=box, title=param['description']
                ).add_class('checkbox-label').add_class('arrange-label'))
        arrange_form.add_element(grouping_div)
    arrange_div.add_element(arrange_form)
    page_content.add_element(arrange_div)

    # Display Form
    display_form_div = Div()
    display_form_div.add_element(Header(level=1, internal='Table Columns'))
    display_form = Form(action=f"/athlete", method='get').add_class('display-form')
    display_groupings = {}
    for grouping in ATHLETE_DISPLAY_PARAMS.keys():
        if grouping not in display_groupings:
            display_groupings[grouping] = []
        for details in ATHLETE_DISPLAY_PARAMS[grouping].values():
            display_groupings[grouping].append(details)
    for grouping in display_groupings.keys():
        params = display_groupings[grouping]
        grouping_div = Div()
        grouping_div.add_element(Header(level=3, internal=grouping))
        for param in params:
            id_base = param['variable'].replace(' ', '-').lower()
            input_kwargs = {
                'type': 'checkbox',
                'id': f"{id_base}-input",
                'name': param['display'],
            }
            if param['html_display_filtering']['checked']:
                input_kwargs['checked'] = True
            input_tag = Input(
                    **input_kwargs
                ).add_class('display-checkbox-input')
            for group_class in param['html_display_filtering']['grouping_classes']:
                input_tag.add_class(group_class)
            box = [
                input_tag,
                Span(internal=param['display'])
            ]
            grouping_div.add_element(
                Label(
                    internal=box, id=f"{id_base}-label", title=param['html_display_filtering']['description'], for_=f"{id_base}-input"
                ).add_class('checkbox-label'))
        display_form.add_element(grouping_div)

    display_form.add_element(
        Button(internal='Toggle all checkboxes', title='Toggle all checkboxes', type='button', onclick='toggleCheckboxesAll()').add_class('small-button'))
    display_form_div.add_element(display_form)
    page_content.add_element(display_form_div)

    page_content.add_element(
        Button(internal='Request Data', type='button', onclick='applyFilterForm()').add_class('big-button').add_class('submit-button'))

    page_content.add_element(
        Button(internal='Apply Column Checkboxes', type='button', onclick='applyDisplayFilters()').add_class('big-button'))

    # Table
    table_div = Div(id='table-div')
    page_content.add_element(table_div)

    # Pagination
    pagination_div = Div().add_class('pagination-div')
    page_content.add_element(pagination_div)

    # JS Files
    js_files = [
        os.path.join('athlete', 'applyFilterForm.js'),
        os.path.join('athlete', 'GETFilterAthlete.js'),
        os.path.join('athlete', 'populateAthleteTable.js'),
        os.path.join('athlete', 'applyDisplayFilters.js'),
        os.path.join('athlete', 'toggleCheckboxes.js'),
        os.path.join('common', 'pagination.js'),
    ]
    for fl in js_files:
        with open(os.path.join('html', fl), 'r') as jf:
            # line = line.replace('SERVICE_URL', service_url)
            js_lines = jf.readlines()
            js_lines[-1] += '\n'  # In case there is not a newline at the end of the file
            page_content.add_element(
                Script(internal=[l[:-1] for l in js_lines])
            )
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


async def find_athletes_html_page(athlete, results):
    base_doc = await project_base_page()

    page_content = Div().add_class('page-content')
    # page_content.add_element(Header(level=1, internal='Athlete Page'))


    athlete_name = f"{athlete.first_name} {athlete.last_name}"
    athlete_info_div = Div()
    athlete_info_div.add_element(Header(level=1, internal=f"{athlete_name}"))
    athlete_info_div.add_element(Header(level=2, internal=f"{athlete.team} - {athlete.gender}"
    ).add_class('athlete-info-tag'))
    athlete_info_div.add_element(Header(level=2, internal=f"Class: {athlete.graduation_year} - {class_formatter(athlete.graduation_year)[0]}"
    ).add_class('athlete-info-tag'))
    if athlete.gender.startswith('M'):
        athlete_info_div.add_class('mens-format')
    else:
        athlete_info_div.add_class('womens-format')

    athlete_info_div.add_element(Header(level=2, internal=f"Tags: {', '.join(athlete.tags)}").add_class('athlete-info-tag'))
    if 'Takeoff' in athlete.athlete_metadata:
        athlete_info_div.add_element(Header(level=2, internal=f"Takeoff: {athlete.athlete_metadata['Takeoff']}").add_class('athlete-info-tag'))

    season_points = {}
    for result in results:
        if result.points:
            if result.meet_date.year not in season_points:
                season_points[result.meet_date.year] = 0
            season_points[result.meet_date.year] += result.points
    if season_points:
        athlete_info_div.add_element(Header(level=2, internal=f"Varsity Points").add_class('athlete-info-tag'))

        season_points = dict(sorted(season_points.items(), key=lambda x: x[0], reverse=False))
    for year, points in season_points.items():
        athlete_info_div.add_element(Header(level=3, internal=f"    {year}: {points}").add_class('athlete-info-tag'))

    page_content.add_element(athlete_info_div)

    page_content.add_element(Header(level=1, internal=f"Events"))

    events_dict = {}
    for result in results:
        if result.event not in events_dict:
            events_dict[result.event] = []
        events_dict[result.event].append(result)

    events_div = Div()
    column_names = ['Place', 'Points', 'Meet', 'Result', 'Wind (m/s)', 'Heat', 'Date']
    for event, results in events_dict.items():
        results.sort(key=lambda x: x.meet_date)
        record_result = results[0]
        for result in results:
            if result.result > record_result.result:
                record_result = result

        event_div = Div().add_class('event-div')
        event_div.add_element(Header(level=3, internal=event))
        event_table = Table().add_class('event-table')
        event_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
        ))

        for index, result in enumerate(results):
            if index % 2:
                event_table_row = TableRow().add_class('odd-row')
            else:
                event_table_row = TableRow().add_class('even-row')
            event_table_row.add_element(
                TableData(internal=f"{result.place}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.points}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.meet}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.result.result_str}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.wind}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.heat}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{display_date(result.meet_date)}").add_class('event-table-data'))
            event_table.add_element(event_table_row)

        # Final rows
        event_table_row = TableRow().add_class('record-row')
        for _ in column_names:
            event_table_row.add_element(
            TableData(internal=f" ").add_class('event-table-data'))
        event_table.add_element(event_table_row)

        event_table_row = TableRow().add_class('record-row')
        event_table_row.add_element(
            TableData(internal=f"{record_result.place}").add_class('event-table-data'))
        event_table_row.add_element(
                TableData(internal=f"{result.points}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.meet}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.result.result_str}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.wind}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.heat}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{display_date(record_result.meet_date)}").add_class('event-table-data'))
        event_table.add_element(event_table_row)

        event_div.add_element(event_table)
        events_div.add_element(event_div)
    page_content.add_element(events_div)
    body_content = BodyContent(body_content=[page_content])

    # Styles
    document_styles = [
        StyleTag(name='.athlete-info-tag', internal="""
            margin: 20px 50px;
            padding: 0;
        """),
    ]


    # Styles
    for style in PAGE_STYLES:
        body_content.add_body_styles(style)
    for style in FILTER_STYLES:
        body_content.add_body_styles(style)
    for style in TABLE_STYLES:
        body_content.add_body_styles(style)
    for style in document_styles:
        body_content.add_body_styles(style)

    base_doc.body_content = body_content
    return base_doc.return_document
