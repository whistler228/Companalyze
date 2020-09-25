import requests
from lxml import html
from scrape.utils.rikunabi import tree_from_rikunabi_api
from scrape.utils.utilities import XpathConvert
from scrape.utils.clean import clean_main_domain, clean_sub_domain, clean_prefecture
from logging import getLogger

logger = getLogger(__name__)


def get_company(company_id):
    tree = tree_from_rikunabi_api(company_id)
    if tree.xpath("//return_code")[0].text != "0":
        logger.error("rikunabi API returned error.")
        return None
    xc = XpathConvert(tree)
    name = xc.text("//company_name")
    main_domain = xc.text("//bcd_main")
    sub_domains = [xc.text("//bcd_sub_%d" % (i + 1)) for i in range(5) if xc.text("//bcd_sub_%d" % (i + 1))]
    prefectures = [xc.text("//prefecture_%d" % (i + 1)) for i in range(5) if xc.text("//prefecture_%d" % (i + 1))]
    profile = xc.profile()
    grad_hire_last_year = f'{xc.text("//model/item/model_name")}:{xc.text("//model/item/number")}'
    employ = xc.employ()
    res = {**{"name": name, "main_domain": clean_main_domain(main_domain), "sub_domains": clean_sub_domain(sub_domains),
              "prefectures": clean_prefecture(prefectures), "grad_hire_last_year": grad_hire_last_year}, **profile, **employ}
    if not res["offices"]:
        res["offices"] = profile["offices"]
    return res
