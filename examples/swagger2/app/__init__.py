# -*- coding:utf-8 -*-
from toybox.simpleapi import run


def includeme(config):
    config.include("toybox.swagger")
    config.include("app.routes")
    config.scan("app.views")


if __name__ == "__main__":
    run.include(includeme)
    run(port=5001)
