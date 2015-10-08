import h5py


class HDFOutputFactory:
    def __init__(self):
        pass

    def save_session_to_hdf5(self, session, output_file_name):
        hdf5_file = h5py.File(output_file_name, 'w')
        session_path = self.get_session_path(hdf5_file)

        # Session Data must be inserted first
        #  H5PY won't instantiate a group (/session/##) without a dataset
        self.insert_session_data(hdf5_file, session_path, session)
        self.insert_session_attributes(hdf5_file, session_path, session)
        hdf5_file.close()

    @staticmethod
    def get_session_path(hdf5_file):
        if len(hdf5_file.items()) > 0:
            session_id = len(hdf5_file['/session'].items()) + 1
        else:
            session_id = 1

        return '/session/%02d' % session_id

    @staticmethod
    def insert_session_attributes(hdf5_file, session_path, session):
        for attribute_name, attribute_value in session.attributes.iteritems():
            hdf5_file[session_path].attrs[attribute_name] = attribute_value

    @staticmethod
    def insert_session_data(hdf5_file, session_path, session):
        band_id = 1
        for band in session.bands:
            band_path = '%s/%s/band_%03d/' % (session_path, session.measurement_type, band_id)
            hdf5_file[band_path] = band.scans_to_numpy()
            for attribute_name, attribute_value in band.attributes.iteritems():
                hdf5_file[band_path].attrs[attribute_name] = attribute_value
            band_id += 1
