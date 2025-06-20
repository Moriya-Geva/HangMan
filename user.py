import json


class user:
    def __init__(self, name, tz, password, numPlay, strAppear, numWin):
        self.name = name
        self.tz = tz
        self.password = password
        self.numPlay = numPlay
        self.strAppear = strAppear
        self.numWin = numWin


    def __eq__(self, other):
        return self.tz == other.tz  # השוואה בין תעודות זהות

    def __hash__(self):
        return hash(self.tz)  # הפיכת האובייקט להאשינג לפי תעודת זהות

    def to_dict(self):
        return {
            "name": self.name,
            "tz": self.tz,
            "password": self.password,
            "numPlay": self.numPlay,
            "strAppear": self.strAppear,
            "numWin": self.numWin
        }

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            name=dict_obj["name"],
            tz=dict_obj["tz"],
            password=dict_obj["password"],
            numPlay=dict_obj["numPlay"],
            strAppear=dict_obj["strAppear"],
            numWin=dict_obj["numWin"]
        )
