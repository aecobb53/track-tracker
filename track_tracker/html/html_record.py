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
from .common import display_date


async def filter_records_html_page(event_details):
    base_doc = await project_base_page()

    page_content = Div().add_class('page-content')
    page_content.add_element(Header(level=1, internal='Team Page'))

    # page_content.add_element(Paragraph(internal='''
    # This page compares every record to see what the current best times or distances are. As a result it 
    # can take a bit to get results back so please be patient.
    # '''))

    # athlete_name = f"{athlete.first_name} {athlete.last_name}"
    # page_content.add_element(Header(level=1, internal=f"{athlete_name}"))
    # page_content.add_element(Header(level=2, internal=f"{athlete.team} - {athlete.gender}"))
    # page_content.add_element(Header(level=2, internal=f"Graduation Year: {athlete.graduation_year}"))

    # page_content.add_element(Header(level=1, internal=f"Events"))

    events_div = Div()
    for event, result in event_details.items():
        column_names = ['Place', 'Meet', 'Athlete', 'Team', 'Result', 'Wind (m/s)', 'Heat', 'Graduation', 'Date']
        event_div = Div().add_class('event-div')
        event_div.add_element(Header(level=3, internal=event))
        event_table = Table().add_class('event-table')
        event_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
        ))

        event_table_row = TableRow().add_class('record-row')
        event_table_row.add_element(
            TableData(internal=f"{result.place}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{result.meet}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{result.athlete.name}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{result.athlete.team}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{result.result.result_str}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{result.wind}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{result.heat}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{result.athlete.graduation_year}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{display_date(result.meet_date)}").add_class('event-table-data'))
        event_table.add_element(event_table_row)
        event_div.add_element(event_table)
        events_div.add_element(event_div)

    page_content.add_element(events_div)
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
