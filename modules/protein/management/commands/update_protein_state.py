import requests
import pandas as pd
import io
from os import path 
import sys
from django.core.management.base import BaseCommand, CommandError
from config.settings import MODULES_ROOT

class Command(BaseCommand):
    help = "Get state information from GPCRdb and relate it with PDBid into a dictionary."
    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            dest='update',
            default=False,
            help='Overwrites already stored data on gpcrdb_table.html.',
        )

    def handle(self, *args, **options):
        #Get data from GPCRdb 

        url = "https://gpcrdb.org/structure/"

        # If we want to update or obtain the data 
        if options['update']: 
            print("- UPDATE STEP...")
            print("     > Refreshing data...")
            table_info = open(mode="w", file=f"{MODULES_ROOT}/protein/management/tools/gpcrdb_table.html")
            urlData = requests.get(url)
            urltext = urlData.text
            l_urltext = urltext.split("\n")

            table = 0
            over_header = 0

            for line in l_urltext:
                if "<table" in line: 
                    table_info.writelines(line+"\n")
                    table = 1
                elif "</table" in line:
                    table_info.writelines(line+"\n")
                    table = 0
                    table_info.close()
                    break
                elif "<tr class='over_header over_header_row'" in line: 
                    over_header = 1
                elif "</tr" in line and over_header == 1: 
                    over_header = 0 
                elif table == 1 and over_header == 0: 
                    table_info.writelines(line+"\n")

            # Get the dataset from gpcrdb on pandas
            print("     > Getting the dataset...")
            gpcrdb_table = pd.read_html("{MODULES_ROOT}/protein/management/tools/gpcrdb_table.html")
            gpcrdb_table = gpcrdb_table[0].iloc[1:,1:-1] 

            # Create State dictionary from table 
            print("     > Creating the state dictionary ([pdb] = state)... ")
            dic_state = {}
            for index, row in gpcrdb_table.iterrows():
                pdb_id = str(row["PDB"])
                state = str(row["State"])
                if pdb_id not in dic_state.keys():
                    dic_state[pdb_id] = state

            # Write information into data.py file on dynadb main directory
            print("     > Writing info into modules/dynadb/data.py...")
            dic_state_file = open(mode="w", file=f"{MODULES_ROOT}/dynadb/data.py")
            dic_state_file.write(f"pdb_state={dic_state}")

        