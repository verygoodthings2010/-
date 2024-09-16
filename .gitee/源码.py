import PySimpleGUI as sg
import random

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
        [sg.Button('开始抽取', button_color=('gold', 'red')), sg.Button('退出', button_color=('gold', 'red'))],
        [sg.Image('D:\\1.png', size=(200, 200), pad=(155, 10), background_color='red')],
        [sg.Text('     公平公正', text_color='gold', font=('隶书', 40), background_color='red', justification='center')],
        [sg.Text('', key='result', text_color='gold', font=('Helvetica', 75), background_color='red')],
    ]

    # 创建窗口，设置尺寸和可调整大小
    window = sg.Window('随机抽取应用', layout, background_color='red', size=(500, 600), resizable=True, finalize=True)

    while True:
        event, values = window.read()

        # 处理关闭窗口或点击退出按钮
        if event in (sg.WIN_CLOSED, '退出'):
            break

        if event == '开始抽取':
            try:
                # 获取并验证输入的最小值和最大值
                min_value = int(values['min_value'])
                max_value = int(values['max_value'])
                validate_range(min_value, max_value)

                # 抽取随机数字
                result = draw_numbers(min_value, max_value)
                window['result'].update(result)

            except ValueError as e:
                sg.popup_error(f'输入错误: {e}')

    window.close()

def validate_range(min_value, max_value):
    """验证输入的范围"""
    if min_value >= max_value:
        raise ValueError("最小值必须小于最大值")
    if max_value - min_value + 1 < 3:
        raise ValueError("区间内至少需要 3 个数")

def draw_numbers(min_value, max_value):
    """从指定范围内随机抽取三个数字"""
    numbers = list(range(min_value, max_value + 1))
    random.shuffle(numbers)
    selected_numbers = numbers[:3]
    return ', '.join(map(str, selected_numbers))

if __name__ == '__main__':
    main()