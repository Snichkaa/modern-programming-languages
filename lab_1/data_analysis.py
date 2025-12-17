import pandas as pd


class DataAnalyzer:
    #Конструктор
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self._clean_data()

    #Удаляем дубликаты из выборки
    def _clean_data(self):
        self.df = self.df.drop_duplicates() #Удаляет при совпадении всех признаков

    #Базовая статистика по данным
    def get_basic_stats(self):
        #Словарь, в котором хранится общая информация
        stats = {
            'total_meals': len(self.df), #Общее кол-во блюд (подсчитывается кол-вом строк в таблице)
            'cuisines': self.df['cuisine'].nunique(), #Считаются уникальные по столбцу кухни
            'healthy_meals': self.df['is_healthy'].sum(), #находим кол-во полезных блюд
            'unhealthy_meals': len(self.df) - self.df['is_healthy'].sum() #и не очень полезных
        }
        return stats

    # Анализ по кухням
    def analyze_by_cuisine(self):
        #Группируем блюда по кухням, и для каждой кухни вычисляем среднюю калорийность и процент полезных блюд
        cuisine_stats = self.df.groupby('cuisine').agg({
        #Название агрегирующей функции (в виде строки). mean - вычисляет среднее значение
            'calories': 'mean',
            'is_healthy': 'mean'
        }).round(2)

        cuisine_stats['is_healthy'] = cuisine_stats['is_healthy'] * 100 #Отображение в процентах

        return cuisine_stats
