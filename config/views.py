from django.http import HttpResponse


def hello_world(request):
    return HttpResponse(
        """
        <!doctype html>
        <html lang="en">
          <head>
            <title>Hello World</title>
          </head>
          <body>
            <h1>Hello World</h1>
          </body>
        </html>
        """,
        content_type="text/html",
    )
