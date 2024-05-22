from __future__ import annotations

import logging
from typing import Dict, List, Literal, Tuple, Union

import requests

logger = logging.getLogger(__name__)


class Naver:
    """NAVER Service API"""

    def __init__(
        self,
        api_key: str,
        api_sec: str,
    ) -> None:
        self.api_key: str = api_key
        self.api_sec: str = api_sec

    def local(
        self,
        query: str,
        display: int = 1,
        start: int = 1,
        sort: str = "random",
    ) -> List[Dict]:
        # https://developers.naver.com/docs/serviceapi/search/local/local.md#%EC%A7%80%EC%97%AD
        url = "https://openapi.naver.com/v1/search/local.json"
        params = {
            "query": query,
            "display": f"{display}",
            "start": f"{start}",
            "sort": f"{sort}",
        }
        headers = {
            "X-Naver-Client-Id": self.api_key,
            "X-Naver-Client-Secret": self.api_sec,
        }
        resp = requests.get(url, params=params, headers=headers)
        parsed = resp.json()
        return parsed.get("items", [])

    def lab_search(
        self,
        start_date: str,
        end_date: str,
        time_unit: Literal["date", "week", "month"],
        keyword_groups: List[Tuple[str, Tuple[str, ...]]],
        device: Literal["pc", "mo"] = None,
        gender: Literal["m", "f"] = None,
        ages: List[
            Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
        ] = None,
        debug: bool = False,
    ) -> Union[Dict, Tuple[Dict, requests.Response]]:
        # https://developers.naver.com/docs/serviceapi/datalab/search/search.md#통합-검색어-트렌드-api-레퍼런스
        url = "https://openapi.naver.com/v1/datalab/search"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": time_unit,
            "keywordGroups": [
                {"groupName": name, "keywords": kw} for name, kw in keyword_groups
            ],
            **({"device": device} if device else {}),
            **({"gender": gender} if gender else {}),
            **({"ages": ages} if ages else {}),
        }
        headers = {
            "X-Naver-Client-Id": self.api_key,
            "X-Naver-Client-Secret": self.api_sec,
        }
        resp = requests.post(url, json=params, headers=headers)
        resp.raise_for_status()
        return resp.json() if not debug else resp.json(), resp

    def lab_shopping(
        self,
        start_date: str,
        end_date: str,
        time_unit: Literal["date", "week", "month"],
        category: List[Tuple[str, Tuple[str, ...]]],
        device: Literal["pc", "mo"] = None,
        gender: Literal["m", "f"] = None,
        ages: List[Literal["10", "20", "30", "40", "50", "60"]] = None,
        debug: bool = False,
    ) -> Union[Dict, Tuple[Dict, requests.Response]]:
        # https://developers.naver.com/docs/serviceapi/datalab/shopping/shopping.md#쇼핑인사이트-api-레퍼런스
        url = "https://openapi.naver.com/v1/datalab/shopping/categories"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": time_unit,
            "category": [{"name": name, "param": kw} for name, kw in category],
            **({"device": device} if device else {}),
            **({"gender": gender} if gender else {}),
            **({"ages": ages} if ages else {}),
        }
        headers = {
            "X-Naver-Client-Id": self.api_key,
            "X-Naver-Client-Secret": self.api_sec,
        }
        resp = requests.post(url, json=params, headers=headers)
        resp.raise_for_status()
        return resp.json() if not debug else resp.json(), resp


if __name__ == "__main__":
    api_key, api_sec = "4LmEBVOylhQ9Da_Rhryr", "WwF0cMKQKS"

    self = naver = Naver(api_key, api_sec)
    resp = naver.lab_search(
        start_date="2017-01-01",
        end_date="2017-04-30",
        time_unit="month",
        keyword_groups=[("한글", ["한글", "korean"]), ("영어", ["영어", "english"])],
        device="pc",
        # gender="f",
        # ages=["1", "2"],
        debug=True,
    )
    resp[1].request.body
