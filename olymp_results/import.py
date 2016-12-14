#!/usr/bin/python2
# -*- coding: utf8 -*-

import sys
import os
import traceback

import csv

# Returns (pupil_fields, z_fields)
# pupil_fields = dict('family': column_num, ...)
# z_fields = dict('1.1': column_num, ...)
def guess_input_columns(row):
    def find_column(name, exactly_one=True):
        ret = []
        for i in range(len(row)):
            if row[i].strip().lower().startswith(name.lower()):
                ret += [i]
        if exactly_one and len(ret) != 1:
            print >> sys.stderr, u"Ошибка при определении поля '%s': должен быть один столбец, а найдено %d %d" % (name, len(ret), ret)
            exit(1)
        return ret

    pupil_fields = {
        'family': find_column('Фамилия')[0],
        'name':   find_column('Имя')[0],
        'paral':  find_column('ПарУ')[0],
        'school': find_column('Шк')[0],
        'district': find_column('Район')[0],
        'result': find_column('Реш')[0],
        'sum':    find_column('Сум')[0]
    }
    print u"Фамилия:   '%s'" % unicode(row[pupil_fields['family']], "utf8")
    print u"Имя:       '%s'" % unicode(row[pupil_fields['name']], "utf8")
    print u"Параллель: '%s'" % unicode(row[pupil_fields['paral']], "utf8")
    print u"Школа:     '%s'" % unicode(row[pupil_fields['school']], "utf8")
    print u"Район:     '%s'" % unicode(row[pupil_fields['district']], "utf8")
    print u"Решение:   '%s'" % unicode(row[pupil_fields['result']], "utf8")
    print u"Сумма:     '%s'" % unicode(row[pupil_fields['sum']], "utf8")
    z_fields = dict()
    cols = find_column('Z', False)
    for z_col in cols:
        z_name = row[z_col][1:].strip()
        z_fields[z_name] = z_col
        print u"Задача: '%s'" % unicode(z_name, "utf8")
    
    return pupil_fields, z_fields

def read_one_file(input_csv_name, pupils, marks):
    global cur_pupil
    print u"============================"
    print u"Разбор файла %s..." % input_csv_name
    with open(input_csv_name, "rb") as input_csv:
        input_reader = csv.reader(input_csv, dialect="excel")
        columns, z_columns = guess_input_columns(input_reader.next())
        for row in input_reader:
            cur_pupil += 1
            pupil = [cur_pupil,
                     row[columns['family']],
                     row[columns['name']],
                     row[columns['paral']],
                     row[columns['school']],
                     row[columns['district']],
                     row[columns['sum']],
                     row[columns['result']]
                    ]
            cur_marks = []
            err = False
            for z_name, z_col in z_columns.items():
                z_mark = row[z_col].strip()
                if len(z_mark) > 0:
                    if not z_mark.isdigit():
                        print >> sys.stderr, u"Ошибка при чтении баллов участника %s %s за задачу %s: не число '%s'" % (
                                            unicode(pupil[1], 'utf8'), 
                                            unicode(pupil[2], 'utf8'), 
                                            unicode(z_name, 'utf8'), 
                                            unicode(z_mark, 'utf8'))
                        err = True
                    else:
                        cur_marks += [[cur_pupil, z_name, int(z_mark)]]
            if not err:
                pupils += [pupil]
                marks += cur_marks

def write_csv(output_csv_name, data):
    with open(output_csv_name, "wb") as outfile:
        wr = csv.writer(outfile, delimiter=",", doublequote=False, escapechar="\\")
        for row in data:
            wr.writerow(row)


#####################################################################


if len(sys.argv) == 1:
    print >> sys.stderr, u"Использование: %s <csv-файл> <csv-файл> ..." % sys.argv[0]
    print >> sys.stderr, u"Вывод будет находиться в файлах pupils.csv и marks.csv в папке с первым входным файлом."
    print >> sys.stderr, u"Нажмите Enter..."
    raw_input()
    exit(1)

cur_pupil = 0
# id_pupil, family, name, paral, school_name, sum, result
pupils_table = []
# id_pupil, z_num, mark
marks_table = []

try:
    for input_file in sys.argv[1:]:
        read_one_file(input_file, pupils_table, marks_table)
    
    file_dir_name = os.path.dirname(sys.argv[1])
    
    output_pupils_name = os.path.join(file_dir_name, "pupils.csv")
    output_marks_name  = os.path.join(file_dir_name, "marks.csv")
    
    print u"Вывод в файлы '%s' и '%s'..." % (output_pupils_name, output_marks_name)
    
    write_csv(output_pupils_name, pupils_table)
    write_csv(output_marks_name,  marks_table)
    
    print u"Нажмите Enter для завершения..."
    raw_input()
except Exception:
    type_, value_, trace_ = sys.exc_info()
    traceback.print_exception(type_, value_, trace_, file=sys.stdout)
    print u"Выполнение завершилось неожиданной ошибкой."
    print u"Нажмите Enter..."
    raw_input()





