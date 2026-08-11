from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Body, Depends, Header, Query, status

from ..api_dependencies import principal, service_from_request
from ..models import StatementEntryIn, TransactionIn
from ..security import Principal
from ..service import ReconForgeService

router = APIRouter(tags=["entries"])


@router.post("/transactions", status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionIn,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    return service.create_transaction(
        user.tenant_id, payload, actor=user.name, idempotency_key=idempotency_key
    )


@router.get("/transactions")
def list_transactions(
    account_id: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    cursor: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.list_transactions(
        user.tenant_id,
        account_id=account_id,
        from_date=from_date,
        to_date=to_date,
        cursor=cursor,
        limit=limit,
    )


@router.post("/statement-entries", status_code=status.HTTP_201_CREATED)
def create_statement_entry(
    payload: StatementEntryIn,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.create_statement_entry(user.tenant_id, payload, actor=user.name)


@router.get("/statement-entries")
def list_statement_entries(
    account_id: str | None = None,
    statement_id: str | None = None,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.list_statement_entries(
        user.tenant_id, account_id=account_id, statement_id=statement_id
    )


@router.post("/imports/transactions.csv", status_code=status.HTTP_201_CREATED)
def import_transactions_csv(
    body: str = Body(media_type="text/csv"),
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.import_transactions_csv(user.tenant_id, body, actor=user.name)


@router.post("/imports/statements.csv", status_code=status.HTTP_201_CREATED)
def import_statements_csv(
    body: str = Body(media_type="text/csv"),
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.import_statements_csv(user.tenant_id, body, actor=user.name)
  # internal: 404043
  # internal: 144582
  # internal: 289373
  # internal: 856254
  # internal: 112468
  # internal: 810287
  # internal: 519300
  # internal: 987187
  # internal: 775788
  # internal: 110206
  # internal: 912915
  # internal: 417645
  # internal: 933298
  # internal: 323573
  # internal: 105948
  # internal: 226204
  # internal: 857619
  # internal: 239834
  # internal: 774442
  # internal: 514089
  # internal: 945581
  # internal: 580339
  # internal: 182533
  # internal: 368727
  # internal: 264925
  # internal: 170332
  # internal: 146675
  # internal: 468451
  # internal: 891507
  # internal: 168466
  # internal: 658352
  # internal: 898063
  # internal: 527063
  # internal: 505048
  # internal: 670950
  # internal: 141350
  # internal: 857513
  # internal: 573213
  # internal: 728820
  # internal: 924357
  # internal: 833621
  # internal: 987631
  # internal: 602194
  # internal: 395433
  # internal: 741346
  # internal: 267642
  # internal: 791300
  # internal: 467635
  # internal: 571342
  # internal: 102074
  # internal: 885858
  # internal: 440888
  # internal: 357533
  # internal: 702848
  # internal: 664913
  # internal: 538327
  # internal: 809102
  # internal: 955089
  # internal: 630935
  # internal: 617506
  # internal: 479191
