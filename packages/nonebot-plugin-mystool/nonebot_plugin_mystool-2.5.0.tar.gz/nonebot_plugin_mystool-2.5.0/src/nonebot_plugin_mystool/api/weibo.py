import copy
import json
import random
import re
from datetime import date
from urllib.parse import unquote

import httpx

from ..utils import logger


class Tool:
    @staticmethod
    def cookie_to_dict(cookie):
        if cookie and '=' in cookie:
            cookie = dict([line.strip().split('=', 1) for line in cookie.split(';')])
        return cookie

    @classmethod
    def nested_lookup(cls, obj, key, with_keys=False, fetch_first=False):
        result = list(cls._nested_lookup(obj, key, with_keys=with_keys))
        if with_keys:
            values = [v for k, v in cls._nested_lookup(obj, key, with_keys=with_keys)]
            result = {key: values}
        if fetch_first:
            result = result[0] if result else result
        return result

    @classmethod
    def _nested_lookup(cls, obj, key, with_keys=False):
        if isinstance(obj, list):
            for i in obj:
                yield from cls._nested_lookup(i, key, with_keys=with_keys)
        if isinstance(obj, dict):
            for k, v in obj.items():
                if key == k:
                    if with_keys:
                        yield k, v
                    else:
                        yield v
                if isinstance(v, (list, dict)):
                    yield from cls._nested_lookup(v, key, with_keys=with_keys)

    @staticmethod
    def weibo_user_dict(data):
        return dict([line.strip().split(':', 1) for line in data.split('|')])


class WeiboCode:
    def __init__(self, user_data: dict):
        self.params = Tool.cookie_to_dict(user_data['params'].replace('&', ';')) if user_data['params'] else None
        """params: s=xxxxxx; gsid=xxxxxx; aid=xxxxxx; from=xxxxxx"""
        self.cookie = Tool.cookie_to_dict(user_data['cookie'])
        self.container_id = {'原神': '100808fc439dedbb06ca5fd858848e521b8716',
                             '崩铁': '100808e1f868bf9980f09ab6908787d7eaf0f0'}
        self.ua = 'WeiboOverseas/4.4.6 (iPhone; iOS 14.0.1; Scale/2.00)'
        self.headers = {'User-Agent': self.ua}
        self.follow_data_url = 'https://api.weibo.cn/2/cardlist'
        self.sign_url = 'https://api.weibo.cn/2/page/button'
        self.event_url = 'https://m.weibo.cn/api/container/getIndex?containerid={container_id}_-_activity_list'
        self.draw_url = 'https://games.weibo.cn/prize/aj/lottery'

    @property
    async def get_ticket_id(self):
        logger.info('开始获取微博兑换码ticket_id')
        ticket_id = {}
        for key, value in self.container_id.items():
            url = self.event_url.replace('{container_id}', value)
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
            responses = response.json()
            group = Tool.nested_lookup(responses, 'group', fetch_first=True)
            if group:
                ticket_id[key] = {}
                ticket_id[key]['id'] = [i
                                        for id in group
                                        for i in re.findall(r'ticket_id=(\d*)', unquote(unquote(id['scheme'])))]
                ticket_id[key]['img'] = group[random.randint(0, len(group) - 1)]['pic']
            else:
                logger.info(f'{key}超话当前没有兑换码')
        if not ticket_id:
            return "超话无兑换码活动"
        else:
            return ticket_id

    async def get_code(self, id: str):
        url = self.draw_url
        self.headers.update({
            'Referer': f'https://games.weibo.cn/prize/lottery?ua={self.ua}&from=10E2295010&ticket_id={id}&ext='
        })
        data = {
            'ext': '', 'ticket_id': id, 'aid': self.params['aid'], 'from': self.params['from']
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=data, headers=self.headers, cookies=self.cookie)
        if response.status_code == 200:
            responses = response.json()
            code = responses['data']['prize_data']['card_no'] if responses['msg'] == 'success' or responses[
                'msg'] == 'recently' else False
            if responses['msg'] == 'fail':
                responses['msg'] = responses['data']['fail_desc1']
            result = {'success': True, 'id': id, 'code': code} if code else {'success': False, 'id': id,
                                                                             'response': responses['msg']}
            return result['code'] if result['success'] else responses['msg']
        else:
            return '获取失败，请重新设置wb_cookie'

    async def get_code_list(self):
        ticket_id = await self.get_ticket_id  # 有活动则返回一个dict，没活动则返回一个str
        '''
        ticket_id = {
            '原神/崩铁': {
                'id': [],
                'img': ''
            }
        }
        '''
        if isinstance(ticket_id, dict):
            msg = ""
            code = {key: [] for key in ticket_id.keys()}
            for key, value in ticket_id.items():
                for k, v in value.items():
                    if k == 'id':
                        for item in v:
                            code[key].append(await self.get_code(item))
                    elif k == 'img':
                        img = v
            for key, values in code.items():
                msg += f"<{key}>超话兑换码：" \
                       "\n1️⃣" \
                       f"  \n{values[0]}" \
                       "\n2️⃣" \
                       f"  \n{values[1]}" \
                       "\n3️⃣" \
                       f"  \n{values[2]}"
            return msg, img
        else:
            return ticket_id


class WeiboSign:

    @staticmethod
    async def format_chaohua_data(data: list):
        """
        单个超话社区格式：
        {
            "card_type": "8",
            "itemid": "follow_super_follow_1_0",
            "scheme": "sinaweibo://pageinfo?containerid=100808e1f868bf9980f09ab6908787d7eaf0f0&extparam=%E5%B4%A9%E5%9D%8F%E6%98%9F%E7%A9%B9%E9%93%81%E9%81%93%23tabbar_follow%3D5032140432213196",
            "title_sub": "崩坏星穹铁道",
            "pic": "https://wx4.sinaimg.cn/thumbnail/008lgPsGly8hph0wdgemlj30sg0sgtcv.jpg",
            "pic_corner_radius": 6,
            "name_font_size": 16,
            "pic_size": 58,
            "top_padding": 12,
            "bottom_padding": 12,
            "buttons": [
                {
                    "type": "default",
                    "params": {
                        "action": "/2/page/button?request_url=http%3A%2F%2Fi.huati.weibo.com%2Fmobile%2Fsuper%2Factive_fcheckin%3Fpageid%3D100808e1f868bf9980f09ab6908787d7eaf0f0%26container_id%3D100808e1f868bf9980f09ab6908787d7eaf0f0%26scheme_type%3D1%26source%3Dfollow"
                    },
                    "actionlog": {
                        "act_code": 3142,
                        "fid": "100803_-_followsuper"
                    },
                    "pic": "https://h5.sinaimg.cn/upload/100/582/2020/04/14/supertopic_fans_icon_register.png",
                    "name": "签到"
                }
            ],
            "title_flag_pic": "https://n.sinaimg.cn/default/944aebbe/20220831/active_level_v.png",
            "desc1": "等级 LV.7",
            "desc2": "#崩坏星穹铁道[超话]##崩坏星穹铁道# \n哈哈哈哈，米哈游，你好事做尽啊。哈哈哈哈 ​",
            "openurl": "",
            "cleaned": true
        },
        """
        # 去除杂项字典
        data = [ch for ch in data if ch.get('card_type') == '8']
        chaohua_list = []
        for onedata in data:
            ch_id = re.findall("(?<=containerid=).*?(?=&)", onedata['scheme'])
            one_dict = {
                'title_sub': onedata['title_sub'],
                'id': ch_id[0],
                'is_sign': onedata['buttons'][0]['name']  # '已签' / '签到'
            }
            chaohua_list.append(one_dict)
        return chaohua_list

    @classmethod
    async def ch_list(cls, params_data: dict, wb_userdata: dict):

        try:
            url = 'https://api.weibo.cn/2/cardlist?'
            params = {
                "containerid": "100803_-_followsuper",
                "fid": "100803_-_followsuper",
                "since_id": '',
                "cout": 20,
            }
            params.update(params_data)
            headers = {
                "User-Agent": "Mi+10_12_WeiboIntlAndroid_6020",
                "Host": "api.weibo.cn"
            }
            cookies = Tool.cookie_to_dict(wb_userdata['cookie'])
            async with httpx.AsyncClient() as client:
                res = await client.get(url, headers=headers, params=params, cookies=cookies)
            json_chdata = json.load(res)['cards'][0]['card_group']
            list_data = await cls.format_chaohua_data(json_chdata)
            wb_userdata['CHdata_list'] = list_data
            return list_data
        except KeyError:
            return '找不到超话列表'
        except IndexError:
            return '超话列表为空'
        except Exception as e:
            # print(f'{type(e)}: {e}')
            return e

    @classmethod
    async def sign(cls, wb_userdata: dict):

        url = 'https://api.weibo.cn/2/page/button'
        request_url = 'http://i.huati.weibo.com/mobile/super/active_checkin?pageid={containerid}'
        headers = {
            "User-Agent": "Mi+10_12_WeiboIntlAndroid_6020",
            'Referer': 'https://m.weibo.cn'
        }

        param_d = Tool.cookie_to_dict(wb_userdata['params'])

        params = {
            "gsid": param_d['gsid'] if 'gsid' in param_d else None,  # 账号身份验证
            "s": param_d['s'] if 's' in param_d else None,  # 校验参数
            "from": param_d['from'] if 'from' in param_d else None,  # 客户端身份验证
            "c": param_d['c'] if 'c' in param_d else None,  # 客户端身份验证
            "aid": param_d['aid'] if 'aid' in param_d else None,  # 作用未知
        }

        msg = f'{date.today()}\n' \
              '微博超话签到：\n'
        try:
            chaohua_list = await cls.ch_list(params, wb_userdata)
            if not isinstance(chaohua_list, list):
                return f'签到失败请重新签到\n{chaohua_list}'
            for ch in chaohua_list:
                params_copy = copy.deepcopy(params)
                if ch['is_sign'] == '签到':
                    params_copy['request_url'] = request_url.format(containerid=ch['id'])
                    async with httpx.AsyncClient() as client:
                        res = await client.get(url, headers=headers, params=params_copy, timeout=10)
                    res_data = json.loads(res.text)
                    if 'msg' in res_data and 'errmsg' not in res_data:  # 今日首次签到成功
                        msg += f"{ch['title_sub']}  ✅\n"
                    elif 'errmsg' in res_data:  # 签到出错
                        # msg = f"{res_data['errmsg']}\n"
                        msg += f"{ch['title_sub']}  ❌\n"
                        msg += f"--{res_data['errmsg']}\n"
                elif ch['is_sign'] == '已签':  # 今日再次进行签到，且之前已经签到成功
                    msg += f"{ch['title_sub']}  ✅\n"
            return msg
        except Exception as e:
            return f'签到失败请重新签到,{e}'
