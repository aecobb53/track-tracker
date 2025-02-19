import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .base_page import project_base_page


service_url = os.environ.get('SERVICE_URL')


def unimplemented_page():
    base_doc = project_base_page()

    unimplemented_div = Div(id='unimplemented-div').add_style({'margin': '50px'})
    unimplemented_div.add_element(Header(level=1, internal=f"This page has not been implemented yet.").add_style({'margin': '20px'}))
    base_doc.body_content.body_content.append(unimplemented_div)
    return base_doc.return_document
