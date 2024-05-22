#! /python3
# -*- coding: utf-8 -*-
# This test launcher script requires Python >=3.8 and an installation of Rhino 8.



import os
import sys
import socketserver
import multiprocessing
import subprocess




class MyUDPHandler(socketserver.BaseRequestHandler):

    quit_on = 'TESTS_FAILED'

    def handle(self):
        data = self.request[0].strip()

        output = data.decode('utf-8')
        print(output)
        if output == self.quit_on:
            sys.exit(1)


def start_UDP_server():
    HOST, PORT = "127.0.0.1", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()

def run_GH_file(gh_file, extra_env_vars):
    p = multiprocessing.Process(target=start_UDP_server)
    p.daemon = True
    print('Starting output printing UDP server.  Press Ctrl+C to quit.')
    p.start()



    env = os.environ.copy()

    # By default, exit Rhino afterwards.
    env['CHEETAH_GH_NON_INTERACTIVE'] = 'True'


    env.update(extra_env_vars)


    print(rf'Opening: {gh_file}')

    command = ( 
           r'"C:\Program Files\Rhino 8\System\Rhino.exe" /nosplash /runscript='
          rf'"-_grasshopper _editor _load _document _open {gh_file} '
          )

    if env['CHEETAH_GH_NON_INTERACTIVE'].lower() not in ('', '0', 'false'):
        command += ' _enter _exit'
    command += ' _enterend"'

    result = subprocess.run(command, env=env, shell=True)
    
    p.terminate()

    return result, p.exitcode




def main(args = sys.argv[1:]):


    gh_file = args[0]
    
    # Subsequent trailing command line args are env variable names and values.
    other_args = iter(args[1:])

    extra_env_vars = dict(zip(other_args, other_args))

    result, exitcode = run_GH_file(gh_file = gh_file, extra_env_vars = extra_env_vars)

    print(f'{result.returncode=}')
    print(f'{exitcode=}')

    if result.returncode != 0 or exitcode: 
        raise Exception(
             'An error occurred while running: {gh_file}. \n'
            f'Test runner retcode: {result.returncode}\n'
            f'Test output server exitcode: {exitcode}\n'
            )
    return 0


if __name__ == '__main__':
    sys.exit(main())