"""Classes to handle API queries/searches"""
import logging
from typing import Any, Dict, List, Type, Optional
from .model import Venue, Event, Attraction, Classification

log = logging.getLogger(__name__)

class BaseQuery:
    """Base query/parent class for specific search types."""
    attr_map = {
        'start_date_time': 'startDateTime',
        'end_date_time': 'endDateTime',
        'onsale_start_date_time': 'onsaleStartDateTime',
        'onsale_end_date_time': 'onsaleEndDateTime',
        'country_code': 'countryCode',
        'state_code': 'stateCode',
        'venue_id': 'venueId',
        'attraction_id': 'attractionId',
        'segment_id': 'segmentId',
        'segment_name': 'segmentName',
        'classification_name': 'classificationName',
        'classification_id': 'classificationId',
        'market_id': 'marketId',
        'promoter_id': 'promoterId',
        'dma_id': 'dmaId',
        'include_tba': 'includeTBA',
        'include_tbd': 'includeTBD',
        'client_visibility': 'clientVisibility',
        'include_test': 'includeTest',
        'keyword': 'keyword',
        'id': 'id',
        'sort': 'sort',
        'page': 'page',
        'size': 'size',
        'locale': 'locale',
        'latlong': 'latlong',
        'radius': 'radius'
    }

    def __init__(self, api_client, method: str, model: Type[Any]):
        self.api_client = api_client
        self.method = method
        self.model = model

    async def _get(self, **kwargs: Any) -> List[Any]:
        """Asynchronously handles basic API search request"""
        params = self._search_params(**kwargs)
        url = f"{self.api_client.url}/{self.method}.json"
        async with self.api_client.session.get(url, params={**self.api_client.api_key, **params}) as response:
            response.raise_for_status()
            data = await response.json()
            return [self.model.from_json(item) for item in data.get('_embedded', {}).get(self.method, [])]

    async def by_id(self, entity_id: str) -> Any:
        """Asynchronously get a specific object by its ID"""
        response = await self._get(id=entity_id)
        return self.model.from_json(response)

    def _search_params(self, **kwargs: Any) -> Dict[str, Any]:
        """Maps parameter names to API-friendly parameters"""
        return {self.attr_map.get(k, k): v for k, v in kwargs.items() if v is not None}

class AttractionQuery(BaseQuery):
    def __init__(self, api_client):
        super().__init__(api_client, 'attractions', Attraction)

    async def find(self, **kwargs: Any) -> List[Attraction]:
        return await self._get(**kwargs)

class ClassificationQuery(BaseQuery):
    def __init__(self, api_client):
        super().__init__(api_client, 'classifications', Classification)

    async def find(self, **kwargs: Any) -> List[Classification]:
        return await self._get(**kwargs)

    async def segment_by_id(self, segment_id: str) -> Optional[Any]:
        """Return a `Segment` matching this ID"""
        classification = await self.by_id(segment_id)
        return classification.segment if classification else None

    async def genre_by_id(self, genre_id: str) -> Optional[Any]:
        """Return a `Genre` matching this ID"""
        classification = await self.by_id(genre_id)
        if classification and classification.segment:
            for genre in classification.segment.genres:
                if genre.id == genre_id:
                    return genre
        return None

    async def subgenre_by_id(self, subgenre_id: str) -> Optional[Any]:
        """Return a `SubGenre` matching this ID"""
        classification = await self.by_id(subgenre_id)
        if classification and classification.segment:
            for genre in classification.segment.genres:
                for subgenre in genre.subgenres:
                    if subgenre.id == subgenre_id:
                        return subgenre
        return None

class EventQuery(BaseQuery):
    def __init__(self, api_client):
        super().__init__(api_client, 'events', Event)

    async def find(self, **kwargs: Any) -> List[Event]:
        return await self._get(**kwargs)

class VenueQuery(BaseQuery):
    def __init__(self, api_client):
        super().__init__(api_client, 'venues', Venue)

    async def find(self, **kwargs: Any) -> List[Venue]:
        return await self._get(**kwargs)
