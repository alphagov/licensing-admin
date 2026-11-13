from django.http import HttpResponse

from authentication.decorators import public_view


@public_view
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
