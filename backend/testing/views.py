import logging
import time

from django.db import connection
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

from util import response


@response.request_get()
@csrf_exempt
def long_running_db_query(request):
    logging.info("Sending Wait request")
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_sleep(15)")
    return response.success(value="DB Query Success")


@response.request_get()
@csrf_exempt
def sse(request):
    def event_stream():
        try:
            for i in range(5):
                yield f"data: Event {i}\n\n".encode()
                time.sleep(1)
        except Exception:
            raise

    return StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream",
    )
