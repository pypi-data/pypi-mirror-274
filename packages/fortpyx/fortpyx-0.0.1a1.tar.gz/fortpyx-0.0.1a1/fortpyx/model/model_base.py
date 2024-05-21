from datetime import date
from enum import Enum
from io import IOBase, BytesIO
from typing import get_args, Optional, Any, Tuple, Union, TextIO

from pydantic import BaseModel, field_validator, ConfigDict, Field
from pydantic_core.core_schema import ValidationInfo


class UploadFile(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    file: Union[IOBase, TextIO, BytesIO] = Field(
        ..., description="A file to be uploaded."
    )


class MetaInformation(BaseModel):
    total_resources: int = Field(
        ...,
        description="The total number of resources available for retrieval.",
        alias="@TotalResources",
    )
    total_pages: int = Field(
        ..., description="The total number of pages.", alias="@TotalPages"
    )
    current_page: int = Field(
        ..., description="The current page index (1-indexed).", alias="@CurrentPage"
    )

    @property
    def pages_left(self) -> int:
        return self.total_pages - self.current_page


class ModelBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    meta_information: Optional[MetaInformation] = Field(
        default=None,
        description="Paging information for paginated GET responses.",
        alias="MetaInformation",
        exclude=True,
    )

    @field_validator("*", mode="before")
    @classmethod
    def normalize_none(cls, v: Any, info: ValidationInfo) -> Any:
        """
        Fortnox unfortunately returns empty strings instead of null in their JSON responses,
        which breaks Pydantic validation for string types that are deserialized into dates, enums
        etc. This validator normalizes this by transforming select types into None instead of empty
        strings before Pydantic validation.
        """
        if isinstance(v, str):
            field_name = info.field_name

            assert field_name
            model_field = cls.model_fields[field_name]

            types = get_args(model_field.annotation)

            if ModelBase.__is_optional(types):
                for current_type in types:
                    if ModelBase.__is_not_allowed_as_empty_string(current_type):
                        return None

        return v

    @classmethod
    def __is_not_allowed_as_empty_string(cls, current_type: Any) -> bool:
        return isinstance(current_type, type(Enum)) or current_type is date

    @classmethod
    def __is_optional(cls, args: Tuple[Any, ...]) -> bool:
        optional_args_length = 2
        return len(args) == optional_args_length and type(None) in args
