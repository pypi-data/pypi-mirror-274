from typing import List

from pytz import timezone
from datetime import datetime
from urllib.parse import urljoin, urlencode

from src.dmk_packages.database import database as db
from src.dmk_packages.crawler.naver_search_volume import NaverSearchVolumeCrawler

import pandas as pd

unique_naver_category_query = """
    WITH unique_naver_category AS (
        SELECT
            naver_category,
            split_part(naver_category, ',', 1) AS main_category,
            split_part(naver_category, ',', 1) AS sub_category,
            is_active
        FROM cheil_keyword_list
        UNION ALL
        SELECT
            naver_category,
            split_part(naver_category, ',', 1) AS main_category,
            split_part(naver_category, ',', 2) AS sub_category,
            is_active
        FROM cheil_keyword_list
    )
    SELECT DISTINCT naver_category, main_category, sub_category
    FROM unique_naver_category
    WHERE is_active
        AND main_category <> '00000000'
        AND sub_category <>'00000000'
    ORDER BY main_category, sub_category
"""

category_group_by_naver_category_query = """
    SELECT 
        STRING_AGG(A.category_num::varchar, ',' ORDER BY A.category_num) AS category_num,
        A.naver_category
    FROM cheil_keyword_list AS A
    JOIN cheil_keyword_list_state_links B
        ON A.category_num = B.keyword_id
    WHERE B.state = (SELECT MAX(state) FROM cheil_keyword_list_state_links)
    GROUP BY A.naver_category
"""

category_keyword_details_query = """
    SELECT 
        A.category_num,
        A.category,
        ARRAY [A.brand || '|b', A.compete_1 || '|c1', A.compete_2 || '|c2', A.goods_1 || '|g1', A.goods_2 || '|g2', A.goods_3 || '|g3'] AS keywords,
        A.naver_category
    FROM cheil_keyword_list AS A
    JOIN cheil_keyword_list_state_links B 
        ON A.category_num = B.keyword_id
    WHERE B.state = (SELECT MAX(state) FROM cheil_keyword_list_state_links)
"""

active_keyword_list_query = """
    WITH base AS (
        SELECT *
        FROM cheil_keyword_list AS A
        JOIN cheil_keyword_list_state_links AS B
            ON A.category_num = B.keyword_id
        WHERE B.state = (
            SELECT max(state)
            FROM cheil_keyword_list_state_links
        )
    )
    (SELECT category_num, category, 'b' AS column_name, brand AS keyword FROM base
    UNION
    SELECT category_num, category, 'c0' AS column_name, category AS keyword FROM base
    UNION
    SELECT category_num, category, 'c1' AS column_name, compete_1 AS keyword FROM base
    UNION
    SELECT category_num, category, 'c2' AS column_name, compete_2 AS keyword FROM base
    UNION
    SELECT category_num, category, 'g1' AS column_name, goods_1 AS keyword FROM base
    UNION
    SELECT category_num, category, 'g2' AS column_name, goods_2 AS keyword FROM base
    UNION
    SELECT category_num, category, 'g3' AS column_name, goods_3 AS keyword FROM base)
    ORDER BY category_num, column_name;
"""


def get_cheil_result(query_name, engine):
    if query_name == "unique_naver_category":
        query = unique_naver_category_query
    elif query_name == "category_group_by_naver_category":
        query = category_group_by_naver_category_query
    elif query_name == "category_keyword_details":
        query = category_keyword_details_query
    elif query_name == "active_keyword_list":
        query = active_keyword_list_query
    else:
        raise Exception("쿼리명을 제대로 입력해 주세요")
    return pd.read_sql_query(query, con=engine)


class NaverAdSearchApi(NaverSearchVolumeCrawler):
    def __init__(self, date_from=None, date_until=None):
        super().__init__(date_from=date_from, date_until=date_until)
        self.engine = db.get_engine("CHEIL")
        self._set_keywords(self.get_keywords())
        self._set_keywords_bundle(self.get_keywords())

    def get_keywords(self):
        return ["멕시카나치킨"]
        # result_df = get_cheil_result("category_keyword_details", self.engine)
        # return result_df.to_dict("records")[:10]

    def main(self, age_gender=False):
        search_volume_result = self.get_search_volume(age_gender=age_gender)
        search_volume_df = (pd.DataFrame
                            .from_dict(search_volume_result, orient="columns")
                            .rename(columns={"keyword_text": "keyword",
                                             "keyword_date": "collect_date",
                                             "keyword_volume": "volume_size",
                                             "collected_at": "run_date"}))

        final_results = search_volume_df.to_dict(orient="records")

        from pprint import pprint
        pprint(final_results)


if __name__ == "__main__":
    crawler = NaverAdSearchApi(
        # date_from="2024-03-01",
        # date_until="2024-03-05"
    )
    crawler.main(age_gender=False)
    # print(hi)
