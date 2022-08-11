import json
from tqdm import tqdm
import pathlib
import os
import math
import collections


def json2txt(input_path, keywords_list, output_path):
    print('Start to convert format from json to txt.')
    for kw in keywords_list:
        jsondir_path = input_path + '/' + kw
        all_json_file = list(pathlib.Path(jsondir_path).glob('**/*.json'))
        for i in tqdm(range(len(all_json_file)), desc=f'keyword:{kw}'):
            input_filename = jsondir_path + f'/{kw}_{i + 1}.json'
            news = json.load(open(input_filename, 'rb'))
            news_content = news['Content']

            # Replace ’\\n‘ or '\n' to '****'
            news_content = news_content.replace(r'\n\n', r'\n')
            news_content = news_content.replace('\\n', '****')
            news_content = news_content.replace(r'\n', '****')
            news_content = news_content.replace(r'  ', '')
            news_content = news_content.replace(r'   ', '')
            news_content = news_content.replace(r'********', '****')

            # Delete some useless information
            news_content = news_content.replace(r"Join us on Facebook.com/CNNOpinion.Read CNNOpinion's Flipboard "
                                                r"magazine.****", '')

            news_content = news_content.replace(r"Follow us on Twitter @CNNOpinion.****Join us on "
                                                r"Facebook.com/CNNOpinion. ****Read CNNOpinion's Flipboard "
                                                r"magazine.****", '')

            news_content = news_content + '\t' + kw + '\n'

            output_dir = output_path + '/' + kw
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            out_filename = output_dir + '/' + f'{kw}_{i + 1}.txt'

            with open(out_filename, 'w', encoding='utf-8') as f:
                f.write(news_content)
    print('Congratulations! You have successfully convert format from json to txt!')


def check_duplicates(input_path, keywords_list, output_path):
    global duplicates_list
    filename_list, news_content_list = [], []
    duplicates_num, duplicates_content, duplicates_filename_dict = [], [], []
    duplicates_filename, duplicates_list = '', ''
    file_content = {}

    print('\nNow, check duplicates.')
    for enu, kw in enumerate(keywords_list):
        # num_kw += 1
        print(f'check {enu + 1}/{(len(keywords_list))} keyword:', kw)
        jsondir_path = input_path + '/' + kw
        all_json_file = list(pathlib.Path(jsondir_path).glob('**/*.json'))
        for i in range(len(all_json_file)):
            input_filename = jsondir_path + f'/{kw}_{i + 1}.json'
            news = json.load(open(input_filename, 'rb'))
            filename = f'{kw}_{i + 1}'
            news_content = news['Content']

            filename_list.append(filename)
            news_content_list.append(news_content)

            filename_list_dict = {filename: news_content}
            file_content.update(filename_list_dict)

    content_list = dict(collections.Counter(news_content_list))
    print(f'Original file num: {len(news_content_list)}, after check duplicates file num: {len(content_list)}')

    # 'dict' or 'str'
    save_format = 'str'
    for key, value in content_list.items():
        if value > 1:
            # dict format
            if save_format == 'dict':
                duplicates_num.append(value)
                duplicates_content.append(key)
                for k, v in file_content.items():
                    if v == key:
                        duplicates_filename += k + ' | '
                duplicates_filename += '||'
                duplicates_filename = duplicates_filename.replace(r' | ||', '\n')
                for z in duplicates_filename.split('\n'):
                    if z.endswith('\n'):
                        duplicates_filename_dict.append(z)
                        duplicates_list = {
                            'duplicates_num': duplicates_num,
                            # 'duplicates_content': duplicates_content,
                            'duplicates_filename': duplicates_filename_dict
                        }
            # str format
            if save_format == 'str':
                duplicates_num = value
                duplicates_content = key
                for k, v in file_content.items():
                    if v == key:
                        duplicates_filename += k + ' | '

                duplicates_filename += '||'
                duplicates_filename = duplicates_filename.replace(r' | ||', '\n')

                duplicates_filename_str = 'Duplicates_num:' + f'{duplicates_num}' + '\n' + 'Duplicates_filename:' + duplicates_filename
                duplicates_list += duplicates_filename_str
                duplicates_filename = ''

    output_dir = output_path
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    out_filename = output_dir + '/' + 'duplicates_list.txt'

    file = open(out_filename, 'w', encoding='utf-8')
    if save_format == 'dict':
        file = open(out_filename, 'w', encoding='utf-8')
        json.dump(duplicates_list, file)
    if save_format == 'str':
        with open(out_filename, 'w', encoding='utf-8') as f:
            f.write(duplicates_list)
    print(f'Finish check duplicates, the results save path: {out_filename}')


def splice_txt(input_path, keywords_list, output_path, mode):
    global len_range
    for kw in keywords_list:
        jsondir_path = input_path + '/' + kw
        all_json_file = list(pathlib.Path(jsondir_path).glob('**/*.json'))

        if mode is 'train':
            length = int(math.ceil(len(all_json_file) * 0.7))
            len_range = range(length)
        elif mode is 'test':
            length = int(math.ceil(len(all_json_file) * 0.3))
            len_range = range(length)[::-1]

        splice_content = ''
        splice_label = ''

        for i in tqdm(len_range, desc=f'keyword:{kw}'):
            input_filename = jsondir_path + f'/{kw}_{i + 1}.json'
            news = json.load(open(input_filename, 'rb'))
            news_content = news['Content']

            # replace ’\\n‘ or '\n' to '****'
            news_content = news_content.replace(r'\n\n', r'\n')
            news_content = news_content.replace(r'\\n', '')
            news_content = news_content.replace(r'\n', '')

            splice_content += news_content + '\n'

            mode = mode.replace("'", '')
            splice_label = f'{i}' + '\r' + mode + '\r' + kw
            splice_label += splice_label + '\n'

        splice_content += splice_content + '\n'
        splice_label += splice_label + '\n'
        output_dir = output_path + '/' + 'dataset'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        out_filename = output_dir + '/' + mode + '_corpus.txt'
        out_label_file = output_dir + '/' + mode + '_label.txt'
        with open(out_filename, 'w', encoding='utf-8') as f:
            f.write(splice_content)
        with open(out_label_file, 'w', encoding='utf-8') as f:
            f.write(splice_label)


if __name__ == '__main__':
    input_path = ""
    output_path = ""
    keywords_list = ['']
    check_duplicates(input_path, keywords_list, output_path)
