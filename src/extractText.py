#
# Recursively extracts the text from a Google Doc.
# Parses text into dictionaries and lists
# ======================================================================================================================
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ======================================================================================================================
# Imports
from collections import OrderedDict
# ======================================================================================================================
# Constant list of months for finding dates
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
# ======================================================================================================================
# Classes for class variables
class TextData:
    """
    """
    t_dct = OrderedDict()
    text_index = 0


class DateData:
    """
    """
    d_list = []


class SupData:
    """
    """
    s_list = []
    sup_line = False


class EmployeeTourData:
    """
    """
    et_list = []
    employee = ''
# ======================================================================================================================


def read_paragraph_element(element):
    """
    Reads ParagraphElements from Doc, adds element to data lists via build_lists function.
    :param element: a ParagraphElement from a Google Doc.
    :return the text in the given ParagraphElement.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    else:
        text = text_run.get('content')
        # put text into TextData dictionary and lists
        build_lists(text)
        # return text content for read_structural_elements recursion
        return text


def read_structural_elements(elements):
    """
    Recurses through a list of Structural Elements to read a document's text where text may be in nested elements.
    :param elements: a list of Structural Elements.
    :return
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        if 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be nested
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text


def build_lists(text):
    """
    Adds text to appropriate list
    called in read_paragraph_element function
    :param text: single line of paragraph content
    """
    # add text and index to TextData.t_dct
    TextData.t_dct[TextData.text_index] = text

    # create sup list, return true if text is sup, false if not
    # if text is not sup, check if text is a data, check if text is in tour body
    if create_sup_list(text) is False:
        # add text to DateData list if text contains a month
        create_date_list(text)
        # add text to EmployeeTourData list if text contains Employee.employee
        create_employee_tour_list(text)
    # increment TextData index (after creating sup, date, and employee tour lists bc those use the TextData.text_index)
    TextData.text_index += 1


def create_sup_list(text):
    """
    Only writes to SupData list if sup contains employee name
    :param text: single line of paragraph content
    :return boolean if text is Supervisor
    """
    sup = 'Supervisor:'
    # check line below occurrence of sup contains employee
    if SupData.sup_line:
        if EmployeeTourData.employee in text:
            SupData.s_list.append(text)
            SupData.s_list.append(TextData.text_index)
        SupData.sup_line = False
    # finds if sup is on the same line as employee name
    elif sup in text and EmployeeTourData.employee in text:
        # add only employee name to s_list
        SupData.s_list.append(text[12:])
        SupData.s_list.append(TextData.text_index)
        SupData.sup_line = False
    elif sup in text:
        # assume name of supervisor is on next line
        SupData.sup_line = True
    else:
        # text does not contain sup, return False
        return False
    # sup in text, return True
    return True


def create_date_list(text):
    """
    Adds text and index of text in TextData to DateData.d_list if text contains a date in MONTHS
    :param text: single line of paragraph content
    """
    if any(date in text for date in MONTHS):
        DateData.d_list.append(text)
        DateData.d_list.append(TextData.text_index)


def create_employee_tour_list(text):
    """
    Finds all text that contains employee and 'No' is not part of the text
    Note: Will only find occurrences of employee in tours, as supervisor employees will not be added to list
    :param text: single line of paragraph content
    """
    if EmployeeTourData.employee in text and 'No' not in text:  # TODO build list of 'No employee' days
        EmployeeTourData.et_list.append(TextData.text_index)
