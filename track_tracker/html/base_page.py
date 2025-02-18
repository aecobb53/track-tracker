import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent


service_url = os.environ.get('SERVICE_URL')


def project_base_page():
    # Sidebar bar
    sidebar_content = Div(id='sidebar-content')
    sidebar_item_corner_style = {
        'background-color': '#393B41',
        'margin': '5px',
        'padding': '10px',
        'border': '2px solid black',
        'border-radius': '15px',
        '-moz-border-radius': '15px',
    }
    sidebar_content.add_element(
        Div(
            Link(internal='Athletes', href=f'{service_url}/html/athletes').add_style({'color': '#949ba4'})
        ).add_style(sidebar_item_corner_style))
    sidebar_content.add_element(
        Div(
            Link(internal='Teams', href=f'{service_url}/html/athletes').add_style({'color': '#949ba4'})
        ).add_style(sidebar_item_corner_style))
    sidebar_content.add_element(
        Div(
            Link(internal='Events', href=f'{service_url}/html/athletes').add_style({'color': '#949ba4'})
        ).add_style(sidebar_item_corner_style))
    sidebar_content.add_element(
        Div(
            Link(internal='Records', href=f'{service_url}/html/athletes').add_style({'color': '#949ba4'})
        ).add_style(sidebar_item_corner_style))

    # Body
    page_content = Div().add_style({'display': 'block'})

    navigation_content = NavigationContent(webpage_name="Fairview Track Data")
    sidebar_content = SidebarContent(sidebar_content=[sidebar_content])
    body_content = BodyContent(body_content=[page_content])
    new_formatted_doc = MyBaseDocument(
        navigation_content=navigation_content,
        sidebar_content=sidebar_content,
        body_content=body_content,
    )
    return new_formatted_doc.return_document

def project_home_page():
    x=1
