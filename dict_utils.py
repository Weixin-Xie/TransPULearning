import numpy as np
from collections import defaultdict


class DictUtils(object):
    def __init__(self):
        self.tag2Idx = {
            "DRUG": 0, "CANCER": 1, "TOXI": 2
        }
        self.idx2tag = {
            0: "DRUG", 1: "CANCER", 2: "TOXI"
        }

    def lookup_in_Dic(self, dicFile, sentences, tag, windowSize):
        tagIdx = self.tag2Idx[tag]
        dic = []
        labeled_word = set()
        count = 0
        mistake = defaultdict(int)
        true = defaultdict(int)
        with open(dicFile, "r",encoding='utf-8') as fw:
            for line in fw:
                line = line.strip()
                if len(line) > 0:
                    dic.append(line)
        for i, sentence in enumerate(sentences):
            wordList = [word for word, label, dicFlags in sentence]
            trueLabelList = [label for word, label, dicFlags in sentence]
            isFlag = np.zeros(len(trueLabelList))
            j = 0
            while j < len(wordList):
                Len = min(windowSize, len(wordList) - j)
                k = Len
                while k >= 1:
                    words = wordList[j:j + k]
                    words_ = " ".join([w for w in words])

                    if words_ in dic:
                        # print(words_)
                        isFlag[j:j + k] = 1
                        j = j + k
                        break
                    k -= 1
                j += 1

            for m, flag in enumerate(isFlag):
                if flag == 1:
                    count += 1
                    labeled_word.add(sentence[m][0])
                    # true[wordList[m]] += 1
                    # if trueLabelList[m] != 'B-MISC' and trueLabelList[m] != 'I-MISC':
                    #     # print(wordList[m] + " " + trueLabelList[m])
                    #     mistake[wordList[m]] += 1
                    sentence[m][2][tagIdx] = 1

        # with open('log.txt','w') as fw:
        #     for k, v in sorted(mistake.items(), reverse=True):
        #         all = true[k]
        #         fw.write('{0}\s{1}\n'.format(k,float(v / all)))
        #
        # with open('log2.txt', 'w') as fw:
        #     for k, v in sorted(true.items(), reverse=True):
        #         fw.write('{0}\n'.format(k))

        return sentences, len(labeled_word), count
