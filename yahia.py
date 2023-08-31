import pandas as pd
import os
from json import dump, load

class yahiadf:
    @staticmethod
    def load_df(loading_function=(lambda : pd.DataFrame({})), args=tuple(), name='dataframe', formating_function=(lambda x: (x, [])), formating_args=tuple()):
        if not os.path.isfile(f'{name}.pkl') or not os.path.isfile(f'labels{name}.json'):
            df = loading_function(*args)
            (df, labels) = formating_function(df, *formating_args)
            df.to_pickle(f'{name}.pkl')
            with open(f'labels_{name}.json', 'w') as labels_json:
                dump(labels, labels_json)
            print(f"Made and dumped {name}")
        else:
            df = pd.read_pickle(f'{name}.pkl')
            with open(f'labels{name}.json', 'r') as labels_json:
                labels = load(labels_json)
            print(f"loaded {df}")
        
        return (df, labels)

class  yahiasql:
    

    def __init__(self, keywords=[], keyranges=[]):
        self.keywords = [*keywords]
        self.keyranges = [*keyranges]
    
    def add_keyword(self, keywords=[]):
        self.keywords.append(keywords)
    
    def add_keyrange(self, keyranges=[]):
        self.keyranges.append(keyranges)
    
    def parase_yahiasql(self, sql):
        parased = dict()
        keys = [*self.keywords, *self.keyranges]
        for key in keys:
            parased[key] = False

        sql = sql.split()
        current_key = sql[0]
        if current_key not in keys:
            raise ValueError("error first argument is not in keys")
        current_range = []
        for argument in sql:
            if argument in keys:
                if current_key in self.keyranges:
                    parased[current_key].append(current_range)
                elif current_range:
                    raise ValueError("keyword folled by non key argument")

                current_range = []
                
                if argument in self.keywords:
                    parased[argument] = True
                elif parased[argument] != False:
                    parased[argument] = []
                current_key = argument
            else:
                current_range.append(argument)
        return parased 
        
