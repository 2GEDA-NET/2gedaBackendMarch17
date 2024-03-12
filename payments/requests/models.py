from pydantic import BaseModel
from typing import Optional, Any, Dict
from pydantic import BaseModel, EmailStr



class InitializeTransactionAuthorizationResponse(BaseModel):
    access_code: str
    authorization_url: str
    reference: str

class IntializeTransactionResponse(BaseModel):
    status: bool
    message: str
    data: InitializeTransactionAuthorizationResponse













# Webhook Payload

class Authorization(BaseModel):
    authorization_code: str
    bin: str
    last4: str
    exp_month: str
    exp_year: str
    channel: str
    card_type: str
    bank: str
    country_code: str
    brand: str
    reusable: bool
    signature: str
    account_name: Optional[str] = None
    receiver_bank_account_number: Optional[str] = None
    receiver_bank: Optional[str] = None

class Customer(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    customer_code: str
    phone: Optional[str] = None
    metadata: Optional[Any] = None
    risk_action: str
    international_format_phone: Optional[str] = None

class Source(BaseModel):
    type: str
    source: str
    entry_point: str
    identifier: Optional[Any] = None

class Data(BaseModel):
    id: int
    domain: str
    status: str
    reference: str
    amount: int
    message: Optional[str] = None
    gateway_response: str
    paid_at: str
    created_at: str
    channel: str
    currency: str
    ip_address: str
    metadata: Optional[Dict[str, Any]] = None
    fees_breakdown: Optional[Any] = None
    log: Optional[Any] = None
    fees: int
    fees_split: Optional[Any] = None
    authorization: Authorization
    customer: Customer
    plan: Dict[str, Any]
    subaccount: Dict[str, Any]
    split: Dict[str, Any]
    order_id: Optional[Any] = None
    paidAt: str
    requested_amount: int
    pos_transaction_data: Optional[Any] = None
    source: Source

class WebhookPayload(BaseModel):
    event: str
    data: Data
