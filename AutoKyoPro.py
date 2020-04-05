import onlinejudge.implementation.main
import onlinejudge.implementation.logging as log
import sys
import os
import subprocess

contest_name = 'abc159' # 暫定

if __name__ == '__main__':
    args = [] + sys.argv[1:]

    # 初期化
    if 'start' in args:
        contest_name = input('contest name: ').upper()
        f = open('onlinejudge/communication.py', 'w')
        f.writelines([contest_name, ' '])
        f.close()
        for c in ['A', 'B', 'C', 'D', 'E', 'F']:
            if os.path.exists(c + '/test'):
                subprocess.run(['rm', '-rf', c + '/test'])
            if os.path.exists(c + '/a.exe'):
                subprocess.run(['rm', c + '/a.exe'])
        sys.exit()

    # ログイン
    if 'login' in args:
        if len(args) != 1:
            log.error('failed to login to AtCoder')
            log.warning('please type just \'login\' as an option')
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
            args = ['t', '-c', 'python', com_prob.lower() + '.py']
            break
    if com_prob == None:
        log.error('failed to develop the process')
        log.warning('please type valid file name')
        sys.exit()

    f = open('onlinejudge/communication.py', 'r')
    contest_name = f.read().split()[0]
    f.close()
    contest_url = 'https://atcoder.jp/contests/' + contest_name.lower() + '/tasks/' + (contest_name.lower().replace('-', '_') if '-' in contest_name.lower() else contest_name.lower())
    f = open('onlinejudge/communication.py', 'w')
    f.writelines([contest_name, ' ', com_prob, ' ', com_lang])
    f.close()

    # サンプルケース取得
    if not os.path.exists(com_prob + '/test'):
        onlinejudge.implementation.main.main(args=['d', contest_url + '_' + com_prob.lower(), '-d', com_prob.upper() + '/test'])

    # サンプルケーステスト
    if com_lang == 'C++':
        p = subprocess.run(['g++', com_prob.upper() + '/' + com_prob.lower() + '.cpp'])
        if p.returncode != 0:
            sys.exit()
        subprocess.run(['mv', 'a.exe', com_prob.upper()])
        onlinejudge.implementation.main.main(args=['t'])
    elif com_lang == 'Python3':
        onlinejudge.implementation.main.main(args=['t', '-c', 'python ' + com_prob.lower() + '.py'])

    # 提出
    f = open('onlinejudge/communication.py', 'r')
    AC_or_WA = f.read().split()[-1]
    f.close()
    if AC_or_WA == 'AC':
        if com_lang == 'C++':
            onlinejudge.implementation.main.main(args=['s', contest_url + '_' + com_prob.lower(), com_prob.upper() + '/' + com_prob.lower() + '.cpp'])
        elif com_lang == 'Python3':
            onlinejudge.implementation.main.main(args=['s', contest_url + '_' + com_prob.lower(), com_prob.upper() + '/' + com_prob.lower() + '.py'])
