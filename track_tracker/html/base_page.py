import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .common import HOME_PAGE_LINK_CONTENT
from .env import (
    SEASON_YEAR,
    BACKGROUND_COLOR,
    SECONDARY_COLOR,
    ACCENT_COLOR,
    TEXT_COLOR_1,
    TEXT_COLOR_2,
    ROW_BACKGROUND_COLOR_1,
    ROW_BACKGROUND_COLOR_2,
)

PAGE_STYLES = [
    StyleTag(name='body', internal=f"""
        margin: 0px;
        padding: 0px;
        font-family: Tahoma, sans-serif;
    """),
    StyleTag(name='.page-content', internal=f"""
        display: block;
        color: {TEXT_COLOR_1};
        margin: 10px;
    """),

]
FILTER_STYLES = [
    StyleTag(name='.filter-checkbox-input', internal=f"""
        margin: 0;
    """),
    StyleTag(name='.big-button', internal=f"""
        margin: 20px;
        padding: 5px;
        font-size: 120%;
        font-weight: bold;
        text-decoration: underline;
    """),
    StyleTag(name='.small-button', internal=f"""
        margin: 5px;
        padding: 5px;
        font-size: 100%;
        font-weight: bold;
    """),
    StyleTag(name='.submit-button', internal=f"""
        background-color: green;
    """),

    StyleTag(name='.pagination-div', internal=f"""
        display: inline-block;
        font-size: 300%;
        color: {TEXT_COLOR_1};
        margin: 10px;
        text-decoration: none;
        text-align: center;
        width: 100%;
    """),
    StyleTag(name='.pagination-div button', internal=f"""
        border-radius: 5px;
        margin: 5px;
        padding: 5px;
        text-decoration: none;
        font-size: 70%;
    """),
    StyleTag(name='.pagination-div button.active', internal=f"""
        color: {TEXT_COLOR_2};
        background-color: green;
    """),
]
TABLE_STYLES = [
        StyleTag(name='table', internal=f"""
            width: 100%;
            height: 100%;
            border: 5px solid black;
            text-align: center;
        """),
        StyleTag(name='thead', internal=f"""
            width: 100%;
            fontWeight: bold;
            padding: 5px;
            color: {TEXT_COLOR_1};
        """),
        StyleTag(name='tbody', internal=f"""
            width: 100%;
            height: 100%;
            border: 5px solid black;
            color: {TEXT_COLOR_1};
        """),
        StyleTag(name='tr', internal=f"""
            padding: 5px;
        """),
        StyleTag(name='td', internal=f"""
            padding: 5px 25px;
        """),
        StyleTag(name='td a', internal=f"""
        color: {TEXT_COLOR_1};
        """),
        StyleTag(name='.even-row', internal=f"""
            background-color: #9f9f9f;
            color: #000000;
        """),
        StyleTag(name='.odd-row', internal=f"""
            background-color: #ffb4b4;
            color: #000000;
        """),
        StyleTag(name='.record-row', internal=f"""
            background-color: #ffdda1;
            color: black;
            font-style: italic;
        """),
        StyleTag(name='.mens-format', internal=f"""
            color: #0b00ab;
        """),
        StyleTag(name='.womens-format', internal=f"""
            color: #ff6e87;
        """),
]


"""

font-style: normal|italic|oblique|initial|inherit;

old mens
07006b
new mens
0b00ab



body text
font-family: Arial, Helvetica, sans-serif;
font-family: Tahoma, sans-serif;


background #9f9f9f
text Black

background #ffb4b4
text black

Record background
ffdda1
text black


text-align: center;










efc9ff








"""


async def project_base_page():
    # Navigation
    navigation_content = NavigationContent(
        webpage_name="Fairview Track Results",
        webpage_name_link='/',
        background_color=SECONDARY_COLOR,
        text_color=TEXT_COLOR_2,
        )

    doc = MyBaseDocument(
        navigation_content=navigation_content,
    )
    return doc


async def project_home_page():
    base_doc = await project_base_page()

    # Body
    page_content = Div().add_class('home-page-content')

    for grouping, pages in HOME_PAGE_LINK_CONTENT.items():
        grouping_div = Div(Header(level=1, internal=grouping)).add_class('page-group-div')

        for page, details in pages.items():
            content = [
                Div(internal=Header(level=2, internal=page)).add_class('page-header'),
                Div(internal=Paragraph(internal=details['description'])).add_class('page-paragraph'),
            ]
            page_link = Link(internal=content, href=f"/html/{details['endpoint']}").add_class('page-link').add_class('page-div')
            grouping_div.add_element(page_link)
        page_content.add_element(grouping_div)

    body_styles = [
        StyleTag(name='.home-page-content', internal=f"""
            color: {TEXT_COLOR_1};
            margin: 10px;
            padding: 0;
        """),
        StyleTag(name='.home-page-content h1', internal=f"""
            margin: 0;
            padding: 20px 40px;
        """),
        StyleTag(name='.page-group-div', internal=f"""
            color: {TEXT_COLOR_1};
            margin: 0;
            padding: 0;
            display: inline;
        """),

        StyleTag(name='.page-div', internal=f"""
            background-color: {ACCENT_COLOR};
            margin: 20px;
            padding: 0;
            border: 3px solid black;
            border-radius: 15px;
            -moz-border-radius: 15px;
            height: 100px;
            width: 400px;
            display: inline-block;
            vertical-align: top;
        """),

        StyleTag(name='.page-link', internal=f"""
            color: {TEXT_COLOR_1};
            text-decoration: none;
        """),


        StyleTag(name='.page-header', internal="""
            margin: 10px;
            padding: 0;
            text-align: center;
        """),
        StyleTag(name='.page-paragraph', internal="""
            margin: 10px;
            padding: 0;
            text-align: center;
        """),


        StyleTag(name='.page-link h2', internal="""
            margin: 15px;
            padding: 0;
        """),
        StyleTag(name='.page-link p', internal="""
            margin: 0;
            padding: 0;
        """),
    ]

    body_content = BodyContent(body_content=[page_content])
    for style in body_styles:
        body_content.add_body_styles(style)


    base_doc.body_content = body_content

    return base_doc.return_document

async def project_about():
    base_doc = await project_base_page()

    # Body
    page_content = Div().add_class('home-page-content')
    page_content.add_element(
        Paragraph(internal="""
        This project is pretty simple in that it tracks data from Milesplit.com so that other coaches and athletes can 
        view progress or stats as the season goes on. It is also used as a full stack project for employment purposes.
        """)
    ).add_style({'font-size': '2.0em', 'margin': '30px', 'padding': '0'})

    body_content = BodyContent(body_content=[page_content])

    base_doc.body_content = body_content

    return base_doc.return_document
