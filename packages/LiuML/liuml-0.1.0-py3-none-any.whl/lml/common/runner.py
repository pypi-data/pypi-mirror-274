#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Inspired by https://github.com/codefuse-ai/CodeFuse-Query
import logging
import subprocess
import threading
import shlex
from typing import List


def output_stream(stream):
    for line in iter(stream.readline, b''):
        output = line.strip()
        if output:
            print(output)


class Runner:
    def __init__(self, cmd: str | List[str], timeout_seconds: float | None = None):
        self.cmd = cmd
        self.timeout_seconds = timeout_seconds

    def subrun(self, output=None):
        cmd = self.cmd if not isinstance(self.cmd, str) else shlex.split(self.cmd)
        logging.info(f"execute : {shlex.join(cmd)}")
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       encoding="utf-8")
            if output is None:
                output = output_stream
            output_thread = threading.Thread(target=output, args=(process.stdout,))
            output_thread.daemon = True
            output_thread.start()

            process.wait(timeout=self.timeout_seconds)

            if process.returncode is None:
                process.kill()
                logging.error(
                    f"execute time > {self.timeout_seconds} s, time out, You can add -t option to adjust timeout")
            return_code = process.wait()
            return return_code
        except Exception as e:
            logging.error(f"execute error: {e}")
            return -1
