import ujson
import os

### VERY LIGHT JSON DB ###
class DB (object):

    def __init__(self, filename="out.jsondb"):
        self.filename = filename
        self.tables = {}
        if os.path.isfile(filename):
            data = None
            with open(filename, "r") as in_db:
                data = in_db.read()
            self.load(data)

    def load(self, raw_data):
        data = None

        data = ujson.loads(raw_data)
        for table_data in data["tables"]:
            self.add_table(Table.load(table_data))


    def save(self):
        out_file = {"filename": self.filename, "tables":[]}
        for id in self.tables:
            out_file["tables"].append(self.tables[id].__dict__)

        with open(self.filename, "w") as db_out:
            db_out.write(ujson.dumps(out_file))

    def add_table(self, table, overwrite=False):
        if table.tablename in self.tables.keys() and not overwrite:
            raise KeyError("Table {} already exists.".format(table.tablename))
        self.tables[table.tablename] = table

class Table (object):
    def __init__(self, tablename, keys, keys_default={}):
        self.tablename = tablename
        self.keys = keys
        self.models = {}
        self.row_num = 0
        self.keys_default = keys_default

    @staticmethod
    def load(data):
        table = Table(data["tablename"], data["keys"], data["keys_default"])
        table.models = data["models"]
        table.row_num = data["row_num"]
        return table

    def find_models(self, keymap={}):
        found = []
        if keymap == {}:
            return self.models.values()

        for id in self.models:
            for key in keymap.keys():
                if self.models[id][key] == keymap[key]:
                    found.append(self.models[id])

        return found

    def find_by_id(self, id):
        try:
            return self.models[str(id)]
        except KeyError:
            return {}

    def insert(self, keymap={}):
        self.row_num+=1
        self.models[str(self.row_num)]={"id":self.row_num}
        for key in self.keys:
            if key in keymap.keys():
                self.models[str(self.row_num)][key] = keymap[key]
            else:
                if key in self.keys_default.keys():
                    self.models[str(self.row_num)][key] = self.keys_default[key]
                else:
                    self.models[str(self.row_num)][key] = None

        return self.row_num

    def delete(self, id):
        if str(id) in self.models:
           del self.models[str(id)]

        else:
            raise KeyError("Row does not exist in {} Table".format(self.tablename))

