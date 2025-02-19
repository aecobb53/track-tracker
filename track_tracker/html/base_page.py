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
    link_style = {'color': '#949ba4'}
    sidebar_content.add_element(
        Div(
            Link(internal='Marks ★', href=f'/html/mark').add_style(link_style)
        ).add_style(sidebar_item_corner_style))
    sidebar_content.add_element(
        Div(
            Link(internal='Athletes', href=f'/html/athlete').add_style(link_style)
        ).add_style(sidebar_item_corner_style))
    sidebar_content.add_element(
        Div(
            Link(internal='Teams', href=f'/html/team').add_style(link_style)
        ).add_style(sidebar_item_corner_style))
    sidebar_content.add_element(
        Div(
            Link(internal='Events', href=f'/html/event').add_style(link_style)
        ).add_style(sidebar_item_corner_style))
    sidebar_content.add_element(
        Div(
            Link(internal='Records', href=f'/html/recored').add_style(link_style)
        ).add_style(sidebar_item_corner_style))

    # Body
    page_content = Div().add_style({'display': 'block'})

    navigation_content = NavigationContent(webpage_name="Fairview Track Data")
    sidebar_content = SidebarContent(sidebar_content=[sidebar_content])
    body_content = BodyContent(
        body_content=[page_content],
        style_details={'width': '90%', 'margin-left': '10%'})
    new_formatted_doc = MyBaseDocument(
        navigation_content=navigation_content,
        sidebar_content=sidebar_content,
        body_content=body_content,
        sidebar_width='10%',
    )
    return new_formatted_doc
    # return new_formatted_doc.return_document

def project_home_page():
    base_doc = project_base_page()
    print(f"FORMAT DOC: {base_doc}")
    print(f"navigation_height: {base_doc.navigation_height}")
    print(f"footer_height: {base_doc.footer_height}")
    print(f"sidebar_width: {base_doc.sidebar_width}")
    print(f"navigation_content: {base_doc.navigation_content}")
    print(f"sidebar_content: {base_doc.sidebar_content}")
    print(f"body_content: {base_doc.body_content}")
    print(f"footer_content: {base_doc.footer_content}")
    print(f"document_style: {base_doc.document_style}")
    return base_doc.return_document
