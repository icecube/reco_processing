model_configs_dict = {}

model_configs_dict["flavor"] = [
  {
    'name':'bdt1',
    'sig_mask': lambda df: 
                   (df['sig_bdt1']) & 
                   (df['TrueLength'] > 10),
    'bg_mask' : 'bg_bdt1'  
  },
  {
    'name':'bdt2',
    'sig_mask': lambda df: 
                   (df['sig_bdt1']) & 
                   (df['TrueLength'] > 10),
    'bg_mask' :'bg_bdt2'
  }
]

model_configs_dict["simpletopology"] = [
  {
    'name':'bdt1',
    'sig_mask': lambda df: 
                   (df['sig_bdt1_simpletopology']) & 
                   (df['TrueLength'] > 10),
    'bg_mask' : 'bg_bdt1_simpletopology'  
  },
  {
    'name':'bdt2',
    'sig_mask': lambda df: 
                   (df['sig_bdt1_simpletopology']) & 
                   (df['TrueLength'] > 10),
    'bg_mask' :'bg_bdt2_simpletopology'
  }
]

# model_configs_dict["truetopology"] = [
#   {
#     'name':'bdt1',
#     'sig_mask': lambda df: 
#                    (df['sig_bdt1_truetopology']) & 
#                    (df['TrueLength'] > 10),
#     'bg_mask' : 'bg_bdt1_truetopology'  
#   },
#   {
#     'name':'bdt2',
#     'sig_mask': lambda df: 
#                    (df['sig_bdt1_truetopology']) & 
#                    (df['TrueLength'] > 10),
#     'bg_mask' :'bg_bdt2_truetopology'
#   }
# ]