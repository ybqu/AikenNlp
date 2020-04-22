from sklearn.metrics import f1_score, classification_report

from . import file_utils
import torch.optim as optim
import sys
import random
import torch
import torch.nn as nn
import logging

stdout_back = sys.stdout
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.INFO,
)
logger = logging.getLogger(__name__)


class Config(object):
    def __init__(self):
        self.conceptAttrPath = None
        self.entityPath = None
        self.propertyPath = None
        self.test_entity_candi_path = None
        self.test_attr_candi_path = None
        self.modelPath = None
        self.use_cuda = False
        self.ent_size = 200
        self.rel_size = 200
        self.batch_size = 64
        self.max_attr_size = 50
        self.matrix_rand_init = True
        self.p_norm = 1
        self.epochs = 1000
        self.margin = 1.0
        self.opt_method = "SGD"
        self.optimizer = None
        self.lr = 0.001
        self.lr_decay = 0.000
        self.weight_decay = 0.000

        self.alpha = 0.0
        self.beta = 0.0
        self.gamma = 0.0

        self.regul_rate = 0.0
        self.norm_flag = False

    def _init(self):
        self.entity2id, self.id2entity, self.entid2tags = file_utils.generate_entity_property_idx(self.entityPath)
        self.property2id, self.id2property, self.proid2tags = file_utils.generate_entity_property_idx(self.propertyPath)

        self.entityTotal = len(self.entity2id)
        self.propertyTotal = len(self.property2id)

        self.test_entity_candidate_ids = file_utils.read_sample_candidates(self.test_entity_candi_path, self.entity2id)
        self.test_attr_candidate_ids = file_utils.read_sample_candidates(self.test_attr_candi_path, self.property2id)

    def set_cuda(self, cuda):
        self.use_cuda = cuda

    def set_epochs(self, epoches):
        self.epochs = epoches

    def set_batch_size(self, batch_size):
        self.batch_size = batch_size

    def set_ent_size(self, size):
        self.ent_size = size

    def set_rel_size(self, size):
        self.rel_size = size

    def set_max_attr_size(self, size):
        self.max_attr_size = size

    def set_p_norm(self, norm):
        self.p_norm = norm

    def set_matrix_randn_init(self, flag):
        self.matrix_rand_init = flag

    def set_lr(self, lr):
        self.lr = lr

    def set_margin(self, margin):
        self.margin = margin

    def set_mk_weight(self, alpha):
        self.alpha = alpha

    def set_ca_weight(self, beta):
        self.beta = beta

    def set_cs_weight(self, gamma):
        self.gamma = gamma

    def set_regul_rate(self, rate):
        self.regul_rate = rate

    def set_norm_flag(self, flag):
        self.norm_flag = flag

    def set_opt_method(self, opt_method):
        self.opt_method = opt_method

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def set_concept_attribute_path(self, path):
        self.conceptAttrPath = path

    def set_entity_path(self, path):
        self.entityPath = path

    def set_property_path(self, path):
        self.propertyPath = path

    def set_test_ent_candi_path(self, path):
        self.test_entity_candi_path = path

    def set_test_attr_candi_path(self, path):
        self.test_attr_candi_path = path

    def set_model_path(self, path):
        self.modelPath = path

    def load_model(self, epoch):
        self.trainModel.load_state_dict(torch.load(self.modelPath + str(epoch) + '.pt'))

    def set_model(self, model):
        logger.info("Setting Model ...")
        self.trainModel = model(config=self)
        if self.use_cuda:
            self.trainModel = self.trainModel.cuda()

        if self.optimizer is not None:
            pass
        elif self.opt_method == "Adagrad":
            self.optimizer = optim.Adagrad(self.trainModel.parameters(), lr=self.lr, lr_decay=self.lr_decay,
                                           weight_decay=self.weight_decay)
        elif self.opt_method == "Adadelta":
            self.optimizer = optim.Adadelta(self.trainModel.parameters(), lr=self.lr)
        elif self.opt_method == "Adam":
            self.optimizer = optim.Adam(self.trainModel.parameters(), lr=self.lr)
        else:
            self.optimizer = optim.SGD(self.trainModel.parameters(), lr=self.lr)


    def metaphor_interpret(self, target, source):
        self.load_model(514)
        if target not in self.entity2id.keys() or source not in self.entity2id.keys():
            return None, None
        triplet = [self.entity2id[target], self.entity2id[source], -1]

        score_dic = {}
        test_triplet_list = file_utils.get_test_candidates(triplet, self.test_entity_candidate_ids,  self.test_attr_candidate_ids, 'p')

        for t in test_triplet_list:
            t = t.view(len(t), 1)
            score = self.trainModel.predict(t[0], t[1], t[2])
            score_dic[t] = score.data
        score_list = file_utils.Counter(score_dic).most_common()
        score_list.reverse()

        pre_properties = []
        for t in score_list[:20]:
            pre_properties.append(self.id2property[t[0][2].item()])

        metaphor_inter = []
        for p in pre_properties:
            sent = target + ' ' + '像' + ' ' + source + '一样' + ' ' + p + '。'
            metaphor_inter.append(sent)

        return pre_properties, metaphor_inter

    def metaphor_generate(self, target, property):
        self.load_model(514)
        if target not in self.entity2id.keys() or property not in self.property2id.keys():
            return None, None
        triplet = [self.entity2id[target], -1, self.property2id[property]]
        score_dic = {}
        test_triplet_list = file_utils.get_test_candidates(triplet, self.test_entity_candidate_ids,  self.test_attr_candidate_ids, 't')

        for t in test_triplet_list:
            t = t.view(len(t), 1)
            score = self.trainModel.predict(t[0], t[1], t[2])
            score_dic[t] = score.data
        score_list = file_utils.Counter(score_dic).most_common()
        score_list.reverse()

        pre_sources = []
        for t in score_list[:20]:
            pre_sources.append(self.id2entity[t[0][1].item()])

        metaphor_sent = []
        for source in pre_sources:
            sent = target + ' 是 ' + source + '。'
            metaphor_sent.append(sent)

        return pre_sources, metaphor_sent
