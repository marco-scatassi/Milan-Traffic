- **Data.rar**: this archive contains raw data relative to traffic flow and weather conditions of some street in Milan between 2022-01-17T00:20 and 2022-01-31T00:30. In particular, data was obtained using the Tom Tom API and the Open Weather API.

- **Data_preparation.py**: this python file contains the code necessary to manipulate raw data and generate the DB.csv file and the files that are contained in DB.rar.

- **DB.rar**: this archive is a collection of csv files, each of which contains a json with traffic and weather information relative to a particular street and time.

- **DB.csv**: this is a csv version of DB.rar 

- **Flow_Weather.knwf**: this knime workflow is used to identify dates between 2022-01-17T00:20 and 2022-01-31T00:30 where traffic and weather information are not available.

- **DB_with_missing.csv**: this is the csv obtained adding missing data to the DB.csv file.

The Data_preparation.py was created togheter with Niccolò Puccinelli (https://www.linkedin.com/in/niccol%C3%B2-puccinelli-b1ba2a232/) and Greta Gravina (https://www.linkedin.com/in/greta-gravina-742925189/).
