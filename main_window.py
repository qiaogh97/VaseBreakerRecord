# -*- coding: utf-8 -*-
import time
import win32process
import win32api
import ctypes
import tkinter as tk

from win32gui import FindWindow
from collections import OrderedDict
from win32con import PROCESS_ALL_ACCESS


# content_dict = {1:'植物', 2:'僵尸', 3:'阳光'}
plant_dict = {52:'双发射手', 17:'    窝瓜', 5:'寒冰射手', 0:'豌豆射手', 18:'三发射手', 4:'  土豆雷', 3:'    坚果', 25:'  灯笼草'}
zombie_dict = {0:'普通僵尸', 4:'铁桶僵尸', 15:'小丑僵尸', 23:'巨人僵尸'}

def find_window():
    hwnd = FindWindow(None, u"Plants vs. Zombies")
    if not hwnd == 0:
        return hwnd
    else:
        hwnd = FindWindow(None, u"植物大战僵尸中文版")
        if not hwnd == 0:
            return hwnd
        else:
            return 0

def get_procss_ID(address, bufflength):
    kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")
    hwnd = find_window()
    ReadProcessMemory = kernel32.ReadProcessMemory
    hpid, pid = win32process.GetWindowThreadProcessId(hwnd)
    hProcess = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    addr = ctypes.c_ulong()
    ReadProcessMemory(int(hProcess), address, ctypes.byref(addr), bufflength, None)
    win32api.CloseHandle(hProcess)
    return addr.value

def get_value(addr_list):
    value = 0
    for addr in addr_list:
        addr = value + addr
        value = get_procss_ID(addr, 4)
    return value

def show(plant_list, zombie_list, sun, plant_var_list, zombie_var_list, sun_var):
    plant_count_dict = OrderedDict({'双发射手': 0, '    窝瓜': 0, '寒冰射手': 0, '豌豆射手': 0, '三发射手': 0, '  土豆雷': 0, '    坚果': 0, '  灯笼草': 0})
    zombie_count_dict = OrderedDict({'普通僵尸': 0, '铁桶僵尸': 0, '小丑僵尸':0, '巨人僵尸': 0})
    for plant_id in plant_list:
        plant_name = plant_dict[plant_id]
        plant_count_dict[plant_name] += 1
    for zombie_id in zombie_list:
        zombie_name = zombie_dict[zombie_id]
        zombie_count_dict[zombie_name] += 1
    if sun>0:
        sun_var.set(f'    阳光：1')
    else:
        sun_var.set(f'    阳光：0')
        # print('还剩1个阳光')
    for i, plant in enumerate(plant_count_dict):
        num = plant_count_dict[plant]
        if num>0:
            plant_var_list[i].set(f'{plant}：{num}')
        else:
            plant_var_list[i].set(f'{plant}：0')
            # print(f'还剩{num}个{plant:4}')
    for i, zombie in enumerate(zombie_count_dict):
        num = zombie_count_dict[zombie]
        if num>0:
            zombie_var_list[i].set(f'{zombie}：{num}')
        else:
            zombie_var_list[i].set(f'{zombie}：0')
            # print(f'还剩{num}个{zombie:4}')


def start():
    hwnd = find_window()
    if hwnd==0:
        return
    global double_shooter_var, squash_var, ice_shooter_var, peashooter_var, trishooter_var, potato_var, nut_var, lantern_grass_var, normal_zombie_var, iron_zombie_var, clown_zombie_var, giant_zombie_var, sun_var
    plant_var_list = [double_shooter_var, squash_var, ice_shooter_var, peashooter_var, trishooter_var, potato_var, nut_var, lantern_grass_var]
    zombie_var_list = [normal_zombie_var, iron_zombie_var, clown_zombie_var, giant_zombie_var]

    cur_exist = 0
    last_exist = 35
    while True:
        zombie_list = []
        plant_list = []
        sun = 0
        for i in range(35):
            exist_addr = get_value([0x006A9EC0, 0x768, 0x11C])
            exist = get_procss_ID(exist_addr + i * 0xEC + 0xEA, 2)
            if not exist == 0:
                content_type = get_value([0x006A9EC0, 0x768, 0x11C, i * 0xEC + 0x44])
                if content_type == 1:
                    plant = get_value([0x006A9EC0, 0x768, 0x11C, i * 0xEC + 0x40])
                    plant_list.append(plant)
                elif content_type == 2:
                    zombie = get_value([0x006A9EC0, 0x768, 0x11C, i * 0xEC + 0x3C])
                    zombie_list.append(zombie)
                else:
                    sun = 1
                cur_exist += 1
        if not last_exist == cur_exist:
            last_exist = cur_exist
            show(plant_list, zombie_list, sun, plant_var_list, zombie_var_list, sun_var)
        time.sleep(0.1)
        window.update()

if __name__ == '__main__':
    window = tk.Tk()
    window.title('Vasebreaker Record')
    window.geometry('450x450')

    plant_label = tk.Label(window, text='植物', font=('宋体', 24), width=12, height=2).grid(row=1, column=1)
    zombie_label = tk.Label(window, text='僵尸', font=('宋体', 24), width=12, height=2).grid(row=1, column=2)
    double_shooter_num = 12

    double_shooter_var = tk.StringVar(value=f'双发射手：0')
    squash_var = tk.StringVar(value=f'    窝瓜：0')
    ice_shooter_var = tk.StringVar(value=f'寒冰射手：0')
    peashooter_var = tk.StringVar(value=f'豌豆射手：0')
    trishooter_var = tk.StringVar(value=f'三发射手：0')
    potato_var = tk.StringVar(value=f'  土豆雷：0')
    nut_var = tk.StringVar(value=f'    坚果：0')
    lantern_grass_var = tk.StringVar(value=f'  灯笼草：0')


    normal_zombie_var = tk.StringVar(value=f'普通僵尸：0')
    iron_zombie_var   = tk.StringVar(value=f'铁桶僵尸：0')
    clown_zombie_var  = tk.StringVar(value=f'小丑僵尸：0')
    giant_zombie_var  = tk.StringVar(value=f'巨人僵尸：0')
    sun_var = tk.StringVar(value=f'    阳光：0')

    double_shooter_label = tk.Label(window, textvariable=double_shooter_var, font=('宋体', 18), width=16, height=1).grid(row=2, column=1)
    squash_label = tk.Label(window, textvariable=squash_var, font=('宋体', 18), width=18, height=1).grid(row=3, column=1)
    ice_shooter_label = tk.Label(window, textvariable=ice_shooter_var, font=('宋体', 18), width=16, height=1).grid(row=4, column=1)
    peashooter_label = tk.Label(window, textvariable=peashooter_var, font=('宋体', 18), width=16, height=1).grid(row=5, column=1)
    trishooter_label = tk.Label(window, textvariable=trishooter_var, font=('宋体', 18), width=16, height=1).grid(row=6, column=1)
    potato_label = tk.Label(window, textvariable=potato_var, font=('宋体', 18), width=16, height=1).grid(row=7, column=1)
    nut_label = tk.Label(window, textvariable=nut_var, font=('宋体', 18), width=16, height=1).grid(row=8, column=1)
    lantern_grass_label = tk.Label(window, textvariable=lantern_grass_var, font=('宋体', 18), width=16, height=1).grid(row=9, column=1)

    normal_zombie_label = tk.Label(window, textvariable=normal_zombie_var, font=('宋体', 18), width=16, height=1).grid(row=2, column=2)
    iron_zombie_label = tk.Label(window, textvariable=iron_zombie_var, font=('宋体', 18), width=16, height=1).grid(row=3, column=2)
    clown_zombie_label = tk.Label(window, textvariable=clown_zombie_var, font=('宋体', 18), width=16, height=1).grid(row=4, column=2)
    giant_zombie_label = tk.Label(window, textvariable=giant_zombie_var, font=('宋体', 18), width=16, height=1).grid(row=5, column=2)

    other_label = tk.Label(window, text='其他', font=('宋体', 24), width=12, height=2).grid(row=6, column=2, rowspan=2)
    sun_label = tk.Label(window, textvariable=sun_var, font=('宋体', 18), width=16, height=1).grid(
        row=8, column=2)

    none_label = tk.Label(window, text='', font=('宋体', 18), width=12, height=1).grid(row=10, column=1)
    start_button = tk.Button(window, text=f'开始', font=('宋体', 20), bg='gray', width=8, height=1, command=start).grid(row=11, column=1, columnspan=2)
    window.mainloop()