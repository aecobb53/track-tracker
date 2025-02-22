import os

from datetime import datetime, timezone
from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .base_page import project_base_page
from .common import ATHLETE_FILTER_PARAMS, ATHLETE_DISPLAY_PARAMS

def filter_athletes_html_page():
    page_content = Div().add_style({'display': 'block', 'color': '#949ba4'})


    # Filter
    # First Name
    # Last Name
    # School

    # Display Each event theyve done in its own tile that can be hidden
    # It should have their record, the date and a list of previous instances





    # Filter Form
    filter_form_div = Div()
    filter_form_div.add_element(Header(level=1, internal='Data Filter'))
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
            # if param.get('required'):
            #     input_kwargs['required'] = True
            if param.get('options'):
                # If there are options add them as a modifier to the input
                input_kwargs['options'] = param['options']
                options = []
                for option in param['options']:
                    options.append(Option(value=option, internal=option))
                select = Select(internal=options, id=f"{id_base}-input-select")
                box = [
                    Span(
                        for_=f"{id_base}-input", internal=param['display']
                    ).add_class('filter-checkbox-input').add_style({'margin': '0px'}),
                    select,
                    Input(**input_kwargs).add_style({'margin': '0px'}),
                ]
            else:
                box = [
                    Span(
                        for_=f"{id_base}-input", internal=param['display']
                    ).add_class('filter-checkbox-input').add_style({'margin': '0px'}),
                    Input(**input_kwargs).add_style({'margin': '0px'}),
                ]

            # print(f"BOX: {box}")
            # print(f"LEN: {len(box)}")
            grouping_div.add_element(
                Label(
                    for_=f"{id_base}-input", internal=box, title=param['description']
                ).add_class('checkbox-label').add_class('filter-label'))
        filter_form.add_element(grouping_div)
    filter_form_div.add_element(filter_form)
    filter_form_div.add_element(
        Button(internal='Submit', type='button', onclick='applyFilterForm()').add_class('big-button'))
    page_content.add_element(filter_form_div)

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
        # print(f"GROUPING: {grouping}")
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
                ).add_class('display-checkbox-input').add_style({'margin': '0px'})
            for group_class in param['html_display_filtering']['grouping_classes']:
                input_tag.add_class(group_class)
            box = [
                input_tag,
                Span(internal=param['display']).add_style({'margin': '0px'}),
            ]
            grouping_div.add_element(
                Label(
                    internal=box, id=f"{id_base}-label", title=param['html_display_filtering']['description'], for_=f"{id_base}-input"
                ).add_class('checkbox-label'))
        display_form.add_element(grouping_div)

    display_form.add_element(
        Button(internal='All', title='Toggle all checkboxes', type='button', onclick='toggleCheckboxesAll()').add_class('small-button'))
    display_form_div.add_element(display_form)
    display_form_div.add_element(
        Button(internal='Apply', type='button', onclick='applyDisplayFilters()').add_class('big-button'))
    page_content.add_element(display_form_div)

    # Table
    table_div = Div(id='table-div').add_style({'margin': '10px'})
    page_content.add_element(table_div)

    # JS Files
    js_files = [
        os.path.join('athlete', 'applyFilterForm.js'),
        os.path.join('athlete', 'GETFilterAthlete.js'),
        os.path.join('athlete', 'populateAthleteTable.js'),
        os.path.join('athlete', 'applyDisplayFilters.js'),
        os.path.join('athlete', 'toggleCheckboxes.js'),
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
    ]

    base_doc = project_base_page()
    base_doc.body_content.body_content.append(page_content)
    for style in document_style:
        base_doc.document.add_head_element(style)
    return base_doc.return_document



def find_athletes_html_page(athlete, marks):
    page_content = Div().add_style({'display': 'block', 'color': '#949ba4'})

    print(f"ATHLETE: {athlete}")

    page_content.add_element(Header(level=1, internal=f"{athlete.first_name} {athlete.last_name}"))
    page_content.add_element(Header(level=2, internal=f"{athlete.team} - {athlete.gender}"))
    page_content.add_element(Header(level=2, internal=f"Graduation Year: {athlete.graduation_year}"))

    page_content.add_element(Header(level=1, internal=f"Events"))

    events_dict = {}
    for mark in marks:
        print(f"MARK: {mark}")
        if mark.event not in events_dict:
            events_dict[mark.event] = []
        events_dict[mark.event].append(mark)

    events_div = Div()
    column_names = ['Place', 'Meet', 'Mark', 'Wind', 'Heat', 'Date']
    # column_names = ['Place', 'Meet', 'Wind', 'Heat', 'Date']
    table_row_background_colors = ('#35363b', '#2c2d2e')
    for event, marks in events_dict.items():
        event_div = Div().add_class('event-div')
        event_div.add_element(Header(level=3, internal=event))
        event_table = Table().add_class('event-table')
        event_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
        ).add_style({'background-color': table_row_background_colors[1]})
        )
        print('')
        print('')

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

# MARK: uid='bc73a769-9306-4665-9555-4fcdaf6e4133' update_datetime=datetime.datetime(2025, 2, 22, 17, 3, 3, 918969) event='Girls Long Jump Finals' heat=1 place=1 wind=-0.9 athlete=None athlete_uid='df35325b-2b2d-41b4-879c-b8afe78a1e2c' team='Fairview High School' meet_date=datetime.datetime(2024, 3, 20, 0, 0) mark=Mark(event_str='Girls Long Jump Finals', mark_str='17-08.50', minutes=None, seconds=None, subsecond=None, feet=17, inches=8, fractions=0.5) meet='The Fairview Quad Meet' gender='Womens'


            # mark_div = Div()
        #     mark_div.add_element(Paragraph(internal=f"-MARK-"))

        #     table_div = Div(id='event-table-div')
        #     table = Table()

        #     # Header
        #     header_row = TableRow()
        #     for column in column_names:
        #         header_row.add_element(TableHeader(internal=column))
        #     table.add_element(header_row)
        #     # Content
        #     mark_div.add_element(table_div)

        #     table_div.add_element(table)
        #     event_div.add_element(table_div)



            # event_div.add_element(mark_div)
        event_div.add_element(event_table)
        events_div.add_element(event_div)
    page_content.add_element(events_div)


# place
# mark
# wind
# heat



#     # JS Files
#     js_files = [
#         os.path.join('athlete', 'applyFilterForm.js'),
#         os.path.join('athlete', 'GETFilterAthlete.js'),
#         os.path.join('athlete', 'populateAthleteTable.js'),
#         os.path.join('athlete', 'applyDisplayFilters.js'),
#         os.path.join('athlete', 'toggleCheckboxes.js'),
#     ]
#     for fl in js_files:
#         with open(os.path.join('html', fl), 'r') as jf:
#             # line = line.replace('SERVICE_URL', service_url)
#             js_lines = jf.readlines()
#             js_lines[-1] += '\n'  # In case there is not a newline at the end of the file
#             page_content.add_element(
#                 Script(internal=[l[:-1] for l in js_lines])
#             )

    # Styles
    document_style = [
        StyleTag(name='h1', internal="""
            margin: 20px;
        """),
        StyleTag(name='h2', internal="""
            margin: 10px 30px;
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

    base_doc = project_base_page()
    base_doc.body_content.body_content.append(page_content)
    for style in document_style:
        base_doc.document.add_head_element(style)
    return base_doc.return_document





