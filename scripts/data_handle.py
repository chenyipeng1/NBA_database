import chardet
import logging
import os
import pandas as pd
import sys as sys



def main(argv=None):
	""""
	Utilize Pandas library to read in both UNSD M49 country and area .csv file
	(tab delimited) as well as the UNESCO heritage site .csv file (tab delimited).
	Extract regions, sub-regions, intermediate regions, country and areas, and
	other column data.  Filter out duplicate values and NaN values and sort the
	series in alphabetical order. Write out each series to a .csv file for inspection.
	"""
	if argv is None:
		argv = sys.argv

	# Setting logging format and default level
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

	# Read Season data (check encoding)
	nba_info_csv = './input/csv/Seasons_Stats.csv'
	encoding = find_encoding(nba_info_csv)
	nba_data_frame_b = read_csv(nba_info_csv, encoding, ',')

	nba_data_frame = trim_columns(nba_data_frame_b)
	csv = './output/nba_info_trimmed.csv'
	write_series_to_csv(nba_data_frame, csv, ',', False)


	# Write team name to a .csv file
	name = extract_filtered_series(nba_data_frame, ['Tm'])
	name_csv = './output/team_name.csv'
	write_series_to_csv(name, name_csv, ',', False)

	# Write season to a .csv file
	name = extract_filtered_series(nba_data_frame, ['Year', 'G'])
	dic = {}
	for index, row in name.iterrows():
		if int(row['Year']) not in dic.keys():
			dic[int(row['Year'])] = int(row['G'])
		if dic[int(row['Year'])] < int(row['G']):
			dic[int(row['Year'])] = int(row['G'])
	d = {'season':list(dic.keys()), 'game':list(dic.values())}
	df = pd.DataFrame(data=d)
	name_csv = './output/season.csv'
	write_series_to_csv(df, name_csv, ',', False)

	# Read Hospital Information data (check encoding)
	player_info_csv = './input/csv/Players.csv'
	encoding = find_encoding(player_info_csv)
	player_data_frame_b = read_csv(player_info_csv, encoding, ',')

	player_data_frame = trim_columns(player_data_frame_b)
	csv = './output/player_info_trimmed.csv'
	write_series_to_csv(player_data_frame, csv, ',', False)

	# Write Player data, all in the player_data_frame

	# Write State to a .csv file
	name = extract_filtered_series(player_data_frame, ['birth_state'])
	name_csv = './output/state.csv'
	write_series_to_csv(name, name_csv, ',', False)	

	# Write Colleage to a .csv file
	name = extract_filtered_series(player_data_frame, ['collage'])
	name_csv = './output/college.csv'
	write_series_to_csv(name, name_csv, ',', False)	

def extract_filtered_series(data_frame, column_name):
	"""
	Returns a filtered Panda Series one-dimensional ndarray from a targeted column.
	Duplicate values and NaN or blank values are dropped from the result set which is
	returned sorted (ascending).
	:param data_frame: Pandas DataFrame
	:param column_name: column name string
	:return: Panda Series one-dimensional ndarray
	"""
	return data_frame[column_name].drop_duplicates().dropna().sort_values(by=column_name)


def read_csv(path, encoding, delimiter=','):
	"""
    Utilize Pandas to read in *.csv file.
    :param path: file path
    :param delimiter: field delimiter
    :return: Pandas DataFrame
    """

	# UnicodeDecodeError: 'utf-8' codec can't decode byte 0x96 in position 450: invalid start byte
	# return pd.read_csv(path, sep=delimiter, encoding='utf-8', engine='python')

	return pd.read_csv(path, sep=delimiter, encoding=encoding, engine='python')
    # return pd.read_csv(path, sep=delimiter, engine='python')


def write_series_to_csv(series, path, delimiter=',', row_name=True):
	"""
	Write Pandas DataFrame to a *.csv file.
	:param series: Pandas one dimensional ndarray
	:param path: file path
	:param delimiter: field delimiter
	:param row_name: include row name boolean
	"""
	series.to_csv(path, sep=delimiter, index=row_name)

def find_encoding(fname):
	r_file = open(fname, 'rb').read()
	result = chardet.detect(r_file)
	charenc = result['encoding']
	return charenc

def trim_columns(data_frame):
	"""
	:param data_frame:
	:return: trimmed data frame
	"""
	trim = lambda x: x.strip() if type(x) is str else x
	return data_frame.applymap(trim)




if __name__ == '__main__':
	sys.exit(main())


