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
    page_content.add_element(Header(level=1, internal='Projected Times').add_class('page-header'))

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
        m100 = None
        m200 = None
        m400 = None
        m100_assumed = False
        m200_assumed = False
        m400_assumed = False

        for result in results:
            if result.result_metadata:
                if result.result_metadata.get('split'):
                    continue
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
                x=1
                continue

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


async def points_html_page(athletes_dict, meet_name_list):
    base_doc = await project_base_page()

    """
    Each athlete should have a score for each column
    Girls team total points
    Boys team total points
    Girls relays total points
    Boys relays total points
    Top Girls scorer for each column
    Top Boys scorer for each column
    """

    # Body
    page_content = Div().add_class('page-content')
    page_content.add_element(Header(level=1, internal='Team Points').add_class('page-header'))
    # page_content.add_element(Paragraph(internal='This is the team points page. A'))

    points_div = Div().add_class('points')
    points_table = Table().add_class('points-table')
    column_names = ['First', 'Last', 'Gender', 'Class', 'Total'] + meet_name_list
    points_table.add_element(TableRow(
            internal=[TableHeader(internal=col).add_class('points-table-header') for col in column_names]
        ))

    display_details_list = []
    relay_details_list = []
    girls_meet_points = {}
    boys_meet_points = {}

    girls_meet_points = {}
    boys_meet_points = {}

    team_total_points = {
        'Girls': {k: 0 for k in meet_name_list},
        'Boys': {k: 0 for k in meet_name_list},
    }
    relay_total_points = {
        'Girls': {k: 0 for k in meet_name_list},
        'Boys': {k: 0 for k in meet_name_list},
    }
    top_scorer = {
        'Girls': {k: [] for k in meet_name_list},
        'Boys': {k: [] for k in meet_name_list},
    }
    new_total_top_scorer = {
        'Girls': [],
        'Boys': [],
    }

    print(f"team_total_points: {team_total_points}")
    print(f"relay_total_points: {relay_total_points}")
    print(f"top_scorer: {top_scorer}")

    """
    points
    {
        'Gender': {
            'Meet Name': meet-points
        }
    }

    scorer
    {
        'Gender': {
            'Meet Name': [
                points,  # This is the max points
                [
                    'Athlete Name'  # list of athletes that meet this value
                ]
            ]
        }
    }
    """

    # print('')
    # print(f"ATHLETE [0]: {athletes_dict[list(athletes_dict.keys())[0]]['athlete']}")

    top_scorers = {m: {'Girls': [], 'Boys': []} for m in meet_name_list}
    for _, details in athletes_dict.items():
        # print(details.keys())
        athlete = details['athlete']
        if 'Relay' in athlete.name:
            continue
        # print(f"ATHLETE: {athlete}")
        # results = details['results']
        if athlete.graduation_year:
            graduation_year = class_formatter(athlete.graduation_year)[0]
        else:
            graduation_year = '-'

        athlete_points_dict = {k: 0 for k in meet_name_list}

        points_dict = {k: 0 for k in meet_name_list}
        # print(points_dict)
        description_dict = {k: [] for k in meet_name_list}
        for result in details['results']:
            # Meet points
            # if result.meet not in points_dict:
            #     # This meet is being skipped for points
            #     continue
            points_dict[result.meet] += result.points
            description_dict[result.meet].append((result.event, result.points))

            # if 'Relay' in result.event:
            #     print(f"RESULT: {result}")
            #     print(type(result))

            # print(result)
            # print(team_total_points[athlete.gender][result.meet])
            athlete_points_dict[result.meet] += result.points
            if result.points:
                team_total_points[athlete.gender][result.meet] += result.points
                # print(top_scorer[athlete.gender][result.meet])
                # if len(top_scorer[athlete.gender][result.meet]) == 0:
                #     # There are no athletes tracked so this will be the first one
                #     top_scorer[athlete.gender][result.meet] = [result.points, [athlete.name]]
                # if len(top_scorer[athlete.gender][result.meet]) == 2:
                #     print(top_scorer[athlete.gender][result.meet])
                #     if top_scorer[athlete.gender][result.meet][0] < result.points
                # else:
                #     print('ELSE')

            # team_total_points
            # relay_total_points
            # top_scorer

            # Relays
            if 'Relay' not in result.event:
                if athlete.gender == 'Girls':
                    if result.meet not in girls_meet_points:
                        girls_meet_points[result.meet] = 0
                    girls_meet_points[result.meet] += result.points
                elif athlete.gender == 'Boys':
                    if result.meet not in boys_meet_points:
                        boys_meet_points[result.meet] = 0
                    boys_meet_points[result.meet] += result.points
        athlete_total_points = sum(athlete_points_dict.values())
        # print(athlete_total_points, athlete_points_dict)

        # Total Top Scorer
        # print(new_total_top_scorer[athlete.gender])
        # if athlete_total_points
        if len(new_total_top_scorer[athlete.gender]) == 0:
            # print('INITIAL CONDITION SETUP')
            new_total_top_scorer[athlete.gender] = [athlete_total_points, [athlete.name]]
        else:
            if new_total_top_scorer[athlete.gender][0] < athlete_total_points:
                new_total_top_scorer[athlete.gender] = [athlete_total_points, [athlete.name]]
            elif new_total_top_scorer[athlete.gender][0] == athlete_total_points:
                new_total_top_scorer[athlete.gender][1].append(athlete.name)

        for meet_name in meet_name_list:
            meet_points = athlete_points_dict[meet_name]
            if not meet_points:
                continue
            # print(top_scorer[athlete.gender][meet_name])
            if len(top_scorer[athlete.gender][meet_name]) == 0:
                # Its the first result to be added
                top_scorer[athlete.gender][meet_name] = [meet_points, [athlete.name]]
            elif len(top_scorer[athlete.gender][meet_name]) == 2:
                if top_scorer[athlete.gender][meet_name][0] < meet_points:
                    top_scorer[athlete.gender][meet_name] = [meet_points, [athlete.name]]
                elif top_scorer[athlete.gender][meet_name][0] == meet_points:
                    top_scorer[athlete.gender][meet_name][1].append(athlete.name)

        total_points = sum(points_dict.values())

        if 'Relay' in athlete.first_name or 'Relay' in athlete.last_name:
            relay_details_list.append({
                'first_name': athlete.first_name,
                'last_name': athlete.last_name,
                'gender': athlete.gender,
                'class': graduation_year,
                'total_points': total_points,
                'points_dict': points_dict,
                'point_description_dict': description_dict,
                })
        else:
            display_details_list.append({
                'first_name': athlete.first_name,
                'last_name': athlete.last_name,
                'gender': athlete.gender,
                'class': graduation_year,
                'total_points': total_points,
                'points_dict': points_dict,
                'point_description_dict': description_dict,
                })

    print('')
    print('')
    print(f"MEET NAME LIST: {meet_name_list}")
    print('')
    print('')
    print(f"team_total_points: {team_total_points}")
    print(f"relay_total_points: {relay_total_points}")
    print(f"top_scorer: {top_scorer}")

    for index, details in enumerate(display_details_list):
        if index % 2:
            points_table_row = TableRow().add_class('odd-row')
        else:
            points_table_row = TableRow().add_class('even-row')
        points_table_row.add_element(
            TableData(internal=details['first_name']).add_class('points-table-data'))
        points_table_row.add_element(
            TableData(internal=details['last_name']).add_class('points-table-data'))
        points_table_row.add_element(
            TableData(internal=details['gender']).add_class('points-table-data'))
        points_table_row.add_element(
            TableData(internal=details['class']).add_class('points-table-data'))

        points_table_row.add_element(
            TableData(internal=details['total_points']).add_class('points-table-data'))

        for meet_name, points in details['points_dict'].items():
            description = details['point_description_dict'][meet_name]
            description = ', '.join([f"{k}: {v}" for k, v in details['point_description_dict'][meet_name]])
            if not points:
                points = ''
            points_table_row.add_element(
                TableData(internal=points, title=description).add_class('points-table-data'))

        points_table.add_element(points_table_row)

    # Top Scorers
    for details in display_details_list:
        athlete_name = f"{details['first_name']} {details['last_name']}"
        for meet, points in details['points_dict'].items():
            if not top_scorers[meet].get(details['gender']):
                top_scorers[meet][details['gender']] = [(athlete_name, points)]
            else:
                # print(f"{athlete_name} {points} {top_scorers[meet][details['gender']]}")
                if points == top_scorers[meet][details['gender']][0][1]:
                    top_scorers[meet][details['gender']].append((athlete_name, points))
                elif points > top_scorers[meet][details['gender']][0][1]:
                    top_scorers[meet][details['gender']] = [(athlete_name, points)]

    # Relay management
    relay_details_list = sorted(relay_details_list, key=lambda x: x['gender'], reverse=True)
    for index, details in enumerate(relay_details_list):
        for meet, points in details['points_dict'].items():
            if details['gender'] == 'Girls':
                girls_meet_points[meet] += points
            if details['gender'] == 'Boys':
                boys_meet_points[meet] += points

    # Final Rows
    points_table_row = TableRow().add_class('record-row')
    for _ in column_names:
        points_table_row.add_element(
        TableData(internal=f" ").add_class('event-table-data'))
    points_table.add_element(points_table_row)

    # # total best scorers
    # total_top_scorer = {'Girls': [], 'Boys': []}
    # for athlete in display_details_list:
    #     athlete_name = f"{athlete['first_name']} {athlete['last_name']}"
    #     total_points = athlete['total_points']
    #     if not total_top_scorer.get(athlete['gender']):
    #         total_top_scorer[athlete['gender']] = [(athlete_name, total_points)]
    #     else:
    #         if total_points == total_top_scorer[athlete['gender']][0][1]:
    #             total_top_scorer[athlete['gender']].append((athlete_name, total_points))
    #         elif total_points > total_top_scorer[athlete['gender']][0][1]:
    #             total_top_scorer[athlete['gender']] = [(athlete_name, total_points)]

    # # Girls
    # points_table_row = TableRow().add_class('record-row')
    # points_table_row.add_element(
    #     TableData(internal='Girls Team').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal=' ').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal='Girls').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal=' ').add_class('points-table-data'))

    # points_table_row.add_element(
    #     TableData(internal=sum([i for i in girls_meet_points.values()])).add_class('points-table-data'))

    # for meet_name, points in girls_meet_points.items():
    #     points_table_row.add_element(
    #         TableData(internal=points).add_class('points-table-data'))
    # points_table.add_element(points_table_row)

    # # Boys
    # points_table_row = TableRow().add_class('record-row')
    # points_table_row.add_element(
    #     TableData(internal='Boys Team').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal=' ').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal='Boys').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal=' ').add_class('points-table-data'))

    # points_table_row.add_element(
    #     TableData(internal=sum([i for i in boys_meet_points.values()])).add_class('points-table-data'))

    # for meet_name, points in boys_meet_points.items():
    #     points_table_row.add_element(
    #         TableData(internal=points).add_class('points-table-data'))
    # points_table.add_element(points_table_row)

    # # Relays
    # for index, details in enumerate(relay_details_list):
    #     points_table_row = TableRow().add_class('record-row')
    #     points_table_row.add_element(
    #         TableData(internal=f"{details['gender']} Relays").add_class('points-table-data'))
    #     points_table_row.add_element(
    #         TableData(internal=' ').add_class('points-table-data'))
    #     points_table_row.add_element(
    #         TableData(internal=details['gender']).add_class('points-table-data'))
    #     points_table_row.add_element(
    #         TableData(internal=' ').add_class('points-table-data'))

    #     points_table_row.add_element(
    #         TableData(internal=details['total_points']).add_class('points-table-data'))

    #     for meet_name, points in details['points_dict'].items():
    #         points_table_row.add_element(
    #             TableData(internal=points).add_class('points-table-data'))

    #     points_table.add_element(points_table_row)

    # # Top Scorers
    # # Girls
    # points_table_row = TableRow().add_class('record-row')
    # points_table_row.add_element(
    #     TableData(internal=f"Girls Top Scorer").add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal=' ').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal='Girls').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal=' ').add_class('points-table-data'))

    # # Top top scorer
    # girl_total_top_scorer = total_top_scorer['Girls'][0]
    # points_table_row.add_element(
    #     TableData(internal=f"{girl_total_top_scorer[0]} ({girl_total_top_scorer[1]})").add_class('points-table-data'))

    # for meet_name in top_scorers.keys():
    #     if len(top_scorers[meet_name]['Girls']) > 1:
    #         girl_top_scorer = (' / '.join([ts[0] for ts in top_scorers[meet_name]['Girls']]), top_scorers[meet_name]['Girls'][0][1])
    #     else:
    #         girl_top_scorer = top_scorers[meet_name]['Girls'][0]
    #     points_table_row.add_element(
    #         TableData(internal=f"{girl_top_scorer[0]} ({girl_top_scorer[1]})").add_class('points-table-data'))
    #     if girl_top_scorer[1] == 0:
    #         girl_top_scorer = ('-', 0)
    # points_table.add_element(points_table_row)

    # # Boys
    # points_table_row = TableRow().add_class('record-row')
    # points_table_row.add_element(
    #     TableData(internal=f"Boys Top Scorer").add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal=' ').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal='Boys').add_class('points-table-data'))
    # points_table_row.add_element(
    #     TableData(internal=' ').add_class('points-table-data'))

    # # Top top scorer
    # girl_total_top_scorer = total_top_scorer['Boys'][0]
    # points_table_row.add_element(
    #     TableData(internal=f"{girl_total_top_scorer[0]} ({girl_total_top_scorer[1]})").add_class('points-table-data'))

    # for meet_name in top_scorers.keys():
    #     if len(top_scorers[meet_name]['Boys']) > 1:
    #         boy_top_scorer = (' / '.join([ts[0] for ts in top_scorers[meet_name]['Boys']]), top_scorers[meet_name]['Boys'][0][1])
    #     else:
    #         boy_top_scorer = top_scorers[meet_name]['Boys'][0]
    #     if boy_top_scorer[1] == 0:
    #         boy_top_scorer = ('-', 0)
    #     points_table_row.add_element(
    #         TableData(internal=f"{boy_top_scorer[0]} ({boy_top_scorer[1]})").add_class('points-table-data'))
    # points_table.add_element(points_table_row)



    # new rows
    # Total points from genders
    # Girls Team Sum of Points
    points_table_row = TableRow().add_class('record-row')
    points_table_row.add_element(
        TableData(internal='Girls Team').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal=' ').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal='Girls').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal=' ').add_class('points-table-data'))

    points_table_row.add_element(
        TableData(internal=sum([i for i in team_total_points['Girls'].values()])).add_class('points-table-data'))

    for meet_name, points in team_total_points['Girls'].items():
        points_table_row.add_element(
            TableData(internal=points).add_class('points-table-data'))
    points_table.add_element(points_table_row)

    # Boys Team Sum of Points
    points_table_row = TableRow().add_class('record-row')
    points_table_row.add_element(
        TableData(internal='Boys Team').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal=' ').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal='Boys').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal=' ').add_class('points-table-data'))

    points_table_row.add_element(
        TableData(internal=sum([i for i in team_total_points['Boys'].values()])).add_class('points-table-data'))

    for meet_name, points in team_total_points['Boys'].items():
        points_table_row.add_element(
            TableData(internal=points).add_class('points-table-data'))
    points_table.add_element(points_table_row)

    # Top Scorer
    # Girls Team top scorers for each meet
    points_table_row = TableRow().add_class('record-row')
    points_table_row.add_element(
        TableData(internal=f"Girls Top Scorer").add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal=' ').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal='Girls').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal=' ').add_class('points-table-data'))

    string = f"{' / '.join(new_total_top_scorer['Girls'][1])} ({new_total_top_scorer['Girls'][0]})"
    points_table_row.add_element(
        TableData(internal=string).add_class('points-table-data'))

    for meet_name, details in top_scorer['Girls'].items():
        if not details:
            # There are no details to add
            points_table_row.add_element(
                TableData(internal=' ').add_class('points-table-data'))
        else:
            string = f"{' / '.join(details[1])} ({details[0]})"
            points_table_row.add_element(
                TableData(internal=string).add_class('points-table-data'))
    points_table.add_element(points_table_row)

    # Boys Team top scorers for each meet
    points_table_row = TableRow().add_class('record-row')
    points_table_row.add_element(
        TableData(internal=f"Boys Top Scorer").add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal=' ').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal='Boys').add_class('points-table-data'))
    points_table_row.add_element(
        TableData(internal=' ').add_class('points-table-data'))

    string = f"{' / '.join(new_total_top_scorer['Boys'][1])} ({new_total_top_scorer['Boys'][0]})"
    points_table_row.add_element(
        TableData(internal=string).add_class('points-table-data'))

    for meet_name, details in top_scorer['Boys'].items():
        if not details:
            # There are no details to add
            points_table_row.add_element(
                TableData(internal='- (0)').add_class('points-table-data'))
        else:
            string = f"{' / '.join(details[1])} ({details[0]})"
            points_table_row.add_element(
                TableData(internal=string).add_class('points-table-data'))
    points_table.add_element(points_table_row)





    points_div.add_element(points_table)
    page_content.add_element(points_div)

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
