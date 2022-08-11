import pathlib
import os


def fill_sequence(input_path, keywords_list):
    for enu, kw in enumerate(keywords_list):
        # num_kw += 1
        print(f'Fill sequence {enu + 1}/{(len(keywords_list))} keyword:', kw)
        txtdir_path = input_path + '/' + kw
        all_txt_file = list(pathlib.Path(txtdir_path).glob('**/*.txt'))
        for i in range(len(all_txt_file)):
            input_file = txtdir_path + f'/{kw}_{i + 1}.txt'
            if not os.path.exists(input_file):
                for add in range(2, 50):
                    next_file = txtdir_path + f'/{kw}_{i + add}.txt'
                    if os.path.exists(next_file):
                        os.rename(next_file, input_file)
                        break


if __name__ == '__main__':
    input_path = ""
    keywords_list = ['']
    fill_sequence(input_path, keywords_list)
