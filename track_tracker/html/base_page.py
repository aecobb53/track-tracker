import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent

service_url = os.environ.get('SERVICE_URL')


def project_base_page():
    # Sidebar bar
    # sidebar_content = Div(id='sidebar-content')
    # sidebar_item_corner_style = {
    #     'background-color': '#393B41',
    #     'margin': '5px',
    #     'padding': '10px',
    #     'border': '2px solid black',
    #     'border-radius': '15px',
    #     '-moz-border-radius': '15px',
    # }
    # link_style = {'color': '#949ba4'}
    # sidebar_content.add_element(
    #     Div(
    #         Link(internal='Marks ★', href=f'/html/mark').add_style(link_style)
    #     ).add_style(sidebar_item_corner_style))
    # sidebar_content.add_element(
    #     Div(
    #         Link(internal='Athletes', href=f'/html/athlete').add_style(link_style)
    #     ).add_style(sidebar_item_corner_style))
    # sidebar_content.add_element(
    #     Div(
    #         Link(internal='Teams', href=f'/html/team').add_style(link_style)
    #     ).add_style(sidebar_item_corner_style))
    # sidebar_content.add_element(
    #     Div(
    #         Link(internal='Events', href=f'/html/event').add_style(link_style)
    #     ).add_style(sidebar_item_corner_style))
    # sidebar_content.add_element(
    #     Div(
    #         Link(internal='Records', href=f'/html/recored').add_style(link_style)
    #     ).add_style(sidebar_item_corner_style))

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

    primary_pages_div = Div(Header(level=1, internal='Primary Pages').add_class('page-group-header'))
    extra_pages_div = Div(Header(level=1, internal='Extra Pages').add_class('page-group-header'))

    # Marks
    marks_div = Div()
    marks_div.add_element(
        Link(internal=Header(level=2, internal='Marks ★'), href=f'/html/marks').add_class('page-link')
        ).add_class('page-div')
    primary_pages_div.add_element(marks_div)

    # Athletes
    athletes_div = Div()
    athletes_div.add_element(
        Link(internal=Header(level=2, internal='Athletes'), href=f'/html/athletes').add_class('page-link')
        ).add_class('page-div')
    primary_pages_div.add_element(athletes_div)

    # Teams
    teams_div = Div()
    teams_div.add_element(
        Link(internal=Header(level=2, internal='Teams'), href=f'/html/teams').add_class('page-link')
        ).add_class('page-div')
    primary_pages_div.add_element(teams_div)

    # Records
    records_div = Div()
    records_div.add_element(
        Link(internal=Header(level=2, internal='Records'), href=f'/html/records').add_class('page-link')
        ).add_class('page-div')
    primary_pages_div.add_element(records_div)

    # Schedule
    schedule_div = Div()
    schedule_div.add_element(
        Link(internal=Header(level=2, internal='Schedule'), href=f'/html/schedule').add_class('page-link')
        ).add_class('page-div')
    primary_pages_div.add_element(schedule_div)

    # Resources
    resources_div = Div()
    resources_div.add_element(
        Link(internal=Header(level=2, internal='Resources'), href=f'/html/resources').add_class('page-link')
        ).add_class('page-div')
    primary_pages_div.add_element(resources_div)

    # Video
    video_div = Div()
    video_div.add_element(
        Link(internal=Header(level=2, internal='Video'), href=f'/html/video').add_class('page-link')
        ).add_class('page-div')
    extra_pages_div.add_element(video_div)

    # Data Request
    request_div = Div()
    request_div.add_element(
        Link(internal=Header(level=2, internal='Request Data'), href=f'/html/request').add_class('page-link')
        ).add_class('page-div')
    extra_pages_div.add_element(request_div)
    # About
    about_div = Div()
    about_div.add_element(
        Link(internal=Header(level=2, internal='About'), href=f'/html/about').add_class('page-link')
        ).add_class('page-div')
    extra_pages_div.add_element(about_div)

    # Roadmap
    roadmap_div = Div()
    roadmap_div.add_element(
        Link(internal=Header(level=2, internal='Roadmap'), href=f'/html/roadmap').add_class('page-link')
        ).add_class('page-div')
    extra_pages_div.add_element(roadmap_div)

    # Health
    health_div = Div()
    health_div.add_element(
        Link(internal=Header(level=2, internal='Service Health'), href=f'/html/health').add_class('page-link')
        ).add_class('page-div')
    extra_pages_div.add_element(health_div)

    # Contact
    contact_div = Div()
    contact_div.add_element(
        Link(internal=Header(level=2, internal='Contact Me'), href=f'/html/contact').add_class('page-link')
        ).add_class('page-div')
    extra_pages_div.add_element(contact_div)

    page_content.add_element(primary_pages_div)
    page_content.add_element(extra_pages_div)

    document_style = base_doc.document_style
    document_style.extend([
        StyleTag(name='.page-group-header', internal="""
            margin: 10px;
        """),
        StyleTag(name='.page-link', internal="""
            color: #949ba4;
            margin: 0;
            padding: 0;
        """),
        StyleTag(name='.page-link h2', internal="""
            margin: 0;
            padding: 15px;
        """),
        StyleTag(name='.page-div', internal="""
            background-color: #393B41;
            margin: 5px 30px;
            padding: 0;
            border: 3px solid black;
            border-radius: 15px;
            -moz-border-radius: 15px;
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
