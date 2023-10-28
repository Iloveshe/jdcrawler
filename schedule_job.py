import schedule
import time
import subprocess
import sys
from datetime import datetime

def job():
    # 保存旧的 stdout
    old_stdout = sys.stdout
    
    # 打开一个文件用于追加输出
    output_file = open("output.txt", "a")


    # 将 sys.stdout 重定向到我们的文件
    sys.stdout = output_file
    result = subprocess.run(["python3", "jdcrawler/nvidia_jobs_scraper.py"], capture_output=True, text=True)
    now = datetime.now()
    print("当前时间：", now)
    if result.returncode != 0:
        print("脚本执行错误:")
        print(result.stderr)
    else:
        print("脚本成功执行，输出为:")
        print(result.stdout)
    # 恢复旧的 stdout
    sys.stdout = old_stdout

    # 关闭文件
    output_file.close()
# 每天9点执行job函数
# schedule.every().day.at("09:00").do(job)
# 每5分钟执行一次job函数
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)