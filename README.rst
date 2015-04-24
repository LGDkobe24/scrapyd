=======
Scrapyd
=======

.. image:: https://secure.travis-ci.org/scrapy/scrapyd.png?branch=master
   :target: http://travis-ci.org/scrapy/scrapyd

Scrapyd is a service for running `Scrapy`_ spiders.

It allows you to deploy your Scrapy projects and control their spiders using a
HTTP JSON API.

The documentation (including installation and usage) can be found at:
http://scrapyd.readthedocs.org/

.. _Scrapy: https://github.com/scrapy/scrapy
=======
news
=======
添加一个新的json接口，请求方式为get
curl http://localhost:6800/spiderid.json?project=myproject 
返回数据为对应爬虫的最后一个调用id
{"status": "ok", "spiderid": {"chinaz_com": "1980725ed77811e4945302004a4c0012", "dg_bendibao_com": "30837c0ee8c511e4945302004a4c0012", "gd_sina_com_cn": "fdf83abae8cc11e4945302004a4c0012", "news_sun0769_com": "23e82d9ae8bc11e4945302004a4c0012", "cqgjj_cn": "80a29cd2de5811e4945302004a4c0012", "ifeng_com_4_1": "dd02d8e8d99911e4945302004a4c0012", "71bbs_people_com_cn": "8a2f5d28e18a11e4945302004a4c0012", "zhuhai.gov.cn": "de0f5e72d9a911e4945302004a4c0012", "mmbang_com": "282b0de4de8711e4945302004a4c0012", "finance_china_com_cn": "4e80016ed9a211e4945302004a4c0012", "ce_cn": "4e693d08d9a211e4945302004a4c0012", "dg_wenming_cn": "9de563eaea4911e4945302004a4c0012", "xmgjj_gov_cn": "338f3a1cddc811e4945302004a4c0012", "xiangrikui_com": "de093178d9a911e4945302004a4c0012", "zhuhai_gov_cn": "67ecd198dcbf11e4945302004a4c0012", "zhuhainews_cn": "8b13d4dce88b11e4945302004a4c0012", "bbs_tianya_cn": "86f4be86e95611e4945302004a4c0012", "people_com_cn": "9712143adcc711e4945302004a4c0012", "anjuke_com": "3b975684dcd011e4945302004a4c0012", "bjgjj_gov_cn": "ad22a2f6dd9b11e4945302004a4c0012", "cnpension_net": "38b0727edcd111e4945302004a4c0012", "taofang_com": "8b0fea70e88b11e4945302004a4c0012", "ccdi_gov_cn": "23517a4ae17c11e4945302004a4c0012", "blogchina_com": "1cd313acd8ff11e4945302004a4c0012", "shgjj_com": "ecf54118e88b11e4945302004a4c0012", "search_fang_com": "a29e5d54dcc711e4945302004a4c0012", "0756_info": "77c70756de8511e4945302004a4c0012", "xiangrikui_com_4_16": "d8716c62e40811e4945302004a4c0012", "x3cn_com": "52e373b4de8711e4945302004a4c0012", "bbs_gd_gov_cn": "05587c98de8711e4945302004a4c0012", "so_china_com": "add09d40dcc711e4945302004a4c0012", "popdg_com": "52ddd144e8b811e4945302004a4c0012", "cnfantan_com": "a531b80ae7cf11e4945302004a4c0012", "bbs_zhnews_net": "893f1938e88a11e4945302004a4c0012", "xiangrikui_com_4_3": "1c46caf2e41011e4945302004a4c0012", "zzz_gov_cn": "a7449c4ae88b11e4945302004a4c0012", "gjj_zhuhai_gov_cn": "68fd6fa8d90311e4945302004a4c0012", "shgjj_com2": "8945e100e88a11e4945302004a4c0012", "zggjj_com": "d14084b8ddc911e4945302004a4c0012", "zgylbx_com": "f1633a04e7cb11e4945302004a4c0012", "dg_southcn_com": "c2b218a2ea4a11e4945302004a4c0012", "szzfgjj_com": "8948546ce88a11e4945302004a4c0012", "zhuhai_gd_cn": "f1700a9ae7d011e4945302004a4c0012", "chinayk_com": "f11e9118ea2511e4945302004a4c0012", "jshrss_gov_cn": "4d22b818dcd411e4945302004a4c0012", "cqgjj_cn2": "bd01bbf0e7d011e4945302004a4c0012", "china_findlaw_cn": "42e20a98ea3011e4945302004a4c0012", "cngold_org": "c83c1d80e7d011e4945302004a4c0012", "news_timedg_com": "d7e7d63cea4811e4945302004a4c0012"}, "node_name": "i-2-15703-VM"}
