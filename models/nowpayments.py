
from pydantic import BaseModel
from typing import Optional, Dict, Any


class NOWPaymentsCreatePaymentRequest(BaseModel):
    price_amount: float
    price_currency: str
    pay_currency: Optional[str] = None
    ipn_callback_url: Optional[str] = None
    order_id: Optional[str] = None
    order_description: Optional[str] = None
    purchase_id: Optional[str] = None
    payout_address: Optional[str] = None
    payout_currency: Optional[str] = None
    payout_extra_id: Optional[str] = None
    fixed_rate: Optional[bool] = True
    is_fee_paid_by_user: Optional[bool] = True


class NOWPaymentsCreatePaymentResponse(BaseModel):
    payment_id: str
    payment_status: str
    pay_address: str
    price_amount: float
    price_currency: str
    pay_amount: float
    pay_currency: str
    order_id: Optional[str] = None
    order_description: Optional[str] = None
    ipn_callback_url: Optional[str] = None
    created_at: str
    updated_at: str
    purchase_id: Optional[str] = None
    amount_received: Optional[float] = None
    payin_extra_id: Optional[str] = None
    smart_contract: Optional[str] = None
    network: Optional[str] = None
    network_precision: Optional[int] = None
    time_limit: Optional[str] = None
    burning_percent: Optional[float] = None
    expiration_estimate_date: Optional[str] = None


class NOWPaymentsWebhookData(BaseModel):
    payment_id: str
    payment_status: str
    pay_address: str
    price_amount: float
    price_currency: str
    pay_amount: float
    actually_paid: float
    pay_currency: str
    order_id: Optional[str] = None
    order_description: Optional[str] = None
    purchase_id: Optional[str] = None
    created_at: str
    updated_at: str
    outcome_amount: Optional[float] = None
    outcome_currency: Optional[str] = None


class NOWPaymentsStatusResponse(BaseModel):
    payment_id: str
    payment_status: str
    pay_address: str
    price_amount: float
    price_currency: str
    pay_amount: float
    actually_paid: Optional[float] = None
    pay_currency: str
    order_id: Optional[str] = None
    order_description: Optional[str] = None
    purchase_id: Optional[str] = None
    created_at: str
    updated_at: str
    outcome_amount: Optional[float] = None
    outcome_currency: Optional[str] = None
    payin_extra_id: Optional[str] = None
    smart_contract: Optional[str] = None
    network: Optional[str] = None
    network_precision: Optional[int] = None
    time_limit: Optional[str] = None
    burning_percent: Optional[float] = None
    expiration_estimate_date: Optional[str] = None
