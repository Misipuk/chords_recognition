import numpy as np
import codecs
import json
import pandas as pd
import csv

class RnnDataSaver:
    songs_list = []
    train_x = []
    train_y = []

    def __init__(self, examples_list=[], dict_ch_id = {}, window_size=4096):
        self.examples_list = examples_list
        self.dict_ch_id = dict_ch_id
        self.window_size = window_size


    def process_examples(self):
        song = []
        for ex in self.examples_list:
            song = []
            j = 0
            curr_time = 0.
            curr_ch_label = ex.chords_list[j].label
            for i in range(len(ex.pcp_list)):
                if j == len(ex.chords_list):
                    continue
                if (ex.chords_list[j].end_time < curr_time + self.window_size / 2):
                    j += 1
                    if j == len(ex.chords_list):
                        continue
                #print('Curr chord = {}, end_t = {}, curr_t = {}'.format(ex.chords_list[j].label, ex.chords_list[j].end_time, curr_time))

                curr_time += self.window_size
                curr_ch_label = ex.chords_list[j].label
                unit = list([curr_ch_label, ex.pcp_list[i].tolist()])
                song.append(unit)
            self.songs_list.append(song)

    def prepare_ex_for_ml(self):
        song = []
        for ex in self.examples_list:
            song = []
            j = 0
            curr_time = 0.
            curr_ch_label = ex.chords_list[j].label
            for i in range(len(ex.pcp_list)):
                if j == len(ex.chords_list):
                    continue
                if (ex.chords_list[j].end_time < curr_time + self.window_size / 2):
                    j += 1
                    if j == len(ex.chords_list):
                        continue
                # print('Curr chord = {}, end_t = {}, curr_t = {}'.format(ex.chords_list[j].label, ex.chords_list[j].end_time, curr_time))

                curr_time += self.window_size
                curr_ch_label = ex.chords_list[j].label
                self.train_x.append(list(ex.pcp_list[i]))
                self.train_y.append(self.dict_ch_id.get(curr_ch_label))
                #song.append([self.train_x, self.train_y])
            #self.songs_list.append(song)

    def results_write_json(self):
        file_path = "D:\\ChordsRecognition\\music-dsp\\tools\\DatasetExtraction\\rnn_data\\songs_ch_pcp.json"
        json.dump(self.songs_list, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
                  indent=4)
        """df = pd.DataFrame(self.songs_list)
        with open('myfile.csv', 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(self.songs_list)"""

    def results_read_json(self):
        file_path = "D:\\ChordsRecognition\\music-dsp\\tools\\DatasetExtraction\\rnn_data\\songs_ch_pcp.json"
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        self.songs_list = json.loads(obj_text)

    def __repr__(self):
        return "(Songs: {}".format(self.songs)