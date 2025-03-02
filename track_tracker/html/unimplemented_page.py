import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .base_page import project_base_page, project_dev_base_page


service_url = os.environ.get('SERVICE_URL')


async def unimplemented_page():
    base_doc = await project_base_page()

    page_content = Div(id='unimplemented-div').add_style({'margin': '50px'})
    page_content.add_element(Header(level=1, internal=f"This page has not been implemented yet.").add_style({'margin': '20px'}))
    # base_doc.body_content.append(page_content)

    body_content = BodyContent(body_content=[page_content])

    base_doc.body_content = body_content
    return base_doc.return_document

async def unimplemented_dev_page():
    base_doc = await project_dev_base_page()

    page_content = Div(id='unimplemented-div').add_style({'margin': '50px'})
    page_content.add_element(Header(level=1, internal=f"This page has not been implemented yet.").add_style({'margin': '20px'}))
    # base_doc.body_content.append(page_content)

    body_content = BodyContent(body_content=[page_content])

    base_doc.body_content = body_content
    return base_doc.return_document
