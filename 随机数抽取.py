import PySimpleGUI as sg
import random
import os

def main():
    # 设置主题为红色
    sg.theme('Reds')

    # 定义窗口布局
    layout = [
        [sg.Text('请输入数字区间：', background_color='red', text_color='gold', font=('Helvetica', 14))],
        [
            sg.Text('最小值：', background_color='red', text_color='gold'),
            sg.InputText(key='min_value', size=(10, 1), background_color='red', text_color='gold'),
            sg.Text('最大值：', background_color='red', text_color='gold'),
            sg.InputText(key='max_value', size=(10, 1), background_color='red', text_color='gold'),
        ],
        [
            sg.Text('随机数数量：', background_color='red', text_color='gold'),
            sg.InputText(key='num_count', size=(5, 1), background_color='red', text_color='gold'),
            sg.Button('抽取随机数', button_color=('gold', 'red')),
            sg.Button('退出', button_color=('gold', 'red'))
        ],
        [sg.Image('D:\\1.png', size=(200, 200), pad=(155, 10), background_color='red')],
        [sg.Text('     公平公正', text_color='gold', font=('隶书', 40), background_color='red',
                 justification='center')],
        [sg.Text('', key='result', text_color='gold', font=('Helvetica', 75), background_color='red')],
    ]

    # 创建窗口，设置尺寸和可调整大小
    window = sg.Window('随机抽取应用', layout, background_color='red', size=(500, 600), resizable=True, finalize=True)

    # 从文件中读取之前保存的结果
    previous_results = load_previous_results()

    while True:
        event, values = window.read()

        # 处理关闭窗口或点击退出按钮
        if event in (sg.WIN_CLOSED, '退出'):
            break

        if event == '抽取随机数':
            try:
                # 获取并验证输入的最小值和最大值
                min_value = int(values['min_value'])
                max_value = int(values['max_value'])
                validate_range(min_value, max_value)

                # 获取用户输入的随机数数量
                num_to_draw = int(values['num_count'])
                if num_to_draw <= 0:
                    raise ValueError("请至少抽取 1 个随机数")

                result = draw_numbers(min_value, max_value, previous_results, num_to_draw)

                # 更新显示结果
                window['result'].update(result)

                    # 更新排除的结果
                previous_results.update(map(int, result.split(', ')))

            except ValueError as e:
                error_message = str(e)
                if error_message == "可抽取的数字不足，请调整区间或排除的数字":
                    delete_result_file()
                    sg.popup_error('输入错误: 请重新打开软件以删除抽取记录')
                else:
                    sg.popup_error(f'输入错误: {error_message}')
                    delete_result_file()

    window.close()

# 下面的辅助函数不变
def validate_range(min_value, max_value):
    """验证输入的范围"""
    if min_value >= max_value:
        raise ValueError("最小值必须小于最大值")
    if max_value - min_value + 1 < 1:
        raise ValueError("区间内至少需要 1 个数")

def draw_numbers(min_value, max_value, excluded, num_to_draw):
    """从指定范围内随机抽取指定数量的数字，同时排除之前的结果"""
    numbers = [num for num in range(min_value, max_value + 1) if num not in excluded]
    if len(numbers) < num_to_draw:
        raise ValueError("可抽取的数字不足，请调整区间或重新打开软件以删除抽取记录")
    random.shuffle(numbers)
    selected_numbers = numbers[:num_to_draw]
    return ', '.join(map(str, selected_numbers))

def save_result(result):
    """将结果保存到文本文件（追加模式）"""
    with open('抽取记录.txt', 'a', encoding='utf-8') as f:
        f.write(result + '\n')  # 每次写入新结果后换行

def load_previous_results():
    """从文件中加载之前保存的结果并返回一个集合"""
    previous_results = set()
    if os.path.isfile('抽取记录.txt'):
        with open('抽取记录.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    previous_results.update(map(int, line.strip().split(', ')))
    return previous_results

def delete_result_file():
    """删除结果文件"""
    if os.path.isfile('抽取记录.txt'):
        os.remove('抽取记录.txt')

if __name__ == '__main__':
    main()