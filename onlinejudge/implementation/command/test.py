# Python Version: 3.x
import onlinejudge
import onlinejudge.implementation.utils as utils
import onlinejudge.implementation.logging as log
import onlinejudge.implementation.format_utils as cutils
import json
import math
import sys
import os
import pathlib
import time
import re
from typing import *
if TYPE_CHECKING:
    import argparse

def compare_as_floats(xs_: str, ys_: str, error: float) -> bool:
    def f(x):
        try:
            y = float(x)
            if not math.isfinite(y):
                faster_warning('not an real number found: %f', y)
            return y
        except ValueError:
            return x
    xs = list(map(f, xs_.split()))
    ys = list(map(f, ys_.split()))
    if len(xs) != len(ys):
        return False
    for x, y in zip(xs, ys):
        if isinstance(x, float) and isinstance(y, float):
            if not math.isclose(x, y, rel_tol=error, abs_tol=error):
                return False
        else:
            if x != y:
                return False
    return True

def test(args: 'argparse.Namespace') -> None:
    # prepare
    if not args.test:
        args.test = cutils.glob_with_format(args.directory, args.format)  # by default
    if args.ignore_backup:
        args.test = cutils.drop_backup_or_hidden_files(args.test)
    # 自分で書き換えた箇所
    f = open('onlinejudge/communication.py', 'r')
    com_prob = f.read().split()[1]
    f.close()
    path = com_prob.upper() + '/test'
    args.test = []
    for p in os.listdir(path):
        args.test.append(pathlib.Path(com_prob.upper() + '/test/' + p))
    tests = cutils.construct_relationship_of_files(args.test, args.directory, args.format)
    if args.error: # float mode
        match = lambda a, b: compare_as_floats(a, b, args.error)
    else:
        def match(a, b):
            # 自分で書き換えた箇所
            a = a.replace(chr(13), '')
            b = b.replace(chr(13), '')
            if a == b:
                return 'AC'
            if args.rstrip and a.rstrip(rstrip_targets) == b.rstrip(rstrip_targets):
                faster_warning('WA if no rstrip')
                return 'AC'

            # 自分で書き換えた箇所
            # 小数出力の誤差許容
            def make_outlist(s):
                outlist = []
                tmp_token = ''
                for i in range(len(s)):
                    if s[i] == ' ' or s[i] == '\n' or i == len(s)-1:
                        if tmp_token != '':
                            outlist.append(tmp_token)
                        tmp_token = ''
                        continue
                    else:
                        tmp_token += s[i]
                return outlist

            outlist_a = make_outlist(a)
            outlist_b = make_outlist(b)

            if len(outlist_a) == len(outlist_b):
                flg = False
                for i in range(len(outlist_a)):
                    def isnum(s):
                        ''' 小数点およびマイナスも含めて数字であるか '''
                        try:
                            int(s)
                        except:
                            return re.fullmatch(r'[-]?[0-9]+[.][0-9]+', s) != None
                        return True

                    if isnum(outlist_a[i]) and isnum(outlist_b[i]):
                        # b が correct だと想定
                        if '.' in outlist_b[i]:
                            flg = True
                        permissible_error = float('1e-6')
                        if not (abs(float(outlist_a[i]) - float(outlist_b[i])) <= permissible_error or abs(float(outlist_a[i]) - float(outlist_b[i])) <= abs(float(outlist_b[i])) * permissible_error):
                            return 'WA'
                    else:
                        return 'WA'
                return ['AC_with_error', flg]
            return 'WA'

    rstrip_targets = ' \t\r\n\f\v\0'  # ruby's one, follow AnarchyGolf
    slowest = -1  # type: Union[int, float]
    slowest_name = ''
    ac_count = 0
    ac_with_error_count = 0
    error_permission = False

    history = []  # type: List[Dict[str, Any]]
    tested_cases = []  # 自分で書き換えた箇所
    for name, it in sorted(tests.items()):
        if name in tested_cases:
            continue
        else:
            tested_cases.append(name)
            
        is_printed_input = not args.print_input
        def print_input():
            nonlocal is_printed_input
            if not is_printed_input:
                is_printed_input = True
                with open(it['in']) as inf:
                    log.faster_emit('input:\n%s', log.bold(inf.read()))

        log.faster_emit('')
        log.faster_info('%s', name)

        # run the binary
        with it['in'].open() as inf:
            begin = time.perf_counter()
            answer_byte, proc = utils.exec_command(args.command, shell=True, stdin=inf, timeout=args.tle)
            end = time.perf_counter()
            elapsed = end - begin
            answer = answer_byte.decode()
            if slowest < elapsed:
                slowest = elapsed
                slowest_name = name
            log.faster_status('time: %f sec', elapsed)
            proc.terminate()

        # check TLE, RE or not
        result = 'AC'
        if proc.returncode is None:
            log.faster_failure(log.red('TLE'))
            result = 'TLE'
            print_input()
        elif proc.returncode != 0:
            log.faster_failure(log.red('RE') + ': return code %d', proc.returncode)
            result = 'RE'
            print_input()

        # check WA or not
        if 'out' in it:
            with it['out'].open() as outf:
                correct = outf.read()
            # compare
            if args.mode == 'all':
                if match(answer, correct) == 'WA':
                    log.faster_failure(log.red('WA'))
                    print_input()
                    if not args.silent:
                        log.faster_emit('output:\n%s', log.bold(answer))
                        log.faster_emit('expected:\n%s', log.bold(correct))
                    result = 'WA'
                elif match(answer, correct) == ['AC_with_error', True]:
                    print_input()
                    if not args.silent:
                        log.faster_emit('output:\n%s', log.bold(answer))
                        log.faster_emit('expected:\n%s', log.bold(correct))
                    result = 'AC_with_error'
                    error_permission = True
                elif match(answer, correct) == ['AC_with_error', False]:
                    print_input()
                    if not args.silent:
                        log.faster_emit('output:\n%s', log.bold(answer))
                        log.faster_emit('expected:\n%s', log.bold(correct))
                    result = 'AC_with_error'
            elif args.mode == 'line':
                answer_words  = answer .splitlines()
                correct_words = correct.splitlines()
                for i, (x, y) in enumerate(zip(answer_words + [ None ] * len(correct_words), correct_words + [ None ] * len(answer_words))):  # type: ignore
                    if x is None and y is None:
                        break
                    elif x is None:
                        print_input()
                        log.faster_failure(log.red('WA') + ': line %d: line is nothing: expected "%s"', i + 1, log.bold(y))
                        result = 'WA'
                    elif y is None:
                        print_input()
                        log.faster_failure(log.red('WA') + ': line %d: unexpected line: output "%s"', i + 1, log.bold(x))
                        result = 'WA'
                    elif match(x, y) == 'WA':
                        print_input()
                        log.faster_failure(log.red('WA') + ': line %d: output "%s": expected "%s"', i + 1, log.bold(x), log.bold(y))
                        result = 'WA'
            else:
                assert False
        else:
            if not args.silent:
                log.faster_emit(log.bold(answer))
        if result == 'AC':
            log.faster_success(log.green('AC'))
            ac_count += 1
        elif result == 'AC_with_error':
            log.faster_success(log.green('AC (with error)'))
            ac_count += 1
            ac_with_error_count += 1

        # push the result
        testcase = {
            'name': name,
            'input': str(it['in'].resolve()),
        }
        if 'out' in it:
            testcase['output'] = str(it['out'].resolve())
        history += [ {
            'result': result,
            'testcase': testcase,
            'output': answer,
            'exitcode': proc.returncode,
            'elapsed': elapsed,
        } ]

    # summarize
    log.faster_emit('')
    log.faster_status('slowest: %f sec  (for %s)', slowest, slowest_name)
    if ac_count == len(tests):
        # 自分で書き換えた箇所
        if ac_with_error_count > 0:
            if error_permission == True:
                log.faster_success('test ' + log.green('success (with error)') + ': %d cases', len(tests))
            else:
                log.faster_failure('test ' + log.green('success (with error)') + ': %d cases', len(tests))
                log.faster_error('your answer has error while correct answer has no error')
                log.faster_warning('please remove error from your answer')
                f = open('onlinejudge/communication.py', 'r')
                com_prev = f.readlines()
                f.close()
                f = open('onlinejudge/communication.py', 'w')
                f.writelines([' '.join(com_prev[0].split())] + [' ', 'WA', '\n'] + com_prev[1].split())
                f.close()
        else:
            log.faster_success('test ' + log.green('success') + ': %d cases', len(tests))
        # 自分で書き換えた箇所
        f = open('onlinejudge/communication.py', 'r')
        com_prev = f.readlines()
        f.close()
        f = open('onlinejudge/communication.py', 'w')
        f.writelines([' '.join(com_prev[0].split())] + [' ', 'AC', '\n'] + com_prev[1].split())
        f.close()
    else:
        log.faster_failure('test ' + log.red('failed') + ': %d AC / %d cases', ac_count, len(tests))
        # 自分で書き換えた箇所
        f = open('onlinejudge/communication.py', 'r')
        com_prev = f.readlines()
        f.close()
        f = open('onlinejudge/communication.py', 'w')
        f.writelines([' '.join(com_prev[0].split())] + [' ', 'WA', '\n'] + com_prev[1].split())
        f.close()

    if args.json:
        print(json.dumps(history))

    if ac_count != len(tests):
        sys.exit(1)
