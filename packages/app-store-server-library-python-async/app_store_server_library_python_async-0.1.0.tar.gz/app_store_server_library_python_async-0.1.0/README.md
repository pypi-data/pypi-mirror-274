# Apple App Store Server Python Library Async Version
The Python server library for the [App Store Server API](https://developer.apple.com/documentation/appstoreserverapi) and [App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications).  This library has been rewritten by [Bahadır Araz](https://github.com/bahadiraraz) to use asynchronous code. This update prevents blocking when handling concurrent API requests and includes instructions on how to use the library with Pydantic for improved data validation with modern Python practices.
## Table of Contents
1. [Installation](#installation)
2. [Documentation](#documentation)
3. [Usage](#usage)
4. [Support](#support)

## Installation

#### Requirements

- Python 3.7+

### pip
```sh
pip install app-store-server-library-async
```

## Documentation

[Documentation](https://apple.github.io/app-store-server-library-python/)

[WWDC Video](https://developer.apple.com/videos/play/wwdc2023/10143/)

### Obtaining an In-App Purchase key from App Store Connect

To use the App Store Server API or create promotional offer signatures, a signing key downloaded from App Store Connect is required. To obtain this key, you must have the Admin role. Go to Users and Access > Integrations > In-App Purchase. Here you can create and manage keys, as well as find your issuer ID. When using a key, you'll need the key ID and issuer ID as well.

### Obtaining Apple Root Certificates

Download and store the root certificates found in the Apple Root Certificates section of the [Apple PKI](https://www.apple.com/certificateauthority/) site. Provide these certificates as an array to a SignedDataVerifier to allow verifying the signed data comes from Apple.

## Usage

### API Usage

```python
from appstoreserverlibrary.api_client import AsyncAppStoreServerAPIClient, APIException
from appstoreserverlibrary.models.Environment import Environment

def read_private_key(file_path):
    with open(file_path, "r") as file:
        return file.read()
private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implementation will vary

key_id = "ABCDEFGHIJ"
issuer_id = "99b16628-15e4-4668-972b-eeff55eeff55"
bundle_id = "com.example"
environment = Environment.SANDBOX

client = AsyncAppStoreServerAPIClient(private_key, key_id, issuer_id, bundle_id, environment)
async def main():
    try:    
        response = await client.request_test_notification()
        print(response)
    except APIException as e:
        print(e)
```

### Verification Usage

```python
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.signed_data_verifier import VerificationException, SignedDataVerifier

def load_root_certificates():
    cert_paths = [
        f"AppleComputerRootCertificate.cer",
        f"AppleRootCA-G3.cer",
        f"AppleRootCA-G2.cer",
        f"AppleIncRootCertificate.cer",
    ]
    certs = []
    for path in cert_paths:
        file = open(path, "rb")
        cert = file.read()
        file.close()
        certs.append(cert)
    return certs

async def main():
    root_certificates = load_root_certificates()
    enable_online_checks = True
    bundle_id = "com.example"
    environment = Environment.SANDBOX
    app_apple_id = None  # appAppleId must be provided for the Production environment
    signed_data_verifier = SignedDataVerifier(root_certificates, enable_online_checks, environment, bundle_id, app_apple_id)

    try:
        signed_notification = "ey.."
        payload = await signed_data_verifier.verify_and_decode_notification(signed_notification)
        print(payload)
    except VerificationException as e:
        print(e)
```

### Receipt Usage

```python
from appstoreserverlibrary.api_client import AsyncAppStoreServerAPIClient, APIException
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.receipt_utility import ReceiptUtility
from appstoreserverlibrary.models.HistoryResponse import HistoryResponse
from appstoreserverlibrary.models.TransactionHistoryRequest import TransactionHistoryRequest, ProductType, Order

def read_private_key(file_path):
    with open(file_path, "r") as file:
        return file.read()

private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implementation will vary

key_id = "ABCDEFGHIJ"
issuer_id = "99b16628-15e4-4668-972b-eeff55eeff55"
bundle_id = "com.example"
environment = Environment.SANDBOX

client = AsyncAppStoreServerAPIClient(private_key, key_id, issuer_id, bundle_id, environment)
receipt_util = ReceiptUtility()
app_receipt = "MI.."
async def extract_transaction_receipts_from_id(app_receipt):
    try:    
        transaction_id = receipt_util.extract_transaction_id_from_app_receipt(app_receipt)
        if transaction_id != None:
            transactions = []
            response: HistoryResponse = None
            request: TransactionHistoryRequest = TransactionHistoryRequest(
                sort=Order.ASCENDING,
                revoked=False,
                productTypes=[ProductType.AUTO_RENEWABLE]
            )
            while response is None or response.hasMore:
                revision = response.revision if response is not None else None
                response = await client.get_transaction_history(transaction_id, revision, request)
                for transaction in response.signedTransactions:
                    transactions.append(transaction)
            print(transactions)
    except APIException as e:
        print(e)
```

### Promotional Offer Signature Creation

```python
from appstoreserverlibrary.promotional_offer import PromotionalOfferSignatureCreator
import time

def read_private_key(file_path):
    with open(file_path, "r") as file:
        return file.read()
    
private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implementation will vary

key_id = "ABCDEFGHIJ"
bundle_id = "com.example"

promotion_code_signature_generator = PromotionalOfferSignatureCreator(private_key, key_id, bundle_id)

product_id = "<product_id>"
subscription_offer_id = "<subscription_offer_id>"
application_username = "<application_username>"
nonce = "<nonce>"
timestamp = round(time.time()*1000)
base64_encoded_signature = promotion_code_signature_generator.create_signature(product_id, subscription_offer_id, application_username, nonce, timestamp)
```
### Pydantic Example
Apple has interestingly chosen to use `attrs` library. Here is an example of how you can convert it to `Pydantic`.
```python
from appstoreserverlibrary.models.JWSTransactionDecodedPayload import JWSTransactionDecodedPayload,Type,InAppOwnershipType,RevocationReason,OfferType,Environment,TransactionReason,OfferDiscountType
from pydantic import BaseModel
import attr
from typing import Optional

example_payload = JWSTransactionDecodedPayload(
    originalTransactionId="1000000077803123",
    transactionId="1000000077803124",
    webOrderLineItemId="1000000077803125",
    bundleId="com.example.app",
    productId="com.example.product",
    subscriptionGroupIdentifier="12345678",
    purchaseDate=1622548800000, 
    originalPurchaseDate=1622548800000,
    expiresDate=1625130800000,
    quantity=1,
    type=Type("Auto-Renewable Subscription"),
    rawType="1",
    appAccountToken="E7DE6CBE-E0C2-4B52-A00C-E0C2E7DE6CBE",
    inAppOwnershipType=InAppOwnershipType("PURCHASED"),
    rawInAppOwnershipType="PURCHASED",
    signedDate=1622548800000,
    revocationReason=RevocationReason(1),
    rawRevocationReason=0,
    revocationDate=1622548800000,
    isUpgraded=False,
    offerType=OfferType(1),
    rawOfferType=1,
    offerIdentifier="offer123",
    environment=Environment("Sandbox"),
    rawEnvironment="PRODUCTION",
    storefront="USA",
    storefrontId="143441",
    transactionReason=TransactionReason("PURCHASE"),
    rawTransactionReason="PURCHASE",
    currency="USD",
    price=499,
    offerDiscountType=OfferDiscountType("FREE_TRIAL"),
    rawOfferDiscountType="FREE_TRIAL"
)


class PydanticJWSTransactionDecodedPayload(BaseModel):
    originalTransactionId: Optional[str] = None
    transactionId: Optional[str] = None
    webOrderLineItemId: Optional[str] = None
    bundleId: Optional[str] = None
    productId: Optional[str] = None
    subscriptionGroupIdentifier: Optional[str] = None
    purchaseDate: Optional[int] = None
    originalPurchaseDate: Optional[int] = None
    expiresDate: Optional[int] = None
    quantity: Optional[int] = None
    type: Optional[str] = None
    rawType: Optional[str] = None
    appAccountToken: Optional[str] = None
    inAppOwnershipType: Optional[str] = None
    rawInAppOwnershipType: Optional[str] = None
    signedDate: Optional[int] = None
    revocationReason: Optional[int] = None
    rawRevocationReason: Optional[int] = None
    revocationDate: Optional[int] = None
    isUpgraded: Optional[bool] = None
    offerType: Optional[int] = None
    rawOfferType: Optional[int] = None
    offerIdentifier: Optional[str] = None
    environment: Optional[str] = None
    rawEnvironment: Optional[str] = None
    storefront: Optional[str] = None
    storefrontId: Optional[str] = None
    transactionReason: Optional[str] = None
    rawTransactionReason: Optional[str] = None
    currency: Optional[str] = None
    price: Optional[int] = None
    offerDiscountType: Optional[str] = None
    rawOfferDiscountType: Optional[str] = None

# Convert to Pydantic
pydanctic_payload = PydanticJWSTransactionDecodedPayload(**attr.asdict(example_payload))
print(pydanctic_payload)
```
## Support

Only the latest major version of the library will receive updates, including security updates. Therefore, it is recommended to update to new major versions.
