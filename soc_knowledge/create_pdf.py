# coding=utf-8

import StringIO
from cgi import escape
# from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import DetailView
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from xhtml2pdf.default import DEFAULT_FONT
from django.template.loader import get_template
from  django.template import Context
import json
import pdfkit
from django.conf import settings

import logging
logger = logging.getLogger("soc_knowledge")


"""
下载生成的PDF 两种方法
1 xhtml2pdf
2 pdfkit 系统需要安装wkhtmltopdf
"""

# pdfmetrics.registerFont(TTFont('st', 'soc_knowledge/templates/STSONG.TTF'))
# DEFAULT_FONT['helvetica'] = 'st'


# def html_pdf(template_src, context_dict, file_name):
#     """ 生成pdf
#     :return:
#     """
#     template = get_template(template_src)
#     context = Context(context_dict)
#     html = template.render(context)
#     result = StringIO.StringIO()
#     rendering = pisa.pisaDocument(StringIO.StringIO(html), result, encoding='UTF-8')
#     response = HttpResponse()
#     if not rendering.err:
#         response.write(result.getvalue())
#         response['Content-Type'] = 'application/pdf'
#         response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
#         return response
#     else:
#         result = {
#             "status": 500,
#             "msg": u'找不到预案',
#             "error": u'找不到预案'
#         }
#         return response(json.dumps(result, ensure_ascii=True), content_type="application/json")


# class PDFTemplateResponse(TemplateResponse):
#
#     def generate_pdf(self, retval):
#         html = self.content
#         result = StringIO.StringIO()
#         rendering = pisa.pisaDocument(StringIO.StringIO(html), result, encoding='UTF-8')
#
#         if rendering.err:
#             return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
#         else:
#             self.content = result.getvalue()
#
#     def __init__(self, *args, **kwargs):
#         super(PDFTemplateResponse, self).__init__(*args, **kwargs)
#         self.add_post_render_callback(self.generate_pdf)


# class PDFTemplateView(DetailView):
#     response_class = PDFTemplateResponse


def get_pdf(template_src, context_dict):
    """获取html"""
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO(html)
    return result.getvalue()


def render_pdf(template_src, context_dict, file_name):
    """

    """
    res = get_pdf(template_src, context_dict)
    path_file = '/tmp/' + file_name
    options = {
        'page-size': 'Letter',
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'encoding': "UTF-8",
        'no-outline': None
    }

    pdfkit.from_string(res, path_file, options=options)

    with open(path_file, 'r') as f:
        data = f.read()

    response = HttpResponse()
    try:
        response.write(data)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    except Exception:
        result = {
            "status": 500,
            "msg": u'找不到预案',
            "error": u'找不到预案'
        }
        return response(json.dumps(result, ensure_ascii=True), content_type="application/json")


def create_pdf_file(template_src, context_dict, file_name):
    """ 生成下载的文件，并返回链接
    """
    media_dir = settings.PDF_DIR
    res = get_pdf(template_src, context_dict)
    path_file = media_dir + '/'  + file_name
    options = {
        'page-size': 'Letter',
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'encoding': "UTF-8",
        'no-outline': None
    }
    try:
        pdfkit.from_string(res, path_file, options=options)
        return_url = '/media/pdf/%s' % file_name
    except Exception as e:
        logger.error(e.message, exc_info=True)
        return_url = None
    return return_url
