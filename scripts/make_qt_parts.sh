#!/usr/bin/env bash
cd "$(dirname "$0")"/..

poetry run pyuic6 mmk_updater/qt/designer
