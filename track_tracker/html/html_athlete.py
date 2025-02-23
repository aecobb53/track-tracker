import os

from datetime import datetime, timezone
from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .base_page import project_base_page
from .common import ATHLETE_FILTER_PARAMS, ATHLETE_ARRANGE_PARAMS, ATHLETE_DISPLAY_PARAMS

async def filter_athletes_html_page():
    page_content = Div().add_class('page-content')

    # Filter Form
    filter_form_div = Div()
    filter_form_div.add_element(Header(level=1, internal='Athlete Results'))
    filter_form_div.add_element(Paragraph(internal='''
    This page is for finding athletes by filtering criteria. You can use it to get headcounts of similar athletes or 
    find similar athletes to compare. The filters are partial as in you can query for the Team "Fairview" to get all 
    Fairview High School marks. Some have additional dropdowns. For example, you can filter for Heats <= 3. 
    Table columns can be toggled with the checkboxes to make viewing easier.
    '''))
    filter_form_div.add_element(Paragraph(
        internal='For multiple items separate with a comma. Ex "Fairview, Boulder"'))
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
    arrange_div.add_element(Header(level=1, internal='Filter Results'))
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

    page_content.add_element(
        Button(internal='Request', type='button', onclick='applyFilterForm()').add_class('big-button'))

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
        Button(internal='All', title='Toggle all checkboxes', type='button', onclick='toggleCheckboxesAll()').add_class('small-button'))
    display_form_div.add_element(display_form)
    page_content.add_element(display_form_div)

    page_content.add_element(
        Button(internal='Apply', type='button', onclick='applyDisplayFilters()').add_class('big-button'))

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

    # Styles
    document_style = [
        StyleTag(name='.athlete-link', internal="""
            color: #949ba4;
            text-decoration: underline;
        """),

        StyleTag(name='.page-content', internal="""
            display: block;
            color: #949ba4;
            margin: 10px;
        """),
        StyleTag(name='.filter-checkbox-input', internal="""
            margin: 0;
        """),
        StyleTag(name='.big-button', internal="""
            margin: 10px;
            padding: 5px;
            font-size: 120%;
            font-weight: bold;
            text-decoration: underline;
        """),
        StyleTag(name='.small-button', internal="""
            margin: 5px;
            padding: 5px;
            font-size: 100%;
            font-weight: bold;
        """),

        StyleTag(name='.pagination-div', internal="""
            display: inline-block;
            font-size: 300%;
            color: #949ba4;
            margin: 10px;
            text-decoration: none;
            text-align: center;
            width: 100%;
        """),
        StyleTag(name='.pagination-div button', internal="""
            border-radius: 5px;
            margin: 4px;
            padding: 5px;
            text-decoration: none;
        """),
        StyleTag(name='.pagination-div button.active', internal="""
            color: #000000;
            background-color: green;
        """),

    ]

    base_doc = await project_base_page()
    base_doc.body_content.body_content.append(page_content)
    for style in document_style:
        base_doc.document.add_head_element(style)
    return base_doc.return_document



async def find_athletes_html_page(athlete, marks):
    page_content = Div().add_class('page-content')
    page_content.add_element(Header(level=1, internal='Athlete Page'))

    page_content.add_element(Paragraph(internal='''
    This page displays information about an athlete. Notice there is one final row in each table and that is the 
    current PR for that event.
    '''))

    athlete_name = f"{athlete.first_name} {athlete.last_name}"
    page_content.add_element(Header(level=1, internal=f"{athlete_name}"))
    page_content.add_element(Header(level=2, internal=f"{athlete.team} - {athlete.gender}"))
    page_content.add_element(Header(level=2, internal=f"Graduation Year: {athlete.graduation_year}"))

    page_content.add_element(Header(level=1, internal=f"Events"))

    events_dict = {}
    for mark in marks:
        if mark.event not in events_dict:
            events_dict[mark.event] = []
        events_dict[mark.event].append(mark)

    events_div = Div()
    column_names = ['Place', 'Meet', 'Mark', 'Wind', 'Heat', 'Date']
    # column_names = ['Place', 'Meet', 'Wind', 'Heat', 'Date']
    table_row_background_colors = ('#35363b', '#2c2d2e')
    for event, marks in events_dict.items():
        marks.sort(key=lambda x: x.meet_date)
        record_mark = marks[0]
        for mark in marks:
            if mark.mark > record_mark.mark:
                record_mark = mark

        event_div = Div().add_class('event-div')
        event_div.add_element(Header(level=3, internal=event))
        event_table = Table().add_class('event-table')
        event_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
        ).add_style({'background-color': table_row_background_colors[1]})
        )

        for index, mark in enumerate(marks):
            print(f"LEN: {len(marks)} INDEX: {index} MOD: {index % 2}")
            event_table_row = TableRow().add_style({'background-color': table_row_background_colors[index % 2]})
            event_table_row.add_element(
                TableData(internal=f"{mark.place}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{mark.meet}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{mark.mark.mark_str}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{mark.wind}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{mark.heat}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{datetime.strftime(mark.meet_date, '%Y-%m-%d')}").add_class('event-table-data'))
            event_table.add_element(event_table_row)

        # Final rows
        event_table_row = TableRow().add_style({'background-color': table_row_background_colors[0]})
        for _ in column_names:
            event_table_row.add_element(
            TableData(internal=f"-").add_class('event-table-data'))
        event_table.add_element(event_table_row)

        event_table_row = TableRow().add_style({'background-color': table_row_background_colors[1]})
        event_table_row.add_element(
            TableData(internal=f"{record_mark.place}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_mark.meet}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_mark.mark.mark_str}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_mark.wind}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_mark.heat}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{datetime.strftime(record_mark.meet_date, '%Y-%m-%d')}").add_class('event-table-data'))
        event_table.add_element(event_table_row)

        event_div.add_element(event_table)
        events_div.add_element(event_div)
    page_content.add_element(events_div)

    # Styles
    document_style = [
        StyleTag(name='h1', internal="""
            margin: 20px;
        """),
        StyleTag(name='h2', internal="""
            margin: 10px 30px;
        """),
        StyleTag(name='p', internal="""
            margin: 20px 30px;
        """),
        # StyleTag(name='.events-div', internal="""
        #     margin: 10px 40px;
        # """),

        # StyleTag(name='.events-div', internal="""
        #     color: #c4cedb;
        #     margin: 0;
        #     padding: 0;
        #     display: inline;
        # """),

        StyleTag(name='.event-div', internal="""
            background-color: #393B41;
            margin: 10px;
            padding: 0px 5px 10px;
            border: 3px solid black;
            border-radius: 15px;
            -moz-border-radius: 15px;
            width: 97%;
            display: inline-block;
            vertical-align: top;
        """),

        # IM NOT SURE WHY IT IS NOT FITTING PROPPERLY AT 100% WIDTH

        StyleTag(name='.event-div h3', internal="""
            margin: 10px;
            padding: 0;
            text-align: center;
        """),
        StyleTag(name='.event-table', internal="""
            width: 100%;
            border: 5 solid black;
        """),
    ]

    base_doc = await project_base_page()
    base_doc.body_content.body_content.append(page_content)
    for style in document_style:
        base_doc.document.add_head_element(style)
    return base_doc.return_document





