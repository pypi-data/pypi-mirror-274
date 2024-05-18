import uuid
from datetime import datetime
from typing import Callable, Optional

import pytest

from acquiring import domain, protocols
from acquiring.domain import decision_logic as dl
from acquiring.enums import OperationStatusEnum, OperationTypeEnum
from tests.domain import factories

COMPLETED_STATUS = [OperationStatusEnum.COMPLETED]

PENDING_STATUS = [OperationStatusEnum.PENDING]

FAILED_STATUS = [
    OperationStatusEnum.STARTED,
    OperationStatusEnum.REQUIRES_ACTION,
    OperationStatusEnum.FAILED,
    OperationStatusEnum.NOT_PERFORMED,
]


def test_statusListsAreComplete() -> None:
    assert set(COMPLETED_STATUS + PENDING_STATUS + FAILED_STATUS) == set(OperationStatusEnum)


@pytest.mark.parametrize(
    "result_status, payment_operation_status",
    [(OperationStatusEnum.COMPLETED, status) for status in COMPLETED_STATUS]
    + [(OperationStatusEnum.PENDING, status) for status in PENDING_STATUS]
    + [(OperationStatusEnum.FAILED, status) for status in FAILED_STATUS],
)
def test_givenAValidPaymentMethod_whenAfterConfirmingCompletes_thenPaymentFlowReturnsTheCorrectOperationResponse(
    fake_unit_of_work: type[protocols.UnitOfWork],
    fake_block: type[protocols.Block],
    fake_process_action_block: type[protocols.Block],
    fake_payment_method_repository_class: Callable[
        [Optional[list[protocols.PaymentMethod]]], type[protocols.Repository]
    ],
    fake_payment_operation_repository_class: Callable[
        [Optional[list[protocols.PaymentOperation]]],
        type[protocols.Repository],
    ],
    fake_block_event_repository_class: Callable[
        [Optional[list[protocols.PaymentOperation]]],
        type[protocols.Repository],
    ],
    fake_transaction_repository_class: Callable[
        [Optional[list[protocols.PaymentOperation]]],
        type[protocols.Repository],
    ],
    result_status: OperationStatusEnum,
    payment_operation_status: OperationStatusEnum,
) -> None:

    payment_attempt = factories.PaymentAttemptFactory()
    payment_method_id = uuid.uuid4()
    payment_method = factories.PaymentMethodFactory(
        payment_attempt=payment_attempt,
        id=payment_method_id,
        confirmable=True,
        payment_operations=[
            domain.PaymentOperation(
                type=OperationTypeEnum.INITIALIZE,
                status=OperationStatusEnum.STARTED,
                payment_method_id=payment_method_id,
            ),
            domain.PaymentOperation(
                type=OperationTypeEnum.INITIALIZE,
                status=OperationStatusEnum.COMPLETED,
                payment_method_id=payment_method_id,
            ),
            domain.PaymentOperation(
                type=OperationTypeEnum.PAY,
                status=OperationStatusEnum.STARTED,
                payment_method_id=payment_method_id,
            ),
            domain.PaymentOperation(
                type=OperationTypeEnum.PAY,
                status=OperationStatusEnum.COMPLETED,
                payment_method_id=payment_method_id,
            ),
            domain.PaymentOperation(
                type=OperationTypeEnum.AFTER_PAY,
                status=OperationStatusEnum.STARTED,
                payment_method_id=payment_method_id,
            ),
            domain.PaymentOperation(
                type=OperationTypeEnum.AFTER_PAY,
                status=OperationStatusEnum.COMPLETED,
                payment_method_id=payment_method_id,
            ),
            domain.PaymentOperation(
                type=OperationTypeEnum.CONFIRM,
                status=OperationStatusEnum.STARTED,
                payment_method_id=payment_method_id,
            ),
            domain.PaymentOperation(
                type=OperationTypeEnum.CONFIRM,
                status=OperationStatusEnum.COMPLETED,
                payment_method_id=payment_method_id,
            ),
        ],
    )

    # when Confirming
    result = domain.PaymentFlow(
        unit_of_work=fake_unit_of_work(
            payment_method_repository_class=fake_payment_method_repository_class([payment_method]),
            payment_operation_repository_class=fake_payment_operation_repository_class([]),
            block_event_repository_class=fake_block_event_repository_class([]),
            transaction_repository_class=fake_transaction_repository_class([]),
        ),
        initialize_block=fake_block(  # type:ignore[call-arg]
            fake_response_status=OperationStatusEnum.COMPLETED,
            fake_response_actions=[],
        ),
        process_action_block=fake_process_action_block(),
        pay_blocks=[],
        after_pay_blocks=[],
        confirm_block=None,
        after_confirm_blocks=[
            fake_block(  # type:ignore[call-arg]
                fake_response_status=payment_operation_status,
            ),
        ],
    ).after_confirm(payment_method)

    # then the payment flow returns the correct Operation Response
    db_payment_operations = payment_method.payment_operations
    assert len(db_payment_operations) == 10

    assert db_payment_operations[0].type == OperationTypeEnum.INITIALIZE
    assert db_payment_operations[0].status == OperationStatusEnum.STARTED

    assert db_payment_operations[1].type == OperationTypeEnum.INITIALIZE
    assert db_payment_operations[1].status == OperationStatusEnum.COMPLETED

    assert db_payment_operations[2].type == OperationTypeEnum.PAY
    assert db_payment_operations[2].status == OperationStatusEnum.STARTED

    assert db_payment_operations[3].type == OperationTypeEnum.PAY
    assert db_payment_operations[3].status == OperationStatusEnum.COMPLETED

    assert db_payment_operations[4].type == OperationTypeEnum.AFTER_PAY
    assert db_payment_operations[4].status == OperationStatusEnum.STARTED

    assert db_payment_operations[5].type == OperationTypeEnum.AFTER_PAY
    assert db_payment_operations[5].status == OperationStatusEnum.COMPLETED

    assert db_payment_operations[6].type == OperationTypeEnum.CONFIRM
    assert db_payment_operations[6].status == OperationStatusEnum.STARTED

    assert db_payment_operations[7].type == OperationTypeEnum.CONFIRM
    assert db_payment_operations[7].status == OperationStatusEnum.COMPLETED

    assert db_payment_operations[8].type == OperationTypeEnum.AFTER_CONFIRM
    assert db_payment_operations[8].status == OperationStatusEnum.STARTED

    assert db_payment_operations[9].type == OperationTypeEnum.AFTER_CONFIRM
    assert db_payment_operations[9].status == result_status

    assert result.type == OperationTypeEnum.AFTER_CONFIRM
    assert result.status == result_status
    assert result.actions == []
    assert result.payment_method is not None
    assert result.payment_method.id == payment_method_id


def test_givenAPaymentMethodThatCannotAfterConfirm_whenAfterConfirming_thenPaymentFlowReturnsAFailedStatusOperationResponse(
    fake_block: type[protocols.Block],
    fake_process_action_block: type[protocols.Block],
    fake_payment_method_repository_class: Callable[
        [Optional[list[protocols.PaymentMethod]]],
        type[protocols.Repository],
    ],
    fake_payment_operation_repository_class: Callable[
        [Optional[list[protocols.PaymentOperation]]],
        type[protocols.Repository],
    ],
    fake_block_event_repository_class: Callable[
        [Optional[list[protocols.PaymentOperation]]],
        type[protocols.Repository],
    ],
    fake_transaction_repository_class: Callable[
        [Optional[list[protocols.PaymentOperation]]],
        type[protocols.Repository],
    ],
    fake_unit_of_work: type[protocols.UnitOfWork],
) -> None:
    # Given a payment method that cannot initialize
    payment_attempt = factories.PaymentAttemptFactory()
    payment_method_id = uuid.uuid4()
    payment_method = factories.PaymentMethodFactory(
        payment_attempt=payment_attempt,
        id=payment_method_id,
        confirmable=False,
    )
    assert dl.can_after_confirm(payment_method) is False

    # When Initializing
    result = domain.PaymentFlow(
        unit_of_work=fake_unit_of_work(
            payment_method_repository_class=fake_payment_method_repository_class([payment_method]),
            payment_operation_repository_class=fake_payment_operation_repository_class([]),
            block_event_repository_class=fake_block_event_repository_class([]),
            transaction_repository_class=fake_transaction_repository_class([]),
        ),
        initialize_block=fake_block(),
        process_action_block=fake_process_action_block(),
        pay_blocks=[],
        after_pay_blocks=[],
        confirm_block=fake_block(),
        after_confirm_blocks=[],
    ).after_confirm(payment_method)

    # then the payment flow returns a failed status operation response
    assert result.type == OperationTypeEnum.AFTER_CONFIRM
    assert result.status == OperationStatusEnum.FAILED
    result.error_message == "PaymentMethod cannot go through this operation"


def test_givenANonExistingPaymentMethod_whenAfterConfirming_thenPaymentFlowReturnsAFailedStatusOperationResponse(
    fake_block: type[protocols.Block],
    fake_process_action_block: type[protocols.Block],
    fake_payment_method_repository_class: Callable[
        [Optional[list[protocols.PaymentMethod]]],
        type[protocols.Repository],
    ],
    fake_payment_operation_repository_class: Callable[
        [Optional[list[protocols.PaymentOperation]]],
        type[protocols.Repository],
    ],
    fake_block_event_repository_class: Callable[
        [Optional[list[protocols.PaymentOperation]]],
        type[protocols.Repository],
    ],
    fake_transaction_repository_class: Callable[
        [Optional[list[protocols.PaymentOperation]]],
        type[protocols.Repository],
    ],
    fake_unit_of_work: type[protocols.UnitOfWork],
) -> None:

    payment_attempt = domain.PaymentAttempt(
        id=uuid.uuid4(),
        created_at=datetime.now(),
        amount=10,
        currency="USD",
        payment_method_ids=[],
    )

    payment_method = domain.PaymentMethod(
        id=uuid.uuid4(),
        payment_attempt=payment_attempt,
        created_at=datetime.now(),
        confirmable=False,
    )

    # When Confirming
    result = domain.PaymentFlow(
        unit_of_work=fake_unit_of_work(
            payment_method_repository_class=fake_payment_method_repository_class([payment_method]),
            payment_operation_repository_class=fake_payment_operation_repository_class([]),
            block_event_repository_class=fake_block_event_repository_class([]),
            transaction_repository_class=fake_transaction_repository_class([]),
        ),
        initialize_block=fake_block(),
        process_action_block=fake_process_action_block(),
        pay_blocks=[],
        after_pay_blocks=[],
        confirm_block=None,
        after_confirm_blocks=[],
    ).after_confirm(payment_method)

    # then the payment flow returns a failed status operation response
    assert result.type == OperationTypeEnum.AFTER_CONFIRM
    assert result.status == OperationStatusEnum.FAILED
    result.error_message == "PaymentMethod not found"
