from abc import ABCMeta, abstractmethod
from accessify import protected
from chord import Chord
import numpy as np
from glob import glob
from chord_quality_t import ChordQuality
from train_example import Train_Example
from ml_classification_methods import MlClassificationMethods
from rnn_data_saver import RnnDataSaver
from iso_adjusting import IsoAdjust


class Dataset:
    song_list = []
    examples_list = []
    dir_path = ""
    window_size = 4096
    #cq_max = chord_quality_t["cq_Min"]
    chords_total = 0
    dict_ch_id = {}
    dict_id_ch = {}
    cnt_chrds = {}
    templ_chrds = {}
    set_chords = set()
    i_matrix = []
    t_matrix = []
    e_matrix = []
    list_curr_chords = []
    kmclassifier = None
    use_train_tmpl = False

    def __init__(self, dir_path, cq_max, use_train_tmpl = False, window_size = 4096):
        list_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']  # better to move?
        self.dict_notes_id = {list_notes[i]: i for i in range(0, len(list_notes))}
        self.dict_id_notes = {i: list_notes[i] for i in range(0, len(list_notes))}
        self.dir_path = dir_path
        self.window_size = window_size
        self.adjuster = IsoAdjust(cq_max, self.dict_notes_id, self.dict_id_notes)
        self.cq_max = cq_max
        self.use_train_tmpl = use_train_tmpl


    @protected
    def validate(self):
        pass

    #@protected
    def load_examples(self, dir_path):
        self.examples_list = []
        file_list = glob(dir_path)
        for file in file_list:
            self.examples_list.append(self.load_ch_pcp(file))
        return self.examples_list

    @protected
    def load_ch_pcp(self, filename):
        pass

    def adjust_to_cqmax(self, label):
        pass

    def load_tpl_templates(self, filename):
        self.templ_chrds = {}
        splits = []
        with open(filename, 'r') as f:
            for line in f:
                if line:
                    splits = line.split(',')
                    splits[-1] = splits[-1][:-1]
                    if "/1" in splits[0] and not "min/1" in splits[0] and not "maj/1" in splits[0]:
                        # print(splits[0])
                        splits[0] = splits[0][:-2]
                        # print(splits[0])
                        # print("*****")
                    self.templ_chrds[splits[0]] = np.array(splits[1:],dtype=float)

        #list_chords = list(self.templ_chrds.keys())
        """for i in range(0, len(list_chords)):
                    print(list_chords[i])
        print("*********************")"""
        self.templ_chrds = self.adjuster.adjust_templ_to_cq_max(self.templ_chrds)
        #list_chords = list(self.templ_chrds.keys())
        self.templ_chrds_2 = self.templ_chrds.copy()
        self.templ_chrds = self.templ_chrds_2.copy()
        #print(list(self.set_chords))
        for item in self.templ_chrds_2.keys():
            #print(item)
            if item not in list(self.set_chords):
                self.templ_chrds.pop(item, None)
        self.list_chords = list(self.templ_chrds.keys())

        """for i in range(0, len(list_chords)):
            print(list_chords[i])
        print("*********************")"""
        self.chords_total = len(self.list_chords)
        self.dict_ch_id = {self.list_chords[i]: i for i in range(0, len(self.list_chords))}
        self.dict_id_ch = {i: self.list_chords[i] for i in range(0, len(self.list_chords))}
        self.cnt_chrds = {i: 0 for i in range(0, len(self.list_chords))}
        self.templ_chrds_2 = {self.dict_ch_id.get(self.list_chords[i]): self.templ_chrds.get(self.list_chords[i]) for i in
                              range(0, len(self.list_chords))}
        self.templ_chrds = self.templ_chrds_2




    def make_templ_list_from_dataset(self):
        self.list_chords = list(self.set_chords)
        self.chords_total = len(self.list_chords)
        self.dict_ch_id = {self.list_chords[i]: i for i in range(0, len(self.list_chords))}
        self.dict_id_ch = {i: self.list_chords[i] for i in range(0, len(self.list_chords))}
        self.cnt_chrds = {i: 0 for i in range(0, len(self.list_chords))}
        self.templ_chrds = {i: np.zeros(24, dtype=float) for i in range(0, len(self.list_chords))}

    def train_templ(self):
        for ex in self.examples_list:
            j = 0
            curr_time = 0.
            curr_ch_id = self.dict_ch_id.get(ex.chords_list[j].label)
            for i in range(len(ex.pcp_list)):
                if (j == len(ex.chords_list)):
                    continue
                if (ex.chords_list[j].end_time < curr_time + self.window_size / 2):
                    j += 1

                if (j == len(ex.chords_list)):
                    #print("****")
                    continue
                #print('Curr chord = {}, end_t = {}, curr_t = {}'.format(ex.chords_list[j].label, ex.chords_list[j].end_time, curr_time))
                curr_time += self.window_size
                curr_ch_id = self.dict_ch_id.get(ex.chords_list[j].label)
                #obs_ch_id = self.min_norm_ch_id(ex.pcp_list[i])
                self.cnt_chrds[curr_ch_id] += 1
                self.templ_chrds[curr_ch_id] = self.templ_chrds[curr_ch_id] + np.array(ex.pcp_list[i], dtype=float)
        for i in range(0, self.chords_total):
            self.templ_chrds[i] = self.templ_chrds[i]/self.cnt_chrds[i]
            #print(str(self.templ_chrds[i]) + " / " + str(self.cnt_chrds[i]))

    #returns vector with probabilities (dtype np array)
    def get_hmm_matrix_i(self):
        i_matrix = np.zeros(self.chords_total, dtype=float) #fix
        for ex in self.examples_list:
            i_matrix[self.dict_ch_id.get(ex.chords_list[0].label)] += 1
        i_matrix = i_matrix / len(self.examples_list)
        self.i_matrix = i_matrix
        return i_matrix

    # returns matrix with probabilities (dtype np array)
    def get_hmm_matrix_t(self):
        tran_count = 0.0
        remainder = 0.0
        drtn = 0.0
        w_cnt = 0.0
        t_matrix = np.zeros((self.chords_total, self.chords_total), dtype=float)
        for ex in self.examples_list:
            song = ex.chords_list
            t_matrix[self.dict_ch_id.get(song[-1].label)][self.dict_ch_id.get(song[-1].label)] += \
                int((song[-1].end_time - song[-1].start_time) / self.window_size)

            for j in range(len(song)-1):
                w_cnt = 0
                curr_chord = song[j]
                drtn = curr_chord.end_time - curr_chord.start_time
                w_cnt = int((int(drtn) / int(self.window_size)))

                remainder = drtn % self.window_size

                if (remainder >= self.window_size / 2):
                    w_cnt += 1

              #  tran_count += w_cnt + 1
                #print(str(curr_chord.label) + " " + str(drtn) + " " + str(w_cnt) + " " + str(self.window_size))
                #print(str(curr_chord.start_time) + " " + str(curr_chord.end_time))
                t_matrix[self.dict_ch_id.get(curr_chord.label)][self.dict_ch_id.get(curr_chord.label)] += w_cnt - 1 #self trasition
                t_matrix[self.dict_ch_id.get(curr_chord.label)][self.dict_ch_id.get(song[j + 1].label)] += 1 #chord changing transition
        #t_matrix = float(t_matrix / tran_count)
        #print(t_matrix)
        for i in range(0, self.chords_total):
            t_matrix[i] = t_matrix[i] / sum(t_matrix[i])
        """f = open("matrix_test.txt", "w")
        f.write(str(t_matrix))
        f.close()"""
        self.t_matrix = t_matrix
        return t_matrix

    def get_hmm_matrix_e(self):
        print("\n Accuracy per window true_chord/observation_chord: \n")
        tot = 0
        mis = 0
        str1 = ""
        self.cnt_chrds = {i: 0 for i in range(0, self.chords_total)}

        e_matrix = np.zeros((self.chords_total, self.chords_total), dtype=float)
        for ex in self.examples_list:
            j = 0
            curr_time = 0.
            obs_ch_id = 0.
            curr_ch_id = self.dict_ch_id.get(ex.chords_list[j].label)
            for i in range(len(ex.pcp_list)):
                if j == len(ex.chords_list):
                    continue
                if (ex.chords_list[j].end_time < curr_time + self.window_size / 2):
                    j += 1
                    if j == len(ex.chords_list):
                        continue
               # print('Curr chord = {}, end_t = {}, curr_t = {}'.format(ex.chords_list[j].label, ex.chords_list[j].end_time, curr_time))
                curr_time += self.window_size
                curr_ch_id = self.dict_ch_id.get(ex.chords_list[j].label)
                #obs_ch_id = self.min_norm_ch_id(ex.pcp_list[i])
                if self.use_train_tmpl == False:
                    obs_ch_id = self.kmclassifier.predict([ex.pcp_list[i]])[0]
                else:
                    obs_ch_id = self.min_norm_ch_id(ex.pcp_list[i])
                e_matrix[curr_ch_id][obs_ch_id] += 1



                self.list_curr_chords.append(ex.chords_list[j].label)
                print('Curr chord = {}, obs_ch_id = {}'.format(ex.chords_list[j].label, self.dict_id_ch.get(obs_ch_id)))
                str1 += 'Curr chord = {}, obs_ch_id = {}'.format(ex.chords_list[j].label, self.dict_id_ch.get(obs_ch_id)) + "\n"
                tot += 1
                if ex.chords_list[j].label != self.dict_id_ch.get(obs_ch_id):
                    mis += 1
                self.cnt_chrds[curr_ch_id] += 1
                #for item in new_list:



        for i in range(0, self.chords_total):
           e_matrix[i] = e_matrix[i] / self.cnt_chrds[i]
        # поделить емиссион матрикс построчно
        self.e_matrix = e_matrix


        print("\nClassifier without hmm accuracy: " + str(float(1 - mis/tot)))
        print("\n")

        print("Emission matrix \n")
        #f = open("this_song.txt", "w")
        #f.write(str1)
        return e_matrix

    def min_norm_ch_id(self, pcp_v):

        min_dist = np.linalg.norm(np.array(pcp_v, dtype=float) - np.array(self.templ_chrds.get(0), dtype=float))

        min_id = 0
        dist = 0
        for i in range(0, self.chords_total):
            dist = np.linalg.norm(np.array(pcp_v, dtype=float) - np.array(self.templ_chrds.get(i), dtype=float))
            if min_dist > dist:
                min_id = i
                min_dist = dist
        #print(min_dist)
        return min_id