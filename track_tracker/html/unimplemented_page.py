import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent


service_url = os.environ.get('SERVICE_URL')


def unimplemented_page():
    page_content = Div().add_style({'display': 'block'})

    # Welcome
    welcome_div = Div(id='welcome-div').add_style({'margin': '50px'})
    welcome_div.add_element(Header(level=1, internal=f"Welcome to the Game Process Calculator!").add_style({'margin': '20px'}))
    welcome_div.add_element(Header(level=2, internal=f"""
    This page has not been implemented yet.
    """).add_style({'margin': '20px'}))
    # page_content.add_element(welcome_div)

    home_page_div = Div(id='home-page-div')
    home_page_div.add_element(Button(
        HtmlListItem(Link(internal='Home', href=f'{service_url}'))))
    welcome_div.add_element(home_page_div)
    page_content.add_element(welcome_div)

    navigation_content = NavigationContent(webpage_name="Game Process Calculator")
    body_content = BodyContent(body_content=[page_content])
    new_formatted_doc = MyBaseDocument(
        navigation_content=navigation_content,
        body_content=body_content,
    )
    return new_formatted_doc.return_document
