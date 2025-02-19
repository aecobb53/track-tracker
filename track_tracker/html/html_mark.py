import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from .base_page import project_base_page
from .common import MARK_FILTER_PARAMS, MARK_DISPLAY_PARAMS

def filter_marks_html_page():
    page_content = Div().add_style({'display': 'block', 'color': '#949ba4'})

    # Filter Form
    filter_form_div = Div()
    filter_form_div.add_element(Header(level=1, internal='Data Filter'))
    filter_form = Form(action=f"/mark", method='get').add_class('filter-form')
    filter_groupings = {}
    for grouping in MARK_FILTER_PARAMS.keys():
        if grouping not in filter_groupings:
            filter_groupings[grouping] = []
        for details in MARK_FILTER_PARAMS[grouping].values():
            filter_groupings[grouping].append(details)
    for grouping in filter_groupings.keys():
        params = filter_groupings[grouping]
        grouping_div = Div()
        grouping_div.add_element(Header(level=3, internal=grouping))
        for param in params:
            id_base = param['display'].replace(' ', '-').lower()
            input_kwargs = {
                'type': param['datatype'],
                'id': f"{id_base}-input",
                'name': param['display'],
                'value': param['default_value'],
            }
            box = [
                Span(
                    for_=f"{id_base}-input", internal=param['display']
                ).add_class('filter-checkbox-input').add_style({'margin': '0px'}),
                Input(**input_kwargs).add_style({'margin': '0px'}),
            ]
            grouping_div.add_element(
                Label(
                    for_=f"{id_base}-input", internal=box, title=param['description']
                ).add_class('checkbox-label').add_class('filter-label'))
        filter_form.add_element(grouping_div)
    filter_form_div.add_element(filter_form)
    filter_form_div.add_element(
        Button(internal='Submit', type='button', onclick='applyFilterForm()').add_class('big-button'))
    page_content.add_element(filter_form_div)

    # Display Form
    display_form_div = Div()
    display_form_div.add_element(Header(level=1, internal='Table Columns'))
    display_form = Form(action=f"/mark", method='get').add_class('display-form')
    display_groupings = {}
    for grouping in MARK_DISPLAY_PARAMS.keys():
        if grouping not in display_groupings:
            display_groupings[grouping] = []
        for details in MARK_DISPLAY_PARAMS[grouping].values():
            display_groupings[grouping].append(details)
    for grouping in display_groupings.keys():
        print(f"GROUPING: {grouping}")
        params = display_groupings[grouping]
        grouping_div = Div()
        grouping_div.add_element(Header(level=3, internal=grouping))
        for param in params:
            id_base = param['display'].replace(' ', '-').lower()
            input_kwargs = {
                'type': 'checkbox',
                'id': f"{id_base}-input",
                'name': param['display'],
            }
            if param['html_display_filtering']['checked']:
                input_kwargs['checked'] = True
            input_tag = Input(
                    **input_kwargs
                ).add_class('display-checkbox-input').add_style({'margin': '0px'})
            for group_class in param['html_display_filtering']['grouping_classes']:
                input_tag.add_class(group_class)
            box = [
                input_tag,
                Span(internal=param['display'].title()).add_style({'margin': '0px'}),
            ]
            grouping_div.add_element(
                Label(
                    internal=box, id=f"{id_base}-label", title=param['html_display_filtering']['description'], for_=f"{id_base}-input"
                ).add_class('checkbox-label'))
        display_form.add_element(grouping_div)

    display_form.add_element(
        Button(internal='All', title='Toggle all checkboxes', type='button', onclick='toggleCheckboxesAll()').add_class('small-button'))

    display_form.add_element(
        Button(internal='Apply', type='button', onclick='applyDisplayFilters()').add_class('big-button'))
    display_form_div.add_element(display_form)
    page_content.add_element(display_form_div)


    # Table
    table_div = Div(id='table-div')
    page_content.add_element(table_div)

    # JS Files
    js_files = [
        os.path.join('mark', 'applyFilterForm.js'),
        os.path.join('mark', 'GETFilterMark.js'),
        os.path.join('mark', 'populateMarkTable.js'),
        os.path.join('mark', 'applyDisplayFilters.js'),
        os.path.join('mark', 'toggleCheckboxes.js'),
    ]
    for fl in js_files:
        with open(os.path.join('html', fl), 'r') as jf:
            # line = line.replace('SERVICE_URL', service_url)
            js_lines = jf.readlines()
            js_lines[-1] += '\n'  # In case there is not a newline at the end of the file
            page_content.add_element(
                Script(internal=[l[:-1] for l in js_lines])
            )

    # Styles

    base_doc = project_base_page()
    base_doc.body_content.body_content.append(page_content)
    return base_doc.return_document
