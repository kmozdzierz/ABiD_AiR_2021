import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020');

def film_in_category(category:Union[int,str])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str, dokładnie taki jak podana wartość
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(category,(int,str)):
        return None

    else:
        if isinstance(category,str):
            query = f'''SELECT
                            title,
                            l.name as languge,
                            c.name as category

                        FROM
                            film f 
                                INNER JOIN language l ON f.language_id = l.language_id
                                INNER JOIN film_category fc ON f.film_id = fc.film_id
                                INNER JOIN category c ON fc.category_id = c.category_id   
                        WHERE
                            c.name LIKE '{category}'
                        ORDER BY
                            f.title, l.name'''
        elif isinstance(category,int):
            query = f'''SELECT
                            title,
                            l.name as languge,
                            c.name as category

                        FROM
                            film f 
                                INNER JOIN language l ON f.language_id = l.language_id
                                INNER JOIN film_category fc ON f.film_id = fc.film_id
                                INNER JOIN category c ON fc.category_id = c.category_id   
                        WHERE
                            c.category_id = {category}
                        ORDER BY
                                f.title, l.name'''
        else:
            return None

        return pd.read_sql(query, con= connection)
    
def film_in_category_case_insensitive(category:Union[int,str])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(category,(int,str)):
        return None

    else:
        if isinstance(category,str):
            query = f'''SELECT
                            title,
                            l.name as languge,
                            c.name as category

                        FROM
                            film f 
                                INNER JOIN language l ON f.language_id = l.language_id
                                INNER JOIN film_category fc ON f.film_id = fc.film_id
                                INNER JOIN category c ON fc.category_id = c.category_id   
                        WHERE
                            c.name ILIKE '{category}'
                        ORDER BY
                            f.title, l.name'''
        elif isinstance(category,int):
            query = f'''SELECT
                            title,
                            l.name as languge,
                            c.name as category

                        FROM
                            film f 
                                INNER JOIN language l ON f.language_id = l.language_id
                                INNER JOIN film_category fc ON f.film_id = fc.film_id
                                INNER JOIN category c ON fc.category_id = c.category_id   
                        WHERE
                            c.category_id = {category}
                        ORDER BY
                                f.title, l.name'''
        else:
            return None

        return pd.read_sql(query, con= connection)
    
def film_cast(title:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o obsadę filmu o dokładnie zadanym tytule.
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |
    |0	|Greg       |Chaplin    | 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    title (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(title,str):
        return None

    else:
        query = f'''SELECT 
                        a.first_name,
                        a.last_name
                    FROM 
                        actor a
                            INNER JOIN film_actor fa ON a.actor_id = fa.actor_id
                            INNER JOIN film f ON fa.film_id = f.film_id
                    WHERE
                        f.title LIKE '{title}' 
                    ORDER BY
                        a.last_name, a.first_name'''

        return pd.read_sql(query, con= connection)
    

def film_title_case_insensitive(words:list) :
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuły filmów zawierających conajmniej jedno z podanych słów z listy words.
    Przykład wynikowej tabeli:
    |   |title              |
    |0	|Crystal Breaking 	| 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    words(list): wartość minimalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(words,list):
        return None

    else:
        words_prep = "|".join(words)
        
        query = fr'''SELECT 
                        f.title
                    FROM 
                        film f
                    WHERE
                        f.title ~* '^({words_prep})\s'
                        OR
                        f.title ~* '\s({words_prep})$'                       
                    ORDER BY
                        f.title'''

        return pd.read_sql(query, con= connection)