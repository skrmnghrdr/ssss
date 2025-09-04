#!/usr/bin/python3
import csv
import re
import pprint
import json
from  jinja2 import Environment, FileSystemLoader
from datetime import datetime


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

        #redundant but cleaner code
        self.building_info_details= {}
        


        
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

    def _process_emh(self):
        """a special function which extracts things from the machine spirit.
        this would be the most stable in communication with the machine god and it's further locomotion
        we just have to perform the cleansing rites and apply purity seals
        we would not need to filter by chapter as the filtration rites already provided by the machine spirit
        """
        BLDG_NUMBER = 0
        BED_NUMBER = 1
        NAME = 5
        RANK = 9
        GENDER = -1

        with open(self.path) as excel_spread_cheeks:
            reader = csv.reader(excel_spread_cheeks)
            for row in reader:
                person_buffer = []
                fullname = row[NAME].split(",")
                last_name = fullname[0]
                first_name = fullname[-1]
                bed_number = row[BED_NUMBER].split("-")[1]
                person_buffer.append(row[BLDG_NUMBER])
                person_buffer.append(bed_number)
                person_buffer.append(last_name)
                person_buffer.append(first_name)
                person_buffer.append(row[RANK])
                person_buffer.append(row[GENDER])
                self.personnel.append(person_buffer)
                if row[BLDG_NUMBER] not in self.building_info_details:
                    self.building_info_details.update({row[BLDG_NUMBER] : {} })
            """
            gameplan:
            check to see if the key exists already, if key exits, then we can populate the dictionary in the key,
            if key does not exist yet, add the key in the dictionary then populate like so
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

            for person_deets in self.personnel:
                #['19735', '3304', 'GONZALES', ' OSCAR', 'E-4', 'M']
                bldg = person_deets[0]
                room_number = person_deets[1]
                last_name = 2
                first_name = 3
                rank = 4
                gender = 5
                #update the bldg with a new key, that consist of these people 
                self.building_info_details[bldg].update({room_number : {}})
                room_details =  self.building_info_details[bldg][room_number]
                room_details.update({"last" : person_deets[last_name]})
                room_details.update( {"first" : person_deets[first_name] })
                room_details.update( {"rank" : person_deets[rank] })
                room_details.update( {"sex" : person_deets[gender] })
                room_details.update( {'company': ""}) #blank for now, you have to edit
                room_details.update( {'phone_number': ""})
                room_details.update( {'comments': ""})
            print()
                
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
            case 9999: #motherroster
                self._process_emh()

        #we might probably stop using self.personnel someday
        #for speed? and computing efficiency
        return self.personnel
    
    def print_personnel(personnel: list):
        #helper function to print personnels
        print(personnel)

def main():

    mother_roster = extract_from_csv("racks_roster/emh_roster.csv", 9999)
    dict_building_info = {**mother_roster.building_info_details}


    data = dict_building_info
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("racksdata.html")

    html_output = template.render(data=data, datenow=datetime.now().date())
    with open("./output/output.html", "w", encoding="utf-8") as f:
        f.write(html_output)




if __name__ == "__main__":  
    print("WARNING, you have to make ./output/ first and racks_roster/ directories before use")
    main()
    





  
