from dataset import Dataset
from chord import Chord
from train_example import Train_Example
import numpy as np
from iso_adjusting import IsoAdjust

class Iso_Dataset(Dataset):

    def load_ch_pcp(self, filename):
        chords_list = []
        pcp_list = []
        with open(filename, 'r') as f:
            for line in f:
                if line:
                    splits = line.split()  # usually looks like
                    if len(splits) == 3:
                        s = splits[0]
                        e = splits[1]
                        l = self.adjuster.label_error_modify(splits[2])  # adjust_to_cqmax
                        l = self.adjuster.adjust_to_cq_max(l)
                        #if "D:min7(*b3)"in l:
                        #    print("********* \n THIS " + filename)
                        self.set_chords.add(l)
                        # id = self.dict_ids.get(l)
                        # print(id)
                        chords_list.append(Chord(id, int(float(s) * 44100), int(float(e) * 44100), l))

        txt_f_name = filename[:-4] + ".txt"
        print(txt_f_name)
        with open(txt_f_name, 'r') as f:
            for line in f:
                if line:
                    arr = line.split(',')
                    #arr[23] = arr[23][:-1]
                    arr = [float(i) for i in arr]
                    arr = np.array(arr, dtype=float)
                   # mx = np.max(arr)
                   # if mx!=0:
                   #     arr = arr/mx
                    #print(len(arr))
                    pcp_list.append(arr)
                    # print(len(line.split(',')))

        return Train_Example(chords_list, pcp_list)

