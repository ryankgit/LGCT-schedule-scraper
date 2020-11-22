#
# Run main to extract text from Doc, write employee's schedule to text file
# ======================================================================================================================
# Imports
from extractText import TextData, DateData, SupData, EmployeeTourData, read_structural_elements
# a lot of these data imports can be removed when program is finished development
from writeFile import write_to_file

from oauth2client import client
from oauth2client import file
from oauth2client import tools
from apiclient import discovery
from httplib2 import Http
# ======================================================================================================================
# Constants for Doc
SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
DOCUMENT_ID = '1hf83Hrd8Nq_3rHsQl77ml53z9QMPsS4cgu-2m6vc1YI'
# ======================================================================================================================


def get_credentials():
    """
    Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth 2.0 flow is completed to obtain the new credentials.
    :return Credentials, the obtained credential.
    """
    store = file.Storage('token.json')
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials


def main():
    """
    Uses the Docs API to read work schedule from Doc and write employee's schedule to text file
    """
    # setup Docs API
    credentials = get_credentials()
    http = credentials.authorize(Http())
    docs_service = discovery.build('docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    doc = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
    doc_content = doc.get('body').get('content')

    # get employee name user input, used in building EmployeeTourData list
    EmployeeTourData.employee = raw_input("Enter employee name: ")
    # Use Docs API to read contents of document into TextData OrderedDict, date, sup, employeeTour lists
    read_structural_elements(doc_content)

    # Print Data for debugging purposes
    for x in TextData.t_dct:
        print(x, TextData.t_dct[x])
    print('SupData list:', SupData.s_list)
    print('DateData list:', DateData.d_list)
    print('EmployeeTourData list:', EmployeeTourData.et_list)

    # write Data to file
    write_to_file()


if __name__ == '__main__':
    main()


# TODO: - Move file write operations to new file
#       - write error message in file if leftover employee instances in EmployeeTourData
#          (If not gonna pop them from EmployeeTourData, increment count, compare count to length, print error if less)
#  Publish on GitHub:
#      - Remove file PATH and DOC ID, replace with <insert here>
#      - Provide file format of doc in read me
#      - Write read me
