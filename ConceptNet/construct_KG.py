from typing import List
import requests

class constructKG():


    def __init__(self, _label_list, _hop_num):
        self.label_list = _label_list
        self.hop_num = _hop_num

        self.entity_list = []
        self.relation_list = []
        self.triples = []

        self.construct(_label_list, _hop_num)

    def construct(self, org_entities, hop_num):

        tmp_entities = set(org_entities)
        next_entities = tmp_entities
        for i in range(hop_num):
            new_triples = []
            new_entities = []
            for entity in next_entities:
                _new_triples, _new_entities = self.req_triples(entity)
                new_triples += _new_triples
                new_entities += _new_entities
            self.triples += list(set(new_triples))
            self.init_ent_rel()
            self.save_data(i + 1)

            next_entities = set(new_entities) - tmp_entities
            tmp_entities |= set(new_entities)
            print('-------------------------------------')
            print(next_entities)

    def req_triples(self, entity):
        triples = []
        entities = []

        ent = requests.get('http://api.conceptnet.io/c/en/{}'.format(entity)).json()

        for edge in ent['edges']:
            org_triple = edge['@id'].split('[')[1].replace (']', '')
            org_p, org_s, org_o = org_triple.split(',')
            if org_s.split('/')[2] != 'en' or org_o.split('/')[2] != 'en':
                continue
            s = org_s.split('/')[3]
            p = org_p.split('/')[2]
            o = org_o.split('/')[3]
            triples.append((s, p, o))
            entities.append(o)
            entities.append(s)
        return triples, entities

    def init_ent_rel(self):
        _triples = set(self.triples)
        for s, p, o in _triples:
            self.entity_list.append(s)
            self.entity_list.append(o)
            self.relation_list.append(p)

        self.triples = list(set(self.triples))
        self.relation_list = list(set(self.relation_list))
        self.entity_list = list(set(self.entity_list))

    def save_data(self, hop_num):
        triples = set(self.triples)
        entities = set(self.entity_list)
        relstions = set(self.relation_list)

        with open('triples_hop_{}.txt'.format(hop_num), 'w') as f_t:
            for s, p, o in triples:
                f_t.write('{}\t{}\t{}\n'.format(s, p, o))
            f_t.flush()
            f_t.close()

        with open('entities_hop_{}.txt'.format(hop_num), 'w') as f_t:
            for entity in entities:
                f_t.write('{}\n'.format(entity))
            f_t.flush()
            f_t.close()

        with open('relations_hop_{}.txt'.format(hop_num), 'w') as f_t:
            for relation in relstions:
                f_t.write('{}\n'.format(relation))
            f_t.flush()
            f_t.close()

label_list = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse,', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hop dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
hop_num = 5
c_KG = constructKG(label_list, hop_num)

triples = c_KG.triples
entities = c_KG.entity_list
relstions = c_KG.relation_list

with open('triples.txt', 'w') as f_t:
    for s, p, o in triples:
        f_t.write('{}\t{}\t{}\n'.format(s, p, o))
    f_t.flush()
    f_t.close()

with open('entities.txt', 'w') as f_t:
    for entity in entities:
        f_t.write('{}\n'.format(entity))
    f_t.flush()
    f_t.close()

with open('relstions.txt', 'w') as f_t:
    for relation in relstions:
        f_t.write('{}\n'.format(relation))
    f_t.flush()
    f_t.close()


