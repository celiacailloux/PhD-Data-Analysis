# pylint: disable=no-member,import-error,invalid-name,too-many-instance-attributes
# pylint: disable=too-many-arguments

"""Convinience interface to the cinfdata database"""

from __future__ import unicode_literals, print_function

from os import path
import os
import sys
from time import time
from operator import itemgetter
# Py 2/3 compatible import of pickle
try:
    import cPickle as pickle
except ImportError:
    import pickle
import logging
from collections import namedtuple

import numpy as np


# Set up logging
logging.basicConfig(format='%(name)s: %(message)s', level=logging.INFO)
LOG = logging.getLogger('CINFDATA')


# First try and import MySQLdb ..
try:
    import MySQLdb
    CONNECT_EXCEPTION = MySQLdb.OperationalError
    LOG.info('Using MySQLdb as the database module')
except ImportError:
    try:
        # .. if that fails, try with pymysql
        import pymysql as MySQLdb
        MySQLdb.install_as_MySQLdb()
        CONNECT_EXCEPTION = MySQLdb.err.OperationalError
        LOG.info('Using pymysql as the database module')
        if sys.version_info.major > 2:
            LOG.info('pymysql is known to be broken with Python 3. Consider '
                     'installing mysqlclient!')
    except ImportError:
        # if that fails, just set it to None to indicate that we have no db module
        MySQLdb = None  # pylint: disable=invalid-name
        LOG.info('Using cinfdata without database')


class CinfdataError(Exception):
    """Generic Cinfdata exception"""


class Cinfdata(object):
    """Class that provides easy access to the cinfdata database with optional local caching"""

    database_name = 'cinfdata'
    main_host = 'servcinf-sql.fysik.dtu.dk'#'servcinf-sql'
    main_port = '3306'
    secondary_host = '127.0.0.1'
    descriptions_table = 'dateplots_description'
    username = 'cinf_reader'
    password = 'cinf_reader'

    def __init__(self, setup_name, local_forward_port=9999, use_caching=False,
                 grouping_column=None, label_column=None,
                 allow_wildcards=False,
                 cache_dir=None, cache_only=False, log_level='INFO',
                 metadata_as_named_tuple=False):
        """Initialize local variables
        Args:
            setup_name (str): The setup name used as a table name prefix in the database.
                E.g. 'vhp' or 'stm312'.
            local_forward_port (int): The local port number that a port forward to the
                database was created on. Default is 9999.
            use_caching (bool): If set to True, this module will locally cache data and
                metadata. WARNING: DO NOT use caching unless you understand the limitations.
            grouping_column (str): The name of the column used for grouping
                column (if different from __init__ value)
            label_column (str): The name of the column that is used for the
                label (if different from __init__ value)
            cache_dir (str): The directory to use for the cache. As default is used a
                directory named 'cache' in the same folder that this file (cinfdata.py) is
                located in
            cache_only (bool): If set to True, no connection will be formed to the database
            log_level (str): A string that indicates the log level, either 'INFO' (default)
                or 'DEBUG' for more output or 'DISABLE' to disable any further output

        .. warning:: Be careful with caching. It will keep returning the version of the
            data from the first time it was retrieved. If data is later added to the
            dataset or it is altered, the data that this module returns, when using
            caching, will not reflect it.

        """
        start = time()

        # Setup logging
        if log_level == 'DEBUG':
            LOG.setLevel(logging.DEBUG)
        elif log_level == 'DISABLE':
            LOG.setLevel(logging.CRITICAL)

        # Init database connection
        self.connection = None
        self.cursor = None
        if MySQLdb is not None and not cache_only:
            self._init_database_connection(local_forward_port)

        # Init cache
        self.cache = None
        if use_caching:
            self.cache = Cache(cache_dir, setup_name)

        # Init local variables
        self.grouping_column = grouping_column
        self.label_column = label_column
        self.setup_name = setup_name
        self._column_names = None

        # Init the metadata named tuple (we need database for this)
        self._metadata_as_named_tuple = metadata_as_named_tuple
        if metadata_as_named_tuple:
            self._metadata_named_tuple = namedtuple('Metadata', self.column_names)

        # Figure out whether the xy_values table has an id
        if self.cache and self.cache.has_infoitem('general', 'xy_values_table_has_id'):
            self._xy_values_table_has_id = \
                self.cache.load_infoitem('general', 'xy_values_table_has_id')
        else:
            if self.cursor is not None:
                self.cursor.execute('DESCRIBE xy_values_{}'.format(setup_name))
                column_names = [item[0] for item in self.cursor.fetchall()]
                self._xy_values_table_has_id = 'id' in column_names
                if self.cache:
                    self.cache.save_infoitem('general', 'xy_values_table_has_id',
                                             self._xy_values_table_has_id)
            else:
                CinfdataError('Could not determine if xy_values_table has id')

        # Init queries
        if self._xy_values_table_has_id:
            self.data_query = 'SELECT x, y FROM xy_values_{} WHERE measurement=%s '\
                              'ORDER BY id'.format(setup_name)
        else:
            self.data_query = 'SELECT x, y FROM xy_values_{} WHERE measurement=%s '\
                              'ORDER BY x'.format(setup_name)
        self.metadata_query = ('SELECT *, UNIX_TIMESTAMP(time) FROM measurements_{} '
                               'WHERE id=%s'.format(setup_name))
        if allow_wildcards:
            self.group_query = 'SELECT `id` FROM measurements_{} WHERE `{{}}` LIKE %s order by '\
                               'id'.format(setup_name)
        else:
            self.group_query = 'SELECT `id` FROM measurements_{} WHERE `{{}}` = %s order by '\
                               'id'.format(setup_name)

        LOG.debug('Completed init in %s s', time() - start)

    def _init_database_connection(self, local_forward_port):
        """Initialize the database connection"""
        LOG.debug('Initialize database connection')
        try:
            self.connection = MySQLdb.connect(
                host=self.main_host, user=self.username, passwd=self.password,
                db=self.database_name,
            )
            LOG.info('Using direct db connection: cinfdata:3306')
        except CONNECT_EXCEPTION:
            try:
                self.connection = MySQLdb.connect(
                    host=self.secondary_host, port=local_forward_port,
                    user=self.username, passwd=self.password, db=self.database_name
                )
                LOG.info('Using port forward db connection: %s:%s', self.secondary_host,
                         local_forward_port)
            except CONNECT_EXCEPTION:
                self.connection = None
                LOG.info('No database connection')

        if self.connection is not None:
            self.cursor = self.connection.cursor()

    def get_data(self, measurement_id, scaling_factors=None):
        """Get data for measurement_id

        Args:
            measurement_id (int): The id of the measurement to fetch
            scaling_factors (sequence): A sequence of scaling factors for the
                columns. If a value of None is supplied for any of the columns,
                that column will not be scaled. Examples values could be (10*6, None)

        Returns:
            numpy.array: The measurement as a numpy array
        """
        # Check if this dataset is in the cache and if so return
        data = None
        if self.cache:
            data = self.cache.load_data(measurement_id)

        # Try and get the dataset from the database
        if data is None and self.cursor is not None:
            start = time()
            self.cursor.execute(self.data_query, (measurement_id,))
            data = np.array(self.cursor.fetchall())
            LOG.debug('Fetched data for id %s from database in %0.4e s', measurement_id,
                      time() - start)

            # If there was data in the db, possibly save to cache and return
            if data.size > 0:
                if self.cache:
                    self.cache.save_data(measurement_id, data)

        if data is None:
            error = 'No data found for id {}'.format(measurement_id)
            raise CinfdataError(error)

        # Apply scaling factors
        if scaling_factors is not None:
            for column_number, scaling_factor in enumerate(scaling_factors):
                if scaling_factor is not None:
                    data[:, column_number] *= scaling_factor

        return data

    def get_metadata(self, measurement_id):
        """Get metadata for measurement_id"""
        # Check if the metadata is in the cache
        metadata = None
        if self.cache:
            if self.cache.has_infoitem('metadata', measurement_id):
                metadata = self.cache.load_infoitem('metadata', measurement_id)


        # Try and get the metadata from the database
        if metadata is None and self.cursor is not None:
            # Get the data
            start = time()
            self.cursor.execute(self.metadata_query, (measurement_id,))
            metadata_raw = self.cursor.fetchall()
            LOG.debug('Fetched metadata for id %s from database in %0.4e s',
                      measurement_id, time() - start)

            # Raise error if there was not exactly 1 line
            if len(metadata_raw) != 1:
                raise CinfdataError('There was not exactly 1 row of metadata returned '
                                    'for id {}'.format(measurement_id))

            # Convert metadata to dict
            metadata = dict(zip(self.column_names, metadata_raw[0]))

            # Save in cache if present
            if self.cache:
                self.cache.save_infoitem('metadata', measurement_id, metadata)

        # Raise error if we could not find any metadata
        if metadata is None:
            raise CinfdataError('No metadata found for id {}'.format(measurement_id))

        # Convert to namedtuple if requested
        if self._metadata_as_named_tuple:
            metadata = self._metadata_named_tuple(**metadata)

        return metadata

    def get_data_group(self, group_id, grouping_column=None, label_column=None,
                       scaling_factors=None):
        """Get a data group

        Args:
            group_id (object): The group id in the grouping column (can have
                different types depending on the type of the grouping column)
            grouping_column (str): The name of the column used for grouping
                column (if different from __init__ value)
            label_column (str): The name of the column that is used for the
                label (if different from __init__ value)
            scaling_factors (dict or sequence): If a sequence is given, it is assumed to
                be a pair of x and y scaling factiors. Where each of the components can
                be left out by giving a value of None. E.g: `(1E6, 1E-3)`, `(1E6, None)`
                or `(None, 1e-3)`. If a dict if given, it is assumed to be mapping of
                label values to scaling pairs as described above.

        Returns:
            dict: Mapping of ids to data

        """
        grouping_column = grouping_column if grouping_column is not None\
                          else self.grouping_column
        if grouping_column is None:
            msg = ('A grouping_column must be given either in __init__ or in '
                   'this method, in order to be able to get a group of data')
            raise CinfdataError(msg)

        group_key = (grouping_column, group_id)
        try:
            hash(group_key)
        except TypeError:
            msg = CinfdataError('group_id must be a immuteable type, not {}'.format(type(group_id)))

        # See the group lookup is in the cache
        ids = None
        if self.cache and self.cache.has_infoitem('groups', group_key):
            ids = self.cache.load_infoitem('groups', group_key)

        # If not known already, try and get the group from the database
        if ids is None and self.cursor is not None:
            if grouping_column not in self.column_names:
                raise CinfdataError(
                    'Grouping column "{}" is not among the metadata column names {}'\
                    .format(grouping_column, self.column_names)
                )
            self.cursor.execute(self.group_query.format(grouping_column), (group_id,))
            ids = [row[0] for row in self.cursor.fetchall()]
            if self.cache:
                self.cache.save_infoitem('groups', group_key, ids)

        # We need ids to proceed, so complain if they are not there
        if ids is None:
            raise CinfdataError('Unable to get ids for group, either from cache, '
                                'database or both')

        group_of_data = {}
        for id_ in ids:
            group_of_data[id_] = self.get_data(id_)

        if scaling_factors is not None:
            if isinstance(scaling_factors, dict):
                # Make sure we have label_column
                label_column = label_column if label_column is not None else self.label_column
                if label_column is None:
                    msg = ('A grouping_column must be given either in __init__ or in '
                           'this method, in order to be able to scale based on label value')
                    raise CinfdataError(msg)

                # Scale
                for id_, data in group_of_data.items():
                    metadata = self.get_metadata(id_)
                    label = metadata[label_column]
                    if label in scaling_factors:
                        self._scale(data, scaling_factors[label])

            else:
                for data in group_of_data.values():
                    self._scale(data, scaling_factors)

        return group_of_data

    def get_metadata_group(self, group_id, grouping_column=None):
        """Get a metadata group

        Args:
            group_id (object): The group id in the grouping column (can have
                different types depending on the type of the grouping column)
            grouping_column (str): The name of the column used for grouping
                column (if different from __init__ value)

        Returns:
            dict: Mapping of ids to metadata

        """
        grouping_column = grouping_column if grouping_column is not None\
                          else self.grouping_column
        if grouping_column is None:
            msg = ('A grouping_column must be given either in __init__ or in '
                   'this method, in order to be able to get a group of metadata')
            raise CinfdataError(msg)

        group_key = (grouping_column, group_id)
        try:
            hash(group_key)
        except TypeError:
            msg = CinfdataError('group_id must be a immuteable type, not {}'.format(type(group_id)))

        # See if the group lookup is in the cache
        ids = None
        if self.cache and self.cache.has_infoitem('groups', group_key):
            ids = self.cache.load_infoitem('groups', group_key)

        # If not known already, try and get the group from the database
        if ids is None and self.cursor is not None:
            if grouping_column not in self.column_names:
                raise CinfdataError(
                    'Grouping column "{}" is not among the metadata column names {}'\
                    .format(grouping_column, self.column_names)
                )
            self.cursor.execute(self.group_query.format(grouping_column), (group_id,))
            ids = [row[0] for row in self.cursor.fetchall()]
            if self.cache:
                self.cache.save_infoitem('groups', group_key, ids)

        # We need ids to proceed, so complain if they are not there
        if ids is None:
            raise CinfdataError('Unable to get ids for group, either from cache, '
                                'database or both')

        group_of_metadata = {}
        for id_ in ids:
            group_of_metadata[id_] = self.get_metadata(id_)

        return group_of_metadata


    def _scale(self, data, scaling_factors):
        """Scale columns in a data set with scaling factors

        Args:
            data (numpy.array): The data to scale
            scaling_factors (sequence): Sequence of scaling factors e.g: (1E6, 1E-3). If
                None is passed in an as a value, that column is not scaled e.g: (1E6, None)

        Return:
            numpy.array: Same array as data, but scaled. NOTE it is the same array, not a copy
        """
        for column_number, scaling_factor in enumerate(scaling_factors):
            if scaling_factor is not None:
                data[:, column_number] *= scaling_factor
        return data


    @property
    def column_names(self):
        """Return the columns names from the measurements table"""
        # Note, this could be done cleverer with a lazy property implementation, but it
        # is more difficult to read
        if self._column_names is not None:
            return self._column_names

        # Check if the column names is in the cache
        if self.cache and self.cache.has_infoitem('general', 'column_names'):
            self._column_names = self.cache.load_infoitem('general', 'column_names')
            return self._column_names

        # Try and get the column names from the database
        if self.cursor is not None:
            self.cursor.execute('DESCRIBE measurements_{}'.format(self.setup_name))
            column_names = [item[0] for item in self.cursor.fetchall()]
            # Add an fictitious column, which will contain time converted to unixtime
            column_names.append('unixtime')

            self._column_names = column_names
            if self.cache:
                self.cache.save_infoitem('general', 'column_names', column_names)
            return column_names

        raise CinfdataError('Column names not found')


def use_labels_in_groups(data_group, metadata_group, label_column):
    """Create new data and metadata groups that use labels as columns"""
    # Check for repeated labels
    labels = [metadata[label_column] for metadata in metadata_group.values()]
    if len(labels) != len(set(labels)):
        msg = "Cannot change keys to labels because the labels are not unique"
        raise CinfdataError(msg)

    data_group_label = {metadata_group[id_][label_column]: data
                        for id_, data in data_group.items()}
    metadata_group_label = {metadata_group[id_][label_column]: metadata
                            for id_, metadata in metadata_group.items()}
    return data_group_label, metadata_group_label


class CinfdataCacheError(CinfdataError):
    """Exception for Cinfdata Cache related errors"""


class Cache(object):
    """Simple file based cache for cinf database loopkups"""

    cache_version = 2

    def __init__(self, cache_dir, setup_name):
        """Initialize local variables"""
        if cache_dir is None:
            this_dir = path.dirname(path.abspath(__file__))
            self.cache_dir = path.join(this_dir, 'cache')
        else:
            self.cache_dir = cache_dir
        LOG.info('Using cache dir: %s', self.cache_dir)

        # Form folder paths, subfolder for each setup and under that a subfolders for data
        self.setup_dir = path.join(self.cache_dir, setup_name)
        self.data_dir = path.join(self.setup_dir, 'data')
        dirs = [self.cache_dir, self.setup_dir, self.data_dir]
        # Check permission on dirs and create them if possible
        self._check_and_create_dirs(dirs)

        # Form infoitem file path and load if present
        self.infoitem_file = path.join(self.setup_dir, 'infoitem.pickle')
        if path.exists(self.infoitem_file):
            error = None
            try:
                start = time()
                with open(self.infoitem_file, 'rb') as file_:
                    self.infoitem = pickle.load(file_)
                LOG.debug('Loaded infoitem dict in %s s', time() - start)
            except IOError:
                error = 'The file: {}\nwhich is needed for the cache, exists, but is '\
                        'not readable'
            except pickle.UnpicklingError:
                error = 'Loading and interpreting the infoitem file: {}\nfailed. '\
                        'Please report this as a bug.'
            if error is not None:
                raise CinfdataCacheError(error.format(self.infoitem_file))

            loaded_cache_version = self.infoitem.get('general', {}).get('cache_version', 1)
            if loaded_cache_version < self.cache_version:
                message = ('Your cache is of the older version {}, wheres cinfdata now '
                           'uses {}. Please delete your cache dir and start building it '
                           'from scratch.')
                raise CinfdataError(message.format(loaded_cache_version, self.version))
        else:
            self.infoitem = {
                'general': {'cache_version': self.cache_version},
                'metadata': {},
                'groups': {},
            }

    @staticmethod
    def _check_and_create_dirs(dirs):
        """Check permissions of the cache directories and create them if necessary"""
        # Check/create directories
        for dir_ in dirs:
            if path.exists(dir_):
                # If the path dir_ exists, check that it is a dir, and that it is read and
                # writeable
                error = None
                if not path.isdir(dir_):
                    error = 'The path: {}\nwhich is needed for the cache as a directory '\
                            'exists, but is not a directory'
                if not os.access(dir_, os.W_OK):
                    error = 'The directory: {}\nwhich is needed for the cache exists, '\
                            'but is not writeable'
                if not os.access(dir_, os.R_OK):
                    error = 'The directory: {}\nwhich is needed for the cache exists, '\
                            'but is not readable'
                if error is not None:
                    raise CinfdataCacheError(error.format(dir_))
            else:
                # If that path does not exist, create it
                try:
                    os.mkdir(dir_)
                except OSError:
                    error = 'Creation of the directory: {}\n which is neede for the '\
                            'cache failed. Please check permissions of the parent folder.'
                    raise CinfdataCacheError(error.format(dir_))

    def save_data(self, measurement_id, data):
        """Save a dataset to the cache

        Args:
            measurement_id (int): The database id of the dataset to save
            data (numpy.array): The data as a numpy array

        Returns:
            str: The file location of the saved array

        Raises:
            CinfdataCacheError: If data is an object array (a numpy array that contains
                generic Python objects)
        """
        start = time()
        filepath = path.join(self.data_dir, '{}.npy'.format(measurement_id))
        if data.dtype.hasobject:
            raise CinfdataCacheError('Saving object arrays is not supported')
        np.save(filepath, data)
        LOG.debug('Saved data for id %s to cache in %0.4e s', measurement_id, time() - start)
        return filepath

    def load_data(self, measurement_id):
        """Load a dataset from the cache

        Args:
            measurement_id (int): The database id of the dataset to load
        """
        start = time()
        # Form filepath and check if the file exists
        filepath = path.join(self.data_dir, '{}.npy'.format(measurement_id))
        if not path.exists(filepath):
            return None

        # Try and load the file and raise error is it fails
        try:
            data = np.load(filepath)
        except IOError:
            message = 'The cache file:\n{}\nexists, but could not be loaded. '\
                      'Check file permissions'
            raise CinfdataCacheError(message.format(filepath))
        LOG.debug('Loaded data for id %s from cache in %0.4e s', measurement_id,
                  time() - start)
        return data

    def save_infoitem(self, group_name, key, infoitem):
        """Save various information in a cached dictionary

        Args:
            group_name (unicode): The group of infoitems to save in. Currently supported
                groups are: 'general'; for general program settings, 'metadata'; to save
                metadata in and 'group'; to save group information in.
            key (dict key): The key to save this information item under
            infoitem (object): The information object to save under ``key``

        Raises:
            CinfdataCacheError: If there are problems with saving the metadata to disk

        """
        start = time()
        try:
            group = self.infoitem[group_name]
        except KeyError:
            message = 'The group name \'{}\' is invalid. Only {} are allowed.'
            raise CinfdataCacheError(message.format(group_name, self.infoitem.keys()))
        group[key] = infoitem
        self._save_infoitems_to_file()
        LOG.debug('Saved infoitem for group \'%s\', key \'%s\' to cache in %0.4e s',
                  group_name, key, time() - start)

    def _save_infoitems_to_file(self):
        """Save the infoitem dict to file"""
        error = None
        try:
            with open(self.infoitem_file, 'wb') as file_:
                pickle.dump(self.infoitem, file_)
        except IOError:
            error = 'The file: {}\nwhich is needed by the cache is not writable. '\
                    'Check the file permissions.'.format(self.infoitem_file)
        except pickle.PickleError:
            error = 'Python was unable to save the infoitem dict. Report this as a bug.'
        if error is not None:
            raise CinfdataCacheError(error)

    def load_infoitem(self, group_name, key):
        """Load information from a cached dictionary

        Args:
            group_name (unicode): The group to load the infoitem from
            key (dict key): The key of the infoitem to load
        """
        start = time()
        try:
            group = self.infoitem[group_name]
        except KeyError:
            message = 'The group name \'{}\' is invalid. Only {} are allowed.'
            raise CinfdataCacheError(message.format(group_name, self.infoitem.keys()))
        metadata = group[key]
        LOG.debug('Loaded infoitem for group \'%s\', key \'%s\' from cache in %0.4e s',
                  group_name, key, time() - start)
        return metadata

    def has_infoitem(self, group_name, key):
        """"""
        return group_name in self.infoitem and key in self.infoitem[group_name]


def run_module():
    """Run the module"""
    #cinfdata = Cinfdata('tof', use_caching=True, log_level='DEBUG')
    #print(cinfdata.get_data(5417))
    #print(cinfdata.get_metadata(5417))

    cinfdata = Cinfdata('sniffer', use_caching=True, log_level='DEBUG',
                        grouping_column='time', label_column='mass_label')
    print(cinfdata.get_data(5421))
    print(cinfdata.get_metadata(5421))
    print()
    datas = cinfdata.get_data_group(
        "2017-03-17 17:42:48",
        scaling_factors={'M4': (None, 10)},
    )
    from matplotlib import pyplot as plt
    for n, data in enumerate(datas.values()):
        if n <= 6:
            continue
        plt.plot(data[:, 0], data[:, 1])
    plt.yscale('log')
    plt.show()
if __name__ == '__main__':
    run_module()