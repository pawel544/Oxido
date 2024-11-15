import openai as op

import os
import requests


op.api_key='Sekretyny_Klucz'
def dowald_text(url):
    response=requests.get(url)
    if response.status_code==200:
        return response.text
    else:
        raise Exception (f'Nie udało się pobrać pliku status błędu{response.status_code}')
def cut_tekst(text, max_token=1000):
    words= text.split()
    chunk=[]
    curry_chunks=[]
    token=0
    for word in words:
        token+=len(word.split())
        if token >max_token:
            chunk.append(" ".join(curry_chunks))
            curry_chunks=[word]
            token=len(word.split())
        else:
            curry_chunks.append(word)
    if curry_chunks:
        chunk.append(" ".join(curry_chunks))
    return chunk


def generator(content):
    prompt=f"""
    Na podstawie poniższego tekstu opracuj artykuł w formacie HTML. Uwzględnij wprowadzenie, podziel treść na sekcje,
    i dodaj miejsca na trzy grafiki z opisami. Treść:
    {content}
    """
    response=op.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
    return response['choices'][0]['message']['content'].strip()
def save_to_html(content,file_name='artykul.html'):
    with open(file_name, 'w', encoding='utf-8') as (file):
        file.write(content)
        return f"plik zapisany pod nazwą {file_name}"


if __name__=="__main__":
    url="https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"
    try:
        print(f'trwa pobieranie pliku')
        dowalnd=dowald_text(url)
        print(f'Pobieranie zakończone momyślnie')
        chunks=cut_tekst(dowalnd)
        html=""
        print(f"Rozpoczęcie przetważania tekstu")
        for chunk in chunks:
            html += generator(chunk)
        print(f'Przetważanie zakończone pomyślnie')


        print(f"Rozpoczynam zapis pliku")
        save=save_to_html(html)
        print(f"Plik zapisany pobyślnie")

    except Exception as e:
        print(f' Błąd {e}')

