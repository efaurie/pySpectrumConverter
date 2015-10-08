from os import path

from hdf_parser_functions import *
from rfeye_parser_functions import *
from filename_parser_fns import *

from RecordingSession import RecordingSession


class SessionFactory:
    def __init__(self):
        return

    def session_from_hdf_file(self, input_path):
        data_file = open_hdf_file(input_path)
        bands = parse_hdf_file(data_file)

        session = RecordingSession(bands)
        self.add_attributes(input_path, session)

        return session

    def session_from_rfeye_file(self, input_path):
        data_file = open_rfeye_file(input_path)
        bands = parse_rfeye_file(data_file)

        session = RecordingSession(bands)
        self.add_attributes(input_path, session)

        return session

    def add_attributes(self, input_path, session):
        filename = self.filename_from_path(input_path)
        session.set_measurement_type(measurement_type_from_name(filename))
        session.add_attribute('Filename', filename)
        session.add_attribute('Date', date_from_name(filename))
        session.add_attribute('Location', site_from_name(filename))
        session.add_attribute('Sensor', sensor_from_name(filename))

    @staticmethod
    def filename_from_path(file_path):
        return path.split(file_path)[1]
