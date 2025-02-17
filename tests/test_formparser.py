from __future__ import annotations

import pytest
from werkzeug.exceptions import RequestEntityTooLarge

from quart.formparser import FormDataParser
from quart.formparser import MultiPartParser
from quart.wrappers.request import Body


async def test_multipart_max_form_memory_size() -> None:
    """max_form_memory_size is tracked across multiple data events."""
    data = b"--bound\r\nContent-Disposition: form-field; name=a\r\n\r\n"
    data += b"a" * 15 + b"\r\n--bound--"
    body = Body(None, None)
    body.set_result(data)
    # The buffer size is less than the max size, so multiple data events will be
    # returned. The field size is greater than the max.
    parser = MultiPartParser(max_form_memory_size=10, buffer_size=5)

    with pytest.raises(RequestEntityTooLarge):
        await parser.parse(body, b"bound", 0)


async def test_formparser_max_num_parts() -> None:
    parser = FormDataParser(max_form_parts=1)
    body = Body(None, None)
    body.set_result(b"param1=data1&param2=data2&param3=data3")

    with pytest.raises(RequestEntityTooLarge):
        await parser.parse(body, "application/x-url-encoded", None)
