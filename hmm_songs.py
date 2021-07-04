import numpy as np
from ml_classification_methods import MlClassificationMethods
from rnn_data_saver import RnnDataSaver

class HmmSongs:
    #should get number of frames
    kmclassifier = None
    use_train_tmpl = False
    list_chords = []

    def __init__(self, list_chords, templ_chrds, i_matrix, t_matrix, e_matrix, ch_pcp_list, examples_list, use_train_tmpl, window_size = 4096):
        self.examples_list = examples_list
        list_chords = list_chords
        self.chords_total = len(list_chords)
        self.dict_ch_id = {list_chords[i]: i for i in range(0, len(list_chords))}
        self.dict_id_ch = {i: list_chords[i] for i in range(0, len(list_chords))}
        self.templ_chrds = templ_chrds
        self.i_matrix = i_matrix
        self.t_matrix = t_matrix
        self.e_matrix = e_matrix
        self.ch_pcp_list = ch_pcp_list
        self.window_size = window_size
        #self.n_frames = len(pcp_v)
        self.chords_total = len(list(templ_chrds.keys()))
        self.final_chords = []
        self.final_accuracy = []
        self.use_train_tmpl = use_train_tmpl


    def initialize(self):
        pcp_list = []
        ch_list = []
        print("\nAccuracy per song:")
        for i in range(len(self.ch_pcp_list)):
            pcp_list = []
            ch_list = []
            for j in range(len(self.ch_pcp_list[i])):
                ch_list.append(self.ch_pcp_list[i][j][0])
                pcp_list.append(self.ch_pcp_list[i][j][1])
            self.process_song(ch_list, pcp_list)
        self.final_accuracy = np.array(self.final_accuracy, dtype=float)
        ac = np.sum(self.final_accuracy)/len(self.final_accuracy)
        print("Mean accuracy = " +  str(ac))

    def process_song(self, ch_list, pcp_list):


        n_frames = len(ch_list)


        (path, states) = self.viterbi(pcp_list, n_frames)
        # normalize path
        #for i in range(self.n_frames):
        #    path[:, i] /= sum(path[:, i])

        final_chords = []
        indices = np.argmax(path, axis=0) #находим индексы аргмакс
        final_states = np.zeros(n_frames)
        #final_states[0] = indices[0]
        #final_chords.append(self.dict_id_ch.get(int(final_states[0])))

        #find no chord zone
        #set_zero = np.where(np.max(path, axis=0) < 0.0001 * np.max(path))[0]
        #if np.size(set_zero) is not 0:
            #indices[set_zero] = -1

        #identify chords
        for i in range(1, n_frames):
            final_states[i] = states[indices[i], i] # берем индексы по аргмакс
            final_chords.append(self.dict_id_ch.get(int(final_states[i])))

        final_chords.append(self.dict_id_ch.get(int(indices[n_frames - 1])))
        self.final_chords = final_chords
        vs = n_frames
        tr = 0

        for i in range(n_frames):
            if (ch_list[i] == final_chords[i]):
                tr +=1
        print("Accuracy = " + str(float(tr/vs)))
        self.final_accuracy.append(float(tr/vs))
            #print("nFrame: {}, Chord: {}".format(i, final_chords[i]))



    def viterbi(self, pcp_v, n_frames):
        #pi =i, a = t, b = e
        (nrow, ncol) = len(self.i_matrix), n_frames
        path = np.zeros((nrow, ncol))
        states = np.zeros((nrow, ncol))
        #obs_ch_id = self.min_norm_ch_id(self.pcp_v[0])
        if (self.use_train_tmpl == False):
            obs_ch_id = self.kmclassifier.predict([pcp_v[0]])[0]
        else:
            obs_ch_id = self.min_norm_ch_id(pcp_v[0])

        path[:, 0] = self.i_matrix * self.e_matrix[:, obs_ch_id]
        mx_p = 0.0
        mx_id = 0
        fl = False
        for i in range(1, ncol):
            #obs_ch_id = self.min_norm_ch_id(self.pcp_v[i])
            if (self.use_train_tmpl == False):
                obs_ch_id = self.kmclassifier.predict([pcp_v[i]])[0]
            else:
                obs_ch_id = self.min_norm_ch_id(pcp_v[i])
            fl = False
            if (np.max(path[:, i - 1]) < 100):
                fl = True
            for j in range(nrow):# use obs id_v      #perehod iz k v j    первые два вместе, так как вер в прошлое и переход из прошлого
                mx_p = 0.0
                mx_id = 0
                for k in range(nrow):
                    s = path[k, i - 1] * self.t_matrix[k, j] * self.e_matrix[j, obs_ch_id]

                    #test = np.array(path[:,i - 1])
                    if fl:
                        s = s*50

                    if mx_p < s:
                        mx_p = s
                        mx_id = k
                #s = [(path[k, i - 1] * self.t_matrix[k, j] * self.e_matrix[j, obs_ch_id], k) for k in range(nrow)] #k - predid chord, i - n_step
                #(prob, state) = max(s)
                prob = mx_p
                state = mx_id
                path[j, i] = prob #got prob, v j na i step
                states[j, i] = state #got the best chord
        return (path, states)


    def min_norm_ch_id(self, pcp_v):
        min_dist = np.linalg.norm(np.array(pcp_v, dtype=float) - np.array(self.templ_chrds.get(0), dtype=float), ord=1)
        min_id = 0
        dist = 0
        for i in range(0, self.chords_total):
            dist = np.linalg.norm(np.array(pcp_v, dtype=float) - np.array(self.templ_chrds.get(i), dtype=float), ord=1)
            if min_dist > dist:
                min_id = i
                min_dist = dist
        return min_id