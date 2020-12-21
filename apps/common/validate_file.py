from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import os

def validate_lecture_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('unsupported file extension.'))
