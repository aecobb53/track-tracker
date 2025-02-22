import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .common import HOME_PAGE_LINK_CONTENT


service_url = os.environ.get('SERVICE_URL')


def project_base_page():
    # Body
    page_content = Div().add_style({'display': 'block'})

    navigation_content = NavigationContent(webpage_name="Fairview Track Data")
    # sidebar_content = SidebarContent(sidebar_content=[sidebar_content])
    body_content = BodyContent(
        body_content=[page_content])
    new_formatted_doc = MyBaseDocument(
        navigation_content=navigation_content,
        body_content=body_content,
        # sidebar_width='5%',
    )
    return new_formatted_doc
    # return new_formatted_doc.return_document

def project_home_page():
    print('')
    print('')
    print('')
    print('')
    print('IN PROJECT HOME PAGE')
    base_doc = project_base_page()

    # Body
    page_content = Div().add_style({'display': 'block'})


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


    document_style = base_doc.document_style
    document_style.extend([
        StyleTag(name='.page-group-div', internal="""
            color: #c4cedb;
            margin: 0;
            padding: 0;
            display: inline;
        """),

        StyleTag(name='.page-div', internal="""
            background-color: #393B41;
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

        StyleTag(name='.page-link', internal="""
            color: #949ba4;
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
    ])

    body_content = BodyContent(
        body_content=[page_content])

    base_doc = MyBaseDocument(
        navigation_height=base_doc.navigation_height,
        footer_height=base_doc.footer_height,
        sidebar_width=base_doc.sidebar_width,
        navigation_content=base_doc.navigation_content,
        sidebar_content=base_doc.sidebar_content,
        body_content=body_content,
        footer_content=base_doc.footer_content,
        document_style=document_style,
    )
    return base_doc.return_document
