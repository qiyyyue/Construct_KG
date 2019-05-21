import time

import requests


class Get_Triples():

    def __init__(self, _hop_num):
        self.hop_num = _hop_num

        self.init_org_data()

    '''
    初始化原始数据
    '''
    def init_org_data(self):
        _org_entities = []
        _org_relations = []
        _org_triples = []
        with open('entities_hop_{}.txt'.format(self.hop_num - 1), 'r') as rf:
            for line in rf:
                _org_entities.append(line.strip())
            rf.close()

        with open('relations_hop_{}.txt'.format(self.hop_num - 1), 'r') as rf:
            for line in rf:
                _org_relations.append(line.strip())
            rf.close()

        with open('triples_hop_{}.txt'.format(self.hop_num - 1), 'r') as rf:
            for line in rf:
                _org_triples.append(line.strip().split())
            rf.close()

        self.org_entities = _org_entities
        self.org_relations = _org_relations
        self.org_triples = _org_triples

    '''
    爬取下一跳的数据
    '''
    def get_next_hop_data(self):

        new_triples = []
        new_entities = []
        for entity in self.org_entities:
            _new_triples, _new_entities = self.req_triples(entity)
            new_triples += _new_triples
            new_entities += _new_entities

        self.new_triples = set(new_triples)
        self.new_entities = set(new_entities)

    '''
    存储
    '''
    def save_data(self):
        self.triples = set(self.org_triples) | set(self.new_triples)
        self.entities = self.org_entities
        self.relations = self.org_relations
        for s, p, o in self.triples:
            self.entities.append(s)
            self.entities.append(o)
            self.relations.append(p)

        self.triples = list(set(self.triples))
        self.entities = list(set(self.entities))
        self.relations = list(set(self.relations))

        with open('triples_hop_{}.txt'.format(self.hop_num), 'w') as f_t:
            for s, p, o in self.triples:
                f_t.write('{}\t{}\t{}\n'.format(s, p, o))
            f_t.flush()
            f_t.close()

        with open('entities_hop_{}.txt'.format(self.hop_num), 'w') as f_t:
            for entity in self.entities:
                f_t.write('{}\n'.format(entity))
            f_t.flush()
            f_t.close()

        with open('relations_hop_{}.txt'.format(self.hop_num), 'w') as f_t:
            for relation in self.relations:
                f_t.write('{}\n'.format(relation))
            f_t.flush()
            f_t.close()

    def req_triples(self, entity):
        triples = []
        entities = []

        ent = requests.get('http://api.conceptnet.io/c/en/{}'.format(entity)).json()

        while 'edges' not in ent.keys():
            time.sleep(600)
            ent = requests.get('http://api.conceptnet.io/c/en/{}'.format(entity)).json()

        for edge in ent['edges']:
            org_triple = edge['@id'].split('[')[1].replace(']', '')
            org_p, org_s, org_o = org_triple.split(',')
            if org_s.split('/')[2] != 'en' or org_o.split('/')[2] != 'en':
                continue
            s = org_s.split('/')[3]
            p = org_p.split('/')[2]
            o = org_o.split('/')[3]
            triples.append([s, p, o])
            entities.append(o)
            entities.append(s)
        return triples, entities

if __name__ == '__main__':
    for hop_num in range(3, 6):
        g_t = Get_Triples(hop_num)
        g_t.get_next_hop_data()
        g_t.save_data()

