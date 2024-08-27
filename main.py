import csv
import glob
import os
import random
import shutil
import time
from py3pin.Pinterest import Pinterest
from constants import *


def check_csv_delimiter(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()

        if ',' in first_line:
            return ','
        elif ';' in first_line:
            return ';'
        else:
            return ','


def open_accounts():
    file_path = ASSETS / 'accounts.csv'
    delimiter = check_csv_delimiter(file_path)

    with open(file_path, "r", newline="") as data:
        heading = next(data)
        reader = csv.reader(data, delimiter=delimiter)

        accounts = []
        for row in reader:
            if row[0] == '1':
                accounts.append(row)
            continue

        return accounts


def pin(accounts, pins, timeout):
    for account in accounts:
        email = account[1]
        password = account[2]
        username = account[3]
        proxy = account[4]
        folder = account[5]
        link = account[6]

        print(f'Working with account {username}')

        if not proxy:
            proxy = None
            proxy_dict = None
        else:
            proxy_dict = {f'{proxy.split("://")[0]}': proxy}

        pinterest = Pinterest(
            email=email,
            password=password,
            username=username,
            cred_root='cred_root',
            proxies=proxy_dict
        )

        cookies_path = BASE_DIR / 'cred_root' / username
        if not os.path.exists(cookies_path):
            pinterest.login(proxy=proxy)

        boards = pinterest.boards(username=username)

        print(f'Found {len(boards)} boards\n')

        images_path = READY / folder / 'images' / '*.png'
        images = glob.glob(str(images_path))
        random.shuffle(images)

        counter = 0
        pin_counter = 1
        for image in images[:pins]:
            if not image:
                print('No images in the folder')
                break

            if not boards:
                print('No boards for pins')
                break

            title_split_png = image.split('/')[-1].replace('.png', '')
            title = title_split_png.split('[[')[0]

            board_name_full = title_split_png.split('[[')[1].replace(']]', '')

            if ':' in board_name_full:
                board_name = board_name_full.split(':')[0]
            else:
                board_name = board_name_full

            description = f'🔥{board_name_full}. {title}'

            boards_ids = []
            for board in boards:
                if board['name'] == board_name:
                    boards_ids.append(board['id'])
                else:
                    continue

            if not boards_ids:
                print(f'No board named "{board_name}"')
                break

            print(f'Found board named "{board_name}"')

            board_id = boards_ids[0]

            try:
                pinterest.upload_pin(board_id=board_id,
                              image_file=image,
                              description=description,
                              title=f'🔥{title}',
                              link=link)

                print(f'{pin_counter} Pin created')

                move_dir = READY / folder / 'pinned'
                move_dir.mkdir(exist_ok=True)
                shutil.move(image, move_dir)

                pin_counter += 1
            except Exception as e:
                print(f'An error occurred while creating a pin'
                      f'Error: {e}'
                      f'Check if a board named "{board_name}" has been created.')

            counter += 1
            if not counter == pins:
                time_out = random.randint(timeout[0], timeout[1])
                print(f'Timeout {time_out} seconds...\n')
                time.sleep(time_out)
            else:
                print('\nDone!\n')


if __name__ == '__main__':
    pins = 1
    timeout = (3, 10)

    accounts = open_accounts()
    if not accounts:
        print('No accounts in work')
    else:
        print(f'{len(accounts)} accounts in work')
        pin(accounts, pins, timeout)

