import pandas as pd
import os
from json import dump, load
import numpy as np
import matplotlib.pyplot as plt

#TODO need to merge these clasess some how
class yahiadf:
    @staticmethod
    def load_df(loading_function=(lambda : pd.DataFrame({})), args=tuple(), name='dataframe', path='./', formating_function=(lambda x: (x, [])), formating_args=tuple()):
        if not os.path.isfile(f'{path}{name}.pkl') or not os.path.isfile(f'{path}labels_{name}.json'):
            df = loading_function(*args)
            (df, labels) = formating_function(df, *formating_args)
            df.to_pickle(f'{path}{name}.pkl')
            with open(f'{path}labels_{name}.json', 'w') as labels_json:
                dump(labels, labels_json)
            print(f"Made and dumped {name}")
        else:
            df = pd.read_pickle(f'{path}{name}.pkl')
            with open(f'{path}labels_{name}.json', 'r') as labels_json:
                labels = load(labels_json)
            print(f"loaded {name}")
        
        return (df, labels)


class  yahiasql:
    
    #TODO need to add way to remove keywords and keyranges

    def __init__(self, keywords=[], keyranges=[], keyfuncs=dict()):
        self.keywords = [*keywords]
        self.keyranges = [*keyranges]
        self.keyfuncs = dict(**keyfuncs)
    
    def add_keyword(self, keywords=[]):
        self.keywords.append(keywords)
    
    def add_keyrange(self, keyranges=[]):
        self.keyranges.append(keyranges)
    
    def add_keyfunc(self, keyfuncs=[]):
        self.keyfuncs.update(keyfuncs)
    
    def parase_yahiasql(self, sql):
        parased = dict()
        keyfuncs = self.keyfuncs.keys() 
        keys = [*self.keywords, *self.keyranges, *keyfuncs]
        keyranges = [ *self.keyranges, *keyfuncs]
        
        for key in keys:
            parased[key] = False

        sql = sql.split()
        current_key = sql[0]

        if current_key not in keys:
            raise ValueError("error first argument is not in keys")
        
        current_range = []
        for argument in sql:
            if argument in keys:
                if current_key in keyranges:
                    parased[current_key].append(current_range)
                elif current_range:
                    raise ValueError("keyword followed by non key argument")

                current_range = []
                
                if argument in self.keywords:
                    parased[argument] = True
                
                else:
                    if parased[argument] == False:
                        parased[argument] = []
                    else:
                        raise ValueError(f"Can only use keyrange {argument} once")
                current_key = argument
            else:
                current_range.append(argument)
        
        for key in keyfuncs:
            if parased[key] != False:
                parased[key] = self.keyfuncs[key](sql)
        return parased 

class yahiaplot:
    @staticmethod
    def plot(column_data, column_name, out_of, n_columns=1, labels=[], path='./curves/'): 
  
        #column_name = column_name.capitalize() 
  
        #TODO add to make sure to maximums if multiple are the same 
  
        # Changing width and Height 
        width = out_of * 3 / 60   
        print(width) 
        if width < 6.4 : 
            width = 6.4 
        elif width > 50:
            width = 50
            print(f"To big to plot {column_name}") 
            return  
  
        height = 4.8 
  
        bins = np.arange(0, out_of + 2) 
        plot = column_data.plot.hist(bins=bins, align='left', edgecolor='black', width=1, alpha=1/n_columns, figsize=(width, height))  
                                     
  
        if len(labels) != 0: 
            if out_of < 50: 
                plot.set_xticks(range(len(labels)), labels, rotation='vertical') 
            else: 
                plot.set_xticks(range(len(labels)), labels, rotation='vertical', size=3) 
        elif n_columns > 1: 
            pass 
        else: 
            #TODO fix means for each column  
  
            plot.xaxis.get_major_locator().set_params(integer=True) 
            #TODO fix mean line make sure in right plce 
            # Mean line 
            plot.axvline(x=column_data.mean(), label='Mean') 
  
            # Standard deviation 
            plot.axvline(x=column_data.mean() + column_data.std()) 
            plot.axvline(x=column_data.mean() - column_data.std()) 
  
        # Limit to edges 
        plot.set_xlim(xmin=-0.5, xmax=out_of + 0.5) 
        # Title 
        plot.set_title(f"{column_name} ({column_data.count()})") 
  
        # Column names 
        if len(labels) == 0: 
            plot.set_xlabel('Grades out of ' + str(out_of)) 
  
        plot.set_ylabel('No. of People') 
        # Save and exit
        column_name= column_name.replace("/", "_")
        #TODO better handle path not present
        plot.figure.savefig(f'{path}{column_name}.png', dpi=1000, bbox_inches='tight') 
        plt.close(plot.figure) 
        print(f'done {column_name}') 
