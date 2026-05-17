from __future__ import annotations

import pytest
from django.core import mail


@pytest.fixture(autouse=True)
def clear_mail_outbox():
    """
    Очищает тестовый почтовый ящик перед каждым тестом.
    """

    mail.outbox = []
