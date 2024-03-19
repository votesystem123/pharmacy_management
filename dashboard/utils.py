from django.http import JsonResponse, HttpResponse
import json
from django.template.loader import render_to_string
from weasyprint import HTML

def download_template(request, template_path, context):
    html_string = render_to_string(template_path, context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response