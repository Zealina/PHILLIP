#!/usr/bin/env python3
"""Pickle Persistence handler"""

from telegram.ext import PicklePersistence


persistence = PicklePersistence(filepath="data/data_storage_persistence")
