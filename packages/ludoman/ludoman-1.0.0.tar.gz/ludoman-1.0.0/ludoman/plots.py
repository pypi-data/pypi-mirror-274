import numpy as np
import matplotlib.pyplot as plt

def Plot(profit_list, string, log):
    plt.figure(figsize=(10, 4))
    x_values = range(1, len(profit_list) + 1)
    y_values = profit_list
    # Логарифмическая шкала
    if log == True:
        plt.yscale('log')
    # Построение графика
    plt.plot(x_values, y_values)  # График с точками marker='o'
    plt.xlabel('Номер сделки')  # Подпись оси x
    plt.ylabel('Процент прибыли')  # Подпись оси y
    plt.title(string)  # Заголовок графика
    plt.grid(True)  # Отображение сетки на графике
    plt.show()
    # # Определяем путь к папке, в которой хотим сохранить изображение
    # save_path = 'C:\\Users\\User\\Desktop\\Trading\\Fig\\'
    # # Указываем имя файла и его расширение
    # file_name = f'{string}.png'
    # # Полный путь к файлу
    # full_path = save_path + file_name
    # # Сохраняем график
    # plt.savefig(full_path)

def plot_profit(profit_list):
    plt.figure(figsize=(10, 4))
    x_values = range(1, len(profit_list) + 1)
    y_values = profit_list
    # Логарифмическая шкала
    if log == True:
        plt.yscale('log')
    # Построение графика
    plt.plot(x_values, y_values)  # График с точками marker='o'
    plt.xlabel('Сделки, n')  # Подпись оси x
    plt.ylabel('Прибыль, %')  # Подпись оси y
    plt.title('График прибыли, %')  # Заголовок графика
    plt.grid(True)  # Отображение сетки на графике
    plt.show()

def PlotDot2D(data1, data2, colors):
    # Используем plt.scatter() для построения точек
    plt.scatter(data1, data2, c=colors)

    # Добавляем подписи к осям
    plt.xlabel('data1')
    plt.ylabel('data2')

    # Добавляем заголовок графика
    plt.title('График с точками')

    # Отображаем график
    plt.show()


def func2D(becground, Strategy):
    x_start, x_fin, x_step, y_start, y_fin, y_num = becground
    func2D = []
    # for i in range(x_start, x_fin, x_step): # n
    for i in np.linspace(y_start, y_fin, num=y_num):
        print(i)
        list_percent_open = []
        percent_open = i #
        for j in range(x_start, x_fin+1, x_step): # percent_open
        # for j in np.linspace(y_start, y_fin, num=y_num):
            n = j #
            profit = round(float(Strategy(n, percent_open)[1]), 2) # [1]
            list_percent_open.append(profit)
        func2D.append(list_percent_open)
    return func2D

def PlotColorMesh(becground, func2D):
    x_start, x_fin, x_step, y_start, y_fin, y_step = becground
    # x_data = list(range(x_start, x_fin, x_step))
    # y_data = list(range(y_start, y_fin, y_step))
    x_data = np.arange(x_start, x_fin, x_step)  # len = 11
    y_data = np.arange(y_start, y_fin, y_step)  # len = 7
    x_data, y_data = np.meshgrid(x_data, y_data)
    z_data = np.array(func2D)

    fig, ax = plt.subplots()
    cax = ax.pcolormesh(x_data, y_data, z_data, cmap='inferno')  # Используем цветовую карту 'viridis', 'inferno'
    cbar = plt.colorbar(cax)
    # Настройка меток осей
    ax.set_xlabel('n свечей')
    ax.set_ylabel('percent')
    # Отображение графика
    plt.show()

def PlotColorMesh_v2(becground_config, func2D, x_label, y_label):
    x_start, x_fin, x_step, y_start, y_fin, y_num = becground_config

    x_data = np.arange(x_start, x_fin+1, x_step)
    y_data = np.linspace(y_start, y_fin, num=y_num)

    # print(f"x_data_grid: \n {x_data}")
    # print(f"y_data_grid: \n {y_data}")

    x_data_grid, y_data_grid = np.meshgrid(x_data, y_data)
    z_data_grid = np.array(func2D)

    z_min, z_max = -abs(z_data_grid).max(), abs(z_data_grid).max()    # -100, 100

    fig, ax = plt.subplots()
    #cmap = plt.get_cmap('RdYlGn')   #'RdYlGn'
    mesh = plt.pcolormesh(x_data_grid, y_data_grid, z_data_grid,
                          cmap='RdYlGn', shading='nearest', antialiased=True,
                          vmin=z_min, vmax=z_max)

    # print(f"x_data_grid: \n {x_data_grid}")
    # print(f"y_data_grid: \n {y_data_grid}")
    # print(f"z_data_grid: \n {z_data_grid}")

    plt.colorbar(mappable=mesh, ax=ax)

    # Set the x- and y-axis major ticks to be at integer values
    ax.xaxis.set_major_locator(plt.MultipleLocator(2))
    ax.yaxis.set_major_locator(plt.MultipleLocator(2))

    # Customize labels of the plot
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Show the plot
    plt.show()