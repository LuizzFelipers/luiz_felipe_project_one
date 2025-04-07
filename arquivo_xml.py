import os
import xmltodict
import json
import pandas as pd
import numpy as np
import openpyxl

def get_information(name_file):
    print(f'the extration information was sucess in {name_file}')
    with open(f"files/{name_file}","rb") as file_xml:
        dict_file = xmltodict.parse(file_xml)
            #print(dict_file)
            #print(json.dumps(dict_file,indent= 4))
        
        if "NFe" in dict_file:
            info_nf = dict_file["NFe"]["infNFe"]
        else:
            info_nf = dict_file['nfeProc']["NFe"]["infNFe"]
        numero_nota = info_nf["@Id"]
        empresa_emissora = info_nf["emit"]["xNome"]
        cliente = info_nf["dest"]["xNome"]
        endereco_dest = info_nf["dest"]["enderDest"]
        if "vol" in info_nf['transp']:
            peso = info_nf['transp']['vol']['pesoB']
        else:
            print("Peso não informado")
        values.append([numero_nota,empresa_emissora,cliente,endereco_dest])

list_file = os.listdir('files')

columns = ['numero_nota','empresa_emissora','cliente','endereco_dest']
values = []

for file in list_file:
    get_information(file)

table = pd.DataFrame(columns= columns,data= values)
print(table)
    
table.to_excel('notas_fiscais.xlsx',index=False)

print('The project is execute whit sucess!!')