#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

from .logger import PreconfLogger

LOGGER = PreconfLogger().get_instance()
