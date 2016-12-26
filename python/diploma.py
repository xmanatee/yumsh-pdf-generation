#!/usr/bin/env python
# -*- coding: utf8 -*-

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# TODO: register all unicode fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font = TTFont('Condensed', 'DejaVuSansCondensed.ttf')
pdfmetrics.registerFont(font)
font_name = 'Condensed'

from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize

PAGE_WIDTH = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]

from os.path import isfile


def generate_filename(details, encrypt=False):
    filename = u"{}_{}_{}_{}".format(details['surname'], details['name'], details['year'], details['id'])
    if encrypt:
        from hashlib import md5
        filename = md5(filename.encode('utf-8')).hexdigest()
        filename = unicode(filename)
        filename = filename[-10:]
    filename += u".pdf"
    return filename


def write_in_center(can, text, y_margin, size):
    text_width = stringWidth(text, font_name, 20)
    pdf_text_object = can.beginText((PAGE_WIDTH - text_width) / 2.0, 500)
    pdf_text_object.textOut(text)
    can.drawText(pdf_text_object)


def generate_info(details):
    info = dict()
    info['fullname'] = u"{name} {surname}".format(details)

    if sex == u"м":
        info['student'] = u"ученик"
    else:
        info['student'] = u"ученица"
    info['student'] += u" {paral} класса".format(details)


def generate_essence(details):
    import io
    packet = io.BytesIO()

    can = canvas.Canvas(packet, pagesize=letter, initialFontName=font_name, initialFontSize=20)
    can.setFont(font_name, 20)

    reason = u"выступление в отборочном (заочном) туре \n" \
             u"олимпиады Юношеской математической школы \n" \
             u"Санкт-Петербургского государственного университета \n" \
             u"среди {paral} классов."

    write_in_center(can, details['name'], 500, 20)

    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    essence = PdfFileReader(packet)
    return essence


def generate_diploma(row):
    file_path = 'diplomas/' + generate_filename(row, True)
    if isfile(file_path):
        # print("Diploma already generated!")
        return

    essence = generate_essence(row)

    template = PdfFileReader(open('assets/template_0.pdf', 'rb'))

    page = template.getPage(0)
    page.mergePage(essence.getPage(0))

    output = PdfFileWriter()
    output.addPage(page)

    output_stream = open(file_path, 'wb')
    output.write(output_stream)
    output_stream.close()
