from django.db import models
from .MetaphorModel.main import METAPHOR_INTERPRET, METAPHOR_GENERATE

# Create your models here.
class Interpretation(models.Model):
    @staticmethod
    def interprete(target, source):
        attribution, interpretation = METAPHOR_INTERPRET.metaphor_interpret(target, source)
        data_list = []
        for p, s in zip(attribution, interpretation):
            data = {'target': target, 'source': source, 'attribution': p, 'interpretation': s}
            data_list.append(data)
        return data_list

class Generation(models.Model):
    @staticmethod
    def generation(target, attribution):
        sources, sentences = METAPHOR_GENERATE.metaphor_generate(target, attribution)

        data_list = []
        for s, sent in zip(sources, sentences):
            data = {'target': target, 'attribution': attribution, 'source': s, 'sentences': sent}
            data_list.append(data)
        
        return data_list