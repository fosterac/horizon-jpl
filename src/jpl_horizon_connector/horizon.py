# python-jpl-horizon
#
# Written by: Matthew Mihok (@mattmattmatt)

import re
from telnetlib import Telnet

from config import (
    HORIZON_HOST,
    HORIZON_PORT,
    HORIZON_PROMPT,
    HORIZON_QUERY_PROMPT,
    DEBUG,
)


class Horizon():
    telnet = Telnet()
    re_version = re.compile("version|v\s?(\d+\.\d+)")
    re_list = re.compile("^\s+-?(\d+)\s\s(\w+)", flags=re.MULTILINE)
    re_meta = re.compile(".+")
    re_cartesian = re.compile(".+")

    def __open(self):
        self.telnet.open(HORIZON_HOST, HORIZON_PORT)
        self.telnet.read_until(HORIZON_PROMPT)
        # self.telnet.read_until(HORIZON_PROMPT)

    def __close(self, send_quit=False):
        if send_quit:
            self.telnet.write("\rquit\n")

        self.telnet.close()

    def __parse_list(self, data):
        matches = self.re_list.findall(data)
        # import pdb; pdb.set_trace()
        if len(matches) is 0:
            return []

        return matches

    def __parse_meta(self, data):
        pass

    def __parse_cartesian(self, data):
        pass

    def __parse_version(self, data):
        matches = self.re_version.search(data)

        if matches is None:
            return 0
        # fail if cant find
        return matches.groups()[0]

    def major(self):
        self.__open()
        self.telnet.write("MB\n")
        # import pdb;pdb.set_trace()

        result = self.telnet.read_until(HORIZON_QUERY_PROMPT)

        if DEBUG:
            print result

        self.__close(send_quit=True)

        return self.__parse_list(result)

    def minor(self):
        self.__open()
        self.telnet.write("SB\n")

        result = self.telnet.read_until(HORIZON_QUERY_PROMPT)

        if DEBUG:
            print result

        self.__close(send_quit=True)

        return self.__parse_list(result)

    def version(self):
        self.__open()

        self.telnet.write("quit\n")
        result = self.telnet.read_until(HORIZON_QUERY_PROMPT)

        if DEBUG:
            print result

        self.__close()

        return self.__parse_version(result)
