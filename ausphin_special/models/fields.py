# -*- coding: utf-8 -*-

import base64
import binascii
import psycopg2

from odoo import models, fields, api
from odoo.tools import pycompat
from odoo.tools.mimetypes import guess_mimetype
from odoo.exceptions import UserError

def convert_to_column(self, value, record, values=None, validate=True):
    if not value:
        return None
    magic_bytes = {
        b'P',
        b'<',
    }
    if isinstance(value, str):
        value = value.encode()
    if value[:1] in magic_bytes:
        try:
            decoded_value = base64.b64decode(value.translate(None, delete=b'\r\n'), validate=True)
        except binascii.Error:
            decoded_value = value
        if (guess_mimetype(decoded_value).startswith('image/svg') and not record.env.user._is_system()):
            raise UserError(_("Only admins can upload SVG files."))
    if isinstance(value, bytes):
        return psycopg2.Binary(value)
    try:
        return psycopg2.Binary(pycompat.text_type(value).encode('ascii'))
    except UnicodeEncodeError:
        raise UserError(_("ASCII characters are required for %s in %s") % (value, self.name))

fields.Binary.convert_to_column = convert_to_column