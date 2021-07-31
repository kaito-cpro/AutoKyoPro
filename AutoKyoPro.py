import onlinejudge.implementation.main
import onlinejudge.implementation.logging as log
import sys
import os
import subprocess
import datetime
import re

contest_name = 'abc159' # 暫定
command_list = ['init', 'info', 'standby', 'login', 'nosub', 'sub']

if __name__ == '__main__':
    args = [] + sys.argv[1:]
    for i in range(len(args)):
        cmd = args[i]
        if cmd not in command_list and re.fullmatch(r'[a-zA-Z][.](cpp|py|awk)', cmd) == None:
            log.faster_error('invalid comand was called')
            log.faster_warning(f'please run the valid comand: {command_list}')
            sys.exit()
        if cmd == 'nosub' or cmd == 'sub':
            if i == 0 or re.fullmatch(r'[a-zA-Z][.](cpp|py|awk)', args[i - 1]) == None:
                log.faster_error('invalid command was called')
                log.faster_warning(f'\'{cmd}\' takes the file name as an argument')
                sys.exit()

    # 初期化
    if 'init' in args:
        if len(args) != 1:
            log.faster_error('invalid argument')
            log.faster_warning(f'\'init\' takes no argument ({len(args) - 1} given)')
            sys.exit()
        contest_name = input('contest name: ').upper()
        alternate_url = input('alternate contest url (default: Enter): ')
        if alternate_url == '':
            alternate_url = contest_name.lower()
        f = open('onlinejudge/communication.py', 'w')
        f.writelines([contest_name, '\n', alternate_url])
        f.close()
        problem_num = input('number of problems (default H: Enter): ')
        if problem_num == '':
            problem_num = 'H'
        if not 'A' <= problem_num <= 'Z':
            log.faster_error('failed to set the number of problems')
            log.faster_warning('please type the valid alphabet from \'A\' to \'Z\'')
            sys.exit()
        problem_list = [chr(num) for num in range(ord('A'), ord(problem_num.upper()) + 1)]
        for c in [chr(num) for num in range(ord('A'), ord('Z') + 1)]:
            if c not in problem_list and os.path.exists(c):
                subprocess.run(['rm', '-rf', c])
        for c in problem_list:
            if os.path.exists(c):
                continue
            subprocess.run(['mkdir', c])
            subprocess.run(['touch', c + '/' + c.lower() + '.cpp'])
            subprocess.run(['touch', c + '/' + c.lower() + '.py'])
        for c in problem_list:
            if os.path.exists(c + '/test'):
                subprocess.run(['rm', '-rf', c + '/test'])
            if os.path.exists(c + '/a.exe'):
                subprocess.run(['rm', c + '/a.exe'])
        sys.exit()

    # AutoKyoPro に登録したコンテスト情報の表示
    if 'info' in args:
        if len(args) != 1:
            log.faster_error('invalid argument')
            log.faster_warning(f'\'info\' takes no argument ({len(args) - 1} given)')
            sys.exit()
        f = open('onlinejudge/communication.py', 'r')
        info = f.read()
        f.close()
        print(info)
        sys.exit()

    # コンテスト参加スタンバイ
    if 'standby' in args:
        if len(args) != 1:
            log.faster_error('invalid argument')
            log.faster_warning(f'\'standby\' takes no argument ({len(args) - 1} given)')
            sys.exit()
        f = open('onlinejudge/communication.py', 'r')
        contest_name = f.readline().split()[0]
        com_url = f.readline().split()[0]
        f.close()
        contest_url = 'https://atcoder.jp/contests/' + contest_name.lower() + '/tasks/' + (com_url.lower().replace('-', '_') if '-' in com_url.lower() else com_url.lower())
        contest_time = input('contest time (default 21:00: Enter): ')
        if contest_time == '':
            contest_time = '21:00'
        contest_time += ':00'
        if len(contest_time) != 8 or contest_time[2] != ':':
            log.faster_error('failed to set the contest time')
            log.faster_warning('please type the valid time in the form such as 21:00')
            sys.exit()
        onlinejudge.implementation.main.main(args=['standby', contest_url, contest_time])
        sys.exit()

    # ログイン
    if 'login' in args:
        if len(args) != 1:
            log.faster_error('invalid argument')
            log.faster_warning(f'\'login\' takes no argument ({len(args) - 1} given)')
            sys.exit()
        onlinejudge.implementation.main.main(args=['login', 'https://atcoder.jp/'])
        sys.exit()

    com_prob, com_lang = None, None
    for cmd in args:
        if '.cpp' in cmd:
            com_prob = cmd[0].upper()
            com_lang = 'C++'
            break
        elif '.py' in cmd:
            com_prob = cmd[0].upper()
            com_lang = 'Python3'
            break
        elif '.awk' in cmd:
            com_prob = cmd[0].upper()
            com_lang = 'Awk'
            break
    if com_prob == None or not os.path.exists(com_prob.upper()):
        log.faster_error('failed to develop the process')
        log.faster_warning('please type valid file name')
        sys.exit()

    f = open('onlinejudge/communication.py', 'r')
    contest_name = f.readline().split()[0]
    com_url = f.readline().split()[0]
    f.close()
    contest_url = 'https://atcoder.jp/contests/' + contest_name.lower() + '/tasks/' + (com_url.lower().replace('-', '_') if '-' in com_url.lower() else com_url.lower())
    f = open('onlinejudge/communication.py', 'w')
    f.writelines([contest_name, ' ', com_prob, ' ', com_lang, '\n', com_url])
    f.close()

    # 強制提出
    if 'sub' in args:
        if com_lang == 'C++':
            onlinejudge.implementation.main.main(args=['s', contest_url + '_' + com_prob.lower(), com_prob.upper() + '/' + com_prob.lower() + '.cpp'])
        elif com_lang == 'Python3':
            onlinejudge.implementation.main.main(args=['s', contest_url + '_' + com_prob.lower(), com_prob.upper() + '/' + com_prob.lower() + '.py'])
        elif com_lang == 'Awk':
            onlinejudge.implementation.main.main(args=['s', contest_url + '_' + com_prob.lower(), com_prob.upper() + '/' + com_prob.lower() + '.awk'])
        sys.exit()

    # サンプルケース取得
    if not os.path.exists(com_prob.upper() + '/test'):
        onlinejudge.implementation.main.main(args=['d', contest_url + '_' + com_prob.lower(), '-d', com_prob.upper() + '/test'])

    # サンプルケーステスト
    if com_lang == 'C++':
        # C++ with ACL も含む
        p = subprocess.run(['g++', com_prob.upper() + '/' + com_prob.lower() + '.cpp'])
        if p.returncode != 0:
            sys.exit()
        if os.path.exists(com_prob.upper() + '/a.exe'):
            subprocess.run(['rm', com_prob.upper() + '/a.exe'])
        subprocess.run(['mv', 'a.exe', com_prob.upper()])
        onlinejudge.implementation.main.main(args=['t'])
    elif com_lang == 'Python3':
        onlinejudge.implementation.main.main(args=['t', '-c', 'python ' + com_prob.lower() + '.py'])
    elif com_lang == 'Awk':
        onlinejudge.implementation.main.main(args=['t', '-c', 'awk -f ' + com_prob.lower() + '.awk'])

    # 提出
    if 'nosub' not in args:
        f = open('onlinejudge/communication.py', 'r')
        AC_or_WA = f.readline().split()[3]
        f.close()
        if AC_or_WA == 'AC':
            if com_lang == 'C++':
                onlinejudge.implementation.main.main(args=['s', contest_url + '_' + com_prob.lower(), com_prob.upper() + '/' + com_prob.lower() + '.cpp'])
            elif com_lang == 'Python3':
                onlinejudge.implementation.main.main(args=['s', contest_url + '_' + com_prob.lower(), com_prob.upper() + '/' + com_prob.lower() + '.py'])
            elif com_lang == 'Awk':
                onlinejudge.implementation.main.main(args=['s', contest_url + '_' + com_prob.lower(), com_prob.upper() + '/' + com_prob.lower() + '.awk'])
