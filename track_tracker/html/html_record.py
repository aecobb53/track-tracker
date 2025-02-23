import os

from datetime import datetime, timezone
from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent

from .base_page import project_base_page


async def filter_records_html_page(event_details):
    page_content = Div().add_class('page-content')
    page_content.add_element(Header(level=1, internal='Team Page'))

    page_content.add_element(Paragraph(internal='''
    This page compares every record to see what the current best times or distances are. As a result it 
    can take a bit to get results back so please be patient.
    '''))

    # athlete_name = f"{athlete.first_name} {athlete.last_name}"
    # page_content.add_element(Header(level=1, internal=f"{athlete_name}"))
    # page_content.add_element(Header(level=2, internal=f"{athlete.team} - {athlete.gender}"))
    # page_content.add_element(Header(level=2, internal=f"Graduation Year: {athlete.graduation_year}"))

    # page_content.add_element(Header(level=1, internal=f"Events"))

    events_div = Div()
    table_row_background_colors = ('#35363b', '#2c2d2e')
    for event, mark in event_details.items():
        column_names = ['Place', 'Meet', 'Athlete', 'Team', 'Mark', 'Wind', 'Heat', 'Graduation', 'Date']
        event_div = Div().add_class('event-div')
        event_div.add_element(Header(level=3, internal=event))
        event_table = Table().add_class('event-table')
        event_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('event-table-header') for col in column_names]
        ).add_style({'background-color': table_row_background_colors[1]})
        )

        event_table_row = TableRow().add_style({'background-color': table_row_background_colors[0]})
        event_table_row.add_element(
            TableData(internal=f"{mark.place}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{mark.meet}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{mark.athlete.name}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{mark.athlete.team}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{mark.mark.mark_str}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{mark.wind}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{mark.heat}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{mark.athlete.graduation_year}").add_class('event-table-data'))
        event_table_row.add_element(
            TableData(internal=f"{datetime.strftime(mark.meet_date, '%Y-%m-%d')}").add_class('event-table-data'))
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
