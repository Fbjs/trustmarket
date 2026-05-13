from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "",
        "Sitemap: https://postulacion.trustmarket.cl/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
