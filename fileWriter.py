import math
# constants

LIST_BEGIN = "{"
LIST_END = "}"
LIST_END_NL = "}\n"
LINE_TAB = "	"
LINE_NEW = "\n"
VISUM_CONCAT_DELIM = ","
LOG_HEADER = "-"*50+"\n\t"


def logPrinter(msg, msg_type = 'finished', Visum = None):
    msg = LOG_HEADER + str(msg) + "\t:\t" + msg_type
    #if Visum is not None:
    Visum.Log(8192, msg)

    print(msg)


def addTable(file, name, table, type_list):
    if name != "":
        file.write(name + ":" + LINE_TAB+str(len(table)) + "\n")
    for line in table:
        appendDataLine(file, line, type_list)
    file.write(LINE_NEW)

def appendDataLine(file, line, type_list):

    toAdd = LIST_BEGIN
    for i, raw_field in enumerate(line):
        try:
            datatype = type_list[i]
        except:
            # exception required for STOP_AREAS only
            datatype = type_list[-1]
        if isinstance(raw_field, list):
            toAdd += LIST_BEGIN
            for raw_nested_field in raw_field:
                    # toAdd += LINE_TAB + '{0:.1f}'.format(float(nested_field))
                    nested_field = datatype(raw_nested_field)
                    toAdd += LINE_TAB + addField(nested_field)
            toAdd += LINE_TAB + LIST_END
        else:
            field = datatype(raw_field)
            add = addField(field)
            toAdd += LINE_TAB + add
    toAdd += LINE_TAB + LIST_END_NL
    file.write(toAdd)

def addField (field):
    if isinstance(field, int):
        return '{:1}'.format(int(field))
    elif isinstance(field, float):
        return '{0:.1f}'.format(float(field))
    elif isinstance(field, str):
        return str(field)
    elif isinstance(field, bytes):
        return str(field)
    else:
        return str(0)


def str_int(in_float):
    # converts float number into string(integer) - NO decimal places
    out_str_int = '{0:g}'.format(float(in_float))
    return(out_str_int)


def convert_ConcatenatedMultiAttValues(input_list):
    # remove NoneTypes
    # remove duplicates (i.e. elements appearing twice IN A ROW)
    # produce list of integers (final output)
    in_list_remove_nones = [i[1] for i in input_list if i[1] is not None]
    in_list_remove_duplicates = []
    i_prev = None

    for i in in_list_remove_nones:
        if i == i_prev:
            pass
        else:
            in_list_remove_duplicates.append(i)
            i_prev = i

    out_list_convert_integers = map(lambda j: int(float(j)), in_list_remove_duplicates)
    output_list = list(out_list_convert_integers)

    return output_list


def calc_BM_list_of_elements(in_int_list):
    """
    returns no. of list elements (e.g. route stops)
    :param in_int_list:
    :return:
    """

    out_str_list = LIST_BEGIN + ' '.join(map(str, in_int_list)) + LIST_END
    return(out_str_list)


def numbering_offset(Visum_Object_List_Creator):
    # calculates the numbering offset of Visum Net elements
    # as a further order of magnitude
    # e.g. max(No) = 7896 => numbering_offset(No) = 10001

    object_no_list = Visum_Object_List_Creator
    object_no_list.AddColumn("No")
    max_object_no = float(object_no_list.Max(0))
    magnitude_order = math.ceil(math.log10(max_object_no))

    output_offset = (10 ** magnitude_order) + 1

    return output_offset