# 关于公司排序：
# 先按照发明评级排序、同一评级按搜索次数排序

dict_company = {
    'A+': 9,  # 世界领先
    'A': 8,
    'A-': 7,
    'B+': 6,
    'B': 5,
    'B-': 4,
    'C+': 3,
    'C': 2,
    'C-': 1,
}


def key_company(item):
    if dict_company.get(item['inventionRating']) is not None:
        return dict_company.get(item['inventionRating'])
    return 0


def key_stock(item):
    item_type = type(eval(item['percent']))
    if item_type is int or item_type is float:
        return float(item['percent'])
    return 0
