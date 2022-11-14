import os.path
import random
import sys

import requests

from paa_selenium import search_with_keyword
from gpt_modules import write_intro, rewrite_text, write_conclusion
from wp_module import upload_image, post_in_wp
from amazon_product import get_product

from youtubesearchpython import VideosSearch
from pexelsapi.pexels import Pexels
pexel = Pexels('563492ad6f917000010000010fcfc730583c45578463dc750fd52a66')

html_template_1 = """<h2>##keyword_main##</h2>
##intro_main##
"""

html_template_2 = """
"""

html_q_a_template = """<##h2or3##> ##keyword## </##h2or3##>
##answer##"""

# tmp text file names
intro_file = 'intro.txt'
first_3_qa = 'first_3.txt'
image1 = 'image1.jpg'
second_2_qa = 'second_2.txt'
video = ''
amazon_product = ''
third_3_qa = 'third_3.txt'
image2 = 'image2.jpg'
last_2_qa = 'last_2.txt'

featured_image = 'featured_image.jpg'

def image_downloader(keyword):
    keyword_ = keyword.replace('?', '')
    pexel = Pexels('563492ad6f917000010000010fcfc730583c45578463dc750fd52a66')
    search_photos = pexel.search_photos(query=keyword, orientation='landscape', size='', color='',
                                        locale='', page=1, per_page=7)
    image_url1 = search_photos.get('photos')[random.randint(1,5)].get('src').get('large')
    image_url2 = search_photos.get('photos')[random.randint(1,5)].get('src').get('large')
    image_url3 = search_photos.get('photos')[random.randint(1,5)].get('src').get('large')
    # try:
    #     image_url = outputs.get('thumbnails')[1].get('url')
    # except:
    #     image_url = outputs.get('thumbnails')[0].get('url')
    fet_img_data = requests.get(image_url1).content
    with open(f'tmps\\{keyword_}\\{featured_image}', 'wb') as handler:
        handler.write(fet_img_data)
    feture_image_id, _ = upload_image(f'tmps\\{keyword_}\\{featured_image}', f'{keyword_}_1.jpg')

    img_data1 = requests.get(image_url2).content
    with open(f'tmps\\{keyword_}\\{image1}', 'wb') as handler:
        handler.write(img_data1)
    _, image1_link = upload_image(f'tmps\\{keyword_}\\{image1}', f'{keyword_}_2.jpg')

    img_data2 = requests.get(image_url3).content
    with open(f'tmps\\{keyword_}\\{image2}', 'wb') as handler:
        handler.write(img_data2)
    _, image2_link = upload_image(f'tmps\\{keyword_}\\{image2}', f'{keyword_}_3.jpg')

    return feture_image_id, image1_link, image2_link

def video_get(keyword):
    videosSearch = VideosSearch(keyword, limit=1)

    outputs = videosSearch.result().get('result')[0]
    embade_code = 'https://www.youtube.com/embed/'
    video_link = embade_code + outputs.get('id')

    iframe = '<iframe width="560" height="315" src="##videourl##" title="YouTube video player" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    iframe = iframe.replace('##videourl##', video_link)
    return iframe

def main():
    # Bring paa
    number_of_questions = 20
    category = input("Enter category: ")
    number_of_heads = int(input("Enter number of headings [Must be larger than 8]: "))
    while number_of_heads <= 8:
        number_of_heads = int(input("Must be larger than 8. \nEnter number of headings: "))
    number_of_questions = number_of_heads * 2 + 2
    amazon_choise = input("Show amazon product? [default is 'yes', press anything to not show]")
    image_choise = input("Show images? [default is 'yes', press anything to not show]")
    re_run_choice = input("If failed re-run automatically? [default is 'yes', press anything to not show] : ")
    keywords_file = open('keywords.txt', 'r')
    keywords_all = keywords_file.readlines()
    keywords_file.close()
    keyword_filter = lambda keyword: keyword.strip() if keyword.strip()[-1] == '?' else keyword.strip() + '?'
    keywords_all = list(map(keyword_filter, keywords_all))
    if '' in keywords_all:
        keywords_all.remove('')
    print(keywords_all)

    run_main_direct_paa(keywords_all, number_of_questions, image_choise, amazon_choise, category)

    with open(f'logs\\keywords_unsuccessful_direct.txt', 'r', encoding='utf-8') as fl:
        keywords_all = fl.read()

    while keywords_all.strip() != '':
        failed_keyword = keywords_all.strip().split("\n")
        if re_run_choice != '':
            breaking_param = input(f'There are {len(failed_keyword)} failed keyword(s). Want to re-run for these?[default is \'yes\', press anything to not show]')
            if breaking_param.strip() != '':
                break
        keywords_all = failed_keyword
        run_main_direct_paa(keywords_all, number_of_questions, image_choise, amazon_choise, category)

        with open(f'logs\\keywords_unsuccessful_direct.txt', 'r', encoding='utf-8') as fl:
            keywords_all = fl.read()


def run_main_direct_paa(keywords_all, number_of_questions, image_choise, amazon_choise, category):
    with open(f'logs\\keywords_unsuccessful_direct.txt', 'w', encoding='utf-8') as fl:
        fl.write('')
    with open(f'logs\\error_log_direct.txt', 'w', encoding='utf-8') as fl:
        fl.write('')

    for index, keyword in enumerate(keywords_all):
        try:
            keyword_ = keyword.replace('?', '')
            if not os.path.isdir(f'tmps\\"{keyword}"'):
                os.system(f'mkdir tmps\\"{keyword_}"')
            questions, answers, time_to_bring = search_with_keyword(keyword, limit=number_of_questions)
            #    intro got for this keyword
            if image_choise == '':
                fet_image_id, image1_link, image2_link = image_downloader(keyword)
            intro = answers[0] + '<br>' + answers [1]
            tmp_html = html_template_1.replace('##keyword_main##', '')
            tmp_html = tmp_html.replace('##intro_main##', intro)
            # get product
            if amazon_choise == '':
                iframe = get_product(keyword_)
                tmp_html += f"<br>{iframe}"
            # with open(f'tmps\\{keyword_}\\{intro_file}', 'w') as fl:
            #     fl.write(tmp_html)

            intro_html = tmp_html
            #     first 3
            tmp_frst3 = ''
            for index_1, i in enumerate(range(2, 6, 2)):
                h2or3 = 'h3'
                question = questions[i].replace('?','')
                if index_1 % 2 == 0:
                    h2or3 = 'h2'
                    question = questions[i]
                answer = answers[i] + '<br><br>' + answers[i + 1]

                tmp_html = html_q_a_template.replace('##h2or3##', h2or3)
                tmp_html = tmp_html.replace('##keyword##', question)
                tmp_html = tmp_html.replace('##answer##', answer)

                tmp_frst3 += tmp_html
            # with open(f'tmps\\{keyword_}\\{first_3_qa}', 'w', encoding='utf-8') as fl:
            #     fl.write(tmp_frst3)

            # get video
            video_link = video_get(keyword)

            #     second 2
            tmp_snd2 = ''
            for index_1, i in enumerate(range(6, 10, 2)):
                h2or3 = 'h3'
                question = questions[i].replace('?', '')
                if index_1 % 2 == 0:
                    h2or3 = 'h2'
                    question = questions[i]
                answer = answers[i] + '<br><br>' + answers[i + 1]

                tmp_html = html_q_a_template.replace('##h2or3##', h2or3)
                tmp_html = tmp_html.replace('##keyword##', question)
                tmp_html = tmp_html.replace('##answer##', answer)

                tmp_snd2 += tmp_html
            tmp_snd2 += f"<br>{video_link}"

            # with open(f'tmps\\{keyword_}\\{second_2_qa}', 'w', encoding='utf-8') as fl:
            #     fl.write(tmp_snd2)

            #     third 3
            tmp_thrd3 = ''
            for index_1, i in enumerate(range(10, 16, 2)):
                h2or3 = 'h3'
                question = questions[i].replace('?', '')
                if index_1 % 2 == 0:
                    h2or3 = 'h2'
                    question = questions[i]
                answer = answers[i] + '<br><br>' + answers[i + 1]

                tmp_html = html_q_a_template.replace('##h2or3##', h2or3)
                tmp_html = tmp_html.replace('##keyword##', question)
                tmp_html = tmp_html.replace('##answer##', answer)

                tmp_thrd3 += tmp_html
            # with open(f'tmps\\{keyword_}\\{third_3_qa}', 'w', encoding='utf-8') as fl:
            #     fl.write(tmp_thrd3)

            #     last 2
            tmp_lst2 = ''
            for index_1, i in enumerate(range(16, number_of_questions, 2)):
                # h2or3 = 'h3'
                question = questions[i].replace('?', '')
                # if index_1 % 2 == 0:
                #     h2or3 = 'h2'
                #     question = questions[i]
                # answer = rewrite_text(answers[i], temp=temperature) + '<br><br>' + rewrite_text(answers[i + 1], temp=temperature)
                if i == number_of_questions-2:
                    answer = answers[i] + '<br><br>' + answers[i + 1]
                    tmp_html = html_q_a_template.replace('##h2or3##', 'h2')
                    conclusions = ['Conclusion' , 'Warp Up' , 'Final Words']
                    tmp_html = tmp_html.replace('##keyword##', random.choice(conclusions))
                    tmp_html = tmp_html.replace('##answer##', answer)
                else:
                    answer = answers[i] + '<br><br>' + answers[i + 1]
                    tmp_html = html_q_a_template.replace('##h2or3##', 'h3')
                    tmp_html = tmp_html.replace('##keyword##', question)
                    tmp_html = tmp_html.replace('##answer##', answer)

                tmp_lst2 += tmp_html
            # with open(f'tmps\\{keyword_}\\{last_2_qa}', 'w', encoding='utf-8') as fl:
            #     fl.write(tmp_lst2)

            if image_choise == '':
                all_post = intro_html + tmp_frst3
                all_post += f'<img src="{image1_link}" alt="{keyword_}_1">'
                all_post += tmp_snd2 + tmp_thrd3
                all_post += f'<img src="{image2_link}" alt="{keyword_}_2">'
                all_post += tmp_lst2

                post_in_wp(title=keyword.capitalize(), body=all_post, thumbnail=fet_image_id, category=category)
            else:
                all_post = intro_html + tmp_frst3
                # all_post += f'<img src="{image1_link}" alt="{keyword_}_1">'
                all_post += tmp_snd2 + tmp_thrd3
                # all_post += f'<img src="{image2_link}" alt="{keyword_}_2">'
                all_post += tmp_lst2

                post_in_wp(title=keyword.capitalize(), body=all_post, category=category)

        except Exception as e:
            print(f'Error: {e}')
            with open(f'logs\\keywords_unsuccessful_direct.txt', 'a', encoding='utf-8') as fl:
                fl.write(keyword_ + '\n')

            with open(f'logs\\error_log_direct.txt', 'a', encoding='utf-8') as fl:
                txt = '#' * 50
                txt = txt + '\n' + keyword_ + '\n\n'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                txt = txt + str(e) + '\n'
                txt = txt + f'{exc_type},\n {fname},\n {exc_tb.tb_lineno}' + '\n\n\n'
                fl.write(txt)
            continue


if __name__ == '__main__':
    main()
    input('All process finished. Press enter to exit.')
