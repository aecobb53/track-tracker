from ast import alias
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
from .common import class_formatter
from models import Result, ResultData

def _sort_function(item):
    if item is None or item == '-':
        return 10000
    return item

async def sprint_html_page(athletes_dict):
    base_doc = await project_base_page()

    # Body
    page_content = Div().add_class('page-content')

    sprinters_div = Div().add_class('sprinters')
    sprinters_table = Table().add_class('sprinters-table')
    column_names = ['First', 'Last', 'Nickname', 'Gender', 'Class', '100M', '200M', '400M']
    sprinters_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('sprinters-table-header') for col in column_names]
        ))

    display_details_list = []
    for _, details in athletes_dict.items():
        athlete = details['athlete']
        results = details['results']
        # print('')
        # print(f"ATHLETE: {athlete}")
        # print(f"RESULTS: {results}")
        m100 = None
        m200 = None
        m400 = None
        m100_assumed = False
        m200_assumed = False
        m400_assumed = False

        for result in results:
            if '100 Meter' in result.event:
                if m100 is None:
                    m100 = result
                else:
                    if result.result > m100.result:
                        m100 = result
            elif '200 Meter' in result.event:
                if m200 is None:
                    m200 = result
                else:
                    if result.result > m200.result:
                        m200 = result
            elif '400 Meter' in result.event:
                if m400 is None:
                    m400 = result
                else:
                    if result.result > m400.result:
                        m400 = result
            else:
                # print('-not found-')
                x=1
                continue

        # print('')
        if not m200:
            m200_assumed = True
            if m100:
                m200 = m100.result.format_smaller_value * 2 + 0.2
            elif m400:
                m200 = ( m400.result.format_smaller_value - 4 ) / 2
            # else:
        if not m100 and m200:
            m100_assumed = True
            if isinstance(m200, ResultData):
                m200_val = m200.result.format_smaller_value
            else:
                m200_val = m200
            m100 = ( m200_val - 0.2 ) / 2

        if not m400 and m200:
            m400_assumed = True
            if isinstance(m200, ResultData):
                m200_val = m200.result.format_smaller_value
            else:
                m200_val = m200
            m400 = ( m200_val * 2) + 4
        if isinstance(m100, ResultData):
            m100 = m100.result.format_smaller_value
        elif m100 is None:
            m100 = None
        else:
            m100 = round(m100, 2)
        if isinstance(m200, ResultData):
            m200 = m200.result.format_smaller_value
        elif m200 is None:
            m200 = None
        else:
            m200 = round(m200, 2)
        if isinstance(m400, ResultData):
            m400 = m400.result.format_smaller_value
        elif m400 is None:
            m400 = None
        else:
            m400 = round(m400, 2)
        if not m100 and not m200 and not m400:
            # Resetting for visual purposes
            m100_assumed = False
            m200_assumed = False
            m400_assumed = False
        # print(f"RESULTS: {m100}, {m200}, {m400}")
        if athlete.graduation_year:
            graduation_year = class_formatter(athlete.graduation_year)[0]
        else:
            graduation_year = '-'

        display_details_list.append({
            'first_name': athlete.first_name,
            'last_name': athlete.last_name,
            'alias': athlete.aliases[0] if athlete.aliases else '',
            'gender': athlete.gender,
            'class': graduation_year,
            '100m': m100,
            '200m': m200,
            '400m': m400,
            '100m_assumed': m100_assumed,
            '200m_assumed': m200_assumed,
            '400m_assumed': m400_assumed,
        })

    display_details_list = sorted(display_details_list, key=lambda x: _sort_function(x['200m']))

    for index, details in enumerate(display_details_list):
        if index % 2:
            sprinters_table_row = TableRow().add_class('odd-row')
        else:
            sprinters_table_row = TableRow().add_class('even-row')

        sprinters_table_row.add_element(
            TableData(internal=details['first_name']).add_class('sprinters-table-data'))
        sprinters_table_row.add_element(
            TableData(internal=details['last_name']).add_class('sprinters-table-data'))
        sprinters_table_row.add_element(
            TableData(internal=details['alias']).add_class('sprinters-table-data'))
        sprinters_table_row.add_element(
            TableData(internal=details['gender']).add_class('sprinters-table-data'))
        sprinters_table_row.add_element(
            TableData(internal=details['class']).add_class('sprinters-table-data'))

        if details['100m_assumed']:
            sprinters_table_row.add_element(
                TableData(internal=str(details['100m']) + '*').add_class('sprinters-table-data'))
        else:
            sprinters_table_row.add_element(
                TableData(internal=details['100m']).add_class('sprinters-table-data'))

        if details['200m_assumed']:
            sprinters_table_row.add_element(
                TableData(internal=str(details['200m']) + '*').add_class('sprinters-table-data'))
        else:
            sprinters_table_row.add_element(
                TableData(internal=details['200m']).add_class('sprinters-table-data'))

        if details['400m_assumed']:
            sprinters_table_row.add_element(
                TableData(internal=str(details['400m']) + '*').add_class('sprinters-table-data'))
        else:
            sprinters_table_row.add_element(
                TableData(internal=details['400m']).add_class('sprinters-table-data'))

        
        sprinters_table.add_element(sprinters_table_row)

    sprinters_div.add_element(sprinters_table)
    page_content.add_element(sprinters_div)

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


async def hurlde_html_page(athletes_dict):
    base_doc = await project_base_page()

    # Body
    page_content = Div().add_class('page-content')

    sprinters_div = Div().add_class('sprinters')
    sprinters_table = Table().add_class('sprinters-table')
    column_names = ['First', 'Last', 'Nickname', 'Gender', 'Class', 'Takeoff']
    sprinters_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('sprinters-table-header') for col in column_names]
        ))

    display_details_list = []
    for _, details in athletes_dict.items():
        athlete = details['athlete']
        # results = details['results']
        if athlete.graduation_year:
            graduation_year = class_formatter(athlete.graduation_year)[0]
        else:
            graduation_year = '-'

        takeoff_zone = athlete.athlete_metadata.get('Takeoff', None)


        display_details_list.append({
            'first_name': athlete.first_name,
            'last_name': athlete.last_name,
            'alias': athlete.aliases[0] if athlete.aliases else '',
            'gender': athlete.gender,
            'class': graduation_year,
            'takeoff': takeoff_zone,
            })

    # display_details_list = sorted(display_details_list, key=lambda x: _sort_function(x['200m']))

    for index, details in enumerate(display_details_list):
        if index % 2:
            sprinters_table_row = TableRow().add_class('odd-row')
        else:
            sprinters_table_row = TableRow().add_class('even-row')
        sprinters_table_row.add_element(
            TableData(internal=details['first_name']).add_class('sprinters-table-data'))
        sprinters_table_row.add_element(
            TableData(internal=details['last_name']).add_class('sprinters-table-data'))
        sprinters_table_row.add_element(
            TableData(internal=details['alias']).add_class('sprinters-table-data'))
        sprinters_table_row.add_element(
            TableData(internal=details['gender']).add_class('sprinters-table-data'))
        sprinters_table_row.add_element(
            TableData(internal=details['class']).add_class('sprinters-table-data'))

        sprinters_table_row.add_element(
            TableData(internal=details['takeoff']).add_class('sprinters-table-data'))
        sprinters_table.add_element(sprinters_table_row)

    sprinters_div.add_element(sprinters_table)
    page_content.add_element(sprinters_div)

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
