import os
import configparser
import sys

import requests

class Search(object):

    def __init__(self):
        self.search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search'  # 搜索模块api链接
        self.knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost'  # 知识库api链接
        self.config_file = 'config.conf'

    def get_user_token(self):
        user_token = ''
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            try:
                user_token = config['token']['token']
            except:
                sys.exit(0)
        return user_token

    def search_data(self, type, input_data):
        data = {
            "pageNo": 1,
            "pageSize": 100,
            "query": input_data,
            "type": type
        }
        return data

    def requests_search_api(self, type,  input_data):
        search_api_url = self.search_api_url
        user_token = self.get_user_token()
        headers = {
            "authorization": user_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        }
        search_data = self.search_data(type=type, input_data=input_data)
        requests_res = requests.post(url=search_api_url, headers=headers, json=search_data).json()
        if requests_res['code'] == 4018:
            print("\033[31m[ERRO]\033[0m " + requests_res['msg'])
            sys.exit(0)
        if type == 'web':
            search_info = requests_res['data']['wsSubDomainInfoDtoList']['wsSubDomainInfoDtos']
            if len(search_info) == 0:
                print('\033[33m[WARN]\033[0m 未查询到信息!')
                sys.exit(0)
            print('\033[32m[SUCC]\033[0m 查询成功')
            self.web_print_data(search_info)
        else:
            search_info = requests_res['data']['wsPortInfoDtoList']['wsPortInfoDtos']
            if len(search_info) == 0:
                print('\033[33m[WARN]\033[0m 未查询到信息!')
                sys.exit(0)
            print('\033[32m[SUCC]\033[0m 查询成功')
            self.host_print_data(search_info)
        # print(search_info)

    def web_print_data(self, search_info):
        for i in range(0, len(search_info)):
            if search_info[i]['subdomainTitle'] == None:
                search_info[i]['subdomainTitle'] = 'Unknow'
            if search_info[i]['subdomainBanner'] == None:
                search_info[i]['subdomainBanner'] = 'Unknow'
            print('\033[34m[INFO] \033[0m' +
                  'Title: ' + search_info[i]['subdomainTitle'],
                  'Subdomain: ' + search_info[i]['subdomain'],
                  'IP_ADDR: ' + search_info[i]['ipAdd'],
                  'Web servers: ' + search_info[i]['subdomainBanner'])

    def host_print_data(self, search_info):
        for i in range(0, len(search_info)):
            if search_info[i]['product'] == '':
                search_info[i]['product'] = 'Unknow'
            print('\033[34m[INFO] \033[0m' +
                  'Subdomain: ' + search_info[i]['subdomain'],
                  'IP_ADDR: ' + search_info[i]['ipAdd'],
                  'Port:' + str(search_info[i]['port']),  # type: int
                  'Service: ' + search_info[i]['service'],
                  'Product: ' + search_info[i]['product'])
    def kownledge_search(self, keyword):
        data = {
            "pageNo": 1,
            "pageSize": 12,
            "platPostDto": {
                "postTitle": keyword,
                "categoryId": ""
            }
        }
        return data

    def requests_kownledge_search_api(self, keyword):
        print('\033[34m[KEYW]\33[0m 关键字: %s' % keyword)
        knowledge_api_url = self.knowledge_api_url
        knowledge_data = self.kownledge_search(keyword)
        user_token = self.get_user_token()
        headers = {
            "authorization": user_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        }
        knowledge_api_res = requests.post(knowledge_api_url, headers=headers, json=knowledge_data)
        try:
            print('\033[32m[SUCC]\033[0m 查询成功')
            knowledge_api_res_json = knowledge_api_res.json()
            knowledge_info = knowledge_api_res_json['data']['platPostSVos']
            for i in range(0, len(knowledge_info)):
                link = 'https://plat.wgpsec.org/knowledge/view/%s' % knowledge_info[i]['postId']
                print('\033[34m[INFO]\033[0m ' + 'Title: ' + knowledge_info[i]['postTitle'], 'Link: ' + link)
        except:
            knowledge_api_res_json = knowledge_api_res.json()
            print('\033[31m[ERRO]\033[0m ' + knowledge_api_res_json['msg'])