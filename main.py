#!/usr/bin/python3
import csv
import re
import pprint
import json
from  jinja2 import Environment, FileSystemLoader
from datetime import datetime

#setup the dang debugger to actually go here
"""
goal is to use regex to extract anything that would say
11th or 11thCyber then we could fish out that data and put it here,
this would be a new object everytime someone would like to initialize a csv. 

do not trust the user for any inputs, hence why we do not get data from the csv to execute
that wouldbe retarded af. only extract and put, not execute.

TODO:
we need to implement dictionary usage in this for easier data manipulation, further down the line
we need to fix the elif and turn it to a regular if, 
    so it does not skip the entire row if it matches the first row
we could refactor the row reader intoa function, that way  it looks cleaner

on the html side,we can add a quick edit function that would edit the json there and then, but we don't need everyone blasted out there, for infomation safety, I can just look it up manually
"""
 #len is 6 when there are no comments  on the room


def hasher(csv):
    """gets hash checksum of the csv
    in the future, we can compare if the csv has been edited or not, 
    that way we do not hve to re-extract

    Args:
        csv (_type_): path to your csv

    returns:
        a hash of your csv
    """
    pass
class extract_from_csv:
    """
    extracts our personnel from all the data in the csv provided
    self.personnel: list: contains the personnel
    self.building_info: dictionary: contains the bldg number
    and the personnel inside the building number

    dictionary structure:
    self.building_info = {
        "<bldg_number>" : {self.building_info_details}
    }

    self.building_info_details: dictionary: used to populate the inner dictionary:
    dictionary structure:
        self.building_info_details = {
        "last" :"str",
        "first": "str",
        "rank" : "str",
        "sex" : "str",
        "company" : "str",
        "phone_number": "str",
        "comments" : "str",
        }
    """

    def __init__(self, path: str, csv_type: int):
        """default init function

        Args:
            path (str): path to the csv 
            csv_type (int): csv version (bldg number)
        """
        self.path = path
        self.csv_type = csv_type
        self.personnel = []
        self.building_info = { str(csv_type) :{} }
        #redundant but cleaner code
        self.building_info_details = self.building_info[str(csv_type)]
        


        
        #populate the list with personnel
        self._get_personnel()
    def add_building_number(self, bldg_number: int):
        """
        add a building number to the row someday 
        """
        pass

    def pretty_format(self, row: list, row_len: int, bldg_num: int):
        """pretty format the row to add a blank column if they
            do not have any remarks

        Args:
            row (_type_): array from the csv

        Returns:
            array: put the array len to 7 as some of the csv has remarks
        """
        row_buffer = row
        if not (len(row_buffer) == row_len):
            #we should just keep appending spaces until 
            #len is 7 in the future, 
            row_buffer.append(" ")
        row_buffer.append(str(bldg_num))
        return row_buffer                           

    def _process_19751(self):
        """populates the get self.personnel array
        """
        HORIZONTAL_CELL_SKIP = 15 
        #we skip 15 cells cause actual roster starts at horizontal 15
        FIRST_FLOOR_UNIT = 5
        SECOND_FLOOR_UNIT = 13
        THIRD_FLOOR_UNIT = 21
        """
        first chunk of info is from 0:7, then 8:15, then 16:23
        processess the 19751 csv [type
        """
        with open(self.path) as excel_spread_cheeks:
            reader = csv.reader(excel_spread_cheeks)
            max_row_len = 7
                        #implement their own function here so this would be cleaner
            for _ in range(HORIZONTAL_CELL_SKIP):
                next(excel_spread_cheeks)
            for row in reader:
                            #eventuall replace 11th wtih regex
                if row[FIRST_FLOOR_UNIT] in ("11TH", "CYBER"):
                    self.personnel.append(self.pretty_format(row[0:7], max_row_len, self.csv_type))
                if row[SECOND_FLOOR_UNIT] in ("11TH", "CYBER"):
                    self.personnel.append(self.pretty_format(row[8:15], max_row_len, self.csv_type))
                if row[THIRD_FLOOR_UNIT] in  ("11TH", "CYBER"):
                    self.personnel.append(self.pretty_format(row[16:23], max_row_len, self.csv_type))
            
            for person_deets in self.personnel:
                #optional refractor for this? we could make a function that would just take an argument and add to dict
                #or we could just keep doing this, sinc each csv would need custom coordiantes

                room_number =  str(person_deets[0])
                self.building_info_details.update({room_number: {}})
                self.building_info_details[room_number].update( {'last': str(person_deets[2]) })
                self.building_info_details[room_number].update( {'first': str(person_deets[3]) })
                self.building_info_details[room_number].update( {'rank': str(person_deets[4]) })
                self.building_info_details[room_number].update( {'sex': str(person_deets[1]) })
                self.building_info_details[room_number].update( {'company': ""}) #blank for now, you have to edit
                self.building_info_details[room_number].update( {'phone_number': ""})
                self.building_info_details[room_number].update( {'comments': ""})
            
    def _process_19753(self):
        """populates the get self.personnel array
        """
        with open(self.path) as excel_spread_cheeks:
            reader = csv.reader(excel_spread_cheeks)

            HORIZONTAL_CELL_SKIP = 15 
            #we skip 15 cells cause actual roster starts at horizontal 15
            FIRST_FLOOR_UNIT = 5
            SECOND_FLOOR_UNIT = 13
            THIRD_FLOOR_UNIT = 21
            max_row_len = 6
            for _ in range(HORIZONTAL_CELL_SKIP):
                next(excel_spread_cheeks)
            for row in reader:
                if (row[FIRST_FLOOR_UNIT] in ("11TH", "CYBER")):
                    self.personnel.append(self.pretty_format(row[0:6], max_row_len, self.csv_type))
                if (row[SECOND_FLOOR_UNIT] in  ("11TH", "CYBER")):
                    self.personnel.append(self.pretty_format(row[8:14], max_row_len, self.csv_type))
                if (row[THIRD_FLOOR_UNIT] in  ("11TH", "CYBER")):
                    self.personnel.append(self.pretty_format(row[16:22], max_row_len, self.csv_type))

            for person_deets in self.personnel:
                room_number =  str(person_deets[0])
                self.building_info_details.update({room_number: {}})
                self.building_info_details[room_number].update( {'last': str(person_deets[2]) })
                self.building_info_details[room_number].update( {'first': str(person_deets[3]) })
                self.building_info_details[room_number].update( {'rank': str(person_deets[4]) })
                self.building_info_details[room_number].update( {'sex': str(person_deets[1]) })
                self.building_info_details[room_number].update( {'company': ""}) #blank for now, you have to edit
                self.building_info_details[room_number].update( {'phone_number': ""})
                self.building_info_details[room_number].update( {'comments': ""})

    def _process_19755(self):
        """populates the get self.personnel array
        """
        with open(self.path) as excel_spread_cheeks:
            reader = csv.reader(excel_spread_cheeks)

            HORIZONTAL_CELL_SKIP = 15 
            #we skip 15 cells cause actual roster starts at horizontal 15
            FIRST_FLOOR_UNIT = 5
            SECOND_FLOOR_UNIT = 13
            THIRD_FLOOR_UNIT = 21

            max_row_len = 7
            for _ in range(HORIZONTAL_CELL_SKIP):
                next(excel_spread_cheeks)
            for row in reader:
                if (row[FIRST_FLOOR_UNIT] in ("11TH", "CYB")):
                    self.personnel.append(self.pretty_format(row[0:6], max_row_len, self.csv_type))
                if (row[SECOND_FLOOR_UNIT] in  ("11TH", "CYB")):
                    self.personnel.append(self.pretty_format(row[8:14], max_row_len, self.csv_type))
                if (row[THIRD_FLOOR_UNIT] in  ("11TH", "CYB")):
                    self.personnel.append(self.pretty_format(row[16:22], max_row_len, self.csv_type))


            for person_deets in self.personnel:
                #optional refractor for this? we could make a function that would just take an argument and add to dict
                #or we could just keep doing this, sinc each csv would need custom coordiantes

                room_number =  str(person_deets[0])
                self.building_info_details.update({room_number: {}})
                self.building_info_details[room_number].update( {'last': str(person_deets[2]) })
                self.building_info_details[room_number].update( {'first': str(person_deets[3]) })
                self.building_info_details[room_number].update( {'rank': str(person_deets[4]) })
                self.building_info_details[room_number].update( {'sex': str(person_deets[1]) })
                self.building_info_details[room_number].update( {'company': ""}) #blank for now, you have to edit
                self.building_info_details[room_number].update( {'phone_number': ""})
                self.building_info_details[room_number].update( {'comments': ""})
            
    def _process_19757(self):
        """populates the get self.personnel array
        """
        HORIZONTAL_CELL_SKIP = 12 
        #we skip 15 cells cause actual roster starts at horizontal 15
        FIRST_FLOOR_UNIT = 6
        SECOND_FLOOR_UNIT = 16
        THIRD_FLOOR_UNIT = 27

        with open(self.path) as excel_spread_cheeks:
            reader = csv.reader(excel_spread_cheeks)

                    #this is a special case since they massacred the format on this one
            max_row_len = 7
            for _ in range(HORIZONTAL_CELL_SKIP):
                next(excel_spread_cheeks)
            for row in reader:
                if (row[FIRST_FLOOR_UNIT] in ("11TH", "CYB")):
                    self.personnel.append(self.pretty_format(row[0:7], max_row_len, self.csv_type))
                if (row[SECOND_FLOOR_UNIT] in  ("11TH", "CYB")):
                    self.personnel.append(self.pretty_format(row[12:19], max_row_len, self.csv_type))
                if (row[THIRD_FLOOR_UNIT] in  ("11TH", "CYB")):
                    self.personnel.append(self.pretty_format(row[21:28], max_row_len, self.csv_type))

            for person_deets in self.personnel:
                #optional refractor for this? we could make a function that would just take an argument and add to dict
                #or we could just keep doing this, sinc each csv would need custom coordiantes
                print(person_deets)
                room_number =  str(person_deets[0])
                self.building_info_details.update({room_number: {}})
                self.building_info_details[room_number].update( {'last': str(person_deets[3]) })
                self.building_info_details[room_number].update( {'first': str(person_deets[4]) })
                self.building_info_details[room_number].update( {'rank': str(person_deets[5]) })
                self.building_info_details[room_number].update( {'sex': str(person_deets[2]) })
                self.building_info_details[room_number].update( {'company': ""}) #blank for now, you have to edit
                self.building_info_details[room_number].update( {'phone_number': ""})
                self.building_info_details[room_number].update( {'comments': ""})
            
    def _get_personnel(self):
        """fell to the voices, we'll be using dict

        Returns:
            dict = {
            "<bldg_number> = {
                "name"
                "last"
                "gender"
                "contact"
                "company"
                "unit"
                }
            }
        """
        max_row_len = 0
        match self.csv_type:
                
            case 19751: #HHC
                self._process_19751()
            case 19753: #rice 
                self._process_19753()
            case 19755: #Alpha
                self._process_19755()
            case 19757: #potatoes
                self._process_19757()

        #we might probably stop using self.personnel someday
        #for speed? and computing efficiency
        return self.personnel
    
    def print_personnel(personnel: list):
        #helper function to print personnels
        print(personnel)

def main():
    """open the xlsx on google and save it there as csv so you would not get corrupted output
    """
    bldg_19751 = extract_from_csv("racks_roster/19751 BARRACKS ROSTER(19751).csv", 19751)

    bldg_19753 = extract_from_csv("racks_roster/19753 BARRACKS ROSTER(19753).csv", 19753)

    bldg_19755 = extract_from_csv("racks_roster/19755 BARRACKS ROSTER(19755).csv", 19755)
    
    bldg_19757 = extract_from_csv("racks_roster/19757 BARRACKS ROSTER(Sheet1).csv", 19757)


    #alpha_roster = extract_from_csv("racks/19755_ACO_FEB25(19755).csv", 19755)
    sorted_roster = sorted([*bldg_19751.personnel, *bldg_19753.personnel, *bldg_19755.personnel, *bldg_19757.personnel], key=lambda last_name: last_name[2])
    
    dict_building_info = {**bldg_19751.building_info, **bldg_19753.building_info, **bldg_19755.building_info, **bldg_19757.building_info}


    for soldier_deets in sorted_roster:
        print(" Last: {2}, sFirst: {3}, BLDG NUM: {0}, Rank: {1}, Sex: {4}, Room#: {5}".format(
            soldier_deets[-1], soldier_deets[4], 
            soldier_deets[2], soldier_deets[3], 
            soldier_deets[1], soldier_deets[0], 
        ))

    #pprint.pprint(dict_building_info)

    #print(json.dumps(dict_building_info, indent=4))
    #experiment time :)))
    data = dict_building_info
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("racksdata.html")

    html_output = template.render(data=data, datenow=datetime.now().date())

    with open("./output/output.html", "w", encoding="utf-8") as f:
        f.write(html_output)

if __name__ == "__main__":  
    main()
    





  
