import math
import operator

count = int(input())
doc_list = []
vocAll = " "
while(count!=0):
    doc_list.append(input()[5:])
    count-=1
query_list = input().split()
vocAll=vocAll.join(doc_list+query_list)
vocAll=list(set(vocAll.split()))

vocIndex = dict()
index = 0
for voc in vocAll:
    vocIndex[voc] = index
    index+=1
def dot_product2(v1, v2):
    return sum(map(operator.mul, v1, v2))

def cosineSimilarity(v1, v2):
    #v1請放入doc，v2請放入query
    prod = dot_product2(v1, v2)
    len1 = math.sqrt(dot_product2(v1, v1))
    len2 = math.sqrt(dot_product2(v2, v2))
    return round(prod / (len1 * len2),4)

def search(voc):
    return vocIndex[voc]
def get_key(dic, value):
    return [k for k, v in dic.items() if v == value][0]

query = [0]*len(vocAll)
for voc in query_list:
    query[vocIndex[voc]]+=1
similar_dic = dict()
similar = []
for d in doc_list:
    dclst = [0]*len(vocAll)
    for doc in d.split():
        dclst[vocIndex[doc]]+=1
    Similarity = cosineSimilarity(dclst,query)
    similar_dic[doc_list.index(d)+1] = Similarity
    similar.append(Similarity)
    print('doc{}'.format(doc_list.index(d)+1),Similarity)
print('best:doc{}'.format(get_key(similar_dic,max(similar))))