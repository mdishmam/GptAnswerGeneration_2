import random
import sys
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# try:
from webdriver_manager.chrome import ChromeDriverManager
# except:
#     os.systemm('pip install webdriver-manager==3.8.3')
#     from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# keywords = ['best budget app\n']
# keywords = ['why is my airbrush not spraying paint', 'how to get paint off of car window', 'why are picasso paintings so expensive', 'is krylon spray paint safe for babies', 'what is monotone paint', 'how to keep spray paints from rubbing off', 'nippon paint vs dulux', 'how to sign acrylic paintings', 'how much does it cost to paint a chevy tahoe', 'is testor enamel paint toxic']
# limit = 20


def search_with_keyword(keyword, limit):
    root_start_time = time.time()
    try:
        options = Options()
        options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    except Exception as e:
        sys.exit(e)

# for keyword in keywords:
    keyword = keyword + '\n'
    browser.get('https://www.google.com/')
    print('Waiting implicitly...')
    browser.implicitly_wait(10)

    browser.find_element(by=By.CSS_SELECTOR, value='body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input').send_keys(keyword)

    tableAnswers = browser.find_elements(by=By.CLASS_NAME, value='wWOJcd')


    index = 0
    # for index, val in enumerate(tableAnswers):
    q_s = []
    ans_s = []
    while index<limit:
        try:
            print(f'Now building article outline = {index+1}')
            # ic = input(f"Click in {tableAnswers[index].text}?")
            #
            # if ic == '-1':
            #     break
            print(f"Click in {tableAnswers[index].text}?")
            time.sleep(random.randint(1, 3))
            tmp_q = tableAnswers[index].text
            # q_s.append(tableAnswers[index].text)
            tableAnswers[index].click()
            ans = browser.find_elements(by=By.CLASS_NAME, value='ymu2Hb')[index].text
            try:
                ans_splitted = ans.split('\n\n')
                ans = ''.join(ans_splitted[:-1])

                ans_splitted = ans.split('.')
                if len(ans_splitted[-1]) <= 13:
                    ans = ''.join(ans_splitted[:-1])
                    ans += '.'
                else:
                    ans = ''.join(ans_splitted)

                ans_splitted = ans.split('\n')
                if len(ans_splitted[0]) <= 5 and len(ans_splitted[1]) <= 5:
                    ans = ''.join(ans_splitted[2:])
                elif len(ans_splitted[0]) <= 5:
                    ans = ''.join(ans_splitted[1:])
                else:
                    ans = ''.join(ans_splitted)
            except:
                pass
            print(ans)
            if 'youtube.com' in ans:
                index += 1
                limit += 1
                continue
            # if ans.strip() == '':
            #     continue
            q_s.append(tmp_q)
            ans_s.append(ans)
            # input(f"Again click in {tableAnswers[index].text}?")
            print(f"Again click in {tableAnswers[index].text}?")
            time.sleep(random.randint(1, 3))
            tableAnswers[index].click()
            tableAnswers = browser.find_elements(by=By.CLASS_NAME, value='wWOJcd')

            # print(f'Now building article outline = {len(tableAnswers)}')
            index += 1
        except:
            break
    # with open(f'{keyword}.txt','w', encoding='utf-8') as output_file:
    #     all_text = ''
    #     for index,qa in enumerate(zip(q_s, ans_s)):
    #         all_text += f'Q{index}: {qa[0]} \n\nA{index}: {qa[1]}\n\n\n'
    #     output_file.write(all_text)

    # print(tableAnswers)
    browser.close()
    # print("--- %s seconds ---" % (time.time() - root_start_time))
    return q_s, ans_s, (time.time() - root_start_time)
# input()
# while(1):
#     table = table.next
#     print(table)
#     input()

def search_with_keyword_manual(keyword, limit):
    root_start_time = time.time()
    try:
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    except Exception as e:
        sys.exit(e)

# for keyword in keywords:
    keyword = keyword + '\n'
    browser.get('https://www.google.com/')
    print('Waiting implicitly...')
    browser.implicitly_wait(10)

    browser.find_element(by=By.CSS_SELECTOR, value='body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input').send_keys(keyword)

    tableAnswers = browser.find_elements(by=By.CLASS_NAME, value='wWOJcd')


    index = 0
    # for index, val in enumerate(tableAnswers):
    q_s = []
    ans_s = []
    while index<limit:
        try:
            # ic = input(f"Click in {tableAnswers[index].text}?")
            #
            # if ic == '-1':
            #     break
            input(f"Click in {tableAnswers[index].text}?")
            # print(f"Click in {tableAnswers[index].text}?")
            time.sleep(random.randint(1, 3))
            tmp_q = tableAnswers[index].text
            # q_s.append(tableAnswers[index].text)
            tableAnswers[index].click()
            ans = browser.find_elements(by=By.CLASS_NAME, value='ymu2Hb')[index].text
            # try:
            #     ans_splitted = ans.split('\n\n')
            #     ans = ''.join(ans_splitted[:-1])
            # except:
            #     pass
            print(ans)
            if 'youtube.com' in ans:
                continue
            # if ans.strip() == '':
            #     continue
            q_s.append(tmp_q)
            ans_s.append(ans)
            input(f"Again click in {tableAnswers[index].text}?")
            # print(f"Again click in {tableAnswers[index].text}?")
            time.sleep(random.randint(1, 3))
            tableAnswers[index].click()
            tableAnswers = browser.find_elements(by=By.CLASS_NAME, value='wWOJcd')
            print(f'Now building article outline  = {len(tableAnswers)}')
            index += 1
        except:
            break
    # with open(f'{keyword}.txt','w', encoding='utf-8') as output_file:
    #     all_text = ''
    #     for index,qa in enumerate(zip(q_s, ans_s)):
    #         all_text += f'Q{index}: {qa[0]} \n\nA{index}: {qa[1]}\n\n\n'
    #     output_file.write(all_text)

    # print(tableAnswers)
    browser.close()
    # print("--- %s seconds ---" % (time.time() - root_start_time))
    return q_s, ans_s, (time.time() - root_start_time)


if __name__ == '__main__':
    search_with_keyword_manual('pva vs acrylic paint youtube', 20)