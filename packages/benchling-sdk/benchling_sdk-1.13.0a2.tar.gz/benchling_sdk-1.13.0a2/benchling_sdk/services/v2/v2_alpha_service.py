from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from benchling_api_client.v2.stable.client import Client

from benchling_sdk.helpers.client_helpers import v2_alpha_client
from benchling_sdk.helpers.retry_helpers import RetryStrategy

if TYPE_CHECKING:
    from benchling_sdk.services.v2.alpha.v2_alpha_app_service import V2AlphaAppService
    from benchling_sdk.services.v2.alpha.v2_alpha_dna_sequence_service import V2AlphaDnaSequenceService

from benchling_sdk.services.v2.base_service import BaseService


class V2AlphaService(BaseService):
    """
    V2-alpha.

    Alpha endpoints have different stability guidelines than other stable endpoints.

    See https://benchling.com/api/v2-alpha/reference
    """

    _app_service: Optional[V2AlphaAppService]
    _dna_sequence_service: Optional[V2AlphaDnaSequenceService]
    _alpha_client: Client

    def __init__(self, client: Client, retry_strategy: RetryStrategy = RetryStrategy()):
        """
        Initialize a v2-alpha service.

        :param client: Underlying generated Client.
        :param retry_strategy: Retry strategy for failed HTTP calls
        """
        super().__init__(client, retry_strategy)
        self._alpha_client = v2_alpha_client(self.client)
        self._app_service = None
        self._dna_sequence_service = None

    @property
    def apps(self) -> V2AlphaAppService:
        """
        V2-Alpha Apps.

        Create and manage Apps on your tenant.

        https://benchling.com/api/v2-alpha/reference?stability=not-available#/Apps
        """
        if self._app_service is None:
            from benchling_sdk.services.v2.alpha.v2_alpha_app_service import V2AlphaAppService

            self._app_service = V2AlphaAppService(self._alpha_client, self._retry_strategy)
        return self._app_service

    @property
    def dna_sequences(self) -> V2AlphaDnaSequenceService:
        """
        V2-Alpha DNA Sequences.

        DNA sequences are the bread and butter of the Benchling Molecular Biology suite. On Benchling, these are
        comprised of a string of nucleotides and collections of other attributes, such as annotations and primers.

        See https://benchling.com/api/v2-alpha/reference#/DNA%20Sequences
        """
        if self._dna_sequence_service is None:
            from benchling_sdk.services.v2.alpha.v2_alpha_dna_sequence_service import (
                V2AlphaDnaSequenceService,
            )

            self._dna_sequence_service = V2AlphaDnaSequenceService(self._alpha_client, self._retry_strategy)
        return self._dna_sequence_service
