from scrape.utils.clean import *


class XpathConvert:
    def __init__(self, tree):
        self.tree = tree

    def text(self, xpath, index=0):
        try:
            return self.tree.xpath(xpath)[index].text
        except IndexError:
            return None

    def profile(self):
        items = self.tree.xpath("//profile/item")
        business = founded = capital = workers = offices = motto = ave_age = None
        for item in items:
            title = item.xpath(".//title")[0].text
            text = item.xpath(".//text")[0].text
            if title == "事業内容":
                business = text
            elif title == "設立":
                founded = clean_year_founded(text)
            elif title == "資本金":
                capital = text
            elif title == "従業員数":
                workers = clean_employee(text)
            elif title == "事業所":
                offices = text
            elif "経営理念" in title or "ビジョン" in title:
                motto = text
            elif title == "平均年齢":
                ave_age = text

        return {"business": business, "year_founded": founded, "capital": capital, "employee": workers,
                "offices": offices, "motto": motto, "ave_age": ave_age}

    def employ(self):
        items = self.tree.xpath("//employ/summary/item")
        offices = working_time = None
        for item in items:
            title = item.find("title").text
            text = item.find("text").text
            if title == "勤務地":
                offices = text
            elif title == "勤務時間":
                working_time = text
        items = self.tree.xpath("//employ/treatment/item")
        salary = benefits = None
        for item in items:
            title = item.find("title").text
            text = item.find("text").text
            if title == "給与":
                salary = text
            elif title == "福利厚生":
                benefits = text

        work_env = self.tree.xpath("//employ/work_environment")[0]
        ave_age = work_env.find("average_age").find("age").text if work_env.find("average_age").find("age") else None
        return {"offices": offices, "working_time": working_time, "salary": salary, "benefit": benefits,
                "ave_age": ave_age}
