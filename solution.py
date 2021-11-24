import csv
import json
import sys
from os import path

class Parse:
    """ A class to parse a csv of a Direct Assessment Evaluation,
        preform some data manipulation, then output the results
        to a json file.

    Args:
        file (str):      File path to csv file

    Methods:
        read_score(column: int)
            Create dict with key of passed column and score as value
        calculate_average():
            Take list of scores and create dict with mean scores.
        calculate_high_low():
            Find highest and lowest scores.
        output_json(file: str)
            Write non-empty dictionaries to the output json file.
    """

    def __init__(self, file: str):
        """ The constructor for Parse class.

        Args:
            file (str):      File path to csv file

        Raises:
            FileExistsError:    Passed csv file does not exist.
        """
        self.file = path.abspath(file)
        if not path.isfile(self.file):
            raise FileExistsError(f"The file {path.abspath(self.file)} does not exist.")
        self.data = {}
        self.averages = {}
        self.high_low = {"highest": {"names": [], "value": 0}, "lowest": {"names": [], "value": 100}}


    def read_score(self, column: int):
        """ Fill dictionary with data from provided csv with key
            from the passed column and the scores as a list of values.

        Args:
            column (int):   The column to be used for the key.

        Raises:
            ValueError:     The score found is the csv file is not of the correct format.
            TypeError:      The column is not an integer.
            IndexError:     The passed column does not exist.
        """

        if type(column) != int:
            raise TypeError(f"Column passed {column} is not an integer.")

        with open(self.file, encoding="utf-8") as csvfile:
            # Load file and remove the header line, finding the column containing scores
            line_reader = csv.reader(csvfile, delimiter=",")
            score_position = next(line_reader).index("q1 score")

            for row in line_reader:
                # Error checking on score
                if not row[score_position].isnumeric() or not 0 <= int(row[score_position]) <= 100:
                    raise ValueError(
                        f"Score {row[score_position]} given by {row[2]} in sentence {row[0]} is not an integer between 0 and 100.")
                score = int(row[score_position])

                # Add all keys to data dict
                try:
                    key = row[column]
                except IndexError:
                    raise IndexError("The passed column does not exist.")

                if key in self.data:
                    self.data[key].append(score)
                else:
                    self.data[key] = [score]


    def calculate_average(self):
        """ Take list of scores and create dict with mean scores. """
        for key in self.data:
            lst = self.data[key]
            average = sum(self.data[key]) / len(self.data[key])
            # Store average, rounding to 2 dp, e.g. 48.28
            self.averages[key] = round(average, 2)


    def calculate_high_low(self):
        """ Find the highest and lowest scores.
        If that score already exists, then append the key to a list.

        Raises:
            ValueError:     Averages need to be calculated before this function.
        """
        highest_val = 0
        lowest_val = 100
        if self.averages == {}:
            raise ValueError("Please first calculate averages before highest/lowest")
        for key in self.averages:
            # self.compare(key, "highest")
            # self.compare(key, "lowest")
            average = self.averages[key]

            # Compare for highest
            if average > self.high_low["highest"]["value"]:
                self.high_low["highest"]["value"] = average
                self.high_low["highest"]["names"] = [key]
            elif average == self.high_low["highest"]["value"]:
                self.high_low["highest"]["names"].append(key)

            # Compare for lowest
            if average < self.high_low["lowest"]["value"]:
                self.high_low["lowest"]["value"] = average
                self.high_low["lowest"]["names"] = [key]
            elif average == self.high_low["lowest"]["value"]:
                self.high_low["lowest"]["names"].append(key)


    def output_json(self, file: str):
        """ Write non-empty dictionaries to the output json file.

        Args:
            file (string):      File path to output json file.
        """
        # Create output
        output = {}
        if self.averages:
            output["averages"] = self.averages
        if self.high_low["highest"]["names"]:
            output["highest"] = self.high_low["highest"]
        if self.high_low["lowest"]["names"]:
            output["lowest"] = self.high_low["lowest"]

        # Write to json file
        with open(file, "w") as json_file:
            json.dump(output, json_file, indent=4)


def main():
    csv_file = sys.argv[1]

    ex_1 = Parse(csv_file)
    ex_1.read_score(2)
    ex_1.calculate_average()
    ex_1.output_json("1.json")

    ex_2 = Parse(csv_file)
    ex_2.read_score(0)
    ex_2.calculate_average()
    ex_2.calculate_high_low()
    ex_2.output_json("2.json")


if __name__ == "__main__":
    main()
