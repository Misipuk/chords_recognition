import codecs
import json
import numpy as np


class HmmDataSaver:
    def __init__(self, dict_id_ch = {}, templ_chrds = {}, i_matrix = [], t_matrix = [], e_matrix = []):
        self.dict_id_ch = dict_id_ch
        self.templ_chrds = templ_chrds
        self.i_matrix = i_matrix
        self.t_matrix = t_matrix
        self.e_matrix = e_matrix

    def results_write_json(self):
        t_file = self.dict_id_ch
        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/dict_id_ch.json"
        json.dump(t_file, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
                  indent=4)

        t_file = self.templ_chrds
        corrected_dict = {int(k): v.tolist() for k, v in t_file.items()}
        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/templ_chrds.json"
        json.dump(corrected_dict, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
                  indent=4)

        t_file = self.i_matrix
        t_list = t_file.tolist()
        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/init_matrix.json"
        json.dump(t_list, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
                  indent=4)

        t_file = self.t_matrix
        t_list = t_file.tolist()
        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/tran_matrix.json"
        json.dump(t_list, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
                  indent=4)

        t_file = self.e_matrix
        t_list = t_file.tolist()
        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/emis_matrix.json"
        json.dump(t_list, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
                  indent=4)



    def results_read_json(self):
        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/dict_id_ch.json"
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        t_dict_new = json.loads(obj_text)
        self.dict_id_ch = {int(k): v for k, v in t_dict_new.items()}

        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/templ_chrds.json"
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        t_dict_new = json.loads(obj_text)
        self.templ_chrds = {int(k): np.array(v, dtype=float) for k, v in t_dict_new.items()}

        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/init_matrix.json"
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        t_list_new = json.loads(obj_text)
        self.i_matrix = np.array(t_list_new, dtype= float)

        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/tran_matrix.json"
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        t_list_new = json.loads(obj_text)
        self.t_matrix = np.array(t_list_new, dtype= float)

        file_path = "/home/max/chords_work/music-dsp/tools/DatasetExtraction/training_result/emis_matrix.json"
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        t_list_new = json.loads(obj_text)
        self.e_matrix = np.array(t_list_new, dtype= float)