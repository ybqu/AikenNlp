# from .MetaphorModel import Config
import os
import random
filepath = os.path.dirname(os.path.abspath(__file__))


def get_entities_properties():
    """
    ? 获取 (target source property)  k
    """
    source_list = []
    target_list = []
    properties_list = []
    mk_data = []
    mk_data_file = open(filepath+'/data/mk_data.txt', 'r', encoding='utf-8')
    for line in mk_data_file:
        mk_data.append(line)
    random.shuffle(mk_data)
    for line in mk_data:
        line_parts = line.strip().split()
        target_list.append(line_parts[0])
        source_list.append(line_parts[1])
        properties_list.append(line_parts[2])
    return target_list, source_list, properties_list