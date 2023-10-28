from selenium import webdriver
from send_email import send_email
from urllib.parse import urljoin
import re
import os


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')#无头，就是不显示浏览器界面
chrome_options.add_argument('--no-sandbox')#禁用沙盒
chrome_options.add_argument('--disable-dev-shm-usage')#禁用/dev/shm使用

chrome_driver_path = '/usr/local/bin/chromedriver'  # 路径为实际的 ChromeDriver 路径
driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)

root_url = 'https://app.mokahr.com'

# 打开英伟达JD网页
driver.get('https://app.mokahr.com/campus-recruitment/nvidia/47111#/jobs?page=1&anchorName=jobsList&commitment%5B0%5D=%E5%AE%9E%E4%B9%A0&location%5B0%5D=%E4%B8%8A%E6%B5%B7%E5%B8%82')

# 等待JavaScript执行并生成内容
driver.implicitly_wait(10)  # 这会让WebDriver等待10秒，或者你可以设置更长的时间

# 假设您的字符串为 result_str
result_str = '<span style="margin-right: 8px;"><span> 14 </span>结果</span>'

# 使用正则表达式提取数字
result = re.findall(r'\d+', result_str)

element_details = driver.find_elements_by_class_name('title-u2qk9xX9Ie')
if len(element_details) == int(result[-1]) :
    print('职位数匹配')
    print('职位数为：', result[-1])
else:
    # 容错处理
    print('职位数不匹配')
    print('职位数为：', result[-1])
    print('职位详情数为：', len(element_details))
    print('职位数为：', len(element_details))
    send_email('职位数不匹配 出现问题', '职位数为：{}'.format(result[-1]), '', '', '')      
    driver.quit()
print('-----------------------------')

details_text = '\n'.join([element_detail.text for element_detail in element_details])

# 获取职位详情链接
job_elements = driver.find_elements_by_class_name('link-txmgVOCVz9')
details_dict = {}

for job_element, element_detail in zip(job_elements, element_details):
    link = urljoin(root_url, job_element.get_attribute('href'))
    job_title = element_detail.text
    details_dict[job_title] = link
# 获取当前脚本的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构造 job_details.txt 的绝对路径
job_details_path = os.path.join(script_dir, 'job_details.txt')
if os.path.exists(job_details_path):
    with open(job_details_path, 'r') as f:
        old_job_details = f.read()
    if old_job_details != details_text:
        # 假设 old_jobs 是之前保存的职位列表，new_jobs 是新获取的职位列表
        old_jobs = set(old_job_details.split('\n'))
        new_jobs = set(details_text.split('\n'))

        # 找到新增的职位
        added_jobs = new_jobs - old_jobs
        for job in added_jobs:
            print('-----------------------------')
            print('新增职位：')
            print(job)
            print('职位详情链接：')
            print(details_dict[job])
        if added_jobs:
            #将新的职位详情保存到文件中
            with open(job_details_path, 'w') as f:
                f.write(details_text)
            # 创建邮件的内容，其中包括新增职位的标题和链接
            email_content = ''
            for job in added_jobs:
                link = details_dict[job]
                email_content+=f'{job}: {link}\n'
            # email_content = '\n'.join([f'{job}: {link}' for job, link in added_jobs.items()])
            # 插入到邮件内容中
            send_email(
                '有职位更新', 
                '新增职位: \n{}\n新增职位数为：{}'.format(email_content, len(added_jobs)), 
                '', 
                '', 
                ''
            )
                # 打印出新增的职位

else:
    #将新的职位详情保存到文件中
    with open(job_details_path, 'w') as f:
        f.write(details_text)
    print('-----------------------------')

# 退出驱动
driver.quit()
