from typing import ClassVar, Literal, Optional, cast

from typing_extensions import Unpack

from unique_sdk._api_resource import APIResource
from unique_sdk._request_options import RequestOptions


class ShortTermMemory(APIResource["ShortTermMemory"]):
    OBJECT_NAME: ClassVar[Literal["ShortTermMemory"]] = "ShortTermMemory"

    class CreateParams(RequestOptions):
        memoryName: str
        chatId: Optional[str]
        companyId: Optional[str]
        messageId: Optional[str]
        data: Optional[str]

    class FindParams(RequestOptions):
        memoryName: str
        chatId: Optional[str]
        companyId: Optional[str]
        messageId: Optional[str]

    class UpdateParams(RequestOptions):
        memoryName: str
        chatId: Optional[str]
        companyId: Optional[str]
        messageId: Optional[str]
        data: Optional[str]

    id: str
    memoryName: str
    chatId: Optional[str]
    companyId: Optional[str]
    messageId: Optional[str]
    data: Optional[str]

    @classmethod
    def create(
        cls,
        user_id: str,
        company_id: str,
        **params: Unpack["ShortTermMemory.CreateParams"],
    ) -> "ShortTermMemory":
        """
        Create Short Term Memory
        """
        return cast(
            "ShortTermMemory",
            cls._static_request(
                "post",
                "/short-term-memory",
                user_id,
                company_id,
                params=params,
            ),
        )

    @classmethod
    def update(
        cls,
        user_id: str,
        company_id: str,
        id: str,
        **params: Unpack["ShortTermMemory.UpdateParams"],
    ) -> "ShortTermMemory":
        """
        Update Short Term Memory
        """
        return cast(
            "ShortTermMemory",
            cls._static_request(
                "post",
                f"/short-term-memory/{id}",
                user_id,
                company_id,
                params=params,
            ),
        )

    @classmethod
    def findLatest(
        cls,
        user_id: str,
        company_id: str,
        id: str,
        **params: Unpack["ShortTermMemory.UpdateParams"],
    ) -> "ShortTermMemory":
        """
        Find latest Short Term Memory
        """
        return cast(
            "ShortTermMemory",
            cls._static_request(
                "get",
                "/short-term-memory",
                user_id,
                company_id,
                params=params,
            ),
        )
