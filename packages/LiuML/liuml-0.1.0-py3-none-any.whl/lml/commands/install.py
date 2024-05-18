#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import subprocess

import click


@click.group(
    "install",
    invoke_without_command=True,
    context_settings={"ignore_unknown_options": True},
)
@click.argument("args", nargs=-1)
@click.option(
    "--mirror",
    type=click.Choice(["tuna", "aliyun", "ustc", "douban", "huawei", "pypi"], case_sensitive=False),
    default="tuna"
)
@click.pass_context
def cli(ctx, args, mirror):
    """
    Install pypi package via mirrors
    """
    if ctx.invoked_subcommand is None:
        mirrors = {
            "tuna": "https://pypi.tuna.tsinghua.edu.cn/simple",
            "aliyun": "https://mirrors.aliyun.com/pypi/simple",
            "ustc": "https://pypi.mirrors.ustc.edu.cn/simple",
            "douban": "https://pypi.douban.com/simple",
            "huawei": "https://mirrors.huaweicloud.com/repository/pypi/simple",
            "pypi": "https://pypi.org/simple",
        }
        cmd = ["pip", "install", "-i", mirrors.get(mirror)] + list(args)
        cmd_text = " ".join(cmd)
        click.echo(f"The command to call is {cmd_text}. ")
        return subprocess.check_call(cmd, env=dict(os.environ))
