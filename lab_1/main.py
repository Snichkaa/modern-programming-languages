#ООП - инкапсуляция (+: данные из CSV-файла загружаются внутрь объекта), абстракция(+: скрыта обработка данных и построение графиков), наследование и полиморфизм(-)
from data_analysis import DataAnalyzer
from visualization import DataVisualizer


def main():
    print("АНАЛИЗ ДАННЫХ О ЗДОРОВОМ ПИТАНИИ:")

    #Инициализируем данные
    analyzer = DataAnalyzer('healthy_eating_dataset.csv')
    visualizer = DataVisualizer()

    #Базовая статистика
    print("\nБАЗОВАЯ СТАТИСТИКА:")
    basic_stats = analyzer.get_basic_stats()
    for key, value in basic_stats.items():
        print(f"{key.replace('_', ' ').title()}: {value}") #title() - первая буква становится заглавной

    #Анализ по кухням
    print("\nАНАЛИЗ ПО КУХНЯМ:")
    cuisine_stats = analyzer.analyze_by_cuisine()
    print(cuisine_stats)

    #Создаем два графика: доля здоровых блюд и средняя калорийность по кухням
    visualizer.plot_simplified_analysis(cuisine_stats)

    print("\nАНАЛИЗ ЗАВЕРШЕН!")
    print("Графики успешно созданы и отображены.")

if __name__ == "__main__":
    main()
