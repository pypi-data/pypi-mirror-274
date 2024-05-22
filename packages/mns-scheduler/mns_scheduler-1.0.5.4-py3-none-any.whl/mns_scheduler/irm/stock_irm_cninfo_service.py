import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import akshare as ak
import mns_common.utils.data_frame_util as data_frame_util
import pandas as pd
from loguru import logger


# 获取股票提问    互动易-提问
def get_stock_irm_cninfo(symbol):
    try:
        stock_irm_cninfo_df = ak.stock_irm_cninfo(symbol)
    except Exception as e:
        logger.error("获取提问者异常:{},{}", symbol, e)
        return pd.DataFrame()
    if data_frame_util.is_empty(stock_irm_cninfo_df):
        return pd.DataFrame()
    stock_irm_cninfo_df = stock_irm_cninfo_df.rename(columns={"股票代码": "symbol",
                                                              "公司简称": "name",
                                                              "行业": "industry",
                                                              "行业代码": "industry_code",
                                                              "问题": "question",
                                                              '提问者': "questioner",
                                                              '来源': "source",
                                                              '提问时间': "question_time",
                                                              '更新时间': "update_time",
                                                              "提问者编号": "questioner_no",
                                                              "问题编号": "question_no",
                                                              "回答ID": "answer_id",
                                                              "回答内容": "answer_content",
                                                              "回答者": "answer"
                                                              })
    return stock_irm_cninfo_df


if __name__ == '__main__':
    get_stock_irm_cninfo('301191')
