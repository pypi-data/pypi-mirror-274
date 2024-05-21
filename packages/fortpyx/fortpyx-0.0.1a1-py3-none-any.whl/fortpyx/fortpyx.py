"""
# Documentation

The Fortnox API is organized around REST. This means that we’ve designed it to have resource-oriented URLs and be as predictable as possible for you as developer.

It also means that we use HTTP status codes when something goes wrong and HTTP verbs understod by many API clients around the web.

We use a modified version of OAuth2 for authentication to offer a secure way for both you and our users to interact.

The API is generally built to support both XML and JSON but in this documentation all the examples will be in JSON.

We encourage you to read all the articles in the [Guides & Good to Know section](https://www.fortnox.se/developer/guides-and-good-to-know/)</a> first, before going forward and learning about the different resources.

This to ensure you get an understanding of some of the shared components of the API such as parameters and error handling.

## Rate limits

The limit per access-token is 25 requests per 5 seconds. This equals to 300 requests per minute.

[Read more about this here.](https://www.fortnox.se/developer/guides-and-good-to-know/rate-limits-for-fortnox-api/)

## Query parameters

Use query parameters with the ?-character and separate parameters with the &-character.

**Example:**
 GET - https://api.fortnox.se/3/invoices?accountnumberfrom=3000&accountnumberto=4000
Read more about our parameters [here](https://www.fortnox.se/developer/guides-and-good-to-know/parameters/)


Search the documentation using the search field in the top left corner.
"""

import contextlib
import functools
import logging
from http import HTTPStatus
from typing import Union, Tuple, Callable, List, Dict, Literal, cast, Any, TypedDict
from urllib.parse import urlencode

import requests
from requests import Request, Session, Response, HTTPError, JSONDecodeError
from requests.adapters import HTTPAdapter


from .error.fortnox_error import FortnoxError
from .model import *  # noqa

logging.getLogger(__name__).addHandler(logging.NullHandler())


class _Merger:
    def __init__(
        self,
        items: Optional[List[Any]] = None,
        return_model: Optional[Any] = None,
    ):
        if items is None:
            items = []

        self.__items = items
        self.__return_model = return_model
        self.__logger = logging.getLogger(__name__)

    def add_item(self, item: Any) -> "_Merger":
        self.__items.append(item)
        return self

    def set_model(self, return_model: Any) -> "_Merger":
        self.__return_model = return_model
        return self

    def merge(self) -> Any:
        self.__logger.debug(
            "About to merge. Items: %s - Return model: %s",
            self.__items,
            self.__return_model,
        )

        if len(self.__items) == 0 and self.__return_model:
            return self.__return_model

        accum: List[ModelBase] = []
        key = None
        for item in self.__items:
            key = self.__accumulate(accum, item)

        assert key, "Key is None, cannot determine which attribute to merge"

        if self.__return_model:
            accum = [getattr(self.__return_model, key), *accum]

        flat_merged_sequence = [
            flat_item for nested_list in accum for flat_item in nested_list
        ]

        return_model = (
            self.__return_model if self.__return_model is not None else self.__items[0]
        )
        setattr(return_model, key, flat_merged_sequence)

        return return_model

    @staticmethod
    def __accumulate(accum: List[ModelBase], item: ModelBase) -> str:
        for entry in vars(item).items():
            if isinstance(entry[1], (list, tuple)):
                to_append = cast(ModelBase, entry[1])
                accum.append(to_append)
                return entry[0]

        msg = f"List or tuple not found in item {item}"
        raise ValueError(msg)


def auto_consume_pages(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper_auto_consume_pages(self: Any, *args: Any, **kwargs: Any) -> Any:
        fortpyx_instance: Fortpyx = self.top
        should_auto_consume = fortpyx_instance._Fortpyx__auto_fetch_all_pages  # type: ignore # noqa

        return_value: ModelBase = func(self, *args, **kwargs)

        if should_auto_consume and return_value.meta_information is not None:
            logger = logging.getLogger(__name__)
            logger.debug("Will auto consume pages")

            current_page = 1
            pages_left = return_value.meta_information.pages_left
            merger = _Merger().set_model(return_value)

            while pages_left > 0:
                current_page += 1
                logger.debug("Consuming page %s", current_page)
                kwargs["page"] = current_page
                current_page_result: ModelBase = func(self, *args, **kwargs)
                merger.add_item(current_page_result)

                assert current_page_result.meta_information, "Meta information missing"
                pages_left = current_page_result.meta_information.pages_left

            return merger.merge()

        return return_value

    return wrapper_auto_consume_pages


class Fortpyx:
    __BASE_URL = "https://api.fortnox.se"
    __AUTHORIZATION_URL = "https://apps.fortnox.se/oauth-v1/auth"
    __TOKEN_URL = "https://apps.fortnox.se/oauth-v1/token"

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        before_token_refresh: Optional[
            Callable[
                [
                    Optional[str],
                    Optional[str],
                    Optional[Callable[[Optional[str], Optional[str]], None]],
                ],
                None,
            ]
        ] = None,
        on_token_refresh: Optional[Callable[[str, str], None]] = None,
        page_size: int = 500,
        auto_fetch_all_pages: bool = False,
        http_adapter: Optional[HTTPAdapter] = None,
    ):
        self.__access_token = access_token
        self.__refresh_token = refresh_token
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.warehouse = Fortpyx.Warehouse(self)
        self.time_reporting = Fortpyx.TimeReporting(self)
        self.fortnox = Fortpyx.Fortnox(self)
        self.fileattachments = Fortpyx.Fileattachments(self)
        self.developer = Fortpyx.Developer(self)

        self.__before_token_refresh = before_token_refresh
        self.__on_token_refresh = on_token_refresh
        self.__page_size = page_size
        self.__auto_fetch_all_pages = auto_fetch_all_pages
        self.__session: Optional[Session] = None
        self.__http_adapter = http_adapter or HTTPAdapter()

    def __enter__(self) -> "Fortpyx":
        self.__session = self.__create_session()
        return self

    def __create_session(self) -> Session:
        session = Session()
        session.mount("https://", self.__http_adapter)
        return session

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if self.__session:
            self.__session.close()
            self.__session = None

    def get_authorization_url(
        self,
        redirect_uri: str,
        scopes: Sequence[str],
        state: Optional[str] = "fortpyx_state",
        use_service_account: bool = True,
    ) -> str:
        query_string = urlencode(
            {
                "redirect_uri": redirect_uri,
                "client_id": self.__client_id,
                "response_type": "code",
                "access_type": "offline",
                "scope": " ".join(scopes),
                "state": state,
                **({"account_type": "service"} if use_service_account else {}),
            },
            doseq=True,
        )
        self._logger.debug("Query string for auth URL: %s", query_string)

        return f"{self.__AUTHORIZATION_URL}?{query_string}"

    def get_tokens(self, authorization_code: str, redirect_uri: str) -> Tuple[str, str]:
        """
        Get access token and refresh token as a tuple, in that order. They are also set
        internally in the Fortpyx client for further use.

        The provided authorization code can be retrieved by utilizing the get_authorization_code
        method.
        """
        body = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": redirect_uri,
        }

        if not all((self.__client_id, self.__client_secret)):
            msg = "Cannot get tokens since client ID or client secret is missing."
            raise FortnoxError(msg)

        assert self.__client_id and self.__client_secret
        response = requests.post(
            url=self.__TOKEN_URL,
            data=body,
            auth=(self.__client_id, self.__client_secret),
        )

        response_json = response.json()
        self.__access_token = response_json.get("access_token")
        self.__refresh_token = response_json.get("refresh_token")
        self.__raise_if_token_missing()
        assert self.__access_token and self.__refresh_token

        return self.__access_token, self.__refresh_token

    def __update_tokens(
        self, access_token: Optional[str], refresh_token: Optional[str]
    ) -> None:
        self.__access_token = access_token
        self.__refresh_token = refresh_token

    def refresh_tokens(self) -> Tuple[str, str]:
        if self.__before_token_refresh is not None:
            self.__before_token_refresh(
                self.__access_token, self.__refresh_token, self.__update_tokens
            )

        self.__raise_if_client_id_or_secret_missing()
        assert self.__client_id
        assert self.__client_secret

        self.__raise_if_refresh_token_missing()
        assert self.__refresh_token

        body = {
            "grant_type": "refresh_token",
            "refresh_token": self.__refresh_token,
        }

        class TypedParams(TypedDict):
            """This makes mypy happy."""

            url: str
            data: Dict[str, str]
            auth: Tuple[str, str]

        params: TypedParams = {
            "url": self.__TOKEN_URL,
            "data": body,
            "auth": (self.__client_id, self.__client_secret),
        }

        use_one_shot_session = self.__session is None
        ctx_manager: contextlib.AbstractContextManager = cast(
            contextlib.AbstractContextManager,
            (
                self.__create_session()
                if use_one_shot_session
                else contextlib.nullcontext()
            ),
        )
        with ctx_manager:
            session = cast(
                Session, ctx_manager if use_one_shot_session else self.__session
            )
            response = session.post(**params)
            response_json = response.json()

            if response.ok:
                self._logger.info("Tokens have been refreshed")
            else:
                self._logger.warning(
                    "Could not refresh tokens (%s) - %s",
                    response.status_code,
                    response_json,
                )
                self.__raise_token_could_not_be_updated(response)

            self.__access_token = response_json.get("access_token")
            self.__refresh_token = response_json.get("refresh_token")

            self.__raise_if_token_missing()

            assert self.__access_token and self.__refresh_token
            if self.__on_token_refresh is not None:
                self.__on_token_refresh(self.__access_token, self.__refresh_token)

            assert self.__access_token and self.__refresh_token
            return self.__access_token, self.__refresh_token

    def __raise_if_client_id_or_secret_missing(self) -> None:
        if not all((self.__client_id, self.__client_secret)):
            msg = "Client ID or client secret missing, cannot refresh tokens"
            raise FortnoxError(msg)

    def __raise_if_refresh_token_missing(self) -> None:
        if not self.__refresh_token:
            msg = "Refresh token is missing, cannot refresh tokens"
            raise FortnoxError(msg)

    def __raise_if_token_missing(self) -> None:
        if not all((self.__access_token, self.__refresh_token)):
            msg = "Access token or refresh token missing from response"
            raise FortnoxError(msg)

    @staticmethod
    def __raise_token_could_not_be_updated(response: Response) -> None:
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise FortnoxError(
                message="Could not refresh tokens",
                original_exception=e,
            ) from e

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    def _execute(
        self,
        http_verb: str,
        path: str,
        request_body: Optional[
            Union[ModelBase, UploadFile, str, int, Sequence[Union[ModelBase, str, int]]]
        ],
        content_type: Optional[str] = None,
        query_params: Optional[Dict[str, Optional[Any]]] = None,
        has_reauthenticated: bool = False,
        *,
        page: int = 1,
        offset: Optional[int] = None,
    ) -> Response:
        headers = {
            "Authorization": f"Bearer {self.__access_token}",
            **({"Content-Type": content_type} if content_type else {}),
        }

        url = f"{self.__BASE_URL}{path}"

        if isinstance(request_body, ModelBase):
            payload = request_body.model_dump_json(
                by_alias=True,
                exclude_unset=True,
            ).encode()
        elif isinstance(request_body, (str, int)):
            payload = f"{request_body}".encode()
        else:
            payload = None

        if isinstance(request_body, UploadFile):
            files = {"file": request_body.file}
        else:
            files = None

        self._logger.debug("Payload type: %s", type(payload))
        self._logger.debug("Payload data: %s", payload)

        params = {
            "limit": self.__page_size,
            **({"page": page} if http_verb == "get" else {}),
            **({"offset": offset} if http_verb == "get" else {}),
            **({k: v for k, v in query_params.items() if v} if query_params else {}),
        }

        self._logger.info("Calling %s %s using params %s", http_verb, url, params)

        request = Request(
            method=http_verb,
            url=url,
            headers=headers,
            params=params,
            # TODO: Create more options. Not everything is json and not everyone has a body!
            data=payload,
            files=files,
        )

        use_one_shot_session = self.__session is None

        ctx_manager: contextlib.AbstractContextManager = cast(
            contextlib.AbstractContextManager,
            (
                self.__create_session()
                if use_one_shot_session
                else contextlib.nullcontext()
            ),
        )
        with ctx_manager:
            session = cast(
                Session, ctx_manager if use_one_shot_session else self.__session
            )

            prepared = session.prepare_request(request)
            response = session.send(prepared)

            if (
                response.status_code == HTTPStatus.UNAUTHORIZED.value
                and not has_reauthenticated
            ):
                self._logger.warning("Unauthorized - will try to refresh tokens")
                self._logger.debug("Refresh token used: %s", self.__refresh_token)
                self.refresh_tokens()
                return self._execute(
                    http_verb,
                    path,
                    request_body,
                    "application/json",
                    has_reauthenticated=True,
                )

            self._logger.info("Response %s - %s", response.status_code, response.text)
            self._logger.debug("Response headers %s", response.headers)

            self.__die_if_unauthorized(response)
            self.__raise_if_not_ok(response)

            return response

    @staticmethod
    def __die_if_unauthorized(response: Response) -> None:
        if response.status_code == HTTPStatus.UNAUTHORIZED.value:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise FortnoxError(
                    message="Unauthorized even after trying to refresh tokens",
                    error_code=None,
                    original_exception=e,
                ) from e

    def __raise_if_not_ok(self, response: Response) -> None:
        try:
            response.raise_for_status()
        except HTTPError as e:
            try:
                as_json = response.json()
                error_info = as_json.get("ErrorInformation")
                if error_info:
                    message = error_info.get("message", "Unknown error")
                    status_code = error_info.get("code", -1)
                else:
                    message = error_info.get("Unknown error")
                    status_code = None
            except JSONDecodeError:
                self._logger.warning(
                    "Error response is not JSON - falling back to text."
                )
                message = response.text
                status_code = None

            self._logger.warning("Response is not OK. Raising.")
            raise FortnoxError(
                message=message, error_code=status_code, original_exception=e
            ) from e

    class Warehouse:
        def __init__(self, parent: "Fortpyx"):
            self.parent = parent
            self.manual_document = Fortpyx.Warehouse.ManualDocument(self, parent)
            self.manual_inbound_document = Fortpyx.Warehouse.ManualInboundDocument(
                self, parent
            )
            self.manual_outbound_document = Fortpyx.Warehouse.ManualOutboundDocument(
                self, parent
            )
            self.custom_document_type = Fortpyx.Warehouse.CustomDocumentType(
                self, parent
            )
            self.custom_inbound_document = Fortpyx.Warehouse.CustomInboundDocument(
                self, parent
            )
            self.custom_outbound_document = Fortpyx.Warehouse.CustomOutboundDocument(
                self, parent
            )
            self.incoming_goods = Fortpyx.Warehouse.IncomingGoods(self, parent)
            self.production_order = Fortpyx.Warehouse.ProductionOrder(self, parent)
            self.purchase_order = Fortpyx.Warehouse.PurchaseOrder(self, parent)
            self.stock_status = Fortpyx.Warehouse.StockStatus(self, parent)
            self.stock_point = Fortpyx.Warehouse.StockPoint(self, parent)
            self.stock_taking = Fortpyx.Warehouse.StockTaking(self, parent)
            self.stock_transfer = Fortpyx.Warehouse.StockTransfer(self, parent)
            self.tenant = Fortpyx.Warehouse.Tenant(self, parent)

        class ManualDocument:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list_manual_documents(
                self,
                state: Optional[
                    Literal["all", "unreleased", "released", "voided"]
                ] = None,
                type: Optional[
                    Literal["all", "inbound", "outbound", "stocktransfer"]
                ] = None,
                item_id: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseManualDocument:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/deliveries-v1",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "state": state,
                        "type": type,
                        "itemId": item_id,
                    },
                )

                return WarehouseManualDocument.model_validate_json(response.text)

        class ManualInboundDocument:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            def create_manual_inbound_document(
                self, request_body: WarehouseManualInboundDocument
            ) -> WarehouseManualInboundDocument:
                """
                The id is set automatically."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/deliveries-v1/inbounddeliveries",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseManualInboundDocument.model_validate_json(response.text)

            @auto_consume_pages
            def get_manual_inbound_document(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseManualInboundDocument:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/deliveries-v1/inbounddeliveries/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseManualInboundDocument.model_validate_json(response.text)

            def update_note_on_manual_inbound_document(
                self,
                request_body: WarehouseManualInboundDocumentPatch,
                resource_id: str,
            ) -> WarehouseWebException:
                """
                When a Manual Inbound has been released, it is locked.
                The note field can still be updated using this endpoint."""
                response = self.top._execute(  # noqa
                    http_verb="patch",
                    path=f"/api/warehouse/deliveries-v1/inbounddeliveries/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseWebException.model_validate_json(response.text)

            def update_manual_inbound_document(
                self, request_body: WarehouseManualInboundDocument, resource_id: str
            ) -> WarehouseManualInboundDocument:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/deliveries-v1/inbounddeliveries/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseManualInboundDocument.model_validate_json(response.text)

            def release_manual_inbound_document(
                self, resource_id: str
            ) -> WarehouseWebException:
                """
                The document will be locked and bookkept.

                The following error codes might be thrown:

                 cannot_release_later_than_current_date
                   Document date cannot be in the future.
                 document_is_voided
                   Document is voided.
                 period_locked
                   Document date is within a locked bookkeeping period.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/deliveries-v1/inbounddeliveries/{resource_id}/release",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

            def void_manual_inbound_document(
                self,
                resource_id: str,
                force: Optional[bool] = None,
                custom_void_date: Optional[str] = None,
            ) -> WarehouseWebException:
                """
                A released manual inbound document might have connected outbounds, and can only be force voided.
                Note that a force void operation might cause a negative stock.

                The following error codes might be thrown:

                 void_linked_outbound
                   If this document has any outbounds transactions connected to it.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/deliveries-v1/inbounddeliveries/{resource_id}/void",
                    request_body=None,
                    query_params={
                        "force": force,
                        "customVoidDate": custom_void_date,
                    },
                )

                return WarehouseWebException.model_validate_json(response.text)

        class ManualOutboundDocument:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            def create_manual_outbound_document(
                self, request_body: WarehouseManualOutboundDocument
            ) -> WarehouseManualOutboundDocument:
                """
                The id is set automatically."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/deliveries-v1/outbounddeliveries",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseManualOutboundDocument.model_validate_json(
                    response.text
                )

            @auto_consume_pages
            def get_manual_outbound_document(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseManualOutboundDocument:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/deliveries-v1/outbounddeliveries/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseManualOutboundDocument.model_validate_json(
                    response.text
                )

            def update_note_on_manual_outbound_document(
                self,
                request_body: WarehouseManualOutboundDocumentPatch,
                resource_id: str,
            ) -> WarehouseWebException:
                """
                When a Manual Outbound has been released, it is locked.
                The note field can still be updated using this endpoint."""
                response = self.top._execute(  # noqa
                    http_verb="patch",
                    path=f"/api/warehouse/deliveries-v1/outbounddeliveries/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseWebException.model_validate_json(response.text)

            def update_manual_outbound_document(
                self, request_body: WarehouseManualOutboundDocument, resource_id: str
            ) -> WarehouseManualOutboundDocument:
                """
                HTTP code 400 cannot_modify_released_document
                HTTP code 400 document_is_voided Document is voided.
                HTTP code 404 not found"""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/deliveries-v1/outbounddeliveries/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseManualOutboundDocument.model_validate_json(
                    response.text
                )

            def release_manual_outbound_document(
                self, resource_id: str
            ) -> WarehouseWebException:
                """
                The document will be locked and bookkept.

                The following error codes might be thrown:

                 cannot_release_later_than_current_date
                   Document date cannot be in the future.
                 document_is_voided
                   Document is voided.
                 period_locked
                   Document date is within a locked bookkeeping period.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/deliveries-v1/outbounddeliveries/{resource_id}/release",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

            def void_manual_outbound_document(
                self, resource_id: str, custom_void_date: Optional[str] = None
            ) -> WarehouseWebException:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/deliveries-v1/outbounddeliveries/{resource_id}/void",
                    request_body=None,
                    query_params={
                        "customVoidDate": custom_void_date,
                    },
                )

                return WarehouseWebException.model_validate_json(response.text)

        class CustomDocumentType:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list_custom_document_types(
                self, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseCustomDocumentType:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/documentdeliveries/custom/documenttypes-v1",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseCustomDocumentType.model_validate_json(response.text)

            def create_custom_document_type(
                self, request_body: WarehouseCustomDocumentType
            ) -> int:
                """Create type, if it doesn't already exists. Note that new custom document types are
                created automatically when you create custom documents, so normally
                you do not need to call this method.

                Throws HTTP 400 referenceTypeNotAllowed if the name of the type is not allowed.
                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/documentdeliveries/custom/documenttypes-v1",
                    request_body=request_body,
                    content_type="application/json",
                )

                return response.json()

            @auto_consume_pages
            def get_custom_document_type(
                self, type: str, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseCustomDocumentType:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/documentdeliveries/custom/documenttypes-v1/{type}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseCustomDocumentType.model_validate_json(response.text)

        class CustomInboundDocument:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def get_custom_inbound_document(
                self,
                type: str,
                resource_id: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseCustomInboundDocument:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/documentdeliveries/custom/inbound-v1/{type}/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseCustomInboundDocument.model_validate_json(response.text)

            def save_custom_inbound_document(
                self,
                request_body: WarehouseCustomInboundDocument,
                type: str,
                resource_id: str,
            ) -> WarehouseCustomInboundDocument:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/documentdeliveries/custom/inbound-v1/{type}/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseCustomInboundDocument.model_validate_json(response.text)

            def release_custom_inbound_document(
                self, type: str, resource_id: str
            ) -> WarehouseWebException:
                """The document will be locked and bookkept.
                The inbound deliveries will affect available stock."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/documentdeliveries/custom/inbound-v1/{type}/{resource_id}/release",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

            def void_custom_inbound_document(
                self, type: str, resource_id: str, force: Optional[bool] = None
            ) -> WarehouseWebException:
                """Voiding a document will undo the possible stock changes that the document had made,
                note that the document and the transactions created are not deleted. Some limitations apply, see below.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/documentdeliveries/custom/inbound-v1/{type}/{resource_id}/void",
                    request_body=None,
                    query_params={
                        "force": force,
                    },
                )

                return WarehouseWebException.model_validate_json(response.text)

        class CustomOutboundDocument:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def get_custom_outbound_document(
                self,
                type: str,
                resource_id: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseCustomOutboundDocument:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/documentdeliveries/custom/outbound-v1/{type}/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseCustomOutboundDocument.model_validate_json(
                    response.text
                )

            def save_a_custom_outbound_document(
                self,
                request_body: WarehouseCustomOutboundDocument,
                type: str,
                resource_id: str,
            ) -> WarehouseCustomOutboundDocument:
                """
                If type is not known, it will be registered as belonging to the OUTBOUND category.
                If type is an existing custom document type of category INBOUND an error is thrown.
                If type is invalid an error is thrown."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/documentdeliveries/custom/outbound-v1/{type}/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseCustomOutboundDocument.model_validate_json(
                    response.text
                )

            def release_custom_outbound_document(
                self, type: str, resource_id: str
            ) -> WarehouseWebException:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/documentdeliveries/custom/outbound-v1/{type}/{resource_id}/release",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

            def void_custom_outbound_document(
                self, type: str, resource_id: str, force: Optional[bool] = None
            ) -> WarehouseWebException:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/documentdeliveries/custom/outbound-v1/{type}/{resource_id}/void",
                    request_body=None,
                    query_params={
                        "force": force,
                    },
                )

                return WarehouseWebException.model_validate_json(response.text)

        class IncomingGoods:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list__incoming__goods__documents(
                self,
                released: Optional[bool] = None,
                completed: Optional[bool] = None,
                voided: Optional[bool] = None,
                supplier_number: Optional[str] = None,
                item_id: Optional[str] = None,
                note: Optional[str] = None,
                delivery_note: Optional[str] = None,
                q: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> Sequence[WarehouseIncomingGoodsListRow]:
                """
                List incoming goods documents matching the given parameters.


                Sortable fields:
                id,
                has_delivery_note,
                delivery_note_id,
                supplier_number,
                date
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/incominggoods-v1",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "released": released,
                        "completed": completed,
                        "voided": voided,
                        "supplierNumber": supplier_number,
                        "itemId": item_id,
                        "note": note,
                        "deliveryNote": delivery_note,
                        "q": q,
                    },
                )

                return response.json()

            def create__incoming__goods_document(
                self, request_body: WarehouseIncomingGoods
            ) -> WarehouseIncomingGoods:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/incominggoods-v1",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseIncomingGoods.model_validate_json(response.text)

            @auto_consume_pages
            def get__incoming__goods_document(
                self,
                resource_id: str,
                ignore_supplier_invoice_id: Optional[int] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseIncomingGoods:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/incominggoods-v1/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "ignoreSupplierInvoiceId": ignore_supplier_invoice_id,
                    },
                )

                return WarehouseIncomingGoods.model_validate_json(response.text)

            def partial_update__incoming__goods_document(
                self, request_body: WarehouseIncomingGoods, resource_id: str
            ) -> WarehouseIncomingGoods:
                """Perform a partial update of an IncomingGoods document. The partial update will update
                note, deliveryNoteId, supplierName and hasDeliveryNote
                It is possible to perform a partial update of a released/completed (TODO: ?) document.
                """
                response = self.top._execute(  # noqa
                    http_verb="patch",
                    path=f"/api/warehouse/incominggoods-v1/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseIncomingGoods.model_validate_json(response.text)

            def update__incoming__goods_document(
                self, request_body: WarehouseIncomingGoods, resource_id: str
            ) -> WarehouseIncomingGoods:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/incominggoods-v1/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseIncomingGoods.model_validate_json(response.text)

            def complete__incoming__goods_document(
                self, request_body: str, resource_id: str
            ) -> WarehouseWebException:
                """Mark a released Incoming Goods document as Completed.
                Bookkeeping will be finalized.
                A Completed Incoming Goods document cannot be matched against
                any more Supplier Invoices."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/incominggoods-v1/{resource_id}/completed",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseWebException.model_validate_json(response.text)

            def release__incoming__goods_document(
                self, resource_id: str
            ) -> WarehouseWebException:
                """The document will be locked and bookkept.
                The inbound deliveries will affect available stock."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/incominggoods-v1/{resource_id}/release",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

            def void__incoming__goods_document(
                self, resource_id: str
            ) -> WarehouseWebException:
                """Void a document.
                If an Incoming Goods document has been Completed, or matched against
                Supplier Invoice, it cannot be voided."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/incominggoods-v1/{resource_id}/void",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

        class ProductionOrder:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list_production_orders(
                self,
                state: Optional[
                    Literal["all", "incomplete", "delayed", "completed", "voided"]
                ] = None,
                item_id: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseProductionOrder:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/productionorders-v1",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "state": state,
                        "itemId": item_id,
                    },
                )

                return WarehouseProductionOrder.model_validate_json(response.text)

            def create_a_new_production_order(
                self, request_body: WarehouseProductionOrder
            ) -> WarehouseProductionOrder:
                """
                Set itemId to the item to be produced.

                Set quantity to number of units to produce.

                Set startDate to production start state.

                ProductionState is set to reserved by default.
                It can also be registered. Then no reservations
                will be made (no quantities will be assigned to the packageItems yet).

                Setting outboundStockPointId (where the packageItems
                will be taken from), and inboundStockPointId (where the
                produced item will be put) is mandatory multiple stockpoints has been activated
                in the warehouse settings.

                Before the document is released, the productionDate must be set.

                The packageItems to include is easiest to get by calling
                the method getRequiredProductionParts."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/productionorders-v1",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseProductionOrder.model_validate_json(response.text)

            @auto_consume_pages
            def get_the_package_items___bill__of__materials__bo_ms__for_a_production_article(
                self,
                item_resource_id: str,
                id: Optional[int] = None,
                quantity: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehousePackageItem:
                """
                If no parameters are supplied, the totalQuantityRequired for producing 1 unit is returned.

                Query parameter quantity can optionally be supplied, which will
                calculate totalQuantityRequired.

                If query parameter id is supplied, it will get the quantity from that
                Production Order (the quantity query parameter is ignored if id
                is included)."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/productionorders-v1/billofmaterials/{item_resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "id": id,
                        "quantity": quantity,
                    },
                )

                return WarehousePackageItem.model_validate_json(response.text)

            def release_a_production_order_document(
                self, resource_id: str
            ) -> WarehouseProductionOrder:
                """
                The document will be locked and bookkept.

                The following error codes might be thrown:

                 PRODUCTION_DATE_IS_EMPTY
                   Production date cannot be empty.
                 CANNOT_RELEASE_AFTER_CURRENT_DATE
                   Document date cannot be in the future.
                 DOCUMENT_IS_VOIDED
                    The document has been voided and can no longer be modified.
                 DOCUMENT_IS_RELEASED
                   The document has already been released and can no longer be modified.
                 DOCUMENT_NOT_FULLY_RESERVED
                   The documents package items (BOMs, Bill Of Materials) has not been fully reserved
                   (reserved quantity is not equal to total required quantity for one or more package item).
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/productionorders-v1/release/{resource_id}",
                    request_body=None,
                )

                return WarehouseProductionOrder.model_validate_json(response.text)

            def void_a_production_order(
                self, resource_id: str, force: Optional[bool] = None
            ) -> WarehouseWebException:
                """
                A released production order might have connected outbounds, and can only be force voided.
                Note that a force void operation might cause a negative stock."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/productionorders-v1/void/{resource_id}",
                    request_body=None,
                    query_params={
                        "force": force,
                    },
                )

                return WarehouseWebException.model_validate_json(response.text)

            @auto_consume_pages
            def get__production__order_document(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseProductionOrder:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/productionorders-v1/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseProductionOrder.model_validate_json(response.text)

            def update_the_note_of_a_production_order(
                self, request_body: WarehouseProductionOrderPatch, resource_id: str
            ) -> WarehouseProductionOrder:
                """
                When a Production Order has been released it is locked.
                However, the note field can still be updated using this endpoint."""
                response = self.top._execute(  # noqa
                    http_verb="patch",
                    path=f"/api/warehouse/productionorders-v1/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseProductionOrder.model_validate_json(response.text)

            def update_a_production_order(
                self, request_body: WarehouseProductionOrder, resource_id: str
            ) -> WarehouseProductionOrder:
                """
                Note that you must submit the full Production Order document
                when updating."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/productionorders-v1/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseProductionOrder.model_validate_json(response.text)

        class PurchaseOrder:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list__purchase__orders(
                self,
                q: Optional[str] = None,
                supplier_number: Optional[str] = None,
                state: Optional[
                    Literal[
                        "NOT_SENT",
                        "SENT",
                        "SENT_NOT_REJECTED",
                        "DELAYED",
                        "RECEIVED",
                        "VOIDED",
                        "CURRENT",
                        "ALL",
                    ]
                ] = None,
                item_id: Optional[str] = None,
                purchase_type: Optional[Literal["WAREHOUSE", "DROPSHIP"]] = None,
                internal_reference: Optional[str] = None,
                note: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehousePurchaseOrder:
                """
                List purchase orders matching the given parameters.


                Sortable fields:
                id,
                supplier_number,
                order_date,
                internal_reference,
                response_state,
                delivery_date
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/purchaseorders-v1",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "q": q,
                        "supplierNumber": supplier_number,
                        "state": state,
                        "itemId": item_id,
                        "purchaseType": purchase_type,
                        "internalReference": internal_reference,
                        "note": note,
                    },
                )

                return WarehousePurchaseOrder.model_validate_json(response.text)

            def create__purchase__order(
                self, request_body: WarehousePurchaseOrder
            ) -> WarehousePurchaseOrder:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/purchaseorders-v1",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehousePurchaseOrder.model_validate_json(response.text)

            @auto_consume_pages
            def get_csv_list_of__purchase__orders(
                self,
                q: Optional[str] = None,
                supplier_number: Optional[str] = None,
                state: Optional[
                    Literal[
                        "NOT_SENT",
                        "SENT",
                        "SENT_NOT_REJECTED",
                        "DELAYED",
                        "RECEIVED",
                        "VOIDED",
                        "CURRENT",
                        "ALL",
                    ]
                ] = None,
                item_id: Optional[str] = None,
                purchase_type: Optional[Literal["WAREHOUSE", "DROPSHIP"]] = None,
                internal_reference: Optional[str] = None,
                note: Optional[str] = None,
                show_purchase_type_column: Optional[bool] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> str:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/purchaseorders-v1/csv",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "q": q,
                        "supplierNumber": supplier_number,
                        "state": state,
                        "itemId": item_id,
                        "purchaseType": purchase_type,
                        "internalReference": internal_reference,
                        "note": note,
                        "showPurchaseTypeColumn": show_purchase_type_column,
                    },
                )

                return response.json()

            def update_response_states(
                self,
                request_body: WarehouseResponseStateChange,
                ids: Optional[int] = None,
            ) -> WarehousePurchaseOrder:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path="/api/warehouse/purchaseorders-v1/response",
                    request_body=request_body,
                    content_type="application/json",
                    query_params={
                        "ids": ids,
                    },
                )

                return WarehousePurchaseOrder.model_validate_json(response.text)

            def sends_multiple_purchase_orders_via_email(
                self, request_body: Sequence[int]
            ) -> WarehouseWebException:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/purchaseorders-v1/sendpurchaseorders",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseWebException.model_validate_json(response.text)

            @auto_consume_pages
            def get__purchase__order(
                self,
                resource_id: str,
                ignore_incoming_goods_id: Optional[int] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehousePurchaseOrder:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "ignoreIncomingGoodsId": ignore_incoming_goods_id,
                    },
                )

                return WarehousePurchaseOrder.model_validate_json(response.text)

            def update__purchase__order(
                self, request_body: WarehousePurchaseOrder, resource_id: str
            ) -> WarehousePurchaseOrder:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehousePurchaseOrder.model_validate_json(response.text)

            def manually_complete__purchase__order(
                self, resource_id: str
            ) -> WarehouseWebException:
                """
                The purchase order will be treated as fully received.
                Any remaining quantity will be ignored."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}/complete",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

            def manually_complete_dropship_order(
                self, resource_id: str
            ) -> WarehouseReleaseParentOrder:
                """
                The dropship order will be treated as fully received.
                Any remaining quantity will be ignored."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}/dropshipcomplete",
                    request_body=None,
                )

                return WarehouseReleaseParentOrder.model_validate_json(response.text)

            @auto_consume_pages
            def list_matched_documents(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseDocumentReference:
                """
                Get a list of DocumentReference of linked/connected purchase orders to incoming goods and/or invoice document.
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}/matches",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseDocumentReference.model_validate_json(response.text)

            @auto_consume_pages
            def get_notes(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> WarehousePurchaseOrderRowNote:
                """
                Get notes for a purchase order."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}/notes",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehousePurchaseOrderRowNote.model_validate_json(response.text)

            def partial_update__purchase__order(
                self, request_body: WarehousePartialPurchaseOrder, resource_id: str
            ) -> WarehousePartialPurchaseOrder:
                """
                Perform a partial update of a purchase order, see PartialPurchaseOrder for possible
                fields that are updateable."""
                response = self.top._execute(  # noqa
                    http_verb="patch",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}/partial",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehousePartialPurchaseOrder.model_validate_json(response.text)

            def update_response_state(
                self, request_body: WarehouseResponseStateChange, resource_id: str
            ) -> WarehousePurchaseOrder:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}/response",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehousePurchaseOrder.model_validate_json(response.text)

            def send_purchase_order_via_email(
                self, request_body: WarehousePurchaseOrderMailSettings, resource_id: str
            ) -> WarehouseWebException:
                """
                Sends the purchase order with the specified id to the recipient and sets the purchase order state to SENT
                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}/send",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseWebException.model_validate_json(response.text)

            def void__purchase__order(self, resource_id: str) -> WarehouseWebException:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/purchaseorders-v1/{resource_id}/void",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

        class StockStatus:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def get_stock_balance(
                self,
                item_ids: Optional[str] = None,
                stock_point_codes: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseStockBalance:
                """
                Get stock balance for each stockpoint.

                Returns a list of itemId, stockPointCode,
                availableStock, inStock.

                (The difference between availableStock and inStock
                is the reserved amount.)"""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/status-v1/stockbalance",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "itemIds": item_ids,
                        "stockPointCodes": stock_point_codes,
                    },
                )

                return WarehouseStockBalance.model_validate_json(response.text)

        class StockPoint:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list_stock_points(
                self,
                q: Optional[str] = None,
                state: Optional[Literal["ALL", "ACTIVE", "INACTIVE"]] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseStockPoint:
                """
                List stock points, optionally include a query parameter `q` to filter on stock point code or name.

                Use query param `state` to filter on ACTIVE, INACTIVE or ALL (default is to include only ACTIVE stock points).

                Stock locations are NOT included in the response."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/stockpoints-v1",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "q": q,
                        "state": state,
                    },
                )

                return WarehouseStockPoint.model_validate_json(response.text)

            def create_stock_point(
                self, request_body: WarehouseStockPoint
            ) -> WarehouseStockPoint:
                """
                Both code and name are mandatory.

                If you want to set a custom delivery address for this stock point,
                you must remember to set usingCompanyAddress to false.

                Returns 400 alreadyexists if a stock point with same code already exists.

                Returns 400 duplicatestocklocations if two or more stock locations have the same code.
                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/stockpoints-v1",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseStockPoint.model_validate_json(response.text)

            @auto_consume_pages
            def get_stock_points(
                self,
                ids: Optional[str] = None,
                state: Optional[Literal["ALL", "ACTIVE", "INACTIVE"]] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseStockPoint:
                """
                Get stock points by IDs.

                Use query param `state` to filter on ACTIVE, INACTIVE or ALL (default is to include ALL stock points).

                Stock locations are NOT included in the response."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/stockpoints-v1/multi",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "ids": ids,
                        "state": state,
                    },
                )

                return WarehouseStockPoint.model_validate_json(response.text)

            def delete_stock_point(self, resource_id: str) -> WarehouseStockPoint:
                """
                Note that it is not allowed to delete a stock point that is in use."""
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/api/warehouse/stockpoints-v1/{resource_id}",
                    request_body=None,
                )

                return WarehouseStockPoint.model_validate_json(response.text)

            @auto_consume_pages
            def get_stock_point(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseStockPoint:
                """
                Get stock point by id or code."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/stockpoints-v1/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseStockPoint.model_validate_json(response.text)

            def append_stock_locations(
                self, request_body: WarehouseStockLocation, resource_id: str
            ) -> WarehouseStockLocation:
                """
                Add new stock locations to specific StockPoint.

                If you include an already existing stock location code, it will be ignored.
                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path=f"/api/warehouse/stockpoints-v1/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseStockLocation.model_validate_json(response.text)

            def update_stock_point(
                self, request_body: WarehouseStockPoint, resource_id: str
            ) -> WarehouseStockPoint:
                """
                Remember to supply the complete representation of stock point including stock locations.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/stockpoints-v1/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseStockPoint.model_validate_json(response.text)

            @auto_consume_pages
            def get_stock_locations(
                self,
                resource_id: str,
                q: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseStockLocation:
                """
                List stock locations for a specific stock point.

                Optionally include a query parameter `q` to filter on stock location code or name.
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/stockpoints-v1/{resource_id}/stocklocations",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "q": q,
                    },
                )

                return WarehouseStockLocation.model_validate_json(response.text)

        class StockTaking:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list_stock_takings(
                self,
                state: Optional[
                    Literal["all", "planning", "started", "completed", "voided"]
                ] = None,
                item_id: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseStockTaking:
                """
                Sortable fields:
                id,
                name,
                date,
                responsible,
                state
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/stocktaking-v1",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "state": state,
                        "itemId": item_id,
                    },
                )

                return WarehouseStockTaking.model_validate_json(response.text)

            def create_stock_taking(
                self, request_body: WarehouseStockTaking
            ) -> WarehouseStockTaking:
                """
                Create a new Stock Taking document.
                The only mandatory fields are name and responsible.
                state will be set to planning for a newly created document.

                The date-field is not mandatory for documents in state planning.
                However, when you update the state to started you have to provide a date.

                name is a descriptive name of the stock taking.

                responsible is the name of the responsible for the stock taking.

                rows are added after creation by using the addRows-method.

                projectId and costCenterCode are used for book-keeping, when the
                Stock Taking document is released.

                The field usingStockPoints is set from Warehouse system settings upon creation.
                If multiple stockpoints is used, then the rows will be per item-stockPoint-stockLocation.
                If multiple stockpoints is NOT used, then the rows will be per item-stockLocation.
                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/stocktaking-v1",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseStockTaking.model_validate_json(response.text)

            def delete__stock__taking_document(
                self, resource_id: str
            ) -> WarehouseWebException:
                """
                Permanently deletes a Stock Taking document and its rows.

                Only for documents in state planning and started."""
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

            @auto_consume_pages
            def get__stock__taking_document(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseStockTaking:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseStockTaking.model_validate_json(response.text)

            def update_a_stock_taking(
                self, request_body: WarehouseStockTaking, resource_id: str
            ) -> WarehouseStockTaking:
                """
                Updates can only be done when state is planning or started.

                All updatable fields (date, name, responsible,
                state, sortingId, costCenterCode, projectId)
                in the document head are set to supplied values.

                You cannot set state to completed or voided. Use endpoints
                release or void for this.

                The date-field is mandatory for documents in state started.

                When state is started you use this endpoint for setting the stock taken quantity.
                Only existing rows can be updated - no new rows will be created (use the addRows endpoint for this).
                Only the supplied rows will be updated. I.e. you don't have to send in all
                document rows - just supply the rows you want to set stockTakenQuantity for. Just make sure
                to always include all the fields from the document head as mentioned above.

                The mandatory fields on the (optionally supplied) rows are: itemId,
                stockPointId, stockLocationId.
                Fields countedBy and stockTakenQuantity are technically
                not mandatory, but will be set to null if you don't supply them."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseStockTaking.model_validate_json(response.text)

            def add_rows_by_filter(
                self,
                resource_id: str,
                item_ids: Optional[str] = None,
                supplier_numbers: Optional[str] = None,
                stock_point_ids: Optional[str] = None,
                stock_location_ids: Optional[str] = None,
                transaction_date: Optional[str] = None,
                item_id_search: Optional[str] = None,
                item_description_search: Optional[str] = None,
                exclude_zero_balance_items: Optional[bool] = None,
                exclude_non_inbound_items: Optional[bool] = None,
            ) -> int:
                """
                Add all matching candidate rows to a stock taking, as specified by filters.
                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}/addrows",
                    request_body=None,
                    query_params={
                        "itemIds": item_ids,
                        "supplierNumbers": supplier_numbers,
                        "stockPointIds": stock_point_ids,
                        "stockLocationIds": stock_location_ids,
                        "transactionDate": transaction_date,
                        "itemIdSearch": item_id_search,
                        "itemDescriptionSearch": item_description_search,
                        "excludeZeroBalanceItems": exclude_zero_balance_items,
                        "excludeNonInboundItems": exclude_non_inbound_items,
                    },
                )

                return response.json()

            @auto_consume_pages
            def get_candidate_rows(
                self,
                resource_id: str,
                item_ids: Optional[str] = None,
                supplier_numbers: Optional[str] = None,
                stock_point_ids: Optional[str] = None,
                stock_location_ids: Optional[str] = None,
                transaction_date: Optional[str] = None,
                item_id_search: Optional[str] = None,
                item_description_search: Optional[str] = None,
                exclude_zero_balance_items: Optional[bool] = None,
                include_non_inbound_items: Optional[bool] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseStockTakingRow:
                """
                A candidate row is a combination of itemId, stockPointId and stockLocationId
                that can be added to the Stock Taking document.

                Rows already added to the Stock Taking are excluded from this list."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}/candidates",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "itemIds": item_ids,
                        "supplierNumbers": supplier_numbers,
                        "stockPointIds": stock_point_ids,
                        "stockLocationIds": stock_location_ids,
                        "transactionDate": transaction_date,
                        "itemIdSearch": item_id_search,
                        "itemDescriptionSearch": item_description_search,
                        "excludeZeroBalanceItems": exclude_zero_balance_items,
                        "includeNonInboundItems": include_non_inbound_items,
                    },
                )

                return WarehouseStockTakingRow.model_validate_json(response.text)

            def release__stock__taking_document(
                self, resource_id: str
            ) -> WarehouseWebException:
                """
                The document will be locked and bookkept.
                The Stock Taking document state will be set to completed.
                The stock amount will be adjusted according to the stock taken quantity.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}/release",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

            def delete_rows_by_filter(
                self,
                resource_id: str,
                item_ids: Optional[str] = None,
                supplier_numbers: Optional[str] = None,
                stock_point_ids: Optional[str] = None,
                stock_location_ids: Optional[str] = None,
                transaction_date: Optional[str] = None,
                item_id_search: Optional[str] = None,
                item_description_search: Optional[str] = None,
                exclude_zero_balance_items: Optional[bool] = None,
            ) -> int:
                """
                Remove all rows matching the filter parameters from the Stock Taking document.
                """
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}/rows",
                    request_body=None,
                    query_params={
                        "itemIds": item_ids,
                        "supplierNumbers": supplier_numbers,
                        "stockPointIds": stock_point_ids,
                        "stockLocationIds": stock_location_ids,
                        "transactionDate": transaction_date,
                        "itemIdSearch": item_id_search,
                        "itemDescriptionSearch": item_description_search,
                        "excludeZeroBalanceItems": exclude_zero_balance_items,
                    },
                )

                return response.json()

            @auto_consume_pages
            def get__stock__taking__rows(
                self,
                resource_id: str,
                item_ids: Optional[str] = None,
                supplier_numbers: Optional[str] = None,
                stock_point_ids: Optional[str] = None,
                stock_location_ids: Optional[str] = None,
                transaction_date: Optional[str] = None,
                item_id_search: Optional[str] = None,
                item_description_search: Optional[str] = None,
                exclude_zero_balance_items: Optional[bool] = None,
                secondarysortby: Optional[str] = None,
                secondaryorder: Optional[str] = None,
                state_filter: Optional[
                    Literal[
                        "all",
                        "notStockTaken",
                        "stockTakenNoDeviation",
                        "stockTakenWithDeviation",
                    ]
                ] = None,
                starting_row_no: Optional[int] = None,
                starting_item_id: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> WarehouseStockTakingRow:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}/rows",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "itemIds": item_ids,
                        "supplierNumbers": supplier_numbers,
                        "stockPointIds": stock_point_ids,
                        "stockLocationIds": stock_location_ids,
                        "transactionDate": transaction_date,
                        "itemIdSearch": item_id_search,
                        "itemDescriptionSearch": item_description_search,
                        "excludeZeroBalanceItems": exclude_zero_balance_items,
                        "secondarysortby": secondarysortby,
                        "secondaryorder": secondaryorder,
                        "stateFilter": state_filter,
                        "startingRowNo": starting_row_no,
                        "startingItemId": starting_item_id,
                    },
                )

                return WarehouseStockTakingRow.model_validate_json(response.text)

            def add_rows(
                self, request_body: WarehouseStockTakingRow, resource_id: str
            ) -> WarehouseWebException:
                """
                Add rows to a stock taking.
                If you add an already existing row noting happens."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}/rows",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseWebException.model_validate_json(response.text)

            def delete_row(self, resource_id: str, row_resource_id: str) -> int:
                """
                Remove single row by id from the Stock Taking document."""
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}/rows/{row_resource_id}",
                    request_body=None,
                )

                return response.json()

            def void__stock__taking_document(
                self, resource_id: str
            ) -> WarehouseWebException:
                """
                Sets the Stock Taking document state to voided.

                Only documents in state planning and started
                can be voided. A completed document may not be voided."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/stocktaking-v1/{resource_id}/void",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

        class StockTransfer:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            def create_a_stock_transfer_document(
                self, request_body: WarehouseStockTransferDocument
            ) -> WarehouseStockTransferDocument:
                """
                Outbounds will be reserved in the from-place.
                Inbounds are created upon release of the stock transfer document."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/warehouse/stocktransfer-v1",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseStockTransferDocument.model_validate_json(response.text)

            @auto_consume_pages
            def get_stock_transfer_document(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseStockTransferDocument:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/warehouse/stocktransfer-v1/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseStockTransferDocument.model_validate_json(response.text)

            def update_a_stock_transfer_document(
                self, request_body: WarehouseStockTransferDocument, resource_id: str
            ) -> WarehouseStockTransferDocument:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/stocktransfer-v1/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return WarehouseStockTransferDocument.model_validate_json(response.text)

            def release_a_stock_transfer_document(
                self, resource_id: str
            ) -> WarehouseWebException:
                """
                This will deliver all outbounds which are reserved in from-place, and
                create inbounds in the to-place.
                Nothing happens if you releasr an already released stock transfer document.

                Returns document_is_voided if document is voided."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/stocktransfer-v1/{resource_id}/release",
                    request_body=None,
                )

                return WarehouseWebException.model_validate_json(response.text)

            def void_a_stock_transfer_document(
                self, resource_id: str, force: Optional[bool] = None
            ) -> WarehouseWebException:
                """
                Voiding a released stock transfer document is not allowed, and
                will return cannot_modify_released_document"""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/warehouse/stocktransfer-v1/{resource_id}/void",
                    request_body=None,
                    query_params={
                        "force": force,
                    },
                )

                return WarehouseWebException.model_validate_json(response.text)

        class Tenant:
            def __init__(self, closest_parent: "Fortpyx.Warehouse", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def get__warehouse_activation_status(
                self, page: int = 1, offset: Optional[int] = None
            ) -> WarehouseTenantInfo:
                """
                Check if current tenant has activated Fortnox Warehouse."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/warehouse/tenants-v4",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return WarehouseTenantInfo.model_validate_json(response.text)

    class TimeReporting:
        def __init__(self, parent: "Fortpyx"):
            self.parent = parent
            self.time_reporting__articles = Fortpyx.TimeReporting.TimeReportingArticles(
                self, parent
            )
            self.registrations = Fortpyx.TimeReporting.Registrations(self, parent)

        class TimeReportingArticles:
            def __init__(self, closest_parent: "Fortpyx.TimeReporting", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def get_full_article_registrations_that_match_filter(
                self,
                from_date: Optional[str] = None,
                to_date: Optional[str] = None,
                customer_ids: Optional[str] = None,
                project_ids: Optional[str] = None,
                include_registrations_without_project: Optional[bool] = None,
                item_ids: Optional[str] = None,
                cost_center_ids: Optional[str] = None,
                owner_ids: Optional[str] = None,
                invoiced: Optional[bool] = None,
                in_invoice_basis: Optional[bool] = None,
                internal_articles: Optional[bool] = None,
                non_invoiceable: Optional[bool] = None,
                include_non_invoiceable_price: Optional[bool] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> Sequence[TimeReportingBaseArticleRegistration]:
                """
                Response property descriptions:
                &nbsp;&nbsp;&nbsp;&nbsp;    id - The unique id of a basic common combination of article registrations. (The basic common combination means "user/purchase date/customer/project/cost center", which leads to a dialog with several article registrations.)
                &nbsp;&nbsp;&nbsp;&nbsp;    purchaseDate - The date on which the article is purchased or registered for charging.
                &nbsp;&nbsp;&nbsp;&nbsp;    ownerId - The user ID who creates the basic common combination.
                &nbsp;&nbsp;&nbsp;&nbsp;    version - The version of the basic common combination (article dialog) being updated, which is used for handling the concurrency issue.
                &nbsp;&nbsp;&nbsp;&nbsp;    registrationType - It is always "ARTICLE" for article list endpoint.
                &nbsp;&nbsp;&nbsp;&nbsp;    Sub-Class - ArticleRegistration:
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        id - The unique id of an article registration.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        registrationId - The id of the basic common combination.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        orderIndex - the order index for the article registration in regard of the common combination.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        ownerId - The user ID who owns the article registration.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        totalQuantity - The quantity of the article.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        unitPrice - The unit price connected to the article registration, which might be locked on an invoice/order basis or for non-invoiceable.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        unitCost - The unit cost connected to the article registration, which might be locked on an invoice/order basis.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        invoiceBasisId - The ID of invoice/order basis which is used for creating an invoice/order.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        nonInvoiceable - If the article registration would be ignored for charging or not.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        note - The note on the article registration.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        documentId - The document ID which includes the article registration and is created in Invoicing application.
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        documentType - The document type which could be "invoice" or "order".
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/time/articles-v1",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "fromDate": from_date,
                        "toDate": to_date,
                        "customerIds": customer_ids,
                        "projectIds": project_ids,
                        "includeRegistrationsWithoutProject": include_registrations_without_project,
                        "itemIds": item_ids,
                        "costCenterIds": cost_center_ids,
                        "ownerIds": owner_ids,
                        "invoiced": invoiced,
                        "inInvoiceBasis": in_invoice_basis,
                        "internalArticles": internal_articles,
                        "nonInvoiceable": non_invoiceable,
                        "includeNonInvoiceablePrice": include_non_invoiceable_price,
                    },
                )

                return response.json()

        class Registrations:
            def __init__(self, closest_parent: "Fortpyx.TimeReporting", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def get_time_absence_registrations_that_match_filter(
                self,
                from_date: Optional[str] = None,
                to_date: Optional[str] = None,
                customer_ids: Optional[str] = None,
                project_ids: Optional[str] = None,
                service_ids: Optional[str] = None,
                cost_center_ids: Optional[str] = None,
                reg_codes: Optional[str] = None,
                user_ids: Optional[str] = None,
                include_registrations_without_project: Optional[bool] = None,
                invoiced: Optional[bool] = None,
                in_invoice_basis: Optional[bool] = None,
                internal_time: Optional[bool] = None,
                non_invoiceable: Optional[bool] = None,
                include_non_invoiceable_charge_hours: Optional[bool] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> Sequence[TimeReportingDetailedRegistration]:
                """
                Response property descriptions:
                &nbsp;&nbsp;&nbsp;&nbsp;    id - The unique id of the registration.
                &nbsp;&nbsp;&nbsp;&nbsp;    userId - The user ID who owns the registration.
                &nbsp;&nbsp;&nbsp;&nbsp;    workedDate - The date for which the registration is created.
                &nbsp;&nbsp;&nbsp;&nbsp;    workedHours - The time spent, or the time of absence.
                &nbsp;&nbsp;&nbsp;&nbsp;    startTime - The start of clock time.
                &nbsp;&nbsp;&nbsp;&nbsp;    stopTime - The end of clock time.
                &nbsp;&nbsp;&nbsp;&nbsp;    invoiceText - The text to be included in the invoice/order basis which would be used to create an invoice/order.
                &nbsp;&nbsp;&nbsp;&nbsp;    note - The note on the registration.
                &nbsp;&nbsp;&nbsp;&nbsp;    chargeHours - The time to be invoiced, or 0 for the absence, or locked for non-invoiceable.
                &nbsp;&nbsp;&nbsp;&nbsp;    childId - The child ID related to the absence registration of parental leave (FPE), which comes from Payroll application.
                &nbsp;&nbsp;&nbsp;&nbsp;    nonInvoiceable - If the registration would be ignored for charging or not.
                &nbsp;&nbsp;&nbsp;&nbsp;    invoiceBasisId - The ID of invoice/order basis which is used for creating an invoice/order.
                &nbsp;&nbsp;&nbsp;&nbsp;    documentId - The document ID which includes the registration and is created in Invoicing application.
                &nbsp;&nbsp;&nbsp;&nbsp;    documentType - The document type which could be "invoice" or "order".
                &nbsp;&nbsp;&nbsp;&nbsp;    unitCost - The unit cost from the registration owner who takes the work.
                &nbsp;&nbsp;&nbsp;&nbsp;    unitPrice - The unit price for the service on the registration, which comes in priority from "invoice/order basis", "price group" or "service".
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/time/registrations-v2",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "fromDate": from_date,
                        "toDate": to_date,
                        "customerIds": customer_ids,
                        "projectIds": project_ids,
                        "serviceIds": service_ids,
                        "costCenterIds": cost_center_ids,
                        "regCodes": reg_codes,
                        "userIds": user_ids,
                        "includeRegistrationsWithoutProject": include_registrations_without_project,
                        "invoiced": invoiced,
                        "inInvoiceBasis": in_invoice_basis,
                        "internalTime": internal_time,
                        "nonInvoiceable": non_invoiceable,
                        "includeNonInvoiceableChargeHours": include_non_invoiceable_charge_hours,
                    },
                )

                return response.json()

    class Fortnox:
        def __init__(self, parent: "Fortpyx"):
            self.parent = parent
            self.absence_transactions = Fortpyx.Fortnox.AbsenceTransactions(
                self, parent
            )
            self.account_charts = Fortpyx.Fortnox.AccountCharts(self, parent)
            self.accounts = Fortpyx.Fortnox.Accounts(self, parent)
            self.archive = Fortpyx.Fortnox.Archive(self, parent)
            self.article_file_connections = Fortpyx.Fortnox.ArticleFileConnections(
                self, parent
            )
            self.articles = Fortpyx.Fortnox.Articles(self, parent)
            self.asset_file_connection = Fortpyx.Fortnox.AssetFileConnection(
                self, parent
            )
            self.assets = Fortpyx.Fortnox.Assets(self, parent)
            self.asset_types = Fortpyx.Fortnox.AssetTypes(self, parent)
            self.attendance_transactions = Fortpyx.Fortnox.AttendanceTransactions(
                self, parent
            )
            self.company_information = Fortpyx.Fortnox.CompanyInformation(self, parent)
            self.contract_accruals = Fortpyx.Fortnox.ContractAccruals(self, parent)
            self.contracts = Fortpyx.Fortnox.Contracts(self, parent)
            self.contract_templates = Fortpyx.Fortnox.ContractTemplates(self, parent)
            self.cost_centers = Fortpyx.Fortnox.CostCenters(self, parent)
            self.currencies = Fortpyx.Fortnox.Currencies(self, parent)
            self.customer_references = Fortpyx.Fortnox.CustomerReferences(self, parent)
            self.customers = Fortpyx.Fortnox.Customers(self, parent)
            self.trusted_email_senders = Fortpyx.Fortnox.TrustedEmailSenders(
                self, parent
            )
            self.employees = Fortpyx.Fortnox.Employees(self, parent)
            self.eu_vat_limit_regulation = Fortpyx.Fortnox.EuVatLimitRegulation(
                self, parent
            )
            self.expenses = Fortpyx.Fortnox.Expenses(self, parent)
            self.financial_years = Fortpyx.Fortnox.FinancialYears(self, parent)
            self.inbox = Fortpyx.Fortnox.Inbox(self, parent)
            self.invoice_accruals = Fortpyx.Fortnox.InvoiceAccruals(self, parent)
            self.invoice_payments = Fortpyx.Fortnox.InvoicePayments(self, parent)
            self.invoices = Fortpyx.Fortnox.Invoices(self, parent)
            self.labels = Fortpyx.Fortnox.Labels(self, parent)
            self.me = Fortpyx.Fortnox.Me(self, parent)
            self.modes_of_payments = Fortpyx.Fortnox.ModesOfPayments(self, parent)
            self.finance_invoices = Fortpyx.Fortnox.FinanceInvoices(self, parent)
            self.offers = Fortpyx.Fortnox.Offers(self, parent)
            self.orders = Fortpyx.Fortnox.Orders(self, parent)
            self.predefined_accounts = Fortpyx.Fortnox.PredefinedAccounts(self, parent)
            self.predefined_voucher_series = Fortpyx.Fortnox.PredefinedVoucherSeries(
                self, parent
            )
            self.price_lists = Fortpyx.Fortnox.PriceLists(self, parent)
            self.prices = Fortpyx.Fortnox.Prices(self, parent)
            self.print_templates = Fortpyx.Fortnox.PrintTemplates(self, parent)
            self.projects = Fortpyx.Fortnox.Projects(self, parent)
            self.salary_transactions = Fortpyx.Fortnox.SalaryTransactions(self, parent)
            self.schedule_times = Fortpyx.Fortnox.ScheduleTimes(self, parent)
            self.company_settings = Fortpyx.Fortnox.CompanySettings(self, parent)
            self.locked_period = Fortpyx.Fortnox.LockedPeriod(self, parent)
            self.sie = Fortpyx.Fortnox.Sie(self, parent)
            self.supplier_invoice_accruals = Fortpyx.Fortnox.SupplierInvoiceAccruals(
                self, parent
            )
            self.supplier_invoice_external_url_connections = (
                Fortpyx.Fortnox.SupplierInvoiceExternalUrlConnections(self, parent)
            )
            self.supplier_invoice_file_connections = (
                Fortpyx.Fortnox.SupplierInvoiceFileConnections(self, parent)
            )
            self.supplier_invoice_payments = Fortpyx.Fortnox.SupplierInvoicePayments(
                self, parent
            )
            self.supplier_invoices = Fortpyx.Fortnox.SupplierInvoices(self, parent)
            self.suppliers = Fortpyx.Fortnox.Suppliers(self, parent)
            self.tax_reductions = Fortpyx.Fortnox.TaxReductions(self, parent)
            self.terms_of_deliveries = Fortpyx.Fortnox.TermsOfDeliveries(self, parent)
            self.terms_of_payments = Fortpyx.Fortnox.TermsOfPayments(self, parent)
            self.units = Fortpyx.Fortnox.Units(self, parent)
            self.vacation_debt_basis = Fortpyx.Fortnox.VacationDebtBasis(self, parent)
            self.voucher_file_connections = Fortpyx.Fortnox.VoucherFileConnections(
                self, parent
            )
            self.vouchers = Fortpyx.Fortnox.Vouchers(self, parent)
            self.voucher_series = Fortpyx.Fortnox.VoucherSeries(self, parent)
            self.way_of_deliveries = Fortpyx.Fortnox.WayOfDeliveries(self, parent)

        class AbsenceTransactions:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def lists_all_absence_transactions(
                self,
                employeeid: Optional[str] = None,
                date: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxAbsenceTransactionListItemWrap:
                """Supports query-string parameters employeeid and date for filtering the result."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/absencetransactions",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "employeeid": employeeid,
                        "date": date,
                    },
                )

                return FortnoxAbsenceTransactionListItemWrap.model_validate_json(
                    response.text
                )

            def create_a_new_absence_transaction(
                self, request_body: FortnoxAbsenceTransactionPayloadWrap
            ) -> FortnoxAbsenceTransactionSingleItemWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/absencetransactions",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAbsenceTransactionSingleItemWrap.model_validate_json(
                    response.text
                )

            @auto_consume_pages
            def retrieve_absence_transactions(
                self,
                employee_resource_id: str,
                date: str,
                code: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxAbsenceTransactionListItemWrap:
                """Retrieves a list of absence transactions for an employee on a specific date and cause code."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/absencetransactions/{employee_resource_id}/{date}/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAbsenceTransactionListItemWrap.model_validate_json(
                    response.text
                )

            def delete_an_absence_transaction(
                self, resource_id: str
            ) -> FortnoxAbsenceTransactionSingleItemWrap:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/absencetransactions/{resource_id}",
                    request_body=None,
                )

                return FortnoxAbsenceTransactionSingleItemWrap.model_validate_json(
                    response.text
                )

            @auto_consume_pages
            def retrieve_a_specific_absence_transaction(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxAbsenceTransactionSingleItemWrap:
                """Retrieves a specific transaction"""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/absencetransactions/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAbsenceTransactionSingleItemWrap.model_validate_json(
                    response.text
                )

            def update_a_single_absence_transaction(
                self,
                request_body: FortnoxAbsenceTransactionPayloadWrap,
                resource_id: str,
            ) -> FortnoxAbsenceTransactionSingleItemWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/absencetransactions/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAbsenceTransactionSingleItemWrap.model_validate_json(
                    response.text
                )

        class AccountCharts:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list_all_account_charts(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxAccountChartWrap:
                """Retrieves a list of all the available account charts."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/accountcharts",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAccountChartWrap.model_validate_json(response.text)

        class Accounts:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list_all_accounts(
                self,
                lastmodified: Optional[str] = None,
                sru: Optional[int] = None,
                sortby: Optional[Literal["number"]] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxAccountListItemWrap:
                """The accounts are returned sorted by account number with the lowest number appearing first."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/accounts",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "lastmodified": lastmodified,
                        "sru": sru,
                        "sortby": sortby,
                    },
                )

                return FortnoxAccountListItemWrap.model_validate_json(response.text)

            def create_an_account(
                self,
                request_body: FortnoxAccountPayloadWrap,
                financialyear: Optional[int] = None,
            ) -> FortnoxAccountSingleItemWrap:
                """The created account will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/accounts",
                    request_body=request_body,
                    content_type="application/json",
                    query_params={
                        "financialyear": financialyear,
                    },
                )

                return FortnoxAccountSingleItemWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_an_account(
                self, number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxAccountSingleItemWrap:
                """Retrieves the details of an account. You need to supply the unique account number that was returned when the account was created or retrieved from the list of accounts."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/accounts/{number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAccountSingleItemWrap.model_validate_json(response.text)

            def update_an_account(
                self,
                request_body: FortnoxAccountPayloadWrap,
                number: str,
                financialyear: Optional[int] = None,
            ) -> FortnoxAccountSingleItemWrap:
                """Updates the specified account with the values provided in the properties. Any property not provided will be left unchanged.
                Note that even though the account number is writeable you can&acute;t change the number of an existing account.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/accounts/{number}",
                    request_body=request_body,
                    content_type="application/json",
                    query_params={
                        "financialyear": financialyear,
                    },
                )

                return FortnoxAccountSingleItemWrap.model_validate_json(response.text)

        class Archive:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            def remove_files(self, path: Optional[str] = None) -> FortnoxWebException:
                """Please note that removing a folder will also resulting in removal of all the contents within!"""
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path="/3/archive",
                    request_body=None,
                    query_params={
                        "path": path,
                    },
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_folder_or_file(
                self,
                path: Optional[str] = None,
                fileid: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxFolderWrap:
                """If no path is provided the root will be returned.
                Providing fileId will return given file from fileattachments."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/archive",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "path": path,
                        "fileid": fileid,
                    },
                )

                return FortnoxFolderWrap.model_validate_json(response.text)

            def upload_a_file_to_a_specific_subdirectory(
                self,
                request_body: UploadFile,
                path: Optional[str] = None,
                folderid: Optional[str] = None,
            ) -> FortnoxFolderFileRowWrap:
                """If not path or folderId is provided, the file will be uploaded to the root directory."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/archive",
                    request_body=request_body,
                    query_params={
                        "path": path,
                        "folderid": folderid,
                    },
                )

                return FortnoxFolderFileRowWrap.model_validate_json(response.text)

            def delete_a_single_file(self, resource_id: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/archive/{resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_file(
                self,
                resource_id: str,
                fileid: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> str:
                """Providing fileId will return given file from fileattachments."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/archive/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "fileid": fileid,
                    },
                )

                return response.json()

        class ArticleFileConnections:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_article_file_connections(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxArticleFileConnectionListItemWrap:
                """The article file connections register can return a list of records or a single record. By specifying a FileId in the URL, a single record will be returned. Not specifying a FileId will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/articlefileconnections",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxArticleFileConnectionListItemWrap.model_validate_json(
                    response.text
                )

            def create_an_article_file_connection(
                self, request_body: FortnoxArticleFileConnectionWrap
            ) -> FortnoxArticleFileConnectionWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/articlefileconnections",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxArticleFileConnectionWrap.model_validate_json(
                    response.text
                )

            def remove_an_article_file_connection(
                self, file_resource_id: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/articlefileconnections/{file_resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_article_file_connection(
                self, file_resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxArticleFileConnectionWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/articlefileconnections/{file_resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxArticleFileConnectionWrap.model_validate_json(
                    response.text
                )

        class Articles:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_articles(
                self,
                filter: Optional[Literal["active", "inactive"]] = None,
                articlenumber: Optional[str] = None,
                description: Optional[str] = None,
                ean: Optional[str] = None,
                suppliernumber: Optional[str] = None,
                manufacturer: Optional[str] = None,
                manufacturerarticlenumber: Optional[str] = None,
                webshop: Optional[str] = None,
                lastmodified: Optional[str] = None,
                sortby: Optional[
                    Literal[
                        "articlenumber",
                        "quantityinstock",
                        "reservedquantity",
                        "stockvalue",
                    ]
                ] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxArticleListItemList:
                """Retrieves a list of articles. The articles are returned sorted by article number with the lowest number appearing first."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/articles",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "filter": filter,
                        "articlenumber": articlenumber,
                        "description": description,
                        "ean": ean,
                        "suppliernumber": suppliernumber,
                        "manufacturer": manufacturer,
                        "manufacturerarticlenumber": manufacturerarticlenumber,
                        "webshop": webshop,
                        "lastmodified": lastmodified,
                        "sortby": sortby,
                    },
                )

                return FortnoxArticleListItemList.model_validate_json(response.text)

            def create_an_article(
                self, request_body: FortnoxArticleWrap
            ) -> FortnoxArticleWrap:
                """The created article will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/articles",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxArticleWrap.model_validate_json(response.text)

            def delete_an_article(self, article_number: str) -> FortnoxWebException:
                """Deletes the article permanently.
                You need to supply the unique article number that was returned when the article was created or retrieved from the list of articles.
                """
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/articles/{article_number}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_an_article(
                self, article_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxArticleWrap:
                """Retrieves the details of an article. You need to supply the unique article number that was returned when the article was created or retrieved from the list of articles."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/articles/{article_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxArticleWrap.model_validate_json(response.text)

            def update_an_article(
                self, request_body: FortnoxArticleWrap, article_number: str
            ) -> FortnoxArticleWrap:
                """Updates the specified article with the values provided in the properties. Any property not provided will be left unchanged.
                You need to supply the unique article number that was returned when the article was created or retrieved from the list of articles.
                Note that even though the article number is writeable you can not change the number of an existing article.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/articles/{article_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxArticleWrap.model_validate_json(response.text)

        class AssetFileConnection:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_asset_file_connections(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxAssetFileConnectionResponse:
                """The asset register can return a list of assets or a single asset. By specifying a FileId in the URL, a single asset will be returned. Not specifying a FileId will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/assetfileconnections",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAssetFileConnectionResponse.model_validate_json(
                    response.text
                )

            def create_an_asset_file_connection(
                self, request_body: FortnoxCreateAssetFileConnection
            ) -> FortnoxAssetFileConnection:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/assetfileconnections",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAssetFileConnection.model_validate_json(response.text)

            def remove_an_asset_file_connection(
                self, file_resource_id: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/assetfileconnections/{file_resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

        class Assets:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_assets(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxListAssetWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/assets",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxListAssetWrap.model_validate_json(response.text)

            def create_an__asset(
                self, request_body: FortnoxCreateAssetWrap
            ) -> FortnoxAssetSingle:
                """The created asset will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/assets",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAssetSingle.model_validate_json(response.text)

            def perform_a__depreciation_of_an__asset(
                self, request_body: FortnoxDepreciationWrap
            ) -> FortnoxDepreciationResponseWrap:
                """The created vouchers list will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/assets/depreciate",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxDepreciationResponseWrap.model_validate_json(
                    response.text
                )

            @auto_consume_pages
            def assets_depreciation_list(
                self, to_date: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxListAssetWrap:
                """Retrieves a list of assets to depreciate."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/assets/depreciations/{to_date}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxListAssetWrap.model_validate_json(response.text)

            def scrap_an__asset(
                self, request_body: FortnoxScrapWrap, given_number: str
            ) -> FortnoxAssetSingle:
                """The updated asset will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/assets/scrap/{given_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAssetSingle.model_validate_json(response.text)

            def sell_an__asset(
                self, request_body: FortnoxSellWrap, given_number: str
            ) -> FortnoxAssetSingle:
                """Partial sell or full sell of an asset."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/assets/sell/{given_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAssetSingle.model_validate_json(response.text)

            def write_down_an__asset(
                self, request_body: FortnoxWriteDownWrap, given_number: str
            ) -> FortnoxAssetSingle:
                """The updated asset will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/assets/writedown/{given_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAssetSingle.model_validate_json(response.text)

            def write_up_an__asset(
                self, request_body: FortnoxWriteUpWrap, given_number: str
            ) -> FortnoxAssetSingle:
                """The updated asset will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/assets/writeup/{given_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAssetSingle.model_validate_json(response.text)

            def delete_or__void_an__asset(
                self, request_body: FortnoxDeleteWrap, given_number: str
            ) -> FortnoxWebException:
                """By specifying a {GivenNumber} in the URL a single &quot;Not active&quot; asset or asset with a type &quot;Not depreciable&quot; can be deleted. By specifying a {GivenNumber} in the URL a single &quot;Active&quot; or &quot;Fully depreciated&quot; assets can be voided and in this case in request body voiddate should be provided, otherwise it will use todays date."""
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/assets/{given_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_asset(
                self, given_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxAssetSingle:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/assets/{given_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAssetSingle.model_validate_json(response.text)

            def change_manual_ob_value_of_an__asset(
                self, request_body: FortnoxManualObAsset, given_number: str
            ) -> FortnoxAssetSingle:
                """The updated asset will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/assets/{given_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAssetSingle.model_validate_json(response.text)

        class AssetTypes:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_asset_types(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxAssetTypeWrapList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/assets/types",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAssetTypeWrapList.model_validate_json(response.text)

            def delete_an_asset_type(self, resource_id: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/assets/types/{resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_an_asset_type(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxAssetTypeWrapSingle:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/assets/types/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAssetTypeWrapSingle.model_validate_json(response.text)

            def create_an_asset_type(
                self, request_body: FortnoxCreateAssetWrap, resource_id: str
            ) -> FortnoxAssetTypeWrapSingle:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path=f"/3/assets/types/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAssetTypeWrapSingle.model_validate_json(response.text)

            def update_an_asset_type(
                self, request_body: FortnoxUpdateAssetUpdateWrap, resource_id: str
            ) -> FortnoxAssetTypeWrapSingle:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/assets/types/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAssetTypeWrapSingle.model_validate_json(response.text)

        class AttendanceTransactions:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def lists_all_attendance_transactions(
                self,
                employeeid: Optional[str] = None,
                date: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxAttendanceTransactionListItemList:
                """Supports query-string parameters employeeid and date for filtering the result."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/attendancetransactions",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "employeeid": employeeid,
                        "date": date,
                    },
                )

                return FortnoxAttendanceTransactionListItemList.model_validate_json(
                    response.text
                )

            def create_a_new_attendance_transaction(
                self, request_body: FortnoxAttendanceTransactionWrap
            ) -> FortnoxAttendanceTransactionWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/attendancetransactions",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAttendanceTransactionWrap.model_validate_json(
                    response.text
                )

            @auto_consume_pages
            def retrieve_attendance_transactions(
                self,
                employee_resource_id: str,
                date: str,
                code: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxAttendanceTransactionListItemList:
                """Retrieves a list of attendance transaction for an employee on a specific date and cause code."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/attendancetransactions/{employee_resource_id}/{date}/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAttendanceTransactionListItemList.model_validate_json(
                    response.text
                )

            def delete_an_attendance_transaction(
                self, resource_id: str
            ) -> FortnoxAttendanceTransactionWrap:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/attendancetransactions/{resource_id}",
                    request_body=None,
                )

                return FortnoxAttendanceTransactionWrap.model_validate_json(
                    response.text
                )

            @auto_consume_pages
            def retrieve_a_specific_attendance_transaction(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxAttendanceTransactionWrap:
                """Retrieves a specific transaction"""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/attendancetransactions/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxAttendanceTransactionWrap.model_validate_json(
                    response.text
                )

            def update_a_single_attendance_transaction(
                self, request_body: FortnoxAttendanceTransactionWrap, resource_id: str
            ) -> FortnoxAttendanceTransactionWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/attendancetransactions/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxAttendanceTransactionWrap.model_validate_json(
                    response.text
                )

        class CompanyInformation:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_the__company__information(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxCompanyInfoWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/companyinformation",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxCompanyInfoWrap.model_validate_json(response.text)

        class ContractAccruals:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_contract_accruals(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxContractAccrualListItemList:
                """The contract accruals register can return a list of records or a single record. By specifying a DocumentNumber in the URL, a single record will be returned. Not specifying a DocumentNumber will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/contractaccruals",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxContractAccrualListItemList.model_validate_json(
                    response.text
                )

            def create_a_contract_accrual(
                self, request_body: FortnoxContractAccrualWrap
            ) -> FortnoxContractAccrualWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/contractaccruals",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxContractAccrualWrap.model_validate_json(response.text)

            def remove_a_contract_accrual(
                self, document_number: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/contractaccruals/{document_number}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_contract_accrual(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxContractAccrualWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/contractaccruals/{document_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxContractAccrualWrap.model_validate_json(response.text)

            def update_a_contract_accrual(
                self, request_body: FortnoxContractAccrualWrap, document_number: str
            ) -> FortnoxContractAccrualWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/contractaccruals/{document_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxContractAccrualWrap.model_validate_json(response.text)

        class Contracts:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_contracts(
                self,
                filter: Optional[Literal["active", "inactive", "finished"]] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxContractListItemList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/contracts",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "filter": filter,
                    },
                )

                return FortnoxContractListItemList.model_validate_json(response.text)

            def create_a_contract(
                self, request_body: FortnoxContractWrap
            ) -> FortnoxContractWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/contracts",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxContractWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_contract(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxContractWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/contracts/{document_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxContractWrap.model_validate_json(response.text)

            def update_a_contract(
                self, request_body: FortnoxContractWrap, document_number: str
            ) -> FortnoxContractWrap:
                """Note that there are two approaches for updating the rows on a contract.

                If RowId is not specified on any row, the rows will be mapped and updated in the order in which they are set in the array. All rows that should remain on the contract needs to be provided.

                If RowId is specified on one or more rows the following goes: Corresponding row with that id will be updated. The rows without RowId will be interpreted as new rows. If a row should not be updated but remain on the contract then specify only RowId like { "RowId": 123 }, otherwise it will be removed. Note that new RowIds are generated for all rows every time a contract is updated.

                When the InvoiceDiscount value is set on the rows and the Contract, the value set on the Contract takes precedence over the row-level InvoiceDiscount.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/contracts/{document_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxContractWrap.model_validate_json(response.text)

            def create_invoice_from_contract(
                self, document_number: str
            ) -> FortnoxInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/contracts/{document_number}/createinvoice",
                    request_body=None,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            def set_a_contract_as_finished(
                self, document_number: str
            ) -> FortnoxContractWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/contracts/{document_number}/finish",
                    request_body=None,
                )

                return FortnoxContractWrap.model_validate_json(response.text)

            def increases_the_invoice_count_without_creating_an_invoice(
                self, document_number: str
            ) -> FortnoxContractWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/contracts/{document_number}/increaseinvoicecount",
                    request_body=None,
                )

                return FortnoxContractWrap.model_validate_json(response.text)

        class ContractTemplates:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_contract_templates(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxContractTemplateListItemList:
                """The contract template resource can return a list of records or a single record. By specifying a TemplateNumber in the URL, a single record will be returned. Not specifying a TemplateNumber will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/contracttemplates",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxContractTemplateListItemList.model_validate_json(
                    response.text
                )

            def create_a_contract_template(
                self, request_body: FortnoxContractTemplateWrap
            ) -> FortnoxContractTemplateWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/contracttemplates",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxContractTemplateWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_contract_template(
                self, template_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxContractTemplateWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/contracttemplates/{template_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxContractTemplateWrap.model_validate_json(response.text)

            def update_a_contract_template(
                self, request_body: FortnoxContractTemplateWrap, template_number: str
            ) -> FortnoxContractTemplateWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/contracttemplates/{template_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxContractTemplateWrap.model_validate_json(response.text)

        class CostCenters:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_cost_centers(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxCostCenterList:
                """The cost centers register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/costcenters",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxCostCenterList.model_validate_json(response.text)

            def create_a_cost_center(
                self, request_body: FortnoxCostCenterWrap
            ) -> FortnoxCostCenterWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/costcenters",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxCostCenterWrap.model_validate_json(response.text)

            def remove_a_cost_center(self, code: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/costcenters/{code}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_cost_center(
                self, code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxCostCenterWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/costcenters/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxCostCenterWrap.model_validate_json(response.text)

            def update_a_cost_center(
                self, request_body: FortnoxCostCenterWrap, code: str
            ) -> FortnoxCostCenterWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/costcenters/{code}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxCostCenterWrap.model_validate_json(response.text)

        class Currencies:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_currencies(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxCurrencyList:
                """The currency register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/currencies",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxCurrencyList.model_validate_json(response.text)

            def create_a_currency(
                self, request_body: FortnoxCurrencyWrap
            ) -> FortnoxCurrencyWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/currencies",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxCurrencyWrap.model_validate_json(response.text)

            def remove_a_currency(self, code: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/currencies/{code}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_currency(
                self, code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxCurrencyWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/currencies/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxCurrencyWrap.model_validate_json(response.text)

            def update_a_currency(
                self, request_body: FortnoxCurrencyWrap, code: str
            ) -> FortnoxCurrencyWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/currencies/{code}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxCurrencyWrap.model_validate_json(response.text)

        class CustomerReferences:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_customers_reference_rows(
                self,
                customer: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxCustomerReferenceWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/customerreferences",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "customer": customer,
                    },
                )

                return FortnoxCustomerReferenceWrap.model_validate_json(response.text)

            def create_a_customer_reference_row(
                self, request_body: FortnoxCustomerReferenceCustomerReferenceRowWrap
            ) -> FortnoxCustomerReferenceWrap:
                """
                The created customer reference row will be returned if everything succeeded, if there was any problems an error will be returned.
                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/customerreferences",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxCustomerReferenceWrap.model_validate_json(response.text)

            def delete_a_customer_reference_row(
                self, customer_reference_row_resource_id: str
            ) -> FortnoxWebException:
                """
                Deletes the customer reference row permanently. If everything succeeded the response will be of the type 204, No content and the response body will be empty.
                If there was any problems an error will be returned.
                You need to supply the unique customer reference row id of the customer reference row that you want to delete.
                """
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/customerreferences/{customer_reference_row_resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_customer_reference_row(
                self,
                customer_reference_row_resource_id: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxCustomerReferenceWrap:
                """
                You need to supply the unique customer reference row id that was returned when the customer reference row was created or retrieved from the list of customer reference rows.
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/customerreferences/{customer_reference_row_resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxCustomerReferenceWrap.model_validate_json(response.text)

            def update_a_customer_reference_row(
                self,
                request_body: FortnoxCustomerReferenceCustomerReferenceRowWrap,
                customer_reference_row_resource_id: str,
            ) -> FortnoxCustomerWrap:
                """
                The updated customer reference row will be returned if everything succeeded, if there was any problems an error will be returned.
                You need to supply the unique customer reference row id of the customer reference row that you want to update.
                Only the properties provided in the request body will be updated, properties not provided will be left unchanged.
                CustomerNumber cannot be changed by this request."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/customerreferences/{customer_reference_row_resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxCustomerWrap.model_validate_json(response.text)

        class Customers:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_customers(
                self,
                filter: Optional[Literal["active", "inactive"]] = None,
                customernumber: Optional[str] = None,
                name: Optional[str] = None,
                zipcode: Optional[str] = None,
                city: Optional[str] = None,
                email: Optional[str] = None,
                phone: Optional[str] = None,
                organisationnumber: Optional[str] = None,
                gln: Optional[str] = None,
                glndelivery: Optional[str] = None,
                lastmodified: Optional[str] = None,
                sortby: Optional[Literal["customernumber", "name"]] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxCustomerListItemList:
                """The customers are returned sorted by customer number with the lowest number appearing first."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/customers",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "filter": filter,
                        "customernumber": customernumber,
                        "name": name,
                        "zipcode": zipcode,
                        "city": city,
                        "email": email,
                        "phone": phone,
                        "organisationnumber": organisationnumber,
                        "gln": gln,
                        "glndelivery": glndelivery,
                        "lastmodified": lastmodified,
                        "sortby": sortby,
                    },
                )

                return FortnoxCustomerListItemList.model_validate_json(response.text)

            def create_a_customer(
                self, request_body: FortnoxCustomerWrap
            ) -> FortnoxCustomerWrap:
                """The created customer will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/customers",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxCustomerWrap.model_validate_json(response.text)

            def delete_a_customer(self, customer_number: str) -> FortnoxWebException:
                """Deletes the customer permanently. If everything succeeded the response will be of the type 204 \u2013 No content and the response body will be empty. If there was any problems an error will be returned.
                You need to supply the unique customer number of the customer that you want to delete.
                """
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/customers/{customer_number}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_customer(
                self, customer_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxCustomerWrap:
                """You need to supply the unique customer number that was returned when the customer was created or retrieved from the list of customers."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/customers/{customer_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxCustomerWrap.model_validate_json(response.text)

            def update_a_customer(
                self, request_body: FortnoxCustomerWrap, customer_number: str
            ) -> FortnoxCustomerWrap:
                """The updated customer will be returned if everything succeeded, if there was any problems an error will be returned.
                You need to supply the unique customer number of the customer that you want to update.
                Only the properties provided in the request body will be updated, properties not provided will left unchanged.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/customers/{customer_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxCustomerWrap.model_validate_json(response.text)

        class TrustedEmailSenders:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_all_trusted_and_rejected_senders(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxTrustedEmailSenderWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/emailsenders",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxTrustedEmailSenderWrap.model_validate_json(response.text)

            def add_a_new_email_address_as_trusted(
                self, request_body: FortnoxTrustedEmailSenderTrustedSenderWrap
            ) -> FortnoxTrustedEmailSenderTrustedSenderWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/emailsenders/trusted",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxTrustedEmailSenderTrustedSenderWrap.model_validate_json(
                    response.text
                )

            def delete_an_email_address_from_the_trusted_senders_list(
                self, resource_id: str
            ) -> FortnoxWebException:
                """Provide an id matching an email to delete."""
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/emailsenders/trusted/{resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

        class Employees:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_employees(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxEmployeeListItemWrap:
                """ScheduleId, MonthlySalary and HourlyPay reflect current values, all
                ScheduleIds are returned in DatedSchedules and all MonthlySalary and
                HourlyPay pairs are returned in DatedWages."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/employees",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxEmployeeListItemWrap.model_validate_json(response.text)

            def create_a_new_employee(
                self, request_body: FortnoxEmployeeWrap
            ) -> FortnoxEmployeeWrap:
                """EmployeeId is optional. If not supplied the program will generate a unique id.

                Only one of DatedSchedules and ScheduleId may be supplied. If DatedSchedules are supplied
                it must have one and only one record where FirstDay = '1970-01-01'.
                All FirstDay values must greater or equal to '1970-01-01' and unique.

                If DatedWages is supplied neither MonthlySalary nor HourlyPay may be supplied. If
                MonthlySalary or HourlyPay are supplied, DatedWages may not be supplied.
                If DatedWages are supplied it must have one and only one record where FirstDay = '1970-01-01'.
                All FirstDay values must greater or equal to '1970-01-01' and unique."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/employees",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxEmployeeWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_specific_employee(
                self,
                employee_resource_id: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxEmployeeWrap:
                """ScheduleId, MonthlySalary and HourlyPay reflect current values, all
                ScheduleIds are returned in DatedSchedules and all MonthlySalary and
                HourlyPay pairs are returned in DatedWages."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/employees/{employee_resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxEmployeeWrap.model_validate_json(response.text)

            def update_employee(
                self, request_body: FortnoxEmployeeWrap, employee_resource_id: str
            ) -> FortnoxEmployeeWrap:
                """Only one of DatedSchedules and ScheduleId may be supplied. If DatedSchedules are supplied
                it must have one and only one record where FirstDay = '1970-01-01'.
                All FirstDay values must greater or equal to '1970-01-01' and unique.

                If DatedWages is supplied neither MonthlySalary nor HourlyPay may be supplied. If
                MonthlySalary or HourlyPay are supplied, DatedWages may not be supplied.
                If DatedWages are supplied it must have one and only one record where FirstDay = '1970-01-01'.
                All FirstDay values must greater or equal to '1970-01-01' and unique."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/employees/{employee_resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxEmployeeWrap.model_validate_json(response.text)

        class EuVatLimitRegulation:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_details_about_eu_vat_limit(
                self,
                year: Optional[int] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxEuVatLimitRegulationWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/euvatlimitregulation",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "year": year,
                    },
                )

                return FortnoxEuVatLimitRegulationWrap.model_validate_json(
                    response.text
                )

        class Expenses:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_expenses(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxExpenseListItemWrap:
                """Retrieve expense codes."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/expenses",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxExpenseListItemWrap.model_validate_json(response.text)

            def create_an_expense(
                self, request_body: FortnoxExpenseWrap
            ) -> FortnoxExpenseWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/expenses",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxExpenseWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_an_expense(
                self, expense_code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxExpenseWrap:
                """Retrieves expense information for specified expense."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/expenses/{expense_code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxExpenseWrap.model_validate_json(response.text)

        class FinancialYears:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_financial_years(
                self,
                date: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxFinancialYearWrapList:
                """Add the query param to filter on specific date."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/financialyears",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "Date": date,
                    },
                )

                return FortnoxFinancialYearWrapList.model_validate_json(response.text)

            def create_a_financial_year(
                self, request_body: FortnoxFinancialYearWrap
            ) -> FortnoxFinancialYearWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/financialyears",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxFinancialYearWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_financial_year_by_id(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxFinancialYearWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/financialyears/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxFinancialYearWrap.model_validate_json(response.text)

        class Inbox:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_the_root_folder_containing_files_and_folders(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxFolderWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/inbox",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxFolderWrap.model_validate_json(response.text)

            def upload_a_file(
                self,
                request_body: UploadFile,
                folder_id: Optional[str] = None,
                path: Optional[str] = None,
            ) -> FortnoxFolderFileRowWrap:
                """Upload a file to a specific subdirectory."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/inbox",
                    request_body=request_body,
                    query_params={
                        "folderId": folder_id,
                        "path": path,
                    },
                )

                return FortnoxFolderFileRowWrap.model_validate_json(response.text)

            def remove_a_file_or_folder(self, resource_id: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/inbox/{resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_file(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> str:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/inbox/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return response.json()

        class InvoiceAccruals:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_invoice_accruals(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxInvoiceAccrualListItemList:
                """The invoice accruals register can return a list of records or a single record. By specifying a InvoiceNumber in the URL, a single record will be returned. Not specifying a InvoiceNumber will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/invoiceaccruals",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxInvoiceAccrualListItemList.model_validate_json(
                    response.text
                )

            def create_an_invoice_accrual(
                self, request_body: FortnoxInvoiceAccrualWrap
            ) -> FortnoxInvoiceAccrualWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/invoiceaccruals",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoiceAccrualWrap.model_validate_json(response.text)

            def remove_an_invoice_accrual(
                self, invoice_number: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/invoiceaccruals/{invoice_number}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_invoice_accrual(
                self, invoice_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxInvoiceAccrualWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/invoiceaccruals/{invoice_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxInvoiceAccrualWrap.model_validate_json(response.text)

            def update_an_invoice_accrual(
                self, request_body: FortnoxInvoiceAccrualWrap, invoice_number: str
            ) -> FortnoxInvoiceAccrualWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/invoiceaccruals/{invoice_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoiceAccrualWrap.model_validate_json(response.text)

        class InvoicePayments:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_invoice_payments(
                self,
                invoicenumber: Optional[int] = None,
                lastmodified: Optional[str] = None,
                sortby: Optional[Literal["paymentdate"]] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxInvoicePaymentListItemList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/invoicepayments",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "invoicenumber": invoicenumber,
                        "lastmodified": lastmodified,
                        "sortby": sortby,
                    },
                )

                return FortnoxInvoicePaymentListItemList.model_validate_json(
                    response.text
                )

            def create_an_invoice_payment(
                self, request_body: FortnoxInvoicePaymentWrap
            ) -> FortnoxInvoicePaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/invoicepayments",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoicePaymentWrap.model_validate_json(response.text)

            def remove_an_invoice_payment(self, number: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/invoicepayments/{number}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_invoice_payment(
                self, number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxInvoicePaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/invoicepayments/{number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxInvoicePaymentWrap.model_validate_json(response.text)

            def update_an_invoice_payment(
                self, request_body: FortnoxInvoicePaymentWrap, number: str
            ) -> FortnoxInvoicePaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/invoicepayments/{number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoicePaymentWrap.model_validate_json(response.text)

            def bookkeep_an_invoice_payment(
                self, request_body: FortnoxInvoicePaymentWrap, number: str
            ) -> FortnoxInvoicePaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/invoicepayments/{number}/bookkeep",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoicePaymentWrap.model_validate_json(response.text)

        class Invoices:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_invoices(
                self,
                filter: Optional[
                    Literal[
                        "cancelled", "fullypaid", "unpaid", "unpaidoverdue", "unbooked"
                    ]
                ] = None,
                costcenter: Optional[str] = None,
                customername: Optional[str] = None,
                customernumber: Optional[str] = None,
                label: Optional[str] = None,
                documentnumber: Optional[str] = None,
                fromdate: Optional[str] = None,
                todate: Optional[str] = None,
                fromfinalpaydate: Optional[str] = None,
                tofinalpaydate: Optional[str] = None,
                lastmodified: Optional[str] = None,
                notcompleted: Optional[str] = None,
                ocr: Optional[str] = None,
                ourreference: Optional[str] = None,
                project: Optional[str] = None,
                sent: Optional[str] = None,
                externalinvoicereference1: Optional[str] = None,
                externalinvoicereference2: Optional[str] = None,
                yourreference: Optional[str] = None,
                invoicetype: Optional[str] = None,
                articlenumber: Optional[str] = None,
                articledescription: Optional[str] = None,
                currency: Optional[str] = None,
                accountnumberfrom: Optional[str] = None,
                accountnumberto: Optional[str] = None,
                yourordernumber: Optional[str] = None,
                credit: Optional[str] = None,
                sortby: Optional[
                    Literal[
                        "customername",
                        "customernumber",
                        "documentnumber",
                        "invoicedate",
                        "ocr",
                        "total",
                    ]
                ] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxInvoiceListItemWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/invoices",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "filter": filter,
                        "costcenter": costcenter,
                        "customername": customername,
                        "customernumber": customernumber,
                        "label": label,
                        "documentnumber": documentnumber,
                        "fromdate": fromdate,
                        "todate": todate,
                        "fromfinalpaydate": fromfinalpaydate,
                        "tofinalpaydate": tofinalpaydate,
                        "lastmodified": lastmodified,
                        "notcompleted": notcompleted,
                        "ocr": ocr,
                        "ourreference": ourreference,
                        "project": project,
                        "sent": sent,
                        "externalinvoicereference1": externalinvoicereference1,
                        "externalinvoicereference2": externalinvoicereference2,
                        "yourreference": yourreference,
                        "invoicetype": invoicetype,
                        "articlenumber": articlenumber,
                        "articledescription": articledescription,
                        "currency": currency,
                        "accountnumberfrom": accountnumberfrom,
                        "accountnumberto": accountnumberto,
                        "yourordernumber": yourordernumber,
                        "credit": credit,
                        "sortby": sortby,
                    },
                )

                return FortnoxInvoiceListItemWrap.model_validate_json(response.text)

            def create_an_invoice(
                self, request_body: FortnoxInvoicePayloadWrap
            ) -> FortnoxInvoiceWrap:
                """An endpoint for creating an invoice. While it is possible to create an invoice without rows, we encourage you to add them if you can.
                Omitted values in the payload will be supplied by Predefined values which can be edited in the Fortnox account settings.
                Note that Predefined values will always be overwritten by values provided through the API.

                Should you have EasyVat enabled, it is mandatory to provide an account in the request should you use a custom VAT rate.

                This endpoint can produce errors, some of which may only be relevant for EasyVat. Refer to the table below.

                Errors that can be raised by this endpoint.

                                       Error Code
                                       HTTP Code
                                       Description
                                       Solution


                                       2004167
                                       400
                                       An account must be provided when using a custom VAT rate and EasyVat has been enabled.
                                       Supply each row which has a custom VAT rate with an account.



                Note: The EuQuarterlyReport property will become obsolete at 2021-12-01.
                This property is currently used by the Quarterly report as one of the conditions that determine if an invoice
                should be included in the report or not.
                A new version of the Quarterly report is released at 2021-12-01. In the new report, this property will not be
                used when determining if an invoice should be included in the report or not, with one exception: if the invoice
                is created before 2021-12-01, and this property is false, the invoice will be excluded from the report.
                For invoices created 2021-12-01 and later, this property will have no effect.
                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/invoices",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_invoice(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/invoices/{document_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            def update_an_invoice(
                self, request_body: FortnoxInvoicePayloadWrap, document_number: str
            ) -> FortnoxInvoiceWrap:
                """Note that there are two approaches for updating the rows on an invoice.

                If RowId is not specified on any row, the rows will be mapped and updated in the order in which they are set in the array. All rows that should remain on the invoice needs to be provided.

                If RowId is specified on one or more rows the following goes: Corresponding row with that id will be updated. The rows without RowId will be interpreted as new rows. If a row should not be updated but remain on the invoice then specify only RowId like { "RowId": 123 }, otherwise it will be removed. Note that new RowIds are generated for all rows every time an invoice is updated.

                Note: The EuQuarterlyReport property will become obsolete at 2021-12-01.
                This property is currently used by the Quarterly report as one of the conditions that determine if an invoice
                should be included in the report or not.
                A new version of the Quarterly report is released at 2021-12-01. In the new report, this property will not be
                used when determining if an invoice should be included in the report or not, with one exception: if the invoice
                is created before 2021-12-01, and this property is false, the invoice will be excluded from the report.
                For invoices created 2021-12-01 and later, this property will have no effect.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/invoices/{document_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            def bookkeep_an_invoice(self, document_number: str) -> FortnoxInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/invoices/{document_number}/bookkeep",
                    request_body=None,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            def cancel_an_invoice(self, document_number: str) -> FortnoxInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/invoices/{document_number}/cancel",
                    request_body=None,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            def credit_an_invoice(self, document_number: str) -> FortnoxInvoiceWrap:
                """The created credit invoice will be referenced in the property CreditInvoiceReference."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/invoices/{document_number}/credit",
                    request_body=None,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            @auto_consume_pages
            def send_an_invoice_as_e_invoice(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/invoices/{document_number}/einvoice",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            @auto_consume_pages
            def send_an_invoice_as_email(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxInvoiceWrap:
                """You can use the properties in the EmailInformation to customize the e-mail message on each invoice."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/invoices/{document_number}/email",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            @auto_consume_pages
            def send_an_invoice_as_e_print(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/invoices/{document_number}/eprint",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            def set_an_invoice_as_sent(
                self, document_number: str
            ) -> FortnoxInvoiceWrap:
                """Use this endpoint to set invoice as sent, without generating an invoice."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/invoices/{document_number}/externalprint",
                    request_body=None,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            @auto_consume_pages
            def preview_an_invoice(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> str:
                """The difference between this and the print-endpoint is that property Sent is not set to TRUE."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/invoices/{document_number}/preview",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return response.json()

            @auto_consume_pages
            def print_an_invoice(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> str:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/invoices/{document_number}/print",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return response.json()

            @auto_consume_pages
            def print_an_invoice_as_reminder(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> str:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/invoices/{document_number}/printreminder",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return response.json()

            def set_an_invoice_as_done(
                self, document_number: str
            ) -> FortnoxInvoiceWrap:
                """Used for marking a document as ready in the warehouse module. DeliveryState needs to be set to &quot;delivery&quot;."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/invoices/{document_number}/warehouseready",
                    request_body=None,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

        class Labels:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_labels(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxLabelList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/labels",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxLabelList.model_validate_json(response.text)

            def create_a_label(
                self, request_body: FortnoxLabelWrap
            ) -> FortnoxLabelWrap:
                """The created label will be returned if everything succeeded, if there was any problems an error will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/labels",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxLabelWrap.model_validate_json(response.text)

            def delete_a_label(self, resource_id: str) -> FortnoxWebException:
                """Deletes the label and its connection to documents permanently.
                You need to supply the unique label id that was returned when the label was created or retrieved from the list of labels.
                """
                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/labels/{resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            def update_a_label(
                self, request_body: FortnoxLabelWrap, resource_id: str
            ) -> FortnoxLabelWrap:
                """Updates the specified label with the values provided in the properties. Any property not provided will be left unchanged."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/labels/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxLabelWrap.model_validate_json(response.text)

        class Me:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_user_information(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxMeWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/me",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxMeWrap.model_validate_json(response.text)

        class ModesOfPayments:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_modes_of_payments(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxModeOfPaymentList:
                """The modes of payments register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/modesofpayments",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxModeOfPaymentList.model_validate_json(response.text)

            def create_a_mode_of_payment(
                self, request_body: FortnoxModeOfPaymentWrap
            ) -> FortnoxModeOfPaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/modesofpayments",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxModeOfPaymentWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_mode_of_payment(
                self, code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxModeOfPaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/modesofpayments/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxModeOfPaymentWrap.model_validate_json(response.text)

            def update_a_mode_of_payment(
                self, request_body: FortnoxModeOfPaymentWrap, code: str
            ) -> FortnoxModeOfPaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/modesofpayments/{code}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxModeOfPaymentWrap.model_validate_json(response.text)

        class FinanceInvoices:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            def send_an_invoice_with__fortnox__finans(
                self, request_body: FortnoxCreatePayloadWrap
            ) -> FortnoxInvoiceResponseWrap:
                """
                When sending an invoice with Fortnox Finans you will get the invoice status returned if everything succeeded,
                if there were any problems, an error will be returned.

                Please note that it can take 1 min to several hours before you will get back status, OCR number and link to
                PDF document, meanwhile the invoice will have status UNKNOWN or NOT_AUTHORIZED.

                Fortnox Finans is currently only accepting invoices in SEK

                Parameters in the body:

                    InvoiceNumber: the invoice number for the invoice which should be sent with Fortnox Finans
                    SendMethod: how to send the invoice; EMAIL, LETTER, EINVOICE or NONE
                    Service: which service to use; LEDGERBASE or REMINDER

                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/noxfinansinvoices",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoiceResponseWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_invoice_payment(
                self, number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxInvoiceResponseWrap:
                """
                Retrieves the status and balance of an invoice sent to Fortnox Finans.
                You need to supply the invoice number in Fortox to retrieve the invoice.

                Note that invoices sent with the old &quot;Noxbox&quot; platform will not have the &quot;ServiceName&quot;
                property in the response. This new property is added to the response if the invoice is
                sent with the new finance service.

                Response explanation for Service and ServiceName

                Service:

                    LEDGERBASE: if the invoice is sent by using the old &quot;Noxbox&quot; platform, or the new finance service with the subtypes &quot;Service Full&quot; or &quot;Service Light&quot;. These services are explained above in the &quot;Fortnox Finans services&quot; section
                    REMINDER: If the invoice is sent by the new finance service, with the service Reminder Service


                ServiceName (only provided for new finance service invoices):

                    SERVICE_FULL: Ledgerbase service with automatic reminders is used
                    SERVICE_LIGHT: Ledgerbase service without automatic reminders is used.
                    REMINDER_SERVICE: Reminder service is used
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/noxfinansinvoices/{number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxInvoiceResponseWrap.model_validate_json(response.text)

            def action__pause(
                self, request_body: FortnoxPausePayloadWrap, number: str
            ) -> FortnoxInvoiceResponseWrap:
                """
                Pauses an invoice for up to 60 days. Pause means that Fortnox Finans reminder process will stop for the invoice. All invoices which have the status OPEN can be paused.

                Parameters in the body:

                    PausedUntilDate: the invoice will be paused to and including this date.

                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/noxfinansinvoices/{number}/pause",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoiceResponseWrap.model_validate_json(response.text)

            def action__report__payment(
                self, request_body: FortnoxReportPaymentPayload, number: str
            ) -> FortnoxInvoiceResponseWrap:
                """
                If a customer has paid some or all of the capital on an invoice directly to the client, this can be reported
                for bookkeeping purposes and reported to Fortnox Finans to actually deduct the paid amount from the invoice.

                Note: this action is not available for invoices sent by the old Noxbox platform

                Parameters in the body:

                    ClientTakesFees: a boolean indicating if the client should take the customer fees or not.
                    BookkeepPaymentInFortnox: a boolean indicating if the payment should be bookkept in Fortnox or not. Usually the payment should be bookkept.
                    ReportToFinance: a boolean indicating if the payment should be reported to Fortnox Finans or not. Usually the payment should be reported.
                    PaymentAmount: a decimal field with the amount to report.
                    PaymentMethodCode: a string with the method code (e.g. BG, PG or other). Could be omitted if BookkeepPaymentInFortnox is false.
                    PaymentMethodAccount: an integer with the account number to bookkeep the payment on (e.g. 1920 or other). Could be omitted if BookkeepPaymentInFortnox is false.

                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/noxfinansinvoices/{number}/report-payment",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxInvoiceResponseWrap.model_validate_json(response.text)

            def action__stop(self, number: str) -> FortnoxInvoiceResponseWrap:
                """
                Removes the invoice from Fortnox Finans process. The invoice can still be handled manually, but no further automatic process will be applied
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/noxfinansinvoices/{number}/stop",
                    request_body=None,
                )

                return FortnoxInvoiceResponseWrap.model_validate_json(response.text)

            def action__take__fees(self, number: str) -> FortnoxInvoiceResponseWrap:
                """
                If fees have been added to an invoice, e.g. reminder fees, the client can choose to pay those fees instead of letting the customer pay.

                Note: this action is not available for invoices sent by the old Noxbox platform
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/noxfinansinvoices/{number}/take-fees",
                    request_body=None,
                )

                return FortnoxInvoiceResponseWrap.model_validate_json(response.text)

            def action__unpause(self, number: str) -> FortnoxInvoiceResponseWrap:
                """
                Unpauses a paused invoice. If the invoice is manually paused, then this action will remove the pause status immediately. Invoices which are paused by the system cannot be unpaused.

                Note: this action is not available for invoices sent by the old Noxbox platform
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/noxfinansinvoices/{number}/unpause",
                    request_body=None,
                )

                return FortnoxInvoiceResponseWrap.model_validate_json(response.text)

        class Offers:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_offers(
                self,
                filter: Optional[
                    Literal[
                        "cancelled",
                        "expired",
                        "completed",
                        "notcompleted",
                        "ordercreated",
                        "ordernotcreated",
                    ]
                ] = None,
                customername: Optional[str] = None,
                customernumber: Optional[str] = None,
                documentnumber: Optional[str] = None,
                costcenter: Optional[str] = None,
                label: Optional[str] = None,
                fromdate: Optional[str] = None,
                todate: Optional[str] = None,
                project: Optional[str] = None,
                sent: Optional[bool] = None,
                notcompleted: Optional[bool] = None,
                ourreference: Optional[str] = None,
                yourreference: Optional[str] = None,
                lastmodified: Optional[str] = None,
                sortby: Optional[
                    Literal["customerName", "id", "transactionDate", "total"]
                ] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxOfferListItemList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/offers",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "filter": filter,
                        "customername": customername,
                        "customernumber": customernumber,
                        "documentnumber": documentnumber,
                        "costcenter": costcenter,
                        "label": label,
                        "fromdate": fromdate,
                        "todate": todate,
                        "project": project,
                        "sent": sent,
                        "notcompleted": notcompleted,
                        "ourreference": ourreference,
                        "yourreference": yourreference,
                        "lastmodified": lastmodified,
                        "sortby": sortby,
                    },
                )

                return FortnoxOfferListItemList.model_validate_json(response.text)

            def create_an_offer(
                self, request_body: FortnoxOfferWrap
            ) -> FortnoxOfferWrap:
                """An endpoint for creating an offer.

                Should you have EasyVat enabled, it is mandatory to provide an account in the request should you use a custom VAT rate.

                This endpoint can produce errors, some of which may only be relevant for EasyVat. Refer to the table below.

                Errors that can be raised by this endpoint.

                                       Error Code
                                       HTTP Code
                                       Description
                                       Solution


                                       2004167
                                       400
                                       An account must be provided when using a custom VAT rate and EasyVat has been enabled.
                                       Supply each row which has a custom VAT rate with an account.

                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/offers",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxOfferWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_offer(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxOfferWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/offers/{document_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxOfferWrap.model_validate_json(response.text)

            def update_an_offer(
                self, request_body: FortnoxOfferWrap, document_number: str
            ) -> FortnoxOfferWrap:
                """Note that there are two approaches for updating the rows on an offer.

                If RowId is not specified on any row, the rows will be mapped and updated in the order in which they are set in the array. All rows that should remain on the offer needs to be provided.

                If RowId is specified on one or more rows the following goes: Corresponding row with that id will be updated. The rows without RowId will be interpreted as new rows. If a row should not be updated but remain on the offer then specify only RowId like { "RowId": 123 }, otherwise it will be removed. Note that new RowIds are generated for all rows every time an offer is updated.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/offers/{document_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxOfferWrap.model_validate_json(response.text)

            def cancels_given_offer(self, document_number: str) -> FortnoxOfferWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/offers/{document_number}/cancel",
                    request_body=None,
                )

                return FortnoxOfferWrap.model_validate_json(response.text)

            def create_invoice_out_of_given_offer(
                self, document_number: str
            ) -> FortnoxOrderWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/offers/{document_number}/createinvoice",
                    request_body=None,
                )

                return FortnoxOrderWrap.model_validate_json(response.text)

            def create_order_out_of_given_offer(
                self, document_number: str
            ) -> FortnoxOrderWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/offers/{document_number}/createorder",
                    request_body=None,
                )

                return FortnoxOrderWrap.model_validate_json(response.text)

            @auto_consume_pages
            def send_given_offer_as_email(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxOfferWrap:
                """You can use the properties in the EmailInformation to customize the e-mail message on each offer."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/offers/{document_number}/email",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxOfferWrap.model_validate_json(response.text)

            def set_given_offer_as_sent(self, document_number: str) -> FortnoxOfferWrap:
                """Use this endpoint to set offer as sent, without generating an offer."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/offers/{document_number}/externalprint",
                    request_body=None,
                )

                return FortnoxOfferWrap.model_validate_json(response.text)

            @auto_consume_pages
            def preview_given_offer(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> str:
                """The difference between this and the print-endpoint is that property Sent is not set to TRUE."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/offers/{document_number}/preview",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return response.json()

            @auto_consume_pages
            def print_given_offer(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> str:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/offers/{document_number}/print",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return response.json()

        class Orders:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_orders(
                self,
                filter: Optional[
                    Literal[
                        "cancelled", "expired", "invoicecreated", "invoicenotcreated"
                    ]
                ] = None,
                customername: Optional[str] = None,
                customernumber: Optional[str] = None,
                label: Optional[str] = None,
                documentnumber: Optional[str] = None,
                externalinvoicereference1: Optional[str] = None,
                externalinvoicereference2: Optional[str] = None,
                fromdate: Optional[str] = None,
                todate: Optional[str] = None,
                costcenter: Optional[str] = None,
                project: Optional[str] = None,
                sent: Optional[bool] = None,
                notcompleted: Optional[bool] = None,
                ourreference: Optional[str] = None,
                yourreference: Optional[str] = None,
                lastmodified: Optional[str] = None,
                ordertype: Optional[str] = None,
                sortby: Optional[
                    Literal[
                        "customername",
                        "customernumber",
                        "orderdate",
                        "documentnumber",
                        "total",
                    ]
                ] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxOrderListItemList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/orders",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "filter": filter,
                        "customername": customername,
                        "customernumber": customernumber,
                        "label": label,
                        "documentnumber": documentnumber,
                        "externalinvoicereference1": externalinvoicereference1,
                        "externalinvoicereference2": externalinvoicereference2,
                        "fromdate": fromdate,
                        "todate": todate,
                        "costcenter": costcenter,
                        "project": project,
                        "sent": sent,
                        "notcompleted": notcompleted,
                        "ourreference": ourreference,
                        "yourreference": yourreference,
                        "lastmodified": lastmodified,
                        "ordertype": ordertype,
                        "sortby": sortby,
                    },
                )

                return FortnoxOrderListItemList.model_validate_json(response.text)

            def create_a_new_order(
                self, request_body: FortnoxOrderWrap
            ) -> FortnoxOrderWrap:
                """An endpoint for creating an order.

                Should you have EasyVat enabled, it is mandatory to provide an account in the request should you use a custom VAT rate.

                This endpoint can produce errors, some of which may only be relevant for EasyVat. Refer to the table below.

                Errors that can be raised by this endpoint.

                                       Error Code
                                       HTTP Code
                                       Description
                                       Solution


                                       2004167
                                       400
                                       An account must be provided when using a custom VAT rate and EasyVat has been enabled.
                                       Supply each row which has a custom VAT rate with an account.

                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/orders",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxOrderWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_order(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxOrderWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/orders/{document_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxOrderWrap.model_validate_json(response.text)

            def update_an_order(
                self, request_body: FortnoxOrderWrap, document_number: str
            ) -> FortnoxOrderWrap:
                """Note that there are two approaches for updating the rows on an order.

                If RowId is not specified on any row, the rows will be mapped and updated in the order in which they are set in the array. All rows that should remain on the order needs to be provided.

                If RowId is specified on one or more rows the following goes: Corresponding row with that id will be updated. The rows without RowId will be interpreted as new rows. If a row should not be updated but remain on the order then specify only RowId like { "RowId": 123 }, otherwise it will be removed. Note that new RowIds are generated for all rows every time an order is updated.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/orders/{document_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxOrderWrap.model_validate_json(response.text)

            def cancels_given_order(self, document_number: str) -> FortnoxOrderWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/orders/{document_number}/cancel",
                    request_body=None,
                )

                return FortnoxOrderWrap.model_validate_json(response.text)

            def create_invoice_out_of_given_order(
                self, document_number: str
            ) -> FortnoxInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/orders/{document_number}/createinvoice",
                    request_body=None,
                )

                return FortnoxInvoiceWrap.model_validate_json(response.text)

            @auto_consume_pages
            def send_given_order_as_email(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxOrderWrap:
                """You can use the properties in the EmailInformation to customize the e-mail message on each order."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/orders/{document_number}/email",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxOrderWrap.model_validate_json(response.text)

            def set_given_order_as_sent(self, document_number: str) -> FortnoxOrderWrap:
                """Use this endpoint to set order as sent, without generating an order."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/orders/{document_number}/externalprint",
                    request_body=None,
                )

                return FortnoxOrderWrap.model_validate_json(response.text)

            @auto_consume_pages
            def preview_given_offer(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> str:
                """The difference between this and the print-endpoint is that property Sent is not set to TRUE."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/orders/{document_number}/preview",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return response.json()

            @auto_consume_pages
            def print_given_order(
                self, document_number: str, page: int = 1, offset: Optional[int] = None
            ) -> str:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/orders/{document_number}/print",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return response.json()

        class PredefinedAccounts:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_all_predefined_accounts(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxPredefinedAccountList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/predefinedaccounts",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPredefinedAccountList.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_information_for_a_specific_account_type(
                self, name: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxPredefinedAccountWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/predefinedaccounts/{name}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPredefinedAccountWrap.model_validate_json(response.text)

            def update_a__predefined__account(
                self, request_body: FortnoxPredefinedAccountWrap, name: str
            ) -> FortnoxPredefinedAccountWrap:
                """An endpoint for updating a Predefined Account. Predefined Accounts are identified by their name-field, and as such must be unique.
                Some Predefined Accounts distinguish between Goods and Services.
                In this case, the former retains the original name whereas the latter ends with a 2. Such as SALES and SALES2.
                Accounts are chosen from the Account Registry, and if you have EasyVat enabled then the new EasyVat Predefined Accounts (SALES_25_SE, etc.) have certain restrictions on the accounts that can be selected.
                Refer to the table below.


                    Account restrictions when EasyVat has been enabled.

                        Name
                        VAT Code
                        Restrictions


                        SALES_25_SE
                        MP1
                        Must have a compatible VAT Code.


                        SALES_12_SE
                        MP2
                        Must have a compatible VAT Code.


                        SALES_6_SE
                        MP3
                        Must have a compatible VAT Code.


                        SALES_0_SE
                        MF
                        Must have a compatible VAT Code.



                This endpoint can produce errors, some of which may only be relevant for EasyVat. Refer to the table below.

                    Errors that can be raised by this endpoint.

                        Error Code
                        HTTP Code
                        Description
                        Solution


                        2001265
                        400
                        The provided account is invalid. It either has not been provided, does not exist, or is inactive.
                        Verify that an account has been provided and that it exists and is active.


                        2002462
                        400
                        The account is not in a valid format.
                        Verify that the format of the account is correct. It has to consist of 4 digits.


                        2000729
                        400
                        A Predefined Account has not been provided.
                        Verify that a valid Predefined Account has been provided as a PATH-parameter.


                        2004052
                        400
                        The provided account has an incompatible VAT Code. Only applies if EasyVat has been enabled.
                        Verify that the provided account has a VAT Code that is compatible with the selected Predefined Account. Refer to the table above for more information about compatibility.



                If you have activated EasyVat, you can read more about how to use the new Predefined Accounts with your documents in their respective api documentation.
                """
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/predefinedaccounts/{name}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxPredefinedAccountWrap.model_validate_json(response.text)

        class PredefinedVoucherSeries:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_predefined_voucher_series(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxPredefinedVoucherSeriesList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/predefinedvoucherseries",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPredefinedVoucherSeriesList.model_validate_json(
                    response.text
                )

            @auto_consume_pages
            def retrieve_a_specific_predefined_voucher_series(
                self, name: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxPredefinedVoucherSeriesWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/predefinedvoucherseries/{name}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPredefinedVoucherSeriesWrap.model_validate_json(
                    response.text
                )

            def update_a_predefined_voucher_series(
                self, request_body: FortnoxPredefinedVoucherSeriesWrap, name: str
            ) -> FortnoxPredefinedVoucherSeriesWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/predefinedvoucherseries/{name}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxPredefinedVoucherSeriesWrap.model_validate_json(
                    response.text
                )

        class PriceLists:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_price_lists(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxPriceListList:
                """The price lists register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/pricelists",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPriceListList.model_validate_json(response.text)

            def create_a_price_list(
                self, request_body: FortnoxPriceListWrap
            ) -> FortnoxPriceListWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/pricelists",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxPriceListWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_price_list(
                self, code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxPriceListWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/pricelists/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPriceListWrap.model_validate_json(response.text)

            def update_a_price_list(
                self, request_body: FortnoxPriceListWrap, code: str
            ) -> FortnoxPriceListWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/pricelists/{code}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxPriceListWrap.model_validate_json(response.text)

        class Prices:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            def create_a_price(
                self, request_body: FortnoxPriceWrap
            ) -> FortnoxPriceWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/prices",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxPriceWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_list_of_articles_with_all_their_prices_in_the_specified_price_list(
                self,
                price_list: str,
                article_number: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxPriceListItemList:
                """The list contains a slimmer version of the prices. To get a full entity, use the GET with a price list, article number and from quantity."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/prices/sublist/{price_list}/{article_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPriceListItemList.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_the_first_price_for_the_specified_article(
                self,
                price_list: str,
                article_number: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxPriceWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/prices/{price_list}/{article_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPriceWrap.model_validate_json(response.text)

            def update_the_first_price_in_the_specified_article(
                self,
                request_body: FortnoxPriceWrap,
                price_list: str,
                article_number: str,
            ) -> FortnoxPriceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/prices/{price_list}/{article_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxPriceWrap.model_validate_json(response.text)

            def delete_a_single_price(
                self, price_list: str, article_number: str, from_quantity: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/prices/{price_list}/{article_number}/{from_quantity}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_price_for_a_specified_article(
                self,
                price_list: str,
                article_number: str,
                from_quantity: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxPriceWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/prices/{price_list}/{article_number}/{from_quantity}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPriceWrap.model_validate_json(response.text)

            def update_a_price(
                self,
                request_body: FortnoxPriceWrap,
                price_list: str,
                article_number: str,
                from_quantity: str,
            ) -> FortnoxPriceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/prices/{price_list}/{article_number}/{from_quantity}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxPriceWrap.model_validate_json(response.text)

        class PrintTemplates:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_print_templates(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxPrintTemplateList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/printtemplates",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxPrintTemplateList.model_validate_json(response.text)

        class Projects:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_projects(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxProjectListItemList:
                """The project register can return a list of records or a single record. By specifying a ProjectNumber in the URL, a single record will be returned. If no ProjectNumber is provided, a list of records will be returned."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/projects",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxProjectListItemList.model_validate_json(response.text)

            def create_a_project(
                self, request_body: FortnoxProjectWrap
            ) -> FortnoxProjectWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/projects",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxProjectWrap.model_validate_json(response.text)

            def remove_a_project(self, project_number: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/projects/{project_number}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_project(
                self, project_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxProjectWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/projects/{project_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxProjectWrap.model_validate_json(response.text)

            def update_a_project(
                self, request_body: FortnoxProjectWrap, project_number: str
            ) -> FortnoxProjectWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/projects/{project_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxProjectWrap.model_validate_json(response.text)

        class SalaryTransactions:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def list_all_salary_transactions_for_all_employees(
                self,
                employee_id: Optional[str] = None,
                date: Optional[str] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxSalaryTransactionListItemList:
                """Supports query-string parameters employeeid and date for filtering the result."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/salarytransactions",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "employeeId": employee_id,
                        "date": date,
                    },
                )

                return FortnoxSalaryTransactionListItemList.model_validate_json(
                    response.text
                )

            def create_a_new_salary_transaction_for_an_employee(
                self, request_body: FortnoxSalaryTransactionWrap
            ) -> FortnoxSalaryTransactionWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/salarytransactions",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSalaryTransactionWrap.model_validate_json(response.text)

            def delete_a_single_salary_transaction(
                self, salary_row: str
            ) -> FortnoxSalaryTransactionWrap:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/salarytransactions/{salary_row}",
                    request_body=None,
                )

                return FortnoxSalaryTransactionWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_salary_transaction(
                self, salary_row: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSalaryTransactionWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/salarytransactions/{salary_row}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSalaryTransactionWrap.model_validate_json(response.text)

            def update_a_salary_transaction(
                self, request_body: FortnoxSalaryTransactionWrap, salary_row: str
            ) -> FortnoxSalaryTransactionWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/salarytransactions/{salary_row}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSalaryTransactionWrap.model_validate_json(response.text)

        class ScheduleTimes:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_specific_schedule_time(
                self,
                employee_resource_id: str,
                date: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxScheduleTimeWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/scheduletimes/{employee_resource_id}/{date}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxScheduleTimeWrap.model_validate_json(response.text)

            def update_a_schedule_time(
                self,
                request_body: FortnoxScheduleTimeWrap,
                employee_resource_id: str,
                date: str,
            ) -> FortnoxScheduleTimeWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/scheduletimes/{employee_resource_id}/{date}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxScheduleTimeWrap.model_validate_json(response.text)

            def reset_schedule_time(
                self, employee_resource_id: str, date: str
            ) -> FortnoxScheduleTimeWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/scheduletimes/{employee_resource_id}/{date}/resetday",
                    request_body=None,
                )

                return FortnoxScheduleTimeWrap.model_validate_json(response.text)

        class CompanySettings:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_the_company_settings(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxCompanySettingsWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/settings/company",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxCompanySettingsWrap.model_validate_json(response.text)

        class LockedPeriod:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_the_locked_period(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxLockedPeriodWrap:
                """If no date is returned, no period is locked."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/settings/lockedperiod",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxLockedPeriodWrap.model_validate_json(response.text)

        class Sie:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_sie_file(
                self,
                type: str,
                financial_year: Optional[int] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxWebException:
                """Retrieves a SIE file as streamed content"""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/sie/{type}",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "financialYear": financial_year,
                    },
                )

                return FortnoxWebException.model_validate_json(response.text)

        class SupplierInvoiceAccruals:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_supplier_invoice_accruals(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSupplierInvoiceAccrualListItemList:
                """The supplier invoice accruals register can return a list of records or a single record. By specifying a SupplierInvoiceNumber in the URL, a single record will be returned. Not specifying a SupplierInvoiceNumber will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/supplierinvoiceaccruals",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierInvoiceAccrualListItemList.model_validate_json(
                    response.text
                )

            def create_a_supplier_invoice_accrual(
                self, request_body: FortnoxSupplierInvoiceAccrualWrap
            ) -> FortnoxSupplierInvoiceAccrualWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/supplierinvoiceaccruals",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierInvoiceAccrualWrap.model_validate_json(
                    response.text
                )

            def remove_a_supplier_invoice_accrual(
                self, supplier_invoice_number: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/supplierinvoiceaccruals/{supplier_invoice_number}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_supplier_invoice_accrual(
                self,
                supplier_invoice_number: str,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxSupplierInvoiceAccrualWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/supplierinvoiceaccruals/{supplier_invoice_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierInvoiceAccrualWrap.model_validate_json(
                    response.text
                )

            def update_a_supplier_invoice_accrual(
                self,
                request_body: FortnoxSupplierInvoiceAccrualWrap,
                supplier_invoice_number: str,
            ) -> FortnoxSupplierInvoiceAccrualWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoiceaccruals/{supplier_invoice_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierInvoiceAccrualWrap.model_validate_json(
                    response.text
                )

        class SupplierInvoiceExternalUrlConnections:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            def create_a_supplier_invoice_external_url_connection(
                self, request_body: FortnoxSupplierInvoiceExternalUrlConnectionUpdate
            ) -> FortnoxSupplierInvoiceExternalUrlConnectionSingle:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/supplierinvoiceexternalurlconnections",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierInvoiceExternalUrlConnectionSingle.model_validate_json(
                    response.text
                )

            def remove_a_supplier_invoice_external_url_connection(
                self, resource_id: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/supplierinvoiceexternalurlconnections/{resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_supplier_invoice_external_url_connection(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSupplierInvoiceExternalUrlConnectionSingle:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/supplierinvoiceexternalurlconnections/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierInvoiceExternalUrlConnectionSingle.model_validate_json(
                    response.text
                )

            def update_a_supplier_invoice_external_url_connection(
                self,
                request_body: FortnoxSupplierInvoiceExternalUrlConnectionUpdate,
                resource_id: str,
            ) -> FortnoxSupplierInvoiceExternalUrlConnectionSingle:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoiceexternalurlconnections/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierInvoiceExternalUrlConnectionSingle.model_validate_json(
                    response.text
                )

        class SupplierInvoiceFileConnections:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_supplier_invoice_file_connections(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSupplierInvoiceFileConnectionList:
                """The supplier invoice file connections register can return a list of records or a single record. By specifying a FileId in the URL, a single record will be returned. Not specifying a FileId will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/supplierinvoicefileconnections",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierInvoiceFileConnectionList.model_validate_json(
                    response.text
                )

            def create_an_supplier_invoice_file_connection(
                self, request_body: FortnoxSupplierInvoiceFileConnectionWrap
            ) -> FortnoxSupplierInvoiceFileConnectionWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/supplierinvoicefileconnections",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierInvoiceFileConnectionWrap.model_validate_json(
                    response.text
                )

            def remove_an_supplier_invoice_file_connection(
                self, file_resource_id: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/supplierinvoicefileconnections/{file_resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_supplier_invoice_file_connection(
                self, file_resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSupplierInvoiceFileConnectionWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/supplierinvoicefileconnections/{file_resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierInvoiceFileConnectionWrap.model_validate_json(
                    response.text
                )

        class SupplierInvoicePayments:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_supplier_invoice_payments(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSupplierInvoicePaymentListItemList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/supplierinvoicepayments",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierInvoicePaymentListItemList.model_validate_json(
                    response.text
                )

            def create_a_supplier_invoice_payment(
                self, request_body: FortnoxSupplierInvoicePaymentWrap
            ) -> FortnoxSupplierInvoicePaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/supplierinvoicepayments",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierInvoicePaymentWrap.model_validate_json(
                    response.text
                )

            def remove_a_supplier_invoice_payment(
                self, number: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/supplierinvoicepayments/{number}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_supplier_invoice_payment(
                self, number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSupplierInvoicePaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/supplierinvoicepayments/{number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierInvoicePaymentWrap.model_validate_json(
                    response.text
                )

            def update_a_supplier_invoice_payment(
                self, request_body: FortnoxSupplierInvoicePaymentWrap, number: str
            ) -> FortnoxSupplierInvoicePaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoicepayments/{number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierInvoicePaymentWrap.model_validate_json(
                    response.text
                )

            def bookkeep_a_supplier_invoice_payment(
                self, number: str
            ) -> FortnoxSupplierInvoicePaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoicepayments/{number}/bookkeep",
                    request_body=None,
                )

                return FortnoxSupplierInvoicePaymentWrap.model_validate_json(
                    response.text
                )

        class SupplierInvoices:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_supplier_invoices(
                self,
                filter: Optional[
                    Literal[
                        "cancelled",
                        "fullypaid",
                        "unpaid",
                        "unpaidoverdue",
                        "unbooked",
                        "pendingpayment",
                        "authorizepending",
                    ]
                ] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxSupplierInvoiceListItemWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/supplierinvoices",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "filter": filter,
                    },
                )

                return FortnoxSupplierInvoiceListItemWrap.model_validate_json(
                    response.text
                )

            def create_a_supplier_invoice(
                self, request_body: FortnoxSupplierInvoiceWrap
            ) -> FortnoxSupplierInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/supplierinvoices",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierInvoiceWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_supplier_invoice(
                self, given_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSupplierInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/supplierinvoices/{given_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierInvoiceWrap.model_validate_json(response.text)

            def update_a_supplier_invoice(
                self, request_body: FortnoxSupplierInvoiceWrap, given_number: str
            ) -> FortnoxSupplierInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoices/{given_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierInvoiceWrap.model_validate_json(response.text)

            def approval_of_bookkeep_of_given_supplier_invoice(
                self, given_number: str
            ) -> FortnoxSupplierInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoices/{given_number}/approvalbookkeep",
                    request_body=None,
                )

                return FortnoxSupplierInvoiceWrap.model_validate_json(response.text)

            def approval_of_payment_of_given_supplier_invoice(
                self, given_number: str
            ) -> FortnoxSupplierInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoices/{given_number}/approvalpayment",
                    request_body=None,
                )

                return FortnoxSupplierInvoiceWrap.model_validate_json(response.text)

            def bookkeep_given_supplier_invoice(
                self, given_number: str
            ) -> FortnoxSupplierInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoices/{given_number}/bookkeep",
                    request_body=None,
                )

                return FortnoxSupplierInvoiceWrap.model_validate_json(response.text)

            def cancels_given_supplier_invoice(
                self, given_number: str
            ) -> FortnoxSupplierInvoiceWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoices/{given_number}/cancel",
                    request_body=None,
                )

                return FortnoxSupplierInvoiceWrap.model_validate_json(response.text)

            def credit_given_supplier_invoice(
                self, given_number: str
            ) -> FortnoxSupplierInvoiceWrap:
                """The created credit invoice will be referenced in the property CreditReference."""
                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/supplierinvoices/{given_number}/credit",
                    request_body=None,
                )

                return FortnoxSupplierInvoiceWrap.model_validate_json(response.text)

        class Suppliers:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_suppliers(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSupplierListItemList:
                """The supplier register can return a list of records or a single record. By specifying a SupplierNumber in the URL, a single record will be returned. Not specifying a SupplierNumber will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/suppliers",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierListItemList.model_validate_json(response.text)

            def create_a_supplier(
                self, request_body: FortnoxSupplierWrap
            ) -> FortnoxSupplierWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/suppliers",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_supplier(
                self, supplier_number: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxSupplierWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/suppliers/{supplier_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxSupplierWrap.model_validate_json(response.text)

            def update_a_supplier(
                self, request_body: FortnoxSupplierWrap, supplier_number: str
            ) -> FortnoxSupplierWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/suppliers/{supplier_number}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxSupplierWrap.model_validate_json(response.text)

        class TaxReductions:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_tax_reductions(
                self,
                filter: Optional[Literal["invoices", "orders", "offers"]] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxTaxReductionListItemList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/taxreductions",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "filter": filter,
                    },
                )

                return FortnoxTaxReductionListItemList.model_validate_json(
                    response.text
                )

            def create_a__tax__reduction(
                self, request_body: FortnoxTaxReductionWrap
            ) -> FortnoxTaxReductionWrap:
                """Note that different types of tax reduction, i.e. ROT, RUT, or Green Technology, applications work differently.
                When creating an application for Green Technology, the field TaxReductionAmounts becomes mandatory as
                it is used to determine how much of the asked amount is intended for which type of work. Similarly, the AskedAmount
                field of the TaxReduction becomes optional, as it will always be considered to be equal to the sum of the TaxReductionAmounts.

                For the other types, ROT and RUT, this field is not required and should be omitted.

                Unlike earlier iterations of this endpoint, specifying the type of reduction for the provided TaxReduction (e.g. ROT, RUT, or Green)
                is not necessary as this value will always be equal to the type set on the provided document instead.

                This endpoint can raise a variety of validation errors, some of which are only relevant for Green Technology applications.
                Those errors will always return an HTTP Code of 400 and include, but are not limited to, those shown below:


                    Errors that can be raised by this endpoint.

                        Error Code
                        Types
                        Description
                        Solution


                        2000600
                        ROT, RUT, GREEN
                        The provided Social Security Number is already in use for this document.
                        Verify that the Social Security Number is different from any other applicants already added.


                        2004217, 2004218
                        ROT, RUT, GREEN
                        The total asked amount of the application is either in an invalid format or is negative.
                        Verify that the AskedAmount-field is a positive number (0 is valid for Green Technology) and that it is an integer.


                        2004209
                        GREEN
                        The WorkType-field contains a work type that is not valid for the given type of reduction.
                        Ensure that the WorkType contains a valid type of work for Green Technology.


                        2004263
                        GREEN
                        The TaxReductionAmounts-field is missing for a Green Technology application.
                        Ensure that the field is included, that it is an array, and that each contained object denotes a specific type's asked amount.


                        2004262
                        GREEN
                        There are more than one object denoting the asked amount for the same type in the TaxReductionAmounts-field.
                        Ensure that there is only one object denoting the asked amount per type contained in the array.

                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/taxreductions",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxTaxReductionWrap.model_validate_json(response.text)

            def remove_a_tax_reduction(self, resource_id: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/taxreductions/{resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_tax_reduction(
                self, resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxTaxReductionWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/taxreductions/{resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxTaxReductionWrap.model_validate_json(response.text)

            def update_a_tax_reduction(
                self, request_body: FortnoxTaxReductionWrap, resource_id: str
            ) -> FortnoxTaxReductionWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/taxreductions/{resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxTaxReductionWrap.model_validate_json(response.text)

        class TermsOfDeliveries:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_terms_of_deliveries(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxTermsOfDeliveryList:
                """The terms of deliveries register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/termsofdeliveries",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxTermsOfDeliveryList.model_validate_json(response.text)

            def create_a_terms_of_delivery(
                self, request_body: FortnoxTermsOfDeliveryWrap
            ) -> FortnoxTermsOfDeliveryWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/termsofdeliveries",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxTermsOfDeliveryWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_terms_of_delivery(
                self, code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxTermsOfDeliveryWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/termsofdeliveries/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxTermsOfDeliveryWrap.model_validate_json(response.text)

            def update_a_terms_of_delivery(
                self, request_body: FortnoxTermsOfDeliveryWrap, code: str
            ) -> FortnoxTermsOfDeliveryWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/termsofdeliveries/{code}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxTermsOfDeliveryWrap.model_validate_json(response.text)

        class TermsOfPayments:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_all_terms_of_payments(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxTermsOfPaymentList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/termsofpayments",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxTermsOfPaymentList.model_validate_json(response.text)

            def create_a_term_of_payment(
                self, request_body: FortnoxTermsOfPaymentWrap
            ) -> FortnoxTermsOfPaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/termsofpayments",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxTermsOfPaymentWrap.model_validate_json(response.text)

            def remove_a_term_of_payment(self, code: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/termsofpayments/{code}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_terms_of_payment(
                self, code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxTermsOfPaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/termsofpayments/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxTermsOfPaymentWrap.model_validate_json(response.text)

            def update_a_term_of_payment(
                self, request_body: FortnoxTermsOfPaymentWrap, code: str
            ) -> FortnoxTermsOfPaymentWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/termsofpayments/{code}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxTermsOfPaymentWrap.model_validate_json(response.text)

        class Units:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_units(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxUnitList:
                """The units register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/units",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxUnitList.model_validate_json(response.text)

            def create_a_unit(self, request_body: FortnoxUnitWrap) -> FortnoxUnitWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/units",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxUnitWrap.model_validate_json(response.text)

            def remove_a_unit(self, code: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/units/{code}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_unit(
                self, code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxUnitWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/units/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxUnitWrap.model_validate_json(response.text)

            def update_a_unit(
                self, request_body: FortnoxUnitWrap, code: str
            ) -> FortnoxUnitWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/units/{code}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxUnitWrap.model_validate_json(response.text)

        class VacationDebtBasis:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_specific_vacation_debt_basis_for_a_posted_voucher(
                self, year: str, month: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxVacationDebtBasisWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/vacationdebtbasis/{year}/{month}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxVacationDebtBasisWrap.model_validate_json(response.text)

        class VoucherFileConnections:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_voucher_file_connections(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxVoucherFileConnectionList:
                """The voucher file connections register can return a list of records or a single record. By specifying a FileId in the URL, a single record will be returned. Not specifying a FileId will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/voucherfileconnections",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxVoucherFileConnectionList.model_validate_json(
                    response.text
                )

            def create_a_voucher_file_connection(
                self, request_body: FortnoxVoucherFileConnectionWrap
            ) -> FortnoxVoucherFileConnectionWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/voucherfileconnections",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxVoucherFileConnectionWrap.model_validate_json(
                    response.text
                )

            def remove_a_voucher_file_connection(
                self, file_resource_id: str
            ) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/voucherfileconnections/{file_resource_id}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_voucher_file_connection(
                self, file_resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxVoucherFileConnectionWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/voucherfileconnections/{file_resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxVoucherFileConnectionWrap.model_validate_json(
                    response.text
                )

        class Vouchers:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_all_vouchers(
                self,
                financialyear: Optional[int] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxVoucherListItemList:
                """Note that vouchers have two keys, one for voucher series and one for voucher number. The financial year is also specified for each voucher, this is due to the same voucher series and number is used each year.
                To get a unique voucher you need the voucher series, the voucher number and the financial year. These properties will always be returned where ever vouchers is used.
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/vouchers",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "financialyear": financialyear,
                    },
                )

                return FortnoxVoucherListItemList.model_validate_json(response.text)

            def create_a_voucher(
                self,
                request_body: FortnoxVoucherWrap,
                financialyear: Optional[int] = None,
            ) -> FortnoxVoucherWrap:
                """The created voucher will be returned if everything succeeded, if there was any problems an error will be returned.
                If no query param is used the voucher will be created in the preselected financial year. Go to the financialyears endpoint to read on how to retreive the Financial year id.
                """
                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/vouchers",
                    request_body=request_body,
                    content_type="application/json",
                    query_params={
                        "financialyear": financialyear,
                    },
                )

                return FortnoxVoucherWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_list_of_vouchers_for_a_specific_series(
                self,
                voucher_series: str,
                financialyear: Optional[int] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxVoucherListItemList:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/vouchers/sublist/{voucher_series}",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "financialyear": financialyear,
                    },
                )

                return FortnoxVoucherListItemList.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_specific_voucher(
                self,
                voucher_series: str,
                voucher_number: str,
                financialyear: Optional[int] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FortnoxVoucherWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/vouchers/{voucher_series}/{voucher_number}",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "financialyear": financialyear,
                    },
                )

                return FortnoxVoucherWrap.model_validate_json(response.text)

        class VoucherSeries:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_voucher_series(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxVoucherSeriesListItemList:
                """The voucher series register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/voucherseries",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxVoucherSeriesListItemList.model_validate_json(
                    response.text
                )

            def create_a_voucher_series(
                self, request_body: FortnoxVoucherSeriesWrap
            ) -> FortnoxVoucherSeriesWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/voucherseries",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxVoucherSeriesWrap.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_voucher_series(
                self, code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxVoucherSeriesWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/voucherseries/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxVoucherSeriesWrap.model_validate_json(response.text)

            def update_a_voucher_series(
                self, request_body: FortnoxVoucherSeriesWrap, code: str
            ) -> FortnoxVoucherSeriesWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/voucherseries/{code}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxVoucherSeriesWrap.model_validate_json(response.text)

        class WayOfDeliveries:
            def __init__(self, closest_parent: "Fortpyx.Fortnox", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def retrieve_a_list_of_way_of_deliveries(
                self, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxWayOfDeliveryList:
                """The way of delivery register can return a list of records or a single record. By specifying a Code in the URL, a single record will be returned. Not specifying a Code will return a list of records."""
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/3/wayofdeliveries",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxWayOfDeliveryList.model_validate_json(response.text)

            def create_a_way_of_delivery(
                self, request_body: FortnoxWayOfDeliveryWrap
            ) -> FortnoxWayOfDeliveryWrap:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/3/wayofdeliveries",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxWayOfDeliveryWrap.model_validate_json(response.text)

            def remove_a_way_of_delivery(self, code: str) -> FortnoxWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/3/wayofdeliveries/{code}",
                    request_body=None,
                )

                return FortnoxWebException.model_validate_json(response.text)

            @auto_consume_pages
            def retrieve_a_single_way_of_delivery(
                self, code: str, page: int = 1, offset: Optional[int] = None
            ) -> FortnoxWayOfDeliveryWrap:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/3/wayofdeliveries/{code}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return FortnoxWayOfDeliveryWrap.model_validate_json(response.text)

            def update_a_way_of_delivery(
                self, request_body: FortnoxWayOfDeliveryWrap, code: str
            ) -> FortnoxWayOfDeliveryWrap:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/3/wayofdeliveries/{code}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FortnoxWayOfDeliveryWrap.model_validate_json(response.text)

    class Fileattachments:
        def __init__(self, parent: "Fortpyx"):
            self.parent = parent
            self.attachment = Fortpyx.Fileattachments.Attachment(self, parent)

        class Attachment:
            def __init__(
                self, closest_parent: "Fortpyx.Fileattachments", top: "Fortpyx"
            ):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def get_attached_files_on_an_entity(
                self,
                entityid: Optional[int] = None,
                entitytype: Optional[
                    Literal["OF", "O", "F", "C", "LGR_IO", "LGR_IG"]
                ] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FileattachmentsAttachment:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/fileattachments/attachments-v1",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "entityid": entityid,
                        "entitytype": entitytype,
                    },
                )

                return FileattachmentsAttachment.model_validate_json(response.text)

            def attach_files_to_one_or_more_entities(
                self, request_body: FileattachmentsAttachment
            ) -> FileattachmentsAttachment:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/fileattachments/attachments-v1",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FileattachmentsAttachment.model_validate_json(response.text)

            @auto_consume_pages
            def list_number_of_attachments(
                self,
                entityids: Optional[int] = None,
                entitytype: Optional[
                    Literal["OF", "O", "F", "C", "LGR_IO", "LGR_IG"]
                ] = None,
                page: int = 1,
                offset: Optional[int] = None,
            ) -> FileattachmentsNumberOfAttachments:

                response = self.top._execute(  # noqa
                    http_verb="get",
                    path="/api/fileattachments/attachments-v1/numberofattachments",
                    request_body=None,
                    page=page,
                    offset=offset,
                    query_params={
                        "entityids": entityids,
                        "entitytype": entitytype,
                    },
                )

                return FileattachmentsNumberOfAttachments.model_validate_json(
                    response.text
                )

            def validates_a_list_of_attachments_that_will_be_included_on_send(
                self, request_body: FileattachmentsAttachment
            ) -> FileattachmentsWebException:

                response = self.top._execute(  # noqa
                    http_verb="post",
                    path="/api/fileattachments/attachments-v1/validateincludedonsend",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FileattachmentsWebException.model_validate_json(response.text)

            def detach_file(
                self, attachment_resource_id: str
            ) -> FileattachmentsWebException:

                response = self.top._execute(  # noqa
                    http_verb="delete",
                    path=f"/api/fileattachments/attachments-v1/{attachment_resource_id}",
                    request_body=None,
                )

                return FileattachmentsWebException.model_validate_json(response.text)

            def update_attachment(
                self,
                request_body: FileattachmentsAttachment,
                attachment_resource_id: str,
            ) -> FileattachmentsAttachment:

                response = self.top._execute(  # noqa
                    http_verb="put",
                    path=f"/api/fileattachments/attachments-v1/{attachment_resource_id}",
                    request_body=request_body,
                    content_type="application/json",
                )

                return FileattachmentsAttachment.model_validate_json(response.text)

    class Developer:
        def __init__(self, parent: "Fortpyx"):
            self.parent = parent
            self.integration__sales = Fortpyx.Developer.IntegrationSales(self, parent)

        class IntegrationSales:
            def __init__(self, closest_parent: "Fortpyx.Developer", top: "Fortpyx"):
                self.closest_parent = closest_parent
                self.top = top

            @auto_consume_pages
            def resolves_sales_information_and_active_users_of_an_integration(
                self, app_resource_id: str, page: int = 1, offset: Optional[int] = None
            ) -> IntegrationPartnerAppSalesResponse:
                """Prerequisites
                The partner has an active developer account and a published integration that is purchased through Fortnox.
                """
                response = self.top._execute(  # noqa
                    http_verb="get",
                    path=f"/api/integration-partner/apps/sales-v1/{app_resource_id}",
                    request_body=None,
                    page=page,
                    offset=offset,
                )

                return IntegrationPartnerAppSalesResponse.model_validate_json(
                    response.text
                )
