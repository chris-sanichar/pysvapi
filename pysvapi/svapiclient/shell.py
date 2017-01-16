#!/usr/bin/python

import argparse
import logging

from elementdriver.sshdriver import sshdriver
from elementdriver.restdriver import restdriver
from svapiclient import client 

def main():
    parser = argparse.ArgumentParser(description="Sandvine Configuration API")
    parser.add_argument("host")
    parser.add_argument("-c","--command",nargs='+',action='append',type=str)
    parser.add_argument("-r","--rest",action="store_true")
    args = parser.parse_args()

    driver = None
    if args.rest:
        driver = restdriver.ElementDriverREST(args.host)
    else:
        driver = sshdriver.ElementDriverSSH(args.host)

    logger = driver.getLogger()
    logger.setLevel(logging.DEBUG)

    if not driver.wait_for_api_ready():
        print("api is not ready!")
        return 1

    for cmd in args.command:
        for str_cmd in cmd:
            driver.add_cmd(str_cmd)

    driver.configuration_commit()

if __name__ == '__main__':
    main()
