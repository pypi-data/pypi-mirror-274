# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import calendar
import datetime
from enum import IntEnum
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from attr import define
import httpx

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter
from .models.CheckTestNotificationResponse import CheckTestNotificationResponse
from .models.ConsumptionRequest import ConsumptionRequest

from .models.Environment import Environment
from .models.ExtendRenewalDateRequest import ExtendRenewalDateRequest
from .models.ExtendRenewalDateResponse import ExtendRenewalDateResponse
from .models.HistoryResponse import HistoryResponse
from .models.MassExtendRenewalDateRequest import MassExtendRenewalDateRequest
from .models.MassExtendRenewalDateResponse import MassExtendRenewalDateResponse
from .models.MassExtendRenewalDateStatusResponse import MassExtendRenewalDateStatusResponse
from .models.NotificationHistoryRequest import NotificationHistoryRequest
from .models.NotificationHistoryResponse import NotificationHistoryResponse
from .models.OrderLookupResponse import OrderLookupResponse
from .models.RefundHistoryResponse import RefundHistoryResponse
from .models.SendTestNotificationResponse import SendTestNotificationResponse
from .models.Status import Status
from .models.StatusResponse import StatusResponse
from .models.TransactionHistoryRequest import TransactionHistoryRequest
from .models.TransactionInfoResponse import TransactionInfoResponse

T = TypeVar('T')

class APIError(IntEnum):
    GENERAL_BAD_REQUEST = 4000000
    """
    An error that indicates an invalid request.
    
    https://developer.apple.com/documentation/appstoreserverapi/generalbadrequesterror
    """

    INVALID_APP_IDENTIFIER = 4000002
    """
    An error that indicates an invalid app identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidappidentifiererror
    """

    INVALID_REQUEST_REVISION = 4000005
    """
    An error that indicates an invalid request revision.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidrequestrevisionerror
    """

    INVALID_TRANSACTION_ID = 4000006
    """
    An error that indicates an invalid transaction identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidtransactioniderror
    """

    INVALID_ORIGINAL_TRANSACTION_ID = 4000008
    """
    An error that indicates an invalid original transaction identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidoriginaltransactioniderror
    """

    INVALID_EXTEND_BY_DAYS = 4000009
    """
    An error that indicates an invalid extend-by-days value.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidextendbydayserror
    """

    INVALID_EXTEND_REASON_CODE = 4000010
    """
    An error that indicates an invalid reason code.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidextendreasoncodeerror
    """

    INVALID_REQUEST_IDENTIFIER = 4000011
    """
    An error that indicates an invalid request identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidrequestidentifiererror
    """

    START_DATE_TOO_FAR_IN_PAST = 4000012
    """
    An error that indicates that the start date is earlier than the earliest allowed date.
    
    https://developer.apple.com/documentation/appstoreserverapi/startdatetoofarinpasterror
    """

    START_DATE_AFTER_END_DATE = 4000013
    """
    An error that indicates that the end date precedes the start date, or the two dates are equal.
    
    https://developer.apple.com/documentation/appstoreserverapi/startdateafterenddateerror
    """

    INVALID_PAGINATION_TOKEN = 4000014
    """
    An error that indicates the pagination token is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidpaginationtokenerror
    """

    INVALID_START_DATE = 4000015
    """
    An error that indicates the start date is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidstartdateerror
    """

    INVALID_END_DATE = 4000016
    """
    An error that indicates the end date is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidenddateerror
    """

    PAGINATION_TOKEN_EXPIRED = 4000017
    """
    An error that indicates the pagination token expired.
    
    https://developer.apple.com/documentation/appstoreserverapi/paginationtokenexpirederror
    """

    INVALID_NOTIFICATION_TYPE = 4000018
    """
    An error that indicates the notification type or subtype is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidnotificationtypeerror
    """

    MULTIPLE_FILTERS_SUPPLIED = 4000019
    """
    An error that indicates the request is invalid because it has too many constraints applied.
    
    https://developer.apple.com/documentation/appstoreserverapi/multiplefilterssuppliederror
    """

    INVALID_TEST_NOTIFICATION_TOKEN = 4000020
    """
    An error that indicates the test notification token is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidtestnotificationtokenerror
    """

    INVALID_SORT = 4000021
    """
    An error that indicates an invalid sort parameter.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidsorterror
    """

    INVALID_PRODUCT_TYPE = 4000022
    """
    An error that indicates an invalid product type parameter.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidproducttypeerror
    """

    INVALID_PRODUCT_ID = 4000023
    """
    An error that indicates the product ID parameter is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidproductiderror
    """

    INVALID_SUBSCRIPTION_GROUP_IDENTIFIER = 4000024
    """
    An error that indicates an invalid subscription group identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidsubscriptiongroupidentifiererror
    """

    INVALID_EXCLUDE_REVOKED = 4000025
    """
    An error that indicates the query parameter exclude-revoked is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidexcluderevokederror

    .. deprecated:: 1.5
    """

    INVALID_IN_APP_OWNERSHIP_TYPE = 4000026
    """
    An error that indicates an invalid in-app ownership type parameter.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidinappownershiptypeerror
    """

    INVALID_EMPTY_STOREFRONT_COUNTRY_CODE_LIST = 4000027
    """
    An error that indicates a required storefront country code is empty.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidemptystorefrontcountrycodelisterror
    """

    INVALID_STOREFRONT_COUNTRY_CODE = 4000028
    """
    An error that indicates a storefront code is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidstorefrontcountrycodeerror
    """

    INVALID_REVOKED = 4000030
    """
    An error that indicates the revoked parameter contains an invalid value.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidrevokederror
    """

    INVALID_STATUS = 4000031
    """
    An error that indicates the status parameter is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidstatuserror
    """

    INVALID_ACCOUNT_TENURE = 4000032
    """
    An error that indicates the value of the account tenure field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidaccounttenureerror
    """

    INVALID_APP_ACCOUNT_TOKEN = 4000033
    """
    An error that indicates the value of the app account token field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidappaccounttokenerror
    """

    INVALID_CONSUMPTION_STATUS = 4000034
    """
    An error that indicates the value of the consumption status field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidconsumptionstatuserror
    """

    INVALID_CUSTOMER_CONSENTED = 4000035
    """
    An error that indicates the customer consented field is invalid or doesn’t indicate that the customer consented.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidcustomerconsentederror
    """

    INVALID_DELIVERY_STATUS = 4000036
    """
    An error that indicates the value in the delivery status field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invaliddeliverystatuserror
    """

    INVALID_LIFETIME_DOLLARS_PURCHASED = 4000037
    """
    An error that indicates the value in the lifetime dollars purchased field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidlifetimedollarspurchasederror
    """

    INVALID_LIFETIME_DOLLARS_REFUNDED = 4000038
    """
    An error that indicates the value in the lifetime dollars refunded field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidlifetimedollarsrefundederror
    """

    INVALID_PLATFORM = 4000039
    """
    An error that indicates the value in the platform field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidplatformerror
    """

    INVALID_PLAY_TIME = 4000040
    """
    An error that indicates the value in the playtime field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidplaytimeerror
    """

    INVALID_SAMPLE_CONTENT_PROVIDED = 4000041
    """
    An error that indicates the value in the sample content provided field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidsamplecontentprovidederror
    """

    INVALID_USER_STATUS = 4000042
    """
    An error that indicates the value in the user status field is invalid.
    
    https://developer.apple.com/documentation/appstoreserverapi/invaliduserstatuserror
    """

    INVALID_TRANSACTION_NOT_CONSUMABLE = 4000043
    """
    An error that indicates the transaction identifier doesn’t represent a consumable in-app purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidtransactionnotconsumableerror

    .. deprecated:: 1.11
    """

    INVALID_TRANSACTION_TYPE_NOT_SUPPORTED = 4000047
    """
    An error that indicates the transaction identifier represents an unsupported in-app purchase type.
    
    https://developer.apple.com/documentation/appstoreserverapi/invalidtransactiontypenotsupportederror
    """

    SUBSCRIPTION_EXTENSION_INELIGIBLE = 4030004
    """
    An error that indicates the subscription doesn't qualify for a renewal-date extension due to its subscription state.
    
    https://developer.apple.com/documentation/appstoreserverapi/subscriptionextensionineligibleerror
    """

    SUBSCRIPTION_MAX_EXTENSION = 4030005
    """
    An error that indicates the subscription doesn’t qualify for a renewal-date extension because it has already received the maximum extensions.
    
    https://developer.apple.com/documentation/appstoreserverapi/subscriptionmaxextensionerror
    """

    FAMILY_SHARED_SUBSCRIPTION_EXTENSION_INELIGIBLE = 4030007
    """
    An error that indicates a subscription isn't directly eligible for a renewal date extension because the user obtained it through Family Sharing.
    
    https://developer.apple.com/documentation/appstoreserverapi/familysharedsubscriptionextensionineligibleerror
    """

    ACCOUNT_NOT_FOUND = 4040001
    """
    An error that indicates the App Store account wasn’t found.
    
    https://developer.apple.com/documentation/appstoreserverapi/accountnotfounderror
    """

    ACCOUNT_NOT_FOUND_RETRYABLE = 4040002
    """
    An error response that indicates the App Store account wasn’t found, but you can try again.
    
    https://developer.apple.com/documentation/appstoreserverapi/accountnotfoundretryableerror
    """

    APP_NOT_FOUND = 4040003
    """
    An error that indicates the app wasn’t found.
    
    https://developer.apple.com/documentation/appstoreserverapi/appnotfounderror
    """

    APP_NOT_FOUND_RETRYABLE = 4040004
    """
    An error response that indicates the app wasn’t found, but you can try again.
    
    https://developer.apple.com/documentation/appstoreserverapi/appnotfoundretryableerror
    """

    ORIGINAL_TRANSACTION_ID_NOT_FOUND = 4040005
    """
    An error that indicates an original transaction identifier wasn't found.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionidnotfounderror
    """

    ORIGINAL_TRANSACTION_ID_NOT_FOUND_RETRYABLE = 4040006
    """
    An error response that indicates the original transaction identifier wasn’t found, but you can try again.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionidnotfoundretryableerror
    """

    SERVER_NOTIFICATION_URL_NOT_FOUND = 4040007
    """
    An error that indicates that the App Store server couldn’t find a notifications URL for your app in this environment.
    
    https://developer.apple.com/documentation/appstoreserverapi/servernotificationurlnotfounderror
    """

    TEST_NOTIFICATION_NOT_FOUND = 4040008
    """
    An error that indicates that the test notification token is expired or the test notification status isn’t available.
    
    https://developer.apple.com/documentation/appstoreserverapi/testnotificationnotfounderror
    """

    STATUS_REQUEST_NOT_FOUND = 4040009
    """
    An error that indicates the server didn't find a subscription-renewal-date extension request for the request identifier and product identifier you provided.
    
    https://developer.apple.com/documentation/appstoreserverapi/statusrequestnotfounderror
    """

    TRANSACTION_ID_NOT_FOUND = 4040010
    """
    An error that indicates a transaction identifier wasn't found.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactionidnotfounderror
    """

    RATE_LIMIT_EXCEEDED = 4290000
    """
    An error that indicates that the request exceeded the rate limit.
    
    https://developer.apple.com/documentation/appstoreserverapi/ratelimitexceedederror
    """

    GENERAL_INTERNAL = 5000000
    """
    An error that indicates a general internal error.
    
    https://developer.apple.com/documentation/appstoreserverapi/generalinternalerror
    """

    GENERAL_INTERNAL_RETRYABLE = 5000001
    """
    An error response that indicates an unknown error occurred, but you can try again.
    
    https://developer.apple.com/documentation/appstoreserverapi/generalinternalretryableerror
    """


@define
class APIException(Exception):
    http_status_code: int
    api_error: Optional[APIError]
    raw_api_error: Optional[int]
    error_message: Optional[str]

    def __init__(self, http_status_code: int, raw_api_error: Optional[int] = None, error_message: Optional[str] = None):
        self.http_status_code = http_status_code
        self.raw_api_error = raw_api_error
        self.api_error = None
        self.error_message = error_message
        try:
            if raw_api_error is not None:
                self.api_error = APIError(raw_api_error)
        except ValueError:
            pass

class AsyncAppStoreServerAPIClient:
    def __init__(self, signing_key: bytes, key_id: str, issuer_id: str, bundle_id: str, environment: Environment):
        if environment == Environment.XCODE:
            raise ValueError("Xcode is not a supported environment for an AppStoreServerAPIClient")
        if environment == Environment.PRODUCTION:
            self._base_url = "https://api.storekit.itunes.apple.com"
        elif environment == Environment.LOCAL_TESTING:
            self._base_url = "https://local-testing-base-url"
        else:
            self._base_url = "https://api.storekit-sandbox.itunes.apple.com"
        self._signing_key = serialization.load_pem_private_key(signing_key, password=None, backend=default_backend())
        self._key_id = key_id
        self._issuer_id = issuer_id
        self._bundle_id = bundle_id

    def _generate_token(self) -> str:
        future_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        return jwt.encode(
            {
                "bid": self._bundle_id,
                "iss": self._issuer_id,
                "aud": "appstoreconnect-v1",
                "exp": calendar.timegm(future_time.timetuple()),
            },
            self._signing_key,
            algorithm="ES256",
            headers={"kid": self._key_id},
        )

    async def _make_request(self, path: str, method: str, queryParameters: Dict[str, Union[str, List[str]]], body, destination_class: Type[T]) -> T:
        url = self._base_url + path
        c = _get_cattrs_converter(type(body)) if body is not None else None
        json = c.unstructure(body) if body is not None else None
        headers = {
            'User-Agent': "app-store-server-library/python/1.2.0",
            'Authorization': 'Bearer ' + self._generate_token(),
            'Accept': 'application/json'
        }

        response = await self._execute_request(method, url, queryParameters, headers, json)
        if 200 <= response.status_code < 300:
            if destination_class is None:
                return
            c = _get_cattrs_converter(destination_class)
            response_body = response.json()
            return c.structure(response_body, destination_class)
        else:
            # Best effort parsing of the response body
            if not 'content-type' in response.headers or response.headers['content-type'] != 'application/json':
                raise APIException(response.status_code)
            try:
                response_body = response.json()
                raise APIException(response.status_code, response_body['errorCode'], response_body['errorMessage'])
            except APIException as e:
                raise e
            except Exception as e:
                raise APIException(response.status_code) from e

    async def _execute_request(self, method: str, url: str, params: Dict[str, Union[str, List[str]]], headers: Dict[str, str], json: Dict[str, Any]) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, params=params, headers=headers, json=json)
        return response

    async def extend_renewal_date_for_all_active_subscribers(self, mass_extend_renewal_date_request: MassExtendRenewalDateRequest) -> MassExtendRenewalDateResponse:
        return await self._make_request("/inApps/v1/subscriptions/extend/mass", "POST", {}, mass_extend_renewal_date_request, MassExtendRenewalDateResponse)

    async def extend_subscription_renewal_date(self, original_transaction_id: str, extend_renewal_date_request: ExtendRenewalDateRequest) -> ExtendRenewalDateResponse:
        return await self._make_request("/inApps/v1/subscriptions/extend/" + original_transaction_id, "PUT", {}, extend_renewal_date_request, ExtendRenewalDateResponse)

    async def get_all_subscription_statuses(self, transaction_id: str, status: Optional[List[Status]] = None) -> StatusResponse:
        queryParameters: Dict[str, List[str]] = dict()
        if status is not None:
            queryParameters["status"] = [s.value for s in status]

        return await self._make_request("/inApps/v1/subscriptions/" + transaction_id, "GET", queryParameters, None, StatusResponse)

    async def get_refund_history(self, transaction_id: str, revision: Optional[str]) -> RefundHistoryResponse:
        queryParameters: Dict[str, List[str]] = dict()
        if revision is not None:
            queryParameters["revision"] = [revision]

        return await self._make_request("/inApps/v2/refund/lookup/" + transaction_id, "GET", queryParameters, None, RefundHistoryResponse)

    async def get_status_of_subscription_renewal_date_extensions(self, request_identifier: str, product_id: str) -> MassExtendRenewalDateStatusResponse:
        return await self._make_request("/inApps/v1/subscriptions/extend/mass/" + product_id + "/" + request_identifier, "GET", {}, None, MassExtendRenewalDateStatusResponse)

    async def get_test_notification_status(self, test_notification_token: str) -> CheckTestNotificationResponse:
        return await self._make_request("/inApps/v1/notifications/test/" + test_notification_token, "GET", {}, None, CheckTestNotificationResponse)

    async def get_notification_history(self, pagination_token: Optional[str], notification_history_request: NotificationHistoryRequest) -> NotificationHistoryResponse:
        queryParameters: Dict[str, List[str]] = dict()
        if pagination_token is not None:
            queryParameters["paginationToken"] = [pagination_token]

        return await self._make_request("/inApps/v1/notifications/history", "POST", queryParameters, notification_history_request, NotificationHistoryResponse)

    async def get_transaction_history(self, transaction_id: str, revision: Optional[str], transaction_history_request: TransactionHistoryRequest) -> HistoryResponse:
        queryParameters: Dict[str, List[str]] = dict()
        if revision is not None:
            queryParameters["revision"] = [revision]

        if transaction_history_request.startDate is not None:
            queryParameters["startDate"] = [str(transaction_history_request.startDate)]

        if transaction_history_request.endDate is not None:
            queryParameters["endDate"] = [str(transaction_history_request.endDate)]

        if transaction_history_request.productIds is not None:
            queryParameters["productId"] = transaction_history_request.productIds

        if transaction_history_request.productTypes is not None:
            queryParameters["productType"] = [product_type.value for product_type in transaction_history_request.productTypes]

        if transaction_history_request.sort is not None:
            queryParameters["sort"] = [transaction_history_request.sort.value]

        if transaction_history_request.subscriptionGroupIdentifiers is not None:
            queryParameters["subscriptionGroupIdentifier"] = transaction_history_request.subscriptionGroupIdentifiers

        if transaction_history_request.inAppOwnershipType is not None:
            queryParameters["inAppOwnershipType"] = [transaction_history_request.inAppOwnershipType.value]

        if transaction_history_request.revoked is not None:
            queryParameters["revoked"] = [str(transaction_history_request.revoked)]

        return await self._make_request("/inApps/v1/history/" + transaction_id, "GET", queryParameters, None, HistoryResponse)

    async def get_transaction_info(self, transaction_id: str) -> TransactionInfoResponse:
        return await self._make_request("/inApps/v1/transactions/" + transaction_id, "GET", {}, None, TransactionInfoResponse)

    async def look_up_order_id(self, order_id: str) -> OrderLookupResponse:
        return await self._make_request("/inApps/v1/lookup/" + order_id, "GET", {}, None, OrderLookupResponse)

    async def request_test_notification(self) -> SendTestNotificationResponse:
        return await self._make_request("/inApps/v1/notifications/test", "POST", {}, None, SendTestNotificationResponse)

    async def send_consumption_data(self, transaction_id: str, consumption_request: ConsumptionRequest):
        await self._make_request("/inApps/v1/transactions/consumption/" + transaction_id, "PUT", {}, consumption_request, None)
