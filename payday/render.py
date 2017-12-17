# -*- coding: utf-8 -*-

"""Rendering related code."""

import os
import subprocess  # nosec
import tempfile

from jinja2 import FileSystemLoader
# from jinja2.runtime import StrictUndefined
from jinja2 import Environment as Jinja2Environment
from webassets import Environment as AssetsEnvironment
from webassets.ext.jinja2 import AssetsExtension


def get_jinja_renderer(template_path):
    """
    This returns a method render(template, data) that will render the provided
    template with the given data using an initialized jinja2 environment.
    The primary reasons why we need this are:
     - asset handling (for example for logos)
     - reloading of templates (while designing the template)

    :param template_path: the directory that contains all templates and assets
    """
    # template_path
    asset_path = os.path.join(template_path, "assets")
    if not os.path.isdir(template_path):
        raise ValueError("%s must be a directory" % template_path)
    if not os.path.isdir(asset_path):
        raise ValueError("%s must be a directory" % asset_path)

    assets_env = AssetsEnvironment(
        asset_path, "file://" + os.path.abspath(asset_path))
    jinja2_env = Jinja2Environment(extensions=[
                                   AssetsExtension],
                                   loader=FileSystemLoader(template_path),
                                   auto_reload=True,
                                   autoescape=True,
                                   # undefined=StrictUndefined
                                   )
    jinja2_env.assets_environment = assets_env

    def jinja_env_renderer(template_filename, data):
        template = jinja2_env.get_template(template_filename)
        return template.render(data)

    return jinja_env_renderer


def get_jinja2_to_wkhtmltopdf_render_method(jinja_render, outfilename):
    def pdf_render(template_filename, data):
        html = jinja_render(template_filename, data)
        thtml = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        thtml.write(html.encode('utf-8'))
        thtml.close()
        # print "temp file {}".format(thtml.name)
        # print outfilename
        convert_html_to_pdf_wkhtmltopdf(thtml.name, outfilename)
        # convert_html_to_pdf_phantomjs(thtml.name, outfilename)
        os.unlink(thtml.name)
    return pdf_render


def convertHtmlToPdf(sourceHtml, fp):
    from xhtml2pdf import pisa

    pisa.showLogging()
    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(sourceHtml, dest=fp)
    # return True on success and False on errors
    return pisaStatus.err


def convert_html_to_pdf_wkhtmltopdf(html_filename, pdf_filename):
    # OS X:
    # wkhtmltopdf installed from http://wkhtmltopdf.org/downloads.html
    # Carbon version
    for p in ["/usr/local/bin/wkhtmltopdf", "/usr/bin/wkhtmltopdf"]:
        if os.path.isfile(p):
            break
    use_xvfb = True
    if use_xvfb:
        cmd = ["xvfb-run", "-a", "-s", "-screen 0 640x480x16"]
    else:
        cmd = []
    cmd.extend([p, html_filename, pdf_filename])
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # nosec
    out, err = proc.communicate()
    if proc.returncode != 0:
        print("{} exited with a non zero exit code:".format(" ".join(cmd)))
        print(out)
        print(err)
    return


def convert_html_to_pdf_phantomjs(url, pdf_filename, page_size="A4"):
    # TODO: use contrib/ directory for this
    "phantomjs rasterize.js http://minitv.local:9091/transmission/web/ out.pdf A4"
    cmd = ["/usr/local/bin/phantomjs", "rasterize.js", url, pdf_filename, page_size]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # nosec
    out, err = proc.communicate()
    print(out, err)
    return
