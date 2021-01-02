#!/usr/bin/env bash
csvs-to-sqlite --replace-tables ../output/csv/*.csv ../output/sqldb/ufo_all_activity.db
