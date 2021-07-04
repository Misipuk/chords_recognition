from chord_quality_t import ChordQuality

class IsoAdjust:
    ch_quality = 0

    def __init__(self, ch_quality, dict_notes_id, dict_id_notes):
        self.ch_quality = ch_quality
        self.dict_notes_id = dict_notes_id
        self.dict_id_notes = dict_id_notes


    def adjust_to_cq_max(self, label):
        #self.ch_quality.value)
        if (self.ch_quality.value < 25):
            if "min13" in label:
                label = label.replace("min13", "min11")

        if (self.ch_quality.value < 24):
            if "maj13" in label:
                label = label.replace("maj13", "maj11")

        if (self.ch_quality.value < 23):
            if "min11" in label:
                label = label.replace("min11", "min9")

        if (self.ch_quality.value < 22):
            if "maj11" in label:
                label = label.replace("maj11", "maj9")

        if (self.ch_quality.value < 21):
            if "aug7" in label:
                label = label.replace("aug7", "aug")

        if (self.ch_quality.value < 20):
            if ":9" in label:
                label = label.replace(":9", ":7")

        if (self.ch_quality.value < 19):
            if ":7(#9)" in label:
                label = label.replace(":7(#9)", ":7")

        if (self.ch_quality.value < 18):
            if "maj(11)" in label:
                label = label.replace("maj(11)", "maj")

        if (self.ch_quality.value < 17):
            if "min9" in label:
                label = label.replace("min9", "min7")

        if (self.ch_quality.value < 16):
            if "maj9" in label:
                label = label.replace("maj9", "maj7")

        if (self.ch_quality.value < 15):
            if "min6" in label:
                label = label.replace("min6", "min")

        if (self.ch_quality.value < 15):
            if "min6" in label:
                label = label.replace("min6", "min")

        if (self.ch_quality.value < 14):
            if "maj6" in label:
                label = label.replace("maj6", "maj")

        if (self.ch_quality.value < 13):
            if "min(9)" in label:
                label = label.replace("min(9)", "min")

        if (self.ch_quality.value == 11):
            if "maj(9)" in label:
                label = label.replace("maj(9)", "maj")
        return label

    def adjust_templ_to_cq_max(self, templ_chrds):

        for label in list(templ_chrds.keys()):

            #self.ch_quality.value)
            if (self.ch_quality.value < 25):
                if "min13" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 24):
                if "maj13" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 23):
                if "min11" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 22):
                if "maj11" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 21):
                if "aug7" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 20):
                if ":9" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 19):
                if ":7(#9)" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 18):
                if "maj(11)" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 17):
                if "min9" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 16):
                if "maj9" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 15):
                if "min6" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 15):
                if "min6" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 14):
                if "maj6" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value < 13):
                if "min(9)" in label:
                    templ_chrds.pop(label, None)

            if (self.ch_quality.value == 11):
                if "maj(9)" in label:
                    templ_chrds.pop(label, None)
        return templ_chrds


    def label_error_modify(self, label):
        if label == 'Emin/4':
            label = 'E:min/4'
        elif label == 'A7/3':
            label = 'A:7/3'
        elif label == 'Bb7/3':
            label = 'Bb:7/3'
        elif label == 'Bb7/5':
            label = 'Bb:7/5'
        elif len(label) == 1 and label != "N":
            label = label + ":min"
            if label == 'G:minmaj7/5':
                print("here")
            # print(label)
        elif label.find(':') == -1:
            if label.find('min') != -1:
                label = label[:label.find('min')] + ':' + label[label.find('min'):]
                #print(label)



        if "/2" == label[-2:]:
            label = label[:-2]
            # print(label)
            # print("********")



        if "/3" == label[-2:]:
            # print(label)
            label = label[:-2]
            #print(label)

        if "/4" == label[-2:]:
            # print(label)
            label = label[:-2]
            # print(label)
            # print("********")



        if "/6" == label[-2:]:
            #print(label)
            label = label[:-2]
            #print(label)
            #print("********")



        if "/b7" == label[-3:]:
            #print(label)
            label = label[:-3]
            #print(label)
            #print("********")

        if "/b9" == label[-3:]:
            #print(label)
            label = label[:-3]
            #print(label)
            #print("********")



        if "/7" == label[-2:]:
            # print(label)
            label = label[:-2]
            # print(label)
            # print("********")

        if "/9" == label[-2:]:
            # print(label)
            label = label[:-2]
            # print(label)
            # print("********")

        if ("/b3" in label or "/3" in label) and "maj/3" not in label and "min/3" not in label:
            # print(label)
            label = label[:-3]
            # print(label)
            # print("********")

        if "/5" in label and "maj/5" not in label and "min/5" not in label:
            # print(label)
            label = label[:-2]
            # print(label)
            # print("********")

        if label[-4:] == "(*5)":
            #print(label)
            label = label[:-4]
            #print(label)
            #print("********")

        if label[-5:] == "(#11)":
            #print(label)
            label = label[:-5]
            #print(label)
            #print("********")

        if label[-6:] == "(9,11)":
            #print(label)
            label = label[:-6]
            #print(label)
            #print("********")



        if label[-4:] == "(b9)" or label[-4:] == "(b5)" or label[-4:] == "(b7)":
            #print(label)
            label = label[:-4]
            #print(label)
            #print("********")

        if label[-8:] == "(1,b3,4)":
           # print(label)
            label = label[:-9]
            #print(label)
            #print("********")

        if label[-10:] == "(1,2,5,b6)":
            #print(label)
            label = label[:-10] + "sus2"
            #print(label)
            #print("********")

        if label[-5:] == "(*b3)" or label[-5:] == "(*b5)":
            #print(label)
            if "min(*b3)" in label:
                label = label[:-8] + "5"
            else:
                label = label[:-5]

            #print(label)
            #print("********")

        if label[-4:] == "(*1)" or label[-4:] == "(13)":
            #print(label)
            label = label[:-4]
            #print(label)
            #print("********")

        if label[-7:] == "(*5,b6)":
            #print(label)
            label = label[:-7]
            #print(label)
            #print("********")

        if label[-4:] == "(*3)" or label[-4:] == "(11)" or label[-4:] == "(*7)" or label[-4:] == "(#4)":
            #print(label)
            label = label[:-4]
            #print(label)
            #print("********")



        if label[-8:] == "(1,4,b7)" or label[-8:] == "(1,4,b5)":
            #print(label)
            label = label[:-8] + "sus4"
            #print(label)
            #print("********")


        if label[-3:] == "(6)":
            #print(label)
            label = label[:-3] + "maj6"
            #print(label)
            #print("********")

        if label[-3:] == "(2)" or label[-3:] == "(4)" or label[-3:] == "(9)" or label[-3:] == "/#5" or label[-3:] == "/#1" or label[-3:] == "/b2" or label[-3:] == "/b5":
            #print(label)
            label = label[:-3]
            #print(label)
            #print("********")

        if "(*1)" in label:
            #print(label)
            label = label[:-4]
            #print(label)
            #print("********")

        if label[-3:] == "/#4":
            #print(label)
            label = label[:-3] + ":maj"
            #print(label)
            #print("********")

        if label[-7:] == "(*5,13)":
            #print(label)
            label = label[:-7]
            #print(label)
            #print("********")

        if label[-7:] == "(1,2,4)":
            #print(label)
            label = label[:-8]
            #print(label)
            #print("********")

        if label[-5:] == "(1,5)":
            #print(label)
            label = label[:-5] + "5"
            #print(label)
            #print("********")



        if label[-6:] == "(1,b3)":
            #print(label)
            label = label[:-6] + "min"
            #print(label)
            #print("********")

        if label[-7:] == "(*3,11)":
            #print(label)
            label = label[:-8] + "min11"
            #print(label)
            #print("********")

        if label[-7:] == "minmaj7":
            #print(label)
            label = label[:-7] + "min"
            #print(label)
            #print("********")


        """if label[-5:] == "(1,4)":
            #print(label)
            label = label[:-5] + "sus4"
            #print(label)
            #print("********")"""


        if "/7" == label[-2:] and len(label) == 3:
            #print(label)
            label = label[0] + ":maj"
            #print(label)
            #print("********")



        if len(label) == 3 and "5" not in label:
            #print(label)
            label = label[:2] + "min" + label[2:]
            #print(label)
            #print("********")

        """if "min5" in label:
            print(label)
            print("********")"""

        if len(label) == 5 and label[-3:] == "(1)":
            #print(label)
            label = label[:-3] + "maj/1"
            #print(label)
            #print("********")

        if len(label) == 5 and label[-3:] == "(7)":
            #print(label)
            label = label[:-3] + "maj7"
            #print(label)
            #print("********")

        if "/b6" == label[-3:] and len(label) == 4:
            # print(label)
            label = label[:-3] + ":maj"
            # print(label)
            # print("********")

        if "/5" == label[-2:] and len(label) == 3:
            # print(label)
            label = label[0] + ":min" + label[-2:]
            # print(label)
            # print("********")

        if len(label)<7 and label[-3:] == "(1)":
            #print(label)
            label = label[:-3] + "maj"
            #print(label)
            #print("********")


        if len(label) > 1 and label[1] == 'b':
            id = self.dict_notes_id.get(label[0])
            conv = self.dict_id_notes.get(id-1)
            #print(label)
            label = conv + label[2:]
            if 'G:minmaj7' in label:
                print("here")
            #print(label)
            #print("********")

        if len(label) <= 2 and label != "N":
            #print(label)
            label = label + ":min"
            #print(label)
            #print("********")



        return label