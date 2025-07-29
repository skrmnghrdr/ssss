#!/usr/bin/python3
import csv
import re

#setup the dang debugger to actually go here
"""
goal is to use regex to extract anything that would say
11th or 11thCyber then we could fish out that data and put it here,
this would be a new object everytime someone would like to initialize a csv. 

do not trust the user for any inputs, hence why we do not get data from the csv to execute
that wouldbe retarded af. only extract and put, not execute.



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

    def _get_personnel(self):
        """helper function for future implementation
        of web interface, debating on jsonifying it

        Returns:
            self.personnel: array type 2D
            [
                [data, data, data ...], 
                [data, data, data ....]
            ]
        """
        max_row_len = 0

        with open(self.path) as excel_spread_cheeks:
            reader = csv.reader(excel_spread_cheeks)
            print("Debuganchor")
            match self.csv_type:
                
                case 19751: #HHC
                    max_row_len = 7
                    #implement their own function here so this would be cleaner
                    for _ in range(15):
                        next(excel_spread_cheeks)
                    for row in reader:
                        #eventuall replace 11th wtih regex
                        if row[5] in ("11TH", "CYBER"):
                            self.personnel.append(self.pretty_format(row[0:7], max_row_len, self.csv_type))
                        elif row[13] in ("11TH", "CYBER"):
                            self.personnel.append(self.pretty_format(row[8:15], max_row_len, self.csv_type))
                        elif row[21] in  ("11TH", "CYBER"):
                            self.personnel.append(self.pretty_format(row[16:23], max_row_len, self.csv_type))

                case 19753: #rice 
                    max_row_len = 6
                    for _ in range(15):
                        next(excel_spread_cheeks)
                    for row in reader:
                        if (row[5] in ("11TH", "CYBER")):
                            self.personnel.append(self.pretty_format(row[0:6], max_row_len, self.csv_type))
                        elif (row[13] in  ("11TH", "CYBER")):
                            self.personnel.append(self.pretty_format(row[8:14], max_row_len, self.csv_type))
                        elif (row[21] in  ("11TH", "CYBER")):
                            self.personnel.append(self.pretty_format(row[16:22], max_row_len, self.csv_type))

                case 19755: #Alpha
                    max_row_len = 7
                    for _ in range(15):
                        next(excel_spread_cheeks)
                    for row in reader:
                        if (row[5] in ("11TH", "CYB")):
                            self.personnel.append(self.pretty_format(row[0:6], max_row_len, self.csv_type))
                        elif (row[13] in  ("11TH", "CYB")):
                            self.personnel.append(self.pretty_format(row[8:14], max_row_len, self.csv_type))
                        elif (row[21] in  ("11TH", "CYB")):
                            self.personnel.append(self.pretty_format(row[16:22], max_row_len, self.csv_type))

                case 19757: #potatoes
                    #this is a special case since they massacred the format on this one
                    max_row_len = 7
                    for _ in range(12):
                        next(excel_spread_cheeks)
                    for row in reader:
                        if (row[5] in ("11TH", "CYB")):
                            self.personnel.append(self.pretty_format(row[0:6], max_row_len, self.csv_type))
                        elif (row[16] in  ("11TH", "CYB")):
                            self.personnel.append(self.pretty_format(row[11:17], max_row_len, self.csv_type))
                        elif (row[27] in  ("11TH", "CYB")):
                            self.personnel.append(self.pretty_format(row[22:28], max_row_len, self.csv_type))

                    pass

        #we might probably stop using self.personnel someday
        #for speed? and computing efficiency
        return self.personnel
    
    def print_personnel(personnel: list):
        #helper function to print personnels
        print(personnel)

def main():
    test = []

    hhc_roster = extract_from_csv("racks_roster/19751hhc.csv", 19751)

    test_roster = extract_from_csv("racks_roster/19753_199th July Barracks Tracker(19753).csv", 19753)

    alpha_roster = extract_from_csv("racks_roster/19755_ACO_FEB25(19755).csv", 19755)
    
    potato_roster = extract_from_csv("racks_roster/19757_104thMICO_Roster(Sheet1).csv", 19757)
        #alpha_roster = extract_from_csv("racks/19755_ACO_FEB25(19755).csv", 19755)
    test = [*hhc_roster.personnel, *test_roster.personnel, *alpha_roster.personnel, *potato_roster.personnel]

    print(test)

    for things in test:
        print(things)


if __name__ == "__main__":
    main()
    