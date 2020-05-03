#!/usr/bin/env python3

import subprocess
import re
import sys


def main():
    proc = subprocess.run('git status'.split(), stdout=subprocess.PIPE)
    o = proc.stdout.decode('utf8').strip().split('\n')
    modified = [line for line in o if line.startswith(
        '\tmodified') or line.startswith("\tnew file")]
    errors = False
    only_missing = False
    for file_ in modified:
        file_ = file_.split(':')[1].strip()
        if file_.endswith('.py'):
            proc = subprocess.run([
                'python3', '-m', 'flake8',
                '--ignore=E402,W503,E731,E501,E121,E122,E123,E124,E125,E126,E127,E128,E131,E116,W504,B008,C408,E252,N802',
                '--exclude=source/testing/rr_behave/',
                file_])
            missing_commans = []

            if proc.returncode != 0:
                errors = True
            with open(file_) as f:
                line_num = 1
                for line in f:
                    if 'print(' in line:
                        print("{} in {}:{}".format(
                            line.strip(), file_, line_num))
                    line_num += 1
        elif file_.endswith('.css'):
            proc = subprocess.run(
                ['csslint', '--ignore=box-model', '--quiet', file_])
            if proc.returncode != 0:
                errors = True
        elif file_.endswith('.ts'):
            print("tslint", file_)
            proc = subprocess.run(
                ['tslint', file_])
            if proc.returncode != 0:
                errors = True
        elif file_.endswith('.js'):
            js_errors = False
            missing_semicolons = []
            proc = subprocess.run(['jshint', file_], stdout=subprocess.PIPE)
            jshint = proc.stdout.decode('utf8')

            if jshint:
                print(jshint)
                if proc.returncode != 0:
                    errors = True

                jshint = jshint.split('\n')
                for line in jshint:
                    if line == '':
                        # blank line indicates end of errors
                        break
                    matches = re.findall(
                        '([^:]+): line ([^,]+), col ([^,]+),([^$]+)', line)
                    if 'Missing semicolon' in line and matches:
                        missing_semicolons.append(matches[0][1])
                    else:
                        # if theres is an error thats not just missing semicolons bail
                        missing_semicolons = []
                        break

                with open(file_, 'r') as f:
                    filelines = f.readlines()

                if missing_semicolons and "/lib/" not in file_:
                    with open(file_, 'w') as f:
                        line_num = 1
                        for line in filelines:
                            if 'console.log' in line:
                                print("{} in {}:{}".format(
                                    line.strip(), file_, line_num))
                            if str(line_num) in missing_semicolons:
                                print(
                                    f"Automatically adding semicolon to {file_}:{line_num}")
                                f.write(line.replace('\n', '') + ';\n')
                            else:
                                f.write(line)
                            line_num += 1
                else:
                    line_num = 1
                    for line in filelines:
                        if 'console.log' in line:
                            print("{} in {}:{}".format(
                                line.strip(), file_, line_num))
                        line_num += 1
    if errors:
        return 1
    else:
        return 0


if __name__ == '__main__':
    if main() == 1:
        sys.exit(1)
    else:
        sys.exit()
