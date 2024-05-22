import subprocess
import os
"""
不需要使用类，如果路径不对，直接先设置环境变量再调用函数即可
"""
def add_nircmd_to_path(nircmd_path):
    path = os.environ.get('PATH', '')   
    if nircmd_path not in path:
        os.environ['PATH'] = path + ';' + nircmd_path
# 调用函数添加nircmd目录到环境变量

add_nircmd_to_path(r'D:\Soft\Tools\nircmd')


def call_nircmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"调用{cmd}成功")
    except subprocess.CalledProcessError as e:
        print("调用nircmd.exe失败:", e)

def speak_text(text):
    cmd = f'nircmd speak text "{text}"'
    call_nircmd(cmd)
        
def close_monitor():
    cmd = f'nircmd monitor off"'
    call_nircmd(cmd)

def increase_volume():
    cmd = f'nircmd changesysvolume 2000'
    call_nircmd(cmd)

def decrease_volume():
    cmd = f'nircmd changesysvolume -2000'
    call_nircmd(cmd)
        
def set_window_as_top(title):
    cmd = f'nircmd win settopmost title "{title}" 1'
    call_nircmd(cmd)
        
def set_window_not_top(title):
    cmd = f'nircmd win settopmost title "{title}" 0'
    call_nircmd(cmd)
        

        
def kill_process(exe_name):
    cmd = f'nircmd killprocess {exe_name}'
    call_nircmd(cmd)
        
def restart_serivce(serivce_name):
    cmd = f'nircmd restartservice {serivce_name}'
    call_nircmd(cmd)

if __name__ == '__main__':
    kill_process('notepad.exe')