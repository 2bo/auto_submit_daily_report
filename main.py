import subprocess
import json
import argparse
import pathlib
from colorama import Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime


def main():

    psr = argparse.ArgumentParser(description='Automatically submit daily report to report system')
    psr.add_argument('file', metavar='SUBMIT_FILE', help='plain text file of daily report to submit')
    psr.add_argument('name', metavar='YOUR_NAME', help='author name(must be registered on system)')
    psr.add_argument('-d', '--date', nargs=1, metavar='', help='submit date - format YYYYMMDD')

    args = psr.parse_args()

    if exists_file(args.file):
        num_of_error = redpen_check(args.file)

        if num_of_error > 0:
            print("redpen detected {0} errors.".format(num_of_error))

        answer = input('Are you sure to submit daily report? yes/no:')
        if answer != 'yes':
            return

        if args.date is not None:
            try:
                date = datetime.strptime(args.date[0], "%Y%m%d")
            except:
                print("Not a valid date: '{0}'".format(args.date[0]))
                return
        else:
            date = datetime.now()

        submit_daily_report(args.file, args.name, date)

    else:
        print('File not found or is not file')
        return


def valide_date(date_str: str):
    try:
        datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        msg = "Not a valid date: '{0}'".format(date_str)
        raise argparse.ArgumentTypeError(msg)


def exists_file(file_path: str) -> bool:
    p = pathlib.Path(file_path)
    if not p.exists():
        return False
    if not p.is_file():
        return False
    return True


def redpen_check(file_path: str):
    # redpenの実行
    cmd = ['redpen', '-r', 'json2', file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # redpenの結果取得
    stdout = result.stdout.decode('utf8')

    # 結果の表示
    if (len(stdout) > 0):
        num_of_errors = 0
        json_dict = json.loads(stdout)
        errors = json_dict[0]['errors']
        if len(errors) < 1:
            return num_of_errors

        for err in errors:
            print(str(err['position']['start']['line']) + ':' + err['sentence'])
            for err_detail in err['errors']:
                num_of_errors += 1
                print(Fore.RED + err_detail['message'] + Fore.RESET)

        return num_of_errors


def submit_daily_report(file_path: str, name: str, date: datetime):
    year = "{0:04d}".format(date.year)
    month = "{0:02d}".format(date.month)
    day = "{0:02d}".format(date.day)

    print(year + month + day)

    url = 'https://www.kiji-check.com/'
    driver = webdriver.Chrome()
    driver.get(url)

    file = pathlib.Path(file_path).open()
    contents = file.read()

    driver.find_element_by_class_name('wac-textarea').send_keys(contents)
    driver.find_element_by_class_name('wac-button').click()

    time.sleep(3)

    print(driver.find_element_by_class_name('wac-result-message').get_attribute('innerText'))

    driver.quit()


if __name__ == '__main__': main()
