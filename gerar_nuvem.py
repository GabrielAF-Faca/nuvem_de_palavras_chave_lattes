# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:00:48 2022

@author: Gabri
"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

def pode_inserir(palavra):
    palavras_proibidas = "da,de,com,das,do,pelo,em,of,the,an,of,and,for,in,from,on,with,por,como,by,or,para,não,as,pós"
    palavras_proibidas = palavras_proibidas.split(",")
    
    if len(palavra) < 2:
        return False
    
    if "&#" in palavra:
        return False
    
    if palavra in palavras_proibidas:
        return False
    
    return True


pessoas = []
palavras_chave = []
palavras_titulo = {}
curriculo = {}

arquivo = open(r'C:\Users\Gabri\Desktop\Codigos bolsa\todos_curriculos.txt','r', encoding="utf8")
linhas = arquivo.readlines()

for linha in linhas:
    linha = linha.rstrip().lstrip()

    if linha.startswith("Nome:"):
        nome = linha.split(": ")[1]
        
        pessoas.append(nome)
        
        curriculo[nome] = ''
        palavras_titulo[nome] = ''
    
    #if "Titulo do artigo" in linha: #<- Esse analisa os titulos dos artigos em ingles (attr do xml que meu documento tambem armazena) alem dos titulo em portugues
    if "Titulo do artigo:" in linha: #<- Esse so analisa a linha que possui a attr titulo do artigo
        
        linha = linha.replace(".", "")
        
        split_linha = linha.split(": ")
         
        titulo = split_linha[1].lower()
        
        
        titulo = titulo.replace(":", " ")
        titulo = titulo.replace("<scp>", "").replace("</scp>","")
        
   
        if len(split_linha) > 2:
            titulo = titulo + " " + split_linha[2]
        
        elementos_titulo = titulo.split(" ")
        
        for palavra in elementos_titulo:
            if "," in palavra:
                palavra = palavra.replace(",", "")
                
            if pode_inserir(palavra.lower()):
                palavras_titulo[pessoas[-1]] += palavra.rstrip().lstrip() + ", "
    
        
    if 'Palavra chave' in linha:
        palavra = linha.split(": ")[1]
        
        palavras_chave.append([pessoas[-1], palavra])
        
        if palavra not in curriculo[pessoas[-1]]:
            curriculo[pessoas[-1]] = curriculo[pessoas[-1]] + palavra + ", "
            

for pessoa in pessoas:
    curriculo[pessoa] = curriculo[pessoa].rstrip(", ")
    palavras_titulo[pessoa] = palavras_titulo[pessoa].rstrip(", ")


num = 3

text = palavras_titulo[pessoas[num]]

wordcloud = WordCloud(width=1520,height=535,collocations=False).generate(text)

plt.figure(figsize=(16,9))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('wordcloud.png',transparent=True)

print("Nome: "+pessoas[num])
print("\n")

palavrasUnicas = text.split(', ')

ocorrencias = Counter(palavrasUnicas)

ocorrencias = dict(sorted(ocorrencias.items(), key=lambda item: item[1]))

print(ocorrencias)