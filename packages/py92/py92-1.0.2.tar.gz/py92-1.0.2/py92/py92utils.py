import pandas as pd
import py92


class py92utils:
    def __init__(self):
        self.df = pd.read_csv(py92.config.CN_SCHOOLS_DIR, encoding='utf-8')

    def is_in(self, name):
        return int(name in self.df["学校"].tolist())

    def is_ins(self, names):
        return [self.is_in(_) for _ in names]

    def is_985(self, name):
        if name not in self.df["学校"].tolist(): return -1
        return int(self.df[self.df["学校"] == name]["985"].values[0] == '是')

    def is_985s(self, names):
        return [self.is_985(_) for _ in names]

    def is_211(self, name):
        if name not in self.df["学校"].tolist():
            return -1
        else:
            return int(self.df[self.df["学校"] == name]["211"].values[0] == '是')

    def is_211s(self, names):
        return [self.is_211(_) for _ in names]

    def is_db1(self, name):
        if name not in self.df["学校"].tolist():
            return -1
        else:
            return int(self.df[self.df["学校"] == name]["双一流"].values[0] == '是')

    def is_db1s(self, names):
        return [self.is_db1(_) for _ in names]

    def is_university(self, name):
        if name not in self.df["学校"].tolist():
            return -1
        else:
            return int(self.df[self.df["学校"] == name]["层次"].values[0] == '本科')

    def is_universitys(self, names):
        return [self.is_university(_) for _ in names]

    def is_public(self, name):
        if name not in self.df["学校"].tolist():
            return -1
        else:
            return int(self.df[self.df["学校"] == name]["性质"].values[0] == '公办')

    def is_publics(self, names):
        return [self.is_public(_) for _ in names]

    def get_highest_label(self, name):
        if name not in self.df["学校"].tolist():
            return ''
        elif self.is_985(name):
            return "985"
        elif self.is_211(name):
            return "211"
        elif self.is_db1(name):
            return "双一流"
        else:
            if self.is_university(name):
                return "本科"
            else:
                return "专科"

    def get_highest_labels(self, names):
        return [self.get_highest_label(_) for _ in names]

    def get_label(self, name):
        return {"name": name,
                "985": self.is_985(name),
                "211": self.is_211(name),
                "双一流": self.is_db1(name),
                "本科": self.is_university(name),
                "公办": self.is_public(name)}

    def get_labels(self, names):
        return [self.get_label(k) for k in names]
