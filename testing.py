from iso_dataset import Iso_Dataset
from chord_quality_t import ChordQuality
from iso_adjusting import IsoAdjust
import numpy as np
from train_example import Train_Example
from glob import glob
import re
from chord import Chord
import json, codecs
from hmm_songs import HmmSongs
from hmm_data_saver import HmmDataSaver
from rnn_data_saver import RnnDataSaver
from ml_classification_methods import MlClassificationMethods


def start_hmm_trained_templ(iso_d):
    use_train_templ = True
    iso_d.make_templ_list_from_dataset()
    iso_d.train_templ()

    print("\nDict chord id:chord")
    print(iso_d.dict_id_ch)
    print("\nDict chord id:amount of windows with this chord")
    print(iso_d.cnt_chrds)

    #Подготовим датасет для тренировки классификатора
    #Запишем в json подготовленный датасет для нейронной сети
    rnnds = RnnDataSaver(iso_d.examples_list, iso_d.dict_ch_id, 4096)
    rnnds.prepare_ex_for_ml()
    rnnds.process_examples()
    rnnds.results_write_json()


    #Натренируем матрицы. Emission matrix тренируется с помощью переданного классификатора
    print("\nInit matrix \n")
    print(iso_d.get_hmm_matrix_i())
    print("\nTransition matrix \n")
    print(iso_d.get_hmm_matrix_t())
    #print("Emission matrix \n")
    print(iso_d.get_hmm_matrix_e())

    #Запустим алгоритм Витерби с данными параметрами
    hmm = HmmSongs(iso_d.list_chords, iso_d.templ_chrds, iso_d.i_matrix, iso_d.t_matrix, iso_d.e_matrix,
                   rnnds.songs_list, iso_d.examples_list, use_train_templ)
    hmm.initialize()

def start_hmm_knn(iso_d):
    use_train_templ = False
    iso_d.make_templ_list_from_dataset()
    #iso_d.train_templ()

    print("\nDict chord id:chord")
    print(iso_d.dict_id_ch)
    print("\nDict chord id:amount of windows with this chord")
    print(iso_d.cnt_chrds)

    # Подготовим датасет для тренировки классификатора
    # Запишем в json подготовленный датасет для нейронной сети
    rnnds = RnnDataSaver(iso_d.examples_list, iso_d.dict_ch_id, 4096)
    rnnds.prepare_ex_for_ml()
    rnnds.process_examples()
    rnnds.results_write_json()

    # Натренируем класификатор по данным, которые мы получили при обработке
    mlcm = MlClassificationMethods(rnnds.train_x, rnnds.train_y)
    mlcm.k_means_train()
    # Передадим классификатор в наш класс обработки датасета
    iso_d.kmclassifier = mlcm.kmclassifier

    # Натренируем матрицы. Emission matrix тренируется с помощью переданного классификатора
    print("\nInit matrix \n")
    print(iso_d.get_hmm_matrix_i())
    print("\nTransition matrix \n")
    print(iso_d.get_hmm_matrix_t())
    #print("Emission matrix \n")
    print(iso_d.get_hmm_matrix_e())

    # Запустим алгоритм Витерби с данными параметрами
    hmm = HmmSongs(iso_d.list_chords, iso_d.templ_chrds, iso_d.i_matrix, iso_d.t_matrix, iso_d.e_matrix,
                   rnnds.songs_list, iso_d.examples_list, use_train_templ)
    hmm.kmclassifier = mlcm.kmclassifier
    hmm.initialize()

def start_hmm_tpl_templates(iso_d, tpl_path):
    iso_d.load_tpl_templates(tpl_path)
    print("\nDict chord id:chord")
    print(iso_d.dict_id_ch)
    print("\nDict chord id:amount of windows with this chord")
    print(iso_d.cnt_chrds)

    # Подготовим датасет для тренировки классификатора
    # Запишем в json подготовленный датасет для нейронной сети
    rnnds = RnnDataSaver(iso_d.examples_list, iso_d.dict_ch_id, 4096)
    rnnds.prepare_ex_for_ml()
    rnnds.process_examples()
    rnnds.results_write_json()

    # Натренируем матрицы. Emission matrix тренируется с помощью переданного классификатора
    print("\nInit matrix \n")
    print(iso_d.get_hmm_matrix_i())
    print("\nTransition matrix \n")
    print(iso_d.get_hmm_matrix_t())
    #print("Emission matrix \n")
    print(iso_d.get_hmm_matrix_e())

    # Запустим алгоритм Витерби с данными параметрами
    hmm = HmmSongs(iso_d.list_chords, iso_d.templ_chrds, iso_d.i_matrix, iso_d.t_matrix, iso_d.e_matrix,
                   rnnds.songs_list, iso_d.examples_list, use_train_templ)
    hmm.initialize()


if __name__ == '__main__':

    #True - шаблоны и мин норма классификатор, False - нет шаблонов, использовать knn classificator
    use_train_templ = False


    #Все, что нужно для первого запуска хранится в проекте, просто укажите путь до DatasetExtraction по примеру:
    tpl_path = "D:\\ChordsRecognition\\music-dsp\\tools\\DatasetExtraction\\templ.txt"
    dataset_path = "D:\\ChordsRecognition\\music-dsp\\tools\\DatasetExtraction\\test_chords_txt\\*.lab"

    iso_d = Iso_Dataset(dataset_path, ChordQuality.cq_Max, use_train_templ, 4096)
    iso_d.load_examples(dataset_path)


    #Чтобы начать, убери комментарий от !одного! нужного старта

    #Использовать тренировочные шаблоны, классификатор - минимальная норма
    #Поставь вверху use_train_templ = True
    #start_hmm_trained_templ(iso_d)

    #Использовать теоритические шаблоны, классификатор - минимальная норма
    #Поставь вверху use_train_templ = True
    #start_hmm_tpl_templates(iso_d, tpl_path)

    #Натренировать knn классификатор и использовать его в алгоритме Витерби
    #Поставь вверху use_train_templ = False
    #start_hmm_knn(iso_d)
