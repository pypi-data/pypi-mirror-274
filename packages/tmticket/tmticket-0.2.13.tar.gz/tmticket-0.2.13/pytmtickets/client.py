import aiohttp
import logging
import re
import ssl
from typing import Any, Dict, Optional
from .query import AttractionQuery, ClassificationQuery, EventQuery, VenueQuery

log = logging.getLogger(__name__)

class AsyncApiClient:
    """AsyncApiClient is the main wrapper for the Discovery API, updated for asynchronous operation."""

    root_url = 'https://app.ticketmaster.com'
    url = 'https://app.ticketmaster.com/discovery/v2'

    def __init__(self, api_key: str):
        self.__api_key = {'apikey': api_key}
        self.events = EventQuery(api_client=self)
        self.venues = VenueQuery(api_client=self)
        self.attractions = AttractionQuery(api_client=self)
        self.classifications = ClassificationQuery(api_client=self)
        self.session = None

    async def __aenter__(self):
        ssl_context = ssl.create_default_context()
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def search(self, method: str, **kwargs: Any) -> Any:
        """Generic API request, converted for asynchronous operation"""
        params = {k: v for k, v in kwargs.items() if v is not None}
        url = self.__method_url(method)
        async with self.session.get(url, params={**self.__api_key, **params}) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Any:
        """Handles response, raising ApiException if needed or returning response JSON object asynchronously"""
        if response.status == 200:
            return await response.json()
        raise ApiException(await response.json())

    async def get_url(self, link: str) -> Any:
        """Gets a specific href from '_links' object in a response, asynchronously"""
        async with self.session.get(link) as resp:
            resp.raise_for_status()
            return await self._handle_response(resp)

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()

    @property
    def api_key(self) -> Dict[str, str]:
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key: str) -> None:
        self.__api_key = {'apikey': api_key}

    @staticmethod
    def __method_url(method: str) -> str:
        return f"{AsyncApiClient.url}/{method}.json"

class ApiException(Exception):
    """Exception thrown for API-related error messages"""
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)

class AsyncPagedResponse:
    """Asynchronously iterates through API response pages."""
    def __init__(self, api_client: AsyncApiClient, response: Dict[str, Any]):
        self.api_client = api_client
        self.page = Page.from_json(response)

    async def limit(self, max_pages: int = 5) -> Any:
        """Asynchronously retrieve a number of pages, returning a list of all entities."""
        all_items = []
        counter = 0
        async for pg in self:
            if counter >= max_pages:
                break
            counter += 1
            all_items.extend(pg)
        return all_items

    async def one(self) -> Any:
        """Asynchronously get items from the first page result."""
        return [i for i in self.page]

    async def maximum(self, max_pages: int = 49) -> Any:
        """Asynchronously retrieves maximum pages in a result, returning a flat list."""
        all_items = []
        counter = 0
        async for pg in self:
            if counter >= max_pages:
                break
            counter += 1
            all_items.extend(pg)
        return all_items

    def __aiter__(self):
        return self._page_iterator()

    async def _page_iterator(self):
        current_page = self.page
        yield current_page
        next_url = current_page.links.get('next')

        while next_url:
            log.debug(f"Requesting page: {next_url}")
            page_data = await self.api_client.get_url(next_url)
            next_page = Page.from_json(page_data)
            yield next_page
            next_url = next_page.links.get('next')

class Page:
    """Represents a page in a paged response."""
    def __init__(self, items: Any, links: Dict[str, str], page: int, size: int, total_elements: int, total_pages: int):
        self.items = items
        self.links = links
        self.page = page
        self.size = size
        self.total_elements = total_elements
        self.total_pages = total_pages

    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> 'Page':
        """Creates a `Page` object from JSON data."""
        items = json_data.get('_embedded', {}).get('events', [])
        links = json_data.get('_links', {})
        page_data = json_data.get('page', {})
        return Page(
            items=items,
            links=links,
            page=page_data.get('number', 0),
            size=page_data.get('size', 0),
            total_elements=page_data.get('totalElements', 0),
            total_pages=page_data.get('totalPages', 0)
        )

    def __iter__(self):
        return iter(self.items)

def _assign_links(obj, json_obj, base_url=None):
    """Assigns `links` attribute to an object from JSON"""
    json_links = json_obj.get('_links')
    if not json_links:
        obj.links = {}
    else:
        obj_links = {}
        for k, v in json_links.items():
            if 'href' in v:
                href = re.sub("({.+})", "", v['href'])
                if base_url:
                    href = f"{base_url}{href}"
                obj_links[k] = href
            else:
                obj_links[k] = v
        obj.links = obj_links
