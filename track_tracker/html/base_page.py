import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .common import HOME_PAGE_LINK_CONTENT


# service_url = os.environ.get('SERVICE_URL')
BACKGROUND_COLOR = '#FFFFFF'
SECONDARY_COLOR = '#bf2420'
ACCENT_COLOR = '#eaeaea'
TEXT_COLOR_1 = '#000000'
TEXT_COLOR_2 = '#FFFFFF'
ROW_BACKGROUND_COLOR_1 = 'black'
ROW_BACKGROUND_COLOR_2 = 'red'

PAGE_STYLES = [
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
        margin: 10px;
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
        margin: 4px;
        padding: 5px;
        text-decoration: none;
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
        """),
        StyleTag(name='thead', internal=f"""
            width: 100%;
            fontWeight: bold;
            padding: 5px;
        """),
        StyleTag(name='tbody', internal=f"""
            width: 100%;
            height: 100%;
            border: 5px solid black;
        """),
        StyleTag(name='tr', internal=f"""
            padding: 5px;
        """),
        StyleTag(name='td', internal=f"""
            padding: 5px 25px;
        """),
        StyleTag(name='td a', internal=f"""
        color: {TEXT_COLOR_2};
        """),
        StyleTag(name='.even-row', internal=f"""
            background-color: {ROW_BACKGROUND_COLOR_1};
            color: white;
        """),
        StyleTag(name='.odd-row', internal=f"""
            background-color: {ROW_BACKGROUND_COLOR_2};
            color: white;
        """),
        StyleTag(name='.record-row', internal=f"""
            background-color: green;
            color: white;
        """),
]



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
            page_div = Div().add_class('page-div')
            content = [
                Div(internal=Header(level=2, internal=page)).add_class('page-header'),
                Div(internal=Paragraph(internal=details['description'])).add_class('page-paragraph'),
            ]
            page_div.add_element(
                Link(internal=content, href=f"/html/{details['endpoint']}").add_class('page-link')
            )
            grouping_div.add_element(page_div)
        page_content.add_element(grouping_div)

    body_styles = [
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
            height: 175px;
            width: 500px;
            display: inline-block;
            vertical-align: top;

        """),

        StyleTag(name='.page-link', internal=f"""
            color: {TEXT_COLOR_1};
            margin: 0;
            padding: 0;
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
