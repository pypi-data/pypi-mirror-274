import json
from typing import List, Union

from zaiclient import config
from zaiclient.request.Recommendations.RecommendationRequest import (
    RecommendationRequest,
)


class GetRerankingRecommendation(RecommendationRequest):
    __default_offset = 0
    __default_recommendation_type = "category_page"

    def __init__(
        self,
        user_id: Union[str, None],
        item_ids: List[str],
        limit: Union[int, None] = None,
        offset: int = __default_offset,
        recommendation_type: str = __default_recommendation_type,
        options: Union[dict, None] = None,
    ):
        _limit = limit

        if limit is None:
            _limit = len(item_ids)

        _options = options

        if options is not None:
            _options = json.dumps(options)

        if item_ids is None:
            raise TypeError("None type is not available for item_ids")

        super().__init__(
            user_id=user_id,
            item_id=None,
            item_ids=item_ids,
            limit=_limit,
            offset=offset,
            recommendation_type=recommendation_type,
            options=_options,
        )

    def get_path(self, client_id: str) -> str:
        return config.ML_API_PATH_PREFIX.format(client_id) + config.RERANKING_RECOMMENDATION_PATH_PREFIX
