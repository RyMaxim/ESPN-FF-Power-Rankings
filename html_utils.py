import re

def format_list(list):
    #print('', flush=True)
    html = '<dl>'
    for line in list:
        #print(line, flush=True)
        if re.match(r'^\d+\)', line):  # if line starts with a 1), 10), etc
            line = '<strong>' + line + '</strong>'  # bold it
        if line[0] == '-':  # if line starts with an hyphen
            line = line.replace('-','&nbsp;&nbsp;',1)  # remove hyphen + indent 2 spaces
        html = html + '<dt>' + line + '</dt>'
    html = html + '</dl>'
    return html

def format_table(row):
    table_width = 666
    cell_width = round(table_width / len(row) / 2, 2)
    cell_percent = round(cell_width / table_width * 100, 2)
    html = '<table width="' + str(table_width) \
           + '" cellpadding="1" cellspacing="0" border="1" ' \
           + 'style="border-collapse: collapse; white-space:pre-wrap"><tr>'
    for cell in row:
        html += format_cell(cell,cell_percent)
    html += '</tr></table>'
    return html

def format_cell(item,width):
    html = ''
    for key in item:
        html += '<td width="' \
             + str(width) \
             + '%" border-left="1" style="background-color:lightgray; text-align:center">' \
             + key \
             + '</td>'
        html += '<td width="' \
             + str(width) \
             + '%" style="text-align:center">' \
             + str(item[key]) \
             + '</td>'
    return html