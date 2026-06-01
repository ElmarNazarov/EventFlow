from decimal import Decimal

import pytest

from app.core.constants import PAYMENT_FAILURE_THRESHOLD
from app.services.payment_service import PaymentService


def test_payment_failure_threshold_rule() -> None:
    service = PaymentService(db=None)  # type: ignore[arg-type]
    assert service._should_fail_payment(PAYMENT_FAILURE_THRESHOLD) is False
    assert service._should_fail_payment(PAYMENT_FAILURE_THRESHOLD + Decimal("0.01")) is True
    assert service._should_fail_payment(Decimal("100")) is False
