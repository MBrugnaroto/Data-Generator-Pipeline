import math
from random import random 

def generate_rand_number(min, max):
    return math.floor((random()*(max-min))+min)

def get_rand_value(df, column):
    total_values = df[column].count()
    position = generate_rand_number(0, total_values-1)
    return df.iloc[position][column]
    
def get_rand_value(dict, column):
    total_values = list(dict.keys())[-1]
    key = generate_rand_number(0, total_values)
    return dict[key][column]

def get_rand_key(dict):
    total_values = list(dict.keys())[-1]
    return generate_rand_number(0, total_values)