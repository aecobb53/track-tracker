from asyncio import events
import os

from datetime import datetime
from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .base_page import (
    project_base_page,
    SEASON_YEAR,
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
from .common import TEAM_FILTER_PARAMS, TEAM_ARRANGE_PARAMS, TEAM_DISPLAY_PARAMS, display_date, class_formatter


async def filter_teams_html_page():
    base_doc = await project_base_page()

    page_content = Div().add_class('page-content')

    # Filter Form
    filter_form_div = Div()
    filter_form_div.add_element(Header(level=1, internal='Team Results'))
    # filter_form_div.add_element(Paragraph(internal='''
    # This page is for finding teams by filtering criteria. You can use it to get headcounts of athletes. The filters are partial as in you can query for the Team "Fairview" to get all 
    # Fairview High School results. Some have additional dropdowns. For example, you can filter for Heats <= 3. 
    # Table columns can be toggled with the checkboxes to make viewing easier.
    # '''))
    # filter_form_div.add_element(Paragraph(
    #     internal='For multiple items separate with a comma. Ex "Fairview, Boulder"'))
    filter_form = Form(action=f"/athlete", method='get').add_class('filter-form')
    filter_groupings = {}
    for grouping in TEAM_FILTER_PARAMS.keys():
        if grouping not in filter_groupings:
            filter_groupings[grouping] = []
        for details in TEAM_FILTER_PARAMS[grouping].values():
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
    arrange_form = Form(action=f"/result", method='get').add_class('arrange-form')
    arrange_groupings = {}
    for grouping in TEAM_ARRANGE_PARAMS.keys():
        if grouping not in arrange_groupings:
            arrange_groupings[grouping] = []
        for details in TEAM_ARRANGE_PARAMS[grouping].values():
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
    display_form = Form(action=f"/team", method='get').add_class('display-form')
    display_groupings = {}
    for grouping in TEAM_DISPLAY_PARAMS.keys():
        if grouping not in display_groupings:
            display_groupings[grouping] = []
        for details in TEAM_DISPLAY_PARAMS[grouping].values():
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
        os.path.join('team', 'applyFilterForm.js'),
        os.path.join('team', 'GETFilterTeam.js'),
        os.path.join('team', 'populateTeamTable.js'),
        os.path.join('team', 'applyDisplayFilters.js'),
        os.path.join('team', 'toggleCheckboxes.js'),
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

async def find_team_html_page(athletes, results, team_name, season_year=SEASON_YEAR):
    base_doc = await project_base_page()

    page_content = Div().add_class('page-content')
    page_content.add_element(Header(level=1, internal='Team Page'))

    # page_content.add_element(Paragraph(internal='''
    # This page displays information about a team. Notice there is one final row in each table and that is 
    # the current record for the team for that event. 
    # '''))

    # Team Info
    page_content.add_element(Header(level=1, internal=f"{athletes[0].team}"))

    boys = [a for a in athletes if a.gender == 'Boys']
    girls = [a for a in athletes if a.gender == 'Girls']

    current_year = datetime.now().year
    freshmen = [a for a in athletes if a.graduation_year == current_year + 3]
    sophomore = [a for a in athletes if a.graduation_year == current_year + 2]
    juniors = [a for a in athletes if a.graduation_year == current_year + 1]
    seniors = [a for a in athletes if a.graduation_year == current_year]


    page_content.add_element(Header(level=2, internal=f"Athlete count: {len(athletes)}").add_class('team-info-tag'))
    page_content.add_element(Header(level=2, internal=f"Boys: {len(boys)}").add_class('team-info-tag').add_class('mens-format'))
    page_content.add_element(Header(level=2, internal=f"Girls: {len(girls)}").add_class('team-info-tag').add_class('womens-format'))
    page_content.add_element(Header(level=2, internal=f"Freshmen: {len(freshmen)}").add_class('team-info-tag'))
    page_content.add_element(Header(level=2, internal=f"Sophomore: {len(sophomore)}").add_class('team-info-tag'))
    page_content.add_element(Header(level=2, internal=f"Juniors: {len(juniors)}").add_class('team-info-tag'))
    page_content.add_element(Header(level=2, internal=f"Seniors: {len(seniors)}").add_class('team-info-tag'))


    # Pulled Content
    season_selector = Div().add_class('season-selector-div')
    season_selector.add_element(Header(level=2, internal='Season Selector'))

    season_selector_link = Link(internal=f'{SEASON_YEAR}', href=f"/html/team/{team_name}/{SEASON_YEAR}"
        ).add_class('team-season-selector').add_class('button-emulator-format')
    if season_year == SEASON_YEAR:
        season_selector_link.add_class('button-activated')
    else:
        season_selector_link.add_class('button-deactivated')
    season_selector.add_element(Div(internal=season_selector_link).add_class('link-workaround-div'))

    season_selector_link = Link(internal=f'{SEASON_YEAR - 1}', href=f"/html/team/{team_name}/{SEASON_YEAR - 1}"
        ).add_class('team-season-selector').add_class('button-emulator-format')
    if season_year == SEASON_YEAR - 1:
        season_selector_link.add_class('button-activated')
    else:
        season_selector_link.add_class('button-deactivated')
    season_selector.add_element(Div(internal=season_selector_link).add_class('link-workaround-div'))

    season_selector_link = Link(internal=f'{SEASON_YEAR - 2}', href=f"/html/team/{team_name}/{SEASON_YEAR - 2}"
        ).add_class('team-season-selector').add_class('button-emulator-format')
    if season_year == SEASON_YEAR - 2:
        season_selector_link.add_class('button-activated')
    else:
        season_selector_link.add_class('button-deactivated')
    season_selector.add_element(Div(internal=season_selector_link).add_class('link-workaround-div'))
    page_content.add_element(season_selector)
    # page_content.add_element(Div(internal=season_selector).add_class('link-workaround-div'))


    # Sorting (added in each section)
    display_form = Form(action=f"/result", method='get').add_class('display-form')
    display_form.add_element(Header(level=2, internal='Display Options'))

    # Primary Content
    display_different_content = Div().add_class('page-content-divs')


    # Events - Chronological
    display_form.add_element(
        Button(internal='Events Chronological', type='button', onclick="teamDisplay('Events-chronological')"
        ).add_class('button-item-events-chronological').add_class('team-display-button').add_class('button-activated'))
    page_content_event = Div().add_class('display-item-activated').add_class('page-content-events-chronological')
    page_content_event.add_element(Header(level=1, internal=f"Events Chronological"))
    event_dict = {}

    for result in results:
        if result.event not in event_dict:
            event_dict[result.event] = []
        for athlete in athletes:
            if athlete.uid == result.athlete_uid:
                result.athlete = athlete
                break
        event_dict[result.event].append(result)
    events_div = Div()
    column_names = ['Place', 'Meet', 'Athlete', 'Result', 'Wind (m/s)', 'Heat', 'Class', 'Date']
    for event, event_results in event_dict.items():
        event_results.sort(key=lambda x: x.meet_date)
        record_result = event_results[0]
        for result in event_results:
            if result.result > record_result.result:
                record_result = result

        event_div = Div().add_class('event-div')
        event_div.add_element(Header(level=3, internal=event))
        event_table = Table().add_class('event-table')
        event_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
        ))

        for index, result in enumerate(event_results):
            if index % 2:
                event_table_row = TableRow().add_class('odd-row')
            else:
                event_table_row = TableRow().add_class('even-row')
            event_table_row.add_element(
                TableData(internal=f"{result.place}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.meet}").add_class('event-table-data'))
            athlete_name = f"{result.athlete.first_name} {result.athlete.last_name}"
            event_table_row.add_element(
                TableData(internal=f"{athlete_name}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.result.result_str}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.wind}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.heat}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{class_formatter(result.athlete.graduation_year)[0]}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{display_date(result.meet_date)}").add_class('event-table-data'))
            event_table.add_element(event_table_row)

        # Final rows
        event_table_row = TableRow().add_class('record-row')
        event_table_row.add_element(
            TableData(internal=f"Current Best").add_class('event-table-data'))
        for _ in column_names[1:]:
            event_table_row.add_element(
                TableData(internal=f" ").add_class('event-table-data'))
        event_table.add_element(event_table_row)

        event_table_row = TableRow().add_class('record-row')
        event_table_row.add_element(
            TableData(internal=f"{record_result.place}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.meet}").add_class('event-table-data'))
        athlete_name = f"{record_result.athlete.first_name} {record_result.athlete.last_name}"
        event_table_row.add_element(
            TableData(internal=f"{athlete_name}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.result.result_str}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.wind}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.heat}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{class_formatter(result.athlete.graduation_year)[0]}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{display_date(record_result.meet_date)}").add_class('event-table-data'))
        event_table.add_element(event_table_row)

        event_div.add_element(event_table)
        events_div.add_element(event_div)

    page_content_event.add_element(events_div)
    # page_content_event.attributes['hidden'] = None
    display_different_content.add_element(page_content_event)


    # Events - Results
    display_form.add_element(
        Button(internal='Events Results', type='button', onclick="teamDisplay('Events-results')"
        ).add_class('button-item-events-results').add_class('team-display-button').add_class('button-deactivated'))
    page_content_event = Div().add_class('display-item-activated').add_class('page-content-events-results')
    page_content_event.add_element(Header(level=1, internal=f"Events Results"))
    event_dict = {}

    for result in results:
        if result.event not in event_dict:
            event_dict[result.event] = []
        for athlete in athletes:
            if athlete.uid == result.athlete_uid:
                result.athlete = athlete
                break
        event_dict[result.event].append(result)
    events_div = Div()
    column_names = ['Place', 'Meet', 'Athlete', 'Result', 'Wind (m/s)', 'Heat', 'Class', 'Date']
    for event, event_results in event_dict.items():
        event_results.sort(key=lambda x: x.result.sort_value)
        record_result = event_results[0]
        for result in event_results:
            if result.result > record_result.result:
                record_result = result

        event_div = Div().add_class('event-div')
        event_div.add_element(Header(level=3, internal=event))
        event_table = Table().add_class('event-table')
        event_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
        ))

        for index, result in enumerate(event_results):
            if index % 2:
                event_table_row = TableRow().add_class('odd-row')
            else:
                event_table_row = TableRow().add_class('even-row')
            event_table_row.add_element(
                TableData(internal=f"{result.place}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.meet}").add_class('event-table-data'))
            athlete_name = f"{result.athlete.first_name} {result.athlete.last_name}"
            event_table_row.add_element(
                TableData(internal=f"{athlete_name}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.result.result_str}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.wind}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{result.heat}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{class_formatter(result.athlete.graduation_year)[0]}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{display_date(result.meet_date)}").add_class('event-table-data'))
            event_table.add_element(event_table_row)

        # Final rows
        event_table_row = TableRow().add_class('record-row')
        event_table_row.add_element(
            TableData(internal=f"Current Best").add_class('event-table-data'))
        for _ in column_names[1:]:
            event_table_row.add_element(
                TableData(internal=f" ").add_class('event-table-data'))
        event_table.add_element(event_table_row)

        event_table_row = TableRow().add_class('record-row')
        event_table_row.add_element(
            TableData(internal=f"{record_result.place}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.meet}").add_class('event-table-data'))
        athlete_name = f"{record_result.athlete.first_name} {record_result.athlete.last_name}"
        event_table_row.add_element(
            TableData(internal=f"{athlete_name}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.result.result_str}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.wind}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{record_result.heat}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{class_formatter(result.athlete.graduation_year)[0]}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{display_date(record_result.meet_date)}").add_class('event-table-data'))
        event_table.add_element(event_table_row)

        event_div.add_element(event_table)
        events_div.add_element(event_div)

    page_content_event.add_element(events_div)
    page_content_event.attributes['hidden'] = None
    display_different_content.add_element(page_content_event)


    # Meets
    display_form.add_element(
        Button(internal='Meets', type='button', onclick="teamDisplay('Meets')"
        ).add_class('button-item-meets').add_class('team-display-button').add_class('button-deactivated'))
    page_content_meet = Div().add_class('display-item-deactivated').add_class('page-content-meets')
    page_content_meet.add_element(Header(level=1, internal=f"Meets"))
    meet_dict = {}
    for result in results:
        if result.meet not in meet_dict:
            meet_dict[result.meet] = {}
        if result.event not in meet_dict[result.meet]:
            meet_dict[result.meet][result.event] = []
        for athlete in athletes:
            if athlete.uid == result.athlete_uid:
                result.athlete = athlete
                break
        meet_dict[result.meet][result.event].append(result)
    meets_div = Div()
    column_names = ['Place', 'Athlete', 'Result', 'Wind (m/s)', 'Heat', 'Class', 'Date']
    for index, (meet, events_results) in enumerate(meet_dict.items()):
        if index % 2:
            meet_div = Div().add_class('odd-content-format')
        else:
            meet_div = Div().add_class('even-content-format')
        event_results.sort(key=lambda x: x.place)
        meet_div.add_element(Header(level=1, internal=meet))
        for event, event_results in events_results.items():
            record_result = event_results[0]
            for result in event_results:
                if result.result > record_result.result:
                    record_result = result

            event_div = Div().add_class('event-div')
            if 'Boys' in event:
                event_div.add_class('mens-format')
            elif 'Girls' in event:
                event_div.add_class('womens-format')
            else:
                raise ValueError(f"Event {event} is not configed")
            event_div.add_element(Header(level=2, internal=event))
            event_table = Table().add_class('event-table')
            event_table.add_element(TableRow(
                internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
            ))

            for index, result in enumerate(event_results):
                if index % 2:
                    event_table_row = TableRow().add_class('odd-row')
                else:
                    event_table_row = TableRow().add_class('even-row')
                event_table_row.add_element(
                    TableData(internal=f"{result.place}").add_class('event-table-data'))
                # event_table_row.add_element(
                #     TableData(internal=f"{result.meet}").add_class('event-table-data'))
                athlete_name = f"{result.athlete.first_name} {result.athlete.last_name}"
                event_table_row.add_element(
                    TableData(internal=f"{athlete_name}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.result.result_str}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.wind}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.heat}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{class_formatter(result.athlete.graduation_year)[0]}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{display_date(result.meet_date)}").add_class('event-table-data'))
                event_table.add_element(event_table_row)

            # Final rows
            event_table_row = TableRow().add_class('record-row')
            event_table_row.add_element(
                TableData(internal=f"Current Best").add_class('event-table-data'))
            for _ in column_names[1:]:
                event_table_row.add_element(
                    TableData(internal=f" ").add_class('event-table-data'))
            event_table.add_element(event_table_row)

            event_table_row = TableRow().add_class('record-row')
            event_table_row.add_element(
                TableData(internal=f"{record_result.place}").add_class('event-table-data'))
            # event_table_row.add_element(
            #     TableData(internal=f"{record_result.meet}").add_class('event-table-data'))
            athlete_name = f"{record_result.athlete.first_name} {record_result.athlete.last_name}"
            event_table_row.add_element(
                TableData(internal=f"{athlete_name}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{record_result.result.result_str}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{record_result.wind}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{record_result.heat}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{class_formatter(result.athlete.graduation_year)[0]}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{display_date(record_result.meet_date)}").add_class('event-table-data'))
            event_table.add_element(event_table_row)

            event_div.add_element(event_table)
            meet_div.add_element(event_div)
        meets_div.add_element(meet_div)

    page_content_meet.add_element(meets_div)
    page_content_meet.attributes['hidden'] = None
    display_different_content.add_element(page_content_meet)


    # Athletes - Events
    display_form.add_element(
        Button(internal='Athlete Events', type='button', onclick="teamDisplay('Athlete-events')"
        ).add_class('button-item-athlete-events').add_class('team-display-button').add_class('button-deactivated'))
    page_content_athlete = Div().add_class('display-item-deactivated').add_class('page-content-athlete-events')
    page_content_athlete.add_element(Header(level=1, internal=f"Athletes"))
    athlete_dict = {}
    for result in results:
        for athlete in athletes:
            if athlete.uid == result.athlete_uid:
                result.athlete = athlete
                break
        athlete_key = f"{result.athlete.last_name} :: {result.athlete.first_name}"
        if athlete_key not in athlete_dict:
            athlete_dict[athlete_key] = {}
        if result.event not in athlete_dict[athlete_key]:
            athlete_dict[athlete_key][result.event] = []
        athlete_dict[athlete_key][result.event].append(result)
    athletes_div = Div()
    column_names = ['Place', 'Meet', 'Athlete', 'Result', 'Wind (m/s)', 'Heat', 'Class', 'Date']
    athlete_keys = list(athlete_dict.keys())
    athlete_keys.sort()
    athlete_dict = {k: athlete_dict[k] for k in athlete_keys}
    for index, (athlete_id, events_results) in enumerate(athlete_dict.items()):
        if index % 2:
            athlete_div = Div().add_class('odd-content-format')
        else:
            athlete_div = Div().add_class('even-content-format')
        athlete = events_results[list(events_results.keys())[0]][0].athlete
#         event_results.sort(key=lambda x: x.place)
        athlete_div.add_element(Header(level=1, internal=athlete.name))
        for event, event_results in events_results.items():
            record_result = event_results[0]
            for result in event_results:
                if result.result > record_result.result:
                    record_result = result

            event_div = Div().add_class('event-div')
            if 'Boys' in event:
                event_div.add_class('mens-format')
            elif 'Girls' in event:
                event_div.add_class('womens-format')
            else:
                raise ValueError(f"Event {event} is not configed")
            event_div.add_element(Header(level=4, internal=event))
            event_table = Table().add_class('event-table')
            event_table.add_element(TableRow(
                internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
            ))

            for index, result in enumerate(event_results):
                if index % 2:
                    event_table_row = TableRow().add_class('odd-row')
                else:
                    event_table_row = TableRow().add_class('even-row')
                event_table_row.add_element(
                    TableData(internal=f"{result.place}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.meet}").add_class('event-table-data'))
                athlete_name = f"{result.athlete.first_name} {result.athlete.last_name}"
                event_table_row.add_element(
                    TableData(internal=f"{athlete_name}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.result.result_str}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.wind}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.heat}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{class_formatter(result.athlete.graduation_year)[0]}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{display_date(result.meet_date)}").add_class('event-table-data'))
                event_table.add_element(event_table_row)

            # Final rows
            event_table_row = TableRow().add_class('record-row')
            event_table_row.add_element(
                TableData(internal=f"Current Best").add_class('event-table-data'))
            for _ in column_names[1:]:
                event_table_row.add_element(
                    TableData(internal=f" ").add_class('event-table-data'))
            event_table.add_element(event_table_row)

            event_table_row = TableRow().add_class('record-row')
            event_table_row.add_element(
                TableData(internal=f"{record_result.place}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{record_result.meet}").add_class('event-table-data'))
            athlete_name = f"{record_result.athlete.first_name} {record_result.athlete.last_name}"
            event_table_row.add_element(
                TableData(internal=f"{athlete_name}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{record_result.result.result_str}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{record_result.wind}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{record_result.heat}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{class_formatter(result.athlete.graduation_year)[0]}").add_class('event-table-data'))
            event_table_row.add_element(
                TableData(internal=f"{display_date(record_result.meet_date)}").add_class('event-table-data'))
            event_table.add_element(event_table_row)

            event_div.add_element(event_table)
            athlete_div.add_element(event_div)
        athletes_div.add_element(athlete_div)

    page_content_athlete.add_element(athletes_div)
    page_content_athlete.attributes['hidden'] = None
    display_different_content.add_element(page_content_athlete)


    # Athletes - Meets
    display_form.add_element(
        Button(internal='Athlete Meets', type='button', onclick="teamDisplay('Athlete-meets')"
        ).add_class('button-item-athlete-meets').add_class('team-display-button').add_class('button-deactivated'))
    page_content_athlete = Div().add_class('display-item-deactivated').add_class('page-content-athlete-meets')
    page_content_athlete.add_element(Header(level=1, internal=f"Athletes"))
    athlete_dict = {}
    for result in results:
        for athlete in athletes:
            if athlete.uid == result.athlete_uid:
                result.athlete = athlete
                break
        athlete_key = f"{result.athlete.last_name} :: {result.athlete.first_name}"
        meet = result.meet
        if athlete_key not in athlete_dict:
            athlete_dict[athlete_key] = {}
        if meet not in athlete_dict[athlete_key]:
            athlete_dict[athlete_key][meet] = []
        athlete_dict[athlete_key][meet].append(result)
    athletes_div = Div()
    column_names = ['Place', 'Event', 'Result', 'Wind (m/s)', 'Heat', 'Class', 'Date']
    athlete_keys = list(athlete_dict.keys())
    athlete_keys.sort()
    athlete_dict = {k: athlete_dict[k] for k in athlete_keys}
    for index, (athlete_id, events_results) in enumerate(athlete_dict.items()):
        if index % 2:
            athlete_div = Div().add_class('odd-content-format')
        else:
            athlete_div = Div().add_class('even-content-format')
        athlete = events_results[list(events_results.keys())[0]][0].athlete
#         event_results.sort(key=lambda x: x.place)
        athlete_div.add_element(Header(level=1, internal=athlete.name))
        for meet, event_results in events_results.items():
            # record_result = event_results[0]
            # for result in event_results:
            #     if result.result > record_result.result:
            #         record_result = result

            event_div = Div().add_class('event-div')
            event_div.add_element(Header(level=4, internal=meet))
            event_table = Table().add_class('event-table')
            event_table.add_element(TableRow(
                internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
            ))

            for index, result in enumerate(event_results):
                if index % 2:
                    event_table_row = TableRow().add_class('odd-row')
                else:
                    event_table_row = TableRow().add_class('even-row')
                event_table_row.add_element(
                    TableData(internal=f"{result.place}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.event}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.result.result_str}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.wind}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{result.heat}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{class_formatter(result.athlete.graduation_year)[0]}").add_class('event-table-data'))
                event_table_row.add_element(
                    TableData(internal=f"{display_date(result.meet_date)}").add_class('event-table-data'))
                event_table.add_element(event_table_row)

            event_div.add_element(event_table)
            athlete_div.add_element(event_div)
        athletes_div.add_element(athlete_div)

    page_content_athlete.add_element(athletes_div)
    page_content_athlete.attributes['hidden'] = None
    display_different_content.add_element(page_content_athlete)


    page_content.add_element(display_form)
    page_content.add_element(display_different_content)
    body_content = BodyContent(body_content=[page_content])

    # Styles
    document_styles = [
        StyleTag(name='.team-display-button', internal=f"""
            margin: 20px;
            padding: 15px;
            font-size: 140%;
            font-weight: bold;
            text-decoration: underline;
        """),
        StyleTag(name='.team-season-selector', internal=f"""
            margin: 20px;
            padding: 15px;
            font-size: 140%;
            font-weight: bold;
            text-decoration: underline;
        """),
        StyleTag(name='.link-workaround-div', internal=f"""
            margin: 20px 0px;
            padding: 0px;
            display: inline-block;
        """),
        StyleTag(name='.event-div', internal=f"""
            margin: 20px;
            padding: 20px;
        """),
        # StyleTag(name='.button-activated', internal="""
        #     background-color: green;
        # """),
        # StyleTag(name='.button-deactivated', internal="""
        #     background-color: #efefef;
        # """),
        # StyleTag(name='.button-emulator-format', internal="""
        #     border: 2px solid black;
        #     color: black;
        # """),
        StyleTag(name='.team-info-tag', internal="""
            margin: 20px 50px;
            padding: 0;
        """),
        # StyleTag(name='.odd-content-format', internal="""
        #     background-color: #efc9ff;
        #     padding: 30px;
        #     margin: 20px;
        # """),
        # StyleTag(name='.even-content-format', internal="""
        #     background-color: #c9ffb6;
        #     padding: 20px;
        #     margin: 20px;
        # """),
    ]

    # JS Files
    js_files = [
        os.path.join('team', 'teamDisplay.js'),
    ]
    for fl in js_files:
        with open(os.path.join('html', fl), 'r') as jf:
            js_lines = jf.readlines()
            js_lines[-1] += '\n'  # In case there is not a newline at the end of the file
            page_content.add_element(
                Script(internal=[l[:-1] for l in js_lines])
            )
    body_content = BodyContent(body_content=[page_content])

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
