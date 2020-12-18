from bs4 import BeautifulSoup
from pandas import DataFrame

from config import settings
from model.active import Active
import pandas as pd


def get_five_list(page, block) -> list:
    actives = []

    bs_obj = BeautifulSoup(page, 'html.parser')
    div_list = bs_obj.find('div', {'id': block})
    div_list = div_list.find('div', {'class': 'list'})
    div_list = div_list.find_all('div', {'class': 'info w-100'})
    top5 = div_list[:settings.get('TOP_FIVE')]
    for active in top5:
        name = active.find('small', {'title': 'Nome da empresa/FII'}).text
        value_opening = active.find('div', {'title': 'Valor de abertura'}).find('span', {'class': 'value'}).text
        value_maximum = active.find('div', {'title': 'Máxima do dia'}).find('span', {'class': 'value'}).text
        value_minimum = active.find('div', {'title': 'Mínima do dia'}).find('span', {'class': 'value'}).text
        value_closure = active.find('div', {'title': 'Valor de fechamento'}).find('span', {'class': 'value'}).text
        volume = active.find('div', {'title': 'Volume financeiro'}).find('span', {'class': 'value'}).text

        actives.append(Active(name, value_opening, value_maximum, value_minimum, value_closure, volume))
    return actives


def generate_dataframe(actives) -> DataFrame:
    df_final = pd.DataFrame()
    for active in actives:
        d = {'Nome': [active.name], 'Abertura': [active.value_opening], 'Mínima': [active.value_minimum],
             'Máxima': [active.value_maximum], 'Atual': [active.value_closure], 'Volume': [active.volume]}
        df = pd.DataFrame(data=d)
        df_final = pd.concat([df_final, df])

    return df_final


class High:
    @classmethod
    def top_five(cls, page):
        actives = get_five_list(page, 'asUp')
        df_final = generate_dataframe(actives)
        print(df_final)
        print(type(df_final))


class Down:
    @classmethod
    def top_five(cls, page):
        actives = get_five_list(page, 'asDown')
        df_final = generate_dataframe(actives)
        print(df_final)
        print(type(df_final))
