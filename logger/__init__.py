#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

from .logger import PreconfLogger

LOGGER = PreconfLogger().get_instance()
