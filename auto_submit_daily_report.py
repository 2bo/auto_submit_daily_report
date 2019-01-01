import subprocess
import json
import argparse
import pathlib
from colorama import Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime


def main():
    # コマンドライン引数の解析
    psr = argparse.ArgumentParser(description='Automatically submit daily report to report system')
    psr.add_argument('file', metavar='SUBMIT_FILE', help='plain text file of daily report to submit')
    psr.add_argument('name', metavar='YOUR_NAME', help='author name(must be registered on system)')
    psr.add_argument('-d', '--date', nargs=1, metavar='', help='submit date - format YYYYMMDD')
    args = psr.parse_args()

    if exists_file(args.file):
        # redpenによるチェックの実行
        num_of_error = redpen_check(args.file)

        if num_of_error > 0:
            print("redpen detected {0} errors.".format(num_of_error))

        # 投稿の実行確認
        answer = input('Are you sure to submit daily report? yes/no:')
        if answer.lower() not in ['yes', 'y']:
            print('canceled')
            return
        # 提出日の指定がない場合は本日付けで提出する
        if args.date is not None:
            try:
                date = datetime.strptime(args.date[0], "%Y%m%d")
            except ValueError:
                print("Not a valid date: '{0}'".format(args.date[0]))
                return
        else:
            date = datetime.now()

        # 投稿の実行
        submit_daily_report(args.file, args.name, date)

    else:
        print('File not found or is not file')
        return


def exists_file(file_path: str) -> bool:
    """
    ファイルが存在する場合Trueを返す。
    :param file_path:
    :return:
    """
    p = pathlib.Path(file_path)
    if not p.exists():
        return False
    if not p.is_file():
        return False
    return True


def redpen_check(file_path: str):
    """
    指定ファイルのredpenによるチェック結果を表示する。またエラー数を返す。
    :param file_path:
    :return:
    """
    # redpenの実行 結果をjson形式で取得
    cmd = ['redpen', '-c', 'conf/redpen-conf.xml', '-r', 'json2', file_path]
    # redpenの実行結果を直接表示させないためにPIPEを指定する
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # redpenの結果取得
    stdout = result.stdout.decode('utf8')

    num_of_errors = 0

    # 結果の表示
    if len(stdout) > 0:
        # jsonをdictionaryに変換
        json_dict = json.loads(stdout)
        errors = json_dict[0]['errors']

        if len(errors) < 1:
            return num_of_errors

        # エラーの内容表示とカウント
        for err in errors:
            print(str(err['position']['start']['line']) + ':' + err['sentence'])
            for err_detail in err['errors']:
                num_of_errors += 1
                # エラー内容をターミナルに赤文字で表示する
                print(Fore.RED + err_detail['message'] + Fore.RESET)

    return num_of_errors


def submit_daily_report(file_path: str, name: str, date: datetime):
    # chromeをヘッドレスモードで使用する
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # docker上で動作させるために必要
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    # FIXME: fix url
    url = 'https://www.kiji-check.com/'
    driver.get(url)

    year = "{0:04d}".format(date.year)
    month = "{0:02d}".format(date.month)
    day = "{0:02d}".format(date.day)

    file = pathlib.Path(file_path).open()
    contents = file.read()

    # FIXME: fix operation via selenium
    driver.find_element_by_class_name('wac-textarea').send_keys(contents)
    driver.find_element_by_class_name('wac-button').click()

    # FIXME:
    print(driver.find_element_by_class_name('wac-result-message').get_attribute('innerText'))

    driver.quit()


if __name__ == '__main__':
    main()
