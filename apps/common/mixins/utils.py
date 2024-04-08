from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class IINRegexValidator(RegexValidator):
    regex = (
        r"^((0[48]|[2468][048]|[13579][26])0229[1-6]|000229[34]|\d\d((0[13578]|1[02])"
        r"(0[1-9]|[12]\d|3[01])|(0[469]|11)(0[1-9]|[12]\d|30)|02(0[1-9]|1\d|2[0-8]))[1-6])\d{5}$"
    )
    message = _("IIN must be 12 digits long.")
    code = "invalid_iin"
