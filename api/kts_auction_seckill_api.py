# -*- coding: utf-8 -*-
# @Time    : 2022/5/12 10:59
# @Author  : SHIXING
# @FileName: kts_auction_seckill.py
# @Software: PyCharm
import os

from Kts_ApiTest_Http.api.base_api import BaseApi


class KtsAuctionSeckillApi(BaseApi):
    """
    竞价秒杀接口
    """
    yml_path = os.path.join(BaseApi.base_path, 'data/kts_auction_seckill/kts_auction_seckill_api.yml')

    # 删除用户的竞拍商品
    def delete_user_auction_goods(self, **kwargs):
        return self.send_steps(self.yml_path, kwargs)

    # 竞拍秒杀-删除用户预约
    def delete_user_subscribe(self, **kwargs):
        return self.send_steps(self.yml_path, kwargs)
