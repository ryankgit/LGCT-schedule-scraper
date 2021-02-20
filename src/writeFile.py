#
# Writes Employee's schedule to text file
# ======================================================================================================================
# Imports
from extractText import TextData, DateData, SupData, EmployeeTourData
from datetime import datetime

import os.path
# ======================================================================================================================
# Constant file path
# text files are saved here
import config
PATH = config.PATH
# ======================================================================================================================
#   Possible tour configs:
#
#   tour time           tour time            tour time           tour time           tour time
#   employee            other employee       employee            other employee      other employee
#   other employee      employee             other employee      employee            other employee
#   amount              amount               other employee      other employee      employee
#                                            amount              amount              amount
#
#
#   HR time             HR time             HR time
#   employee            other employee      employee
#   amount              employee            other employee
#                       amount              amount
#
# ======================================================================================================================


def create_file():
    """
    Create file with current date in name to write to.
    :return: file
    """
    # file name containing employee name, time, and date
    date = datetime.now().strftime('%Hh-%Mm-%Ss-%m-%d-%Y')
    file_name = EmployeeTourData.employee + '-' + date + '.txt'
    complete_name = os.path.join(PATH + file_name)
    f = open(complete_name, 'w')
    return f


def write_to_file():
    """
    Writes Employee's schedule to text file.
    """
    # create file to write to
    f = create_file()
    # write heading to file
    f.write(EmployeeTourData.employee + '\'s Schedule\n')
    f.write('Generated ' + datetime.strftime(datetime.today(), '%m-%d-%Y') + '\n\n')
    # define line break string for formatting file
    line_brk = '------------------------------\n'

    # iterate DateData.d_list, write to file
    for i in range(0, len(DateData.d_list), 2):
        # write date to file
        f.write(line_brk + '    ' + str(DateData.d_list[i]) + line_brk + '\n')

        # get current and next date indexes
        current_date_index = DateData.d_list[i + 1]
        next_date_index = get_next_date_index(i)

        # write sup to file
        for j in range(0, len(SupData.s_list), 2):
            try:
                sup_index = SupData.s_list[j + 1]
                if current_date_index < sup_index < next_date_index:
                    f.write('Supervisor: ' + str(SupData.s_list[j]) + '\n')
            except IndexError:
                print('Index error')

        # write employee tours to file
        # while TextData.t_dct index is between current_date_index and next_date_index, write tours
        write_tours_to_file(current_date_index, next_date_index, f)

    f.close()


def get_next_date_index(i):
    """
    Gets the index of the next date from DateData list
    :param i: current date index
    :return: index of next date
    """
    try:
        # get index position of next index in list
        next_index = DateData.d_list[i + 3]
    # if the end of list has been reached, set end_index to the final item in the list
    except IndexError:
        next_index = TextData.t_dct.keys()[-1]
    return next_index


def write_tours_to_file(current_index, next_index, f):
    """
    Writes Employee's tours to text file.
    Called in write_to_file function
    :param next_index:
    :param current_index:
    :param f: file
    """
    # TODO This concept works, but is not implemented efficiently or 100% accurate. Needs to be updated.
    #   Would be helpful to reimplement w/ a data-parsing library.
    # write employee tours to file
    for et_index in EmployeeTourData.et_list:
        if current_index < et_index < next_index:
            # TODO Format, determine what to write better, make sure contains time in one of the lines
            #   if line is blank, don't print, unless two in a row, which indicates unbooked tour
            employee = TextData.t_dct.get(et_index)
            u1_employee = TextData.t_dct.get(et_index - 1)
            if ':' in u1_employee:
                f.write(u1_employee)        # 1:00pm-3:00pm
                f.write(employee)           # employee
            u2_employee = TextData.t_dct.get(et_index - 2)
            if ':' in u2_employee:
                f.write(u2_employee)        # 1:00pm-3:00pm
                f.write(u1_employee)        # other employee
                f.write(employee)           # employee
            u3_employee = TextData.t_dct.get(et_index - 3)
            if ':' in u3_employee:
                f.write(u3_employee)        # 1:00pm-3:00pm
                f.write(u2_employee)        # other employee
                f.write(u1_employee)        # other employee
                f.write(employee)           # employee

            try:    # in try-catch bc could try to get index off bottom of TextData
                # print below employee until int or until 2 consecutive blank lines (unbooked tours)
                i = 1
                while i < 4:
                    employee = TextData.t_dct.get(et_index + i)
                    if employee is '':
                        f.write('\n')
                    else:
                        f.write(employee)
                    i += 1

            except IndexError:
                print('Index Error')
