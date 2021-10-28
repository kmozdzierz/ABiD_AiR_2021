import numpy as np
import pickle
from pandas.core.algorithms import isin

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020')

def film_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(category_id, int):
        return None
    else:
        query = f'''SELECT
                        f.title,
                        l.name as languge,
                        c.name as category 
                    FROM film f
                        JOIN
                            language l ON f.language_id = l.language_id
                        JOIN
                            film_category fc ON f.film_id = fc.film_id
                        JOIN 
                            category c ON c.category_id = fc.category_id
                        WHERE
                            fc.category_id = {category_id}
                        ORDER BY 
                            f.title, l.name'''

        return pd.read_sql(query, con = connection)
        
    
def number_films_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategori przez id kategorii.
    Przykład wynikowej tabeli:
    |   |category   |count|
    |0	|Action 	|64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(category_id, int):
        return None
    else:
        
        query = f'''SELECT
                        c.name as category,
                        COUNT(*)
                    FROM film f
                        JOIN film_category fc ON f.film_id = fc.film_id
                        JOIN category c ON fc.category_id = c.category_id
                    WHERE 
                        fc.category_id = {category_id}
                    GROUP BY 
                        c.name'''

    return pd.read_sql(query, con = connection)

def number_film_by_length(min_length: Union[int,float] = 0, max_length: Union[int,float] = 1e6 ) :
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczegolnych długości pomiędzy wartościami min_length a max_length.
    Przykład wynikowej tabeli:
    |   |length     |count|
    |0	|46 	    |64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    min_length (int,float): wartość minimalnej długości filmu
    max_length (int,float): wartość maksymalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not (isinstance(min_length, (int, float)) and isinstance(max_length, (int,float))):
        return None

    if max_length < min_length:
        return None 
    else:
        query = f'''SELECT
                        f.length,
                        COUNT (*)

                    FROM film f
                    WHERE      
                        f.length BETWEEN {min_length} AND {max_length}
                    GROUP BY
                        f.length'''

        return pd.read_sql(query, con = connection)

def client_from_city(city:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    Przykład wynikowej tabeli:
    |   |city	    |first_name	|last_name
    |0	|Athenai	|Linda	    |Williams
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    city (str): nazwa miaste dla którego mamy sporządzić listę klientów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''


    if not isinstance(city, str):
        return None
    else:
        query = f'''SELECT
                        city.city,
                        c.first_name,
                        c.last_name 
                    FROM customer c
                        JOIN address a ON c.address_id = a.address_id
                        JOIN city ON a.city_id = city.city_id
                    WHERE
                        city.city = '{city}' 
                    ORDER BY 
                        c.first_name, c.last_name ASC'''

        return pd.read_sql(query, con = connection)

def avg_amount_by_length(length:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla zadanej długości length.
    Przykład wynikowej tabeli:
    |   |length |avg
    |0	|48	    |4.295389
    
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    length (int,float): długość filmu dla którego mamy pożyczyć średnią wartość wypożyczonych filmów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not (isinstance(length, (int, float))):
        return None
    else:
        query = f'''SELECT
                        f.length,
                        AVG(p.amount)

                    FROM film f
                        JOIN inventory inv ON f.film_id = inv.film_id
                        JOIN rental rent ON inv.inventory_id = rent.inventory_id
                        JOIN payment p ON rent.rental_id = p.rental_id
                    WHERE      
                        f.length = {length}
                    GROUP BY
                        f.length'''

        return pd.read_sql(query, con = connection)
    

def client_by_sum_length(sum_min:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów przez klientów powyżej zadanej wartości .
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |sum
    |0  |Brian	    |Wyman  	|1265
    
    Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów którą musi spełniać klient
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(sum_min, (int, float)):
        return None
    else:
        query = f'''SELECT
                        c.first_name,
                        c.last_name,
                        SUM(f.length) as sum
                    FROM customer c
                        JOIN rental r ON c.customer_id = r.customer_id
                        JOIN inventory i ON r.inventory_id = i.inventory_id
                        JOIN film f ON i.film_id = f.film_id 
                    GROUP BY
                        c.first_name, c.last_name
                    HAVING  
                        SUM(f.length) > {sum_min}
                    ORDER BY
                        sum, last_name, first_name'''

    return pd.read_sql(query, con = connection)  

def category_statistic_length(name:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    Przykład wynikowej tabeli:
    |   |category   |avg    |sum    |min    |max
    |0	|Action 	|111.60 |7143   |47 	|185
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    name (str): Nazwa kategorii dla której ma zostać wypisana statystyka
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if not isinstance(name, str):
        return None
    else:
        
        query = f'''SELECT
                        c.name as category,
                        AVG(f.length),
                        SUM(f.length),
                        MIN(f.length),
                        MAX(f.length)
                    FROM
                        film f
                            JOIN film_category fc ON f.film_id = fc.film_id
                            JOIN category c ON fc.category_id = c.category_id
                    GROUP BY
                        c.name
                    HAVING 
                        c.name = '{name}' '''


        return pd.read_sql(query, con = connection)  