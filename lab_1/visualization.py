import matplotlib.pyplot as plt


class DataVisualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8') #Стиль графиков
        self.colors = ['#FFD1DC', '#F8C8DC', '#F4BBD3', '#FFB7C5', '#F4ACB7', '#E8ADAA'] #Цвета для столбцов

    def plot_simplified_analysis(self, cuisine_stats):
        fig, axes = plt.subplots(1, 2, figsize=(15, 6)) #Разбиваем холст 15x6 на две части

        # Доля здоровых блюд по кухням
        cuisines = cuisine_stats.index #Получаем индексы из переданных данных
        healthy_ratio = cuisine_stats['is_healthy'] #Данные о доле здоровых блюд

        axes[0].bar(cuisines, healthy_ratio, color=self.colors) #Столбчатая диаграмма
        axes[0].set_title('Доля здоровых блюд по кухням', fontsize=14, fontweight='bold') #Заголовок
        axes[0].set_ylabel('Доля здоровых блюд') #Метка (название) для оси Y
        axes[0].tick_params(axis='x', rotation=45) #Поворот меток на Х

        # Добавляем значения на столбцы
        for i, v in enumerate(healthy_ratio):
            #.2f - с двумя знаками после запятой, ha='center' - выравнивание по горизонтали: центр
            #va='bottom' - выравнивание по вертикали: снизу,
            #enumerate - возвращает (индекс, значение) для каждого элемента в списке
            axes[0].text(i, v + 0.00025, f'{v:.2f}', ha='center', va='bottom')

        # Средняя калорийность по кухням (Аналогично)
        calories = cuisine_stats['calories']
        axes[1].bar(cuisines, calories, color=self.colors)
        axes[1].set_title('Средняя калорийность по кухням', fontsize=14, fontweight='bold')
        axes[1].set_ylabel('Калории')
        axes[1].tick_params(axis='x', rotation=45)

        # Добавляем значения на столбцы
        for i, v in enumerate(calories):
            axes[1].text(i, v + 5, f'{v:.0f}', ha='center', va='bottom')

        plt.tight_layout() #Автоматически подгоняем параметры графиков для лучшего отображения
        plt.show() #Отображаем графики на экране
