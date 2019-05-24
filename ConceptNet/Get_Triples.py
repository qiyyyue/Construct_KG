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
                s, p, o = line.strip().split()
                _org_triples.append((s, p, o))
            rf.close()

        self.org_entities = _org_entities
        self.org_relations = _org_relations
        self.org_triples = _org_triples

    '''
    爬取下一跳的数据
    '''
    def get_next_hop_data(self):

        new_triples = []
        for i, entity in enumerate(self.org_entities):

            #下一次开始位置
            last_i = -1
            if i <= last_i:
                continue
            #

            print('get {}/{} : {}'.format(i, len(self.org_entities), entity))
            new_triples += self.req_triples(entity)

            # 每1K实体存储一次，下一次手动设置从i开始
            if i%1000 == 0:
                print('save {}'.format(i))
                self.save_tmp_data(new_triples)

        self.new_triples = set(new_triples)

    def save_tmp_data(self, triples):
        triples = set(self.org_triples) | set(triples)
        entities = self.org_entities
        relations = self.org_relations
        for s, p, o in triples:
            entities.append(s)
            entities.append(o)
            relations.append(p)

        triples = list(set(triples))
        entities = list(set(entities))
        relations = list(set(relations))

        with open('triples_hop_{}_tmp.txt'.format(self.hop_num), 'a+', encoding='utf8') as f_t:
            for s, p, o in triples:
                f_t.write('{}\t{}\t{}\n'.format(s, p, o))
            f_t.flush()
            f_t.close()

        with open('entities_hop_{}_tmp.txt'.format(self.hop_num), 'a+', encoding='utf8') as f_t:
            for entity in entities:
                f_t.write('{}\n'.format(entity))
            f_t.flush()
            f_t.close()

        with open('relations_hop_{}_tmp.txt'.format(self.hop_num), 'a+', encoding='utf8') as f_t:
            for relation in relations:
                f_t.write('{}\n'.format(relation))
            f_t.flush()
            f_t.close()

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

        ent = requests.get('http://api.conceptnet.io/c/en/{}'.format(entity)).json()

        while 'edges' not in ent.keys():
            time.sleep(600)
            ent = requests.get('http://api.conceptnet.io/c/en/{}'.format(entity)).json()

        for edge in ent['edges']:
            try:
                org_triple = edge['@id'].split('[')[1].replace(']', '')
                org_p, org_s, org_o = org_triple.split(',')
                if org_s.split('/')[2] != 'en' or org_o.split('/')[2] != 'en':
                    continue
                s = org_s.split('/')[3]
                p = org_p.split('/')[2]
                o = org_o.split('/')[3]
                triples.append((s, p, o))
            except  Exception as e:
                print('erro:' + str(e))
                print(edge)
                pass
        return triples

if __name__ == '__main__':
    for hop_num in range(4, 6):
        print('hop_num: {}'.format(hop_num))
        g_t = Get_Triples(hop_num)
        g_t.get_next_hop_data()
        g_t.save_data()

