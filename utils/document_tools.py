import pdfkit
import win32com.client

"""
apt-get install wkhtmltopdf
apt-get install xvfb
echo -e '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*' > /usr/bin/wkhtmltopdf.sh
chmod a+x /usr/bin/wkhtmltopdf.sh
ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf
"""

"""
1、unoconv
    优点
        使用简单
    缺点
        只能对静态html进行转换，对于页面中有使用ajax异步获取数据的地方也不能转换（主要是要保证从web页面保存下来的html文件中有数据）。
        只能对html进行转换，如果页面中有使用echarts,highcharts等js代码生成的图片，是无法将这些图片转换到word文档中；
        生成的word文档内容格式不容易控制。

2、python-docx

3、win32
"""


class Html2PDF(object):
    """
    html 转 pdf
    """

    def __init__(self):
        pass

    def writepdf(self, html):
        pdfkit.from_url('http://baike.baidu.com/item/Google?fromtitle=%E8%B0%B7%E6%AD%8C&fromid=117920', 'google1.pdf')
        pass


class Html2doc(object):
    """
    html 转 word
    """

    def __init__(self):
        pass

    def writedoc(self, html):

        word = win32com.client.Dispatch('Word.Application')

        doc = word.Documents.Add('news.html')
        doc.SaveAs('news.doc', FileFormat=0)
        doc.Close()

        word.Quit()
