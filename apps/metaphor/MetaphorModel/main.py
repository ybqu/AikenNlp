from metaphor_web.MetaphorModel import Config
from .transHmeta import transHmeta
import os

filepath = os.path.dirname(os.path.abspath(__file__))


def metaphor_interpret(target, source):
    # load model
    con = Config.Config()
    con.set_concept_attribute_path(filepath+'data/concept_pro.txt')
    con.set_entity_path(filepath+"/data/entity_set.txt")
    con.set_property_path(filepath+"/data/property_set.txt")
    con.set_model_path(filepath+'/model/transHMetaJoint/model_')
    con.set_test_ent_candi_path(filepath+"/data/entity_set.txt")
    con.set_test_attr_candi_path(filepath+"/data/property_set.txt")
    con._init()
    con.set_model(transHmeta)
    properties, metaphor_inter = con.metaphor_interpret(target, source)

    return properties, metaphor_inter


def metaphor_generate(target, property):
    # 加载模型
    con = Config.Config()
    con.set_concept_attribute_path(filepath+'data/concept_pro.txt')
    con.set_entity_path(filepath+"/data/entity_set.txt")
    con.set_property_path(filepath+"/data/property_set.txt")
    con.set_model_path(filepath+'/model/transHMetaJoint/model_')
    # 设置预测时的概念和属性的候选集(_small 表示mk中的小候选集，entity_set / property_set 表示大候选)
    con.set_test_ent_candi_path(filepath+"/data/entity_set_small.txt")
    con.set_test_attr_candi_path(filepath+"/data/property_set_small.txt")

    con._init()
    con.set_model(transHmeta)
    # 预测
    sources, metaphor_sent = con.metaphor_generate(target, property)

    return sources, metaphor_sent
