#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 03:17:41 2017

@author: scott
"""
import os, platform, re, codecs
import time, datetime, pytz  #all three seem necessary for dealing with timezones.
import numpy as np

float_match = '[-]?\d+[\.]?\d*(e[-]?\d+)?'     #matches floats like '-3.5e4' or '7' or '245.13' or '1e-15'
#note, no white space included on the ends! Seems to work fine.
timestamp_match = '([0-9]{2}:){2}[0-9]{2}'     #matches timestamps like '14:23:01'

def numerize(data):
    for col in data['data_cols']: #numerize!
        data[col] = np.array(data[col])

def get_empty_set(cols, **kwargs):
        #get the colheaders and make space for data
        # cols should be a set
    data = {}
    data.update(kwargs)
    for col in cols:
        data[col] = []
    data['data_cols'] = cols
    return data

def parse_timezone(tz=None):
    '''
    Gets a timezone object from a timezone string. Includes some abbreviations
    useful for Scott. If the input is not a string, it is returned as is.
    '''
    abbreviations = {'CA':'US/Pacific', 'DK':'Europe/Copenhagen',}
    if tz in abbreviations:
        return pytz.timezone(abbreviations[tz])
    elif type(tz) is str:
        return pytz.timezone(tz)
    else:
        return tz

def parse_date(line):
    date_match = '([0-9]{2}[/\-\.]){2}[0-9]{4}'
    # ^ matches dates like '01/15/2018' or '09-07-2016' or '04.20.2019'. Saw that last one in Degenhart's EC-Lab data
    #^  mm/dd/yyyy, as EC lab does
    # older EC-Lab seems to have dashes in date, and newer has slashes.
    # Both seem to save month before day, regardless of where the data was taken or .mpt exported.
    d1 = re.search(date_match, line)
    if d1:
        date1 = d1.group()
        yyyy, mm, dd  = date1[-4:], date1[:2], date1[3:5]
        date = yyyy + '/' + mm + '/' + dd
        return date

    date_match_2 = '[0-9]{4}([/-][0-9]{2}){2}'          #matches dates like '2018/01/15' or '2018-09-07'
    #^  yyyy/mm/dd, as cinfdata does
    d2 = re.search(date_match_2, line)
    if d2:
        date2 = d2.group()
        yyyy, mm, dd = date2[:4], date2[5:7], date2[-2:]
        date = yyyy + '/' + mm + '/' + dd
        return date

    month_names = {'01':'January', '02':'February', '03':'March', '04':'April',
                   '05':'May', '06':'June', '07':'July', '08':'August',
                   '09':'September', '10':'October', '11':'November', '12':'December'}
    month_match = '(' + ''.join(list([v[:3] + '|' for v in month_names.values()]))[:-1] + ')' + '[a-z]*(\.)?'
    date_match_3 = month_match + ' [0-9]+, [0-9]{4}'    #matches dates like 'Apr. 12, 2019' or 'August 1, 2019'
    d3 = re.search(date_match_3, line)
    if d3:
        date3 = d3.group()
        month = re.search(month_match, date3).group()
        mm = next(key for key, value in month_names.items() if value[:3]==month[:3])
        yyyy = date3[-4:]
        dd = re.search('[0-9]+,', date3).group()[:-1]
        date = yyyy + '/' + mm + '/' + dd
        return date

    print('can\'t find date in line \'' + line + '\'. parse_date() is returning None.')
    return None


def timestring_to_epoch_time(timestring, date=None, tz=None, verbose=True,
                             form='%Y/%m/%d %H:%M:%S', out='tstamp'):
    '''
    A way to convert a number of timestrings read from my data into a standard-formatted
    date and time, and then to an epoch (unix) time.

    tz is the Timezone, which is only strictly necessary when synchronizing
    data taken at different places or accross dst at a place with different dst
    implementation than the local (dst is stupid!).
    If timezone is a number, it is interpreted as the offset from GMT of the
    data.

    The epoch time is referred to here and elsewhere as tstamp.
    '''
    if tz is not None:
        tz = parse_timezone(tz)
        if verbose:
            print('getting epoch time given a timestamp local to ' + str(tz))
        epoch = pytz.utc.localize(datetime.datetime.utcfromtimestamp(0))

    if timestring == 'now':
        return time.time()
    elif type(timestring) is time.struct_time:
        if verbose:
            print('\'timestring_to_epoch_time\' revieved a time.struct_time object. ' +
                  'Returning the corresponding epoch time.')
        return time.mktime(timestring)

    elif type(timestring) is not str:
        if verbose:
            print('timestamp_to_unix_time\' didn\'t receive a string. ' +
                  'Received:\n' + str(timestring) + ' \nReturning the argument.')
        return timestring

    if len(timestring) > 8:
        try:
           # print(timestring) # debugging
            timestamp = re.search(timestamp_match, timestring).group()
            hh = int(timestamp[0:2])
            if 'PM' in timestring and not hh==12:
            # Holy fuck the whole AM/PM thing is stupid
                timestamp = str(hh + 12) + timestamp[2:]
            elif 'AM' in timestring and hh==12:
                timestamp = '00' + timestamp[2:]
        except AttributeError:
            if verbose:
                print('WARNING: I got no clue what you\'re talking \'bout ' +
                      'when you say ' + timestamp + '. It didn\'t match \.' +
                      timestamp_match + '\'. Assuming you want 00:00:00')
            timestamp = '00:00:00'
    else:
        timestamp = timestring

    if date is None:
        if verbose:
            print('\'timestring_to_epoch_time\' is assuming' +
                  ' the date is in the timestring.')
        date = parse_date(timestring)

    if date is None:
        if verbose:
            print('couldn\'t figure out the date for ' + timestring + '. Assuming today.')
        date = 'today'
    if date == 'today':
        date = time.strftime('%Y/%m/%d')
    #print('timestring = ' + timestring) # debugging
    if tz is None:
        if '-' in date:
            date = date.replace('-','/') #18D08
        struct = time.strptime(date + ' ' + timestamp, form)
        tstamp = time.mktime(struct)
    else:
        dt_naive = datetime.datetime.strptime(date + ' ' + timestamp, form)
        dt = tz.localize(dt_naive)
        tstamp = (dt - epoch).total_seconds()

    if out == 'all':
        return tstamp, date, timestamp
    return tstamp


def epoch_time_to_timestamp(tstamp, tz=None, verbose=True):
    '''
    tz is the Timezone, which is only strictly necessary when synchronizing
    data taken at different places or accross dst at a place with different dst
    implementation than the local (dst is stupid!).
    If timezone is a number, it is interpreted as the offset from GMT of the
    data in hours (+1 for Denmark, -8 for California)
    '''
    if tz is None:
        struct = time.localtime(tstamp)
    else:
        tz = parse_timezone(tz)
        if verbose:
            print('getting the timestamp local to ' + str(tz) + ' from epoch time.')
        dt_utc = datetime.datetime.utcfromtimestamp(tstamp)
        dt_tz = tz.fromutc(dt_utc)
        struct = dt_tz.timetuple()
    hh = str(struct.tm_hour)
    if len(hh) == 1:
        hh = '0' + hh
    mm = str(struct.tm_min)
    if len(hh) == 1:
        mm = '0' + mm
    ss = str(struct.tm_sec)
    if len(hh) == 1:
        ss = '0' + ss
    timestamp = hh + ':' + mm + ':' + ss
    return timestamp

def timetag_to_timestamp(filename):
    '''
    Converts a time tag of format _<hh>h<mm>m<ss>_ to timestamp of format
    <hh>:<mm>:<ss>, which is what synchronize reads (I should maybe change
    synchronize to work with the unix epoch timestamp instead...)
    The time tag is something we write in the file names to give an approximate
    sense of when a measurement is started. It can be used as the measurement
    start time if there really is no better way.
    I can't beleive SPEC doesn't save time. I will pressure them to fix this.
    '''
    hm_match = re.search(r'_[0-9]{2}h[0-9]{2}', filename)
    hm_str = hm_match.group()
    hh = hm_str[1:3]
    mm = hm_str[-2:]
    ss_match = re.search(r'_[0-9]{2}h[0-9]{2}m[0-9]{2}', filename)
    if ss_match is None:
        ss = '00'
    else:
        ss = ss_match.group()[-2:]
    return hh + ':' + mm + ':' + ss


def get_creation_timestamp(filepath):
    '''
    Returns creation timestamp of a file in the format that
    combining.syncrhonize reads.
    The timestamp is local time, not absolute time.
    We need to move to epoch time everywhere!!!
    '''
    t = get_creation_time(filepath)
    struct = time.localtime(t)
    hh = str(struct.tm_hour)
    mm = str(struct.tm_minute)
    ss = str(struct.tm_second)
    return hh + ':' + mm + ':' + ss


def get_creation_time(filepath, verbose=True):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        tstamp = os.path.getctime(filepath)
        if verbose:
            print('In Windows. Using os.path.getctime(\'' + filepath + '\') as tstamp.')
    else:
        stat = os.stat(filepath)
        try:
            tstamp = stat.st_birthtime
            if verbose:
                print('In linux. Using os.stat(\'' + filepath + '\').st_birthtime as tstamp.')
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            tstamp = stat.st_mtime
            if verbose:
                print('Couldn\'t get creation time! Returing modified time.\n' +
                  'In linux. Using os.stat(\'' + filepath + '\').st_mtime as tstamp.')
    return tstamp

def timestamp_from_file(filepath, verbose=True):
    a = re.search('[0-9]{2}h[0-9]{2}', filepath)
    if a is None:
        if verbose:
            print('trying to read creation time')
        timestamp = get_creation_timestamp(filepath)
    else:
        if verbose:
            print('getting timestamp from filename ' + filepath)
        timestamp = timetag_to_timestamp(filepath)
    return timestamp

def load_from_csv(filepath, multiset=False, timestamp=None, verbose=True):
    '''
    This function is made a bit more complicated by the fact that some csvs
    seem to have multiple datasets appended, with a new col_header line as the
    only indication. If multiset=True, this will separate them and return them
    as a list.
    if timestamp = None, the timestamp will be the date created
    I hate that SPEC doesn't save absolute time in a useful way.
    '''
    if verbose:
        print('function \'load_from_csv\' at your service!')
    if timestamp is None:
        a = re.search('[0-9]{2}h[0-9]{2}', filepath)
        if a is None:
            print('trying to read creation time')
            timestamp = get_creation_timestamp(filepath)
        else:
            print('getting timestamp from filename ' + filepath)
            timestamp = timetag_to_timestamp(filepath)

    with open(filepath,'r') as f: # read the file!
        lines = f.readlines()
    colheaders = [col.strip() for col in lines[0].split(',')]
    data = get_empty_set(set(colheaders), title=filepath,
                         timestamp=timestamp, data_type='SPEC')
    datasets = []

    for line in lines[1:]: #put data in lists!
        vals = [val.strip() for val in line.split(',')]
        not_data = []
        newline = {}
        for col, val in zip(colheaders, vals):
            if col in data['data_cols']:
                try:
                    val = float(val)
                except ValueError:
                    print('value ' + val + ' of col ' + col + ' is not data.')
                    not_data += [col]
            newline[col] = val
        if len(not_data) == len(data['data_cols']):
            print('it looks like there is another data set appended!')
            if multiset:
                print('continuing to next set.')
                numerize(data)
                datasets += [data.copy()]
                colheaders = [val.strip() for val in vals]
                data = get_empty_set(set(colheaders),
                         timestamp=timestamp, data_type='SPEC')
                continue
            else:
                print('returning first set.')
                numerize(data)
                return data
        else:
            for col in not_data:
                data['data_cols'].remove(col)
                print('column ' + col + ' removed from \'data_cols \'.')

        for col, val in zip(colheaders, vals):
            data[col] += [newline[col]]

    numerize(data)
    datasets += [data]
    if verbose:
        print('function \'load_from_csv\' finished!')
    if multiset:
        return datasets
    return data


def read_macro(file):
    with open(file) as macro:
        lines = macro.readlines()
    lines = remove_comments(lines)
    settings = {'tth':[], 'alpha':[], 'savepath':[], 'newfile':[], 'measurements':[]}
    for line in lines:
        #print(line)
        tth_match = re.search('umv tth ' + float_match, line)
        if tth_match:
            #print('got tth!')
            settings['tth'] += [float(tth_match.group()[7:])]
            continue
        alpha_match = re.search('umv th ' + float_match, line)
        if alpha_match:
            settings['alpha'] += [float(alpha_match.group()[6:])]
            continue
        if 'pd savepath' in line:
            settings['savepath'] += [line[12:]]
            continue
        if 'newfile ' in line:
            settings['newfile'] += [line[8:]]
            continue
        if '_timescan ' in line or 'ascan ' in line or 'pdascan ' in line:
            settings['measurements'] += [line]
            continue
    return settings

def remove_comments(lines):
    new_lines = []
    for line in lines:
        if '#' in line:
            line = re.search('^.*\#', line).group()[:-1]
            if re.search(r'\w', line): #to drop lines that only have comments
                new_lines += [line]
        else:
            new_lines += [line] #I don't want to get rid of empty lines here
    return new_lines



def import_EC_data(full_path_name, title='get_from_file',
                 data_type='EC', N_blank=10, verbose=True,
                 header_string=None, timestamp=None, ):
    file_lines = import_text(full_path_name, verbose=verbose)
    dataset = text_to_data(file_lines, title='get_from_file',
                           data_type='EC', N_blank=10, verbose=True,
                           header_string=None, timestamp=None)
    numerize(dataset)
    return dataset

'''
The following couple functions are adapted from EC_MS on 17L09
as last commited to EC_MS with code c1c6efa
They might benifit from a full rewrite, but not now.
'''


def import_text(full_path_name='current', verbose=True):
    '''
    This method will import the full text of a file selected by user input as a
    list of lines.
    When I first wrote it for EC_MS, way back in the day, I made it so you can
    call it without any arguments, and then input. probably unecessary.
    '''
    if verbose:
        print('\n\nfunction \'import_text\' at your service!\n')

    if full_path_name == 'input':
        full_path_name = input('Enter full path for the file name as \'directory' + os.sep + 'file.extension\'')
    if full_path_name == 'current':
        full_path_name = os.getcwd()

    [directory_name, file_name] = os.path.split(full_path_name)
    if directory_name == '':
        directory_name = '.'
    original_directory = os.getcwd()
    os.chdir(directory_name)

    if os.path.isdir(full_path_name) and not os.path.isfile(file_name):
        directory_name = full_path_name
        os.chdir(directory_name)
        ls_string = str(os.listdir())
        print('\n' + full_path_name + '\n ls: \n' + ls_string + '\n')
        file_name = input('Directory given. Enter the full name of the file to import\n')

    if verbose:
        print('directory: ' + directory_name)
        print('importing data from ' + file_name )

    possible_encodings = ['utf8','iso8859_15']
    #mpt files seem to be the latter encoding, even though they refer to themselves as ascii
    for encoding_type in possible_encodings:
        try:
            with codecs.open(file_name, 'r', encoding = encoding_type) as file_object:
                file_lines = file_object.readlines()
            if verbose:
                print('Was able to readlines() with encoding ' + encoding_type)
            break
        except UnicodeDecodeError:
            if verbose:
                print('Shit, some encoding problem in readlines() for ' + encoding_type)
    else:
        print('couldn\'t read ' + file_name + '\n ... may by due to an encoding issue')

    os.chdir(original_directory)

    if verbose:
        print('\nfunction \'import_text\' finished!\n\n')
    return file_lines


def text_to_data(file_lines, title=None,
                 timestamp=None, date='today', tstamp=None, tz=None,
                 data_type='EC', sep=None,
                 header_string=None, verbose=True):
    '''
    This method will organize data in the lines of text from a file useful for
    electropy into a dictionary as follows (plus a few more keys)
    {'title':title, 'header':header, 'timestamp':timestamp,
     'data_cols':{colheader1, colheader2, ...},
     colheader1:data1, colheader2:data2, ...}

    Supported data types:
        'EC': text output (.mpt) from Biologic for any voltammetric technique
        'MS': text output from cinfdata for mass_time_scan, run by PyExpLabSys
        'SPEC': .csv file saved by SPEC diffraction program at SSRL BL2.1
        'XAS': text saved by XAS program at SSRL BL11.2
        'SI': text ouptut (.csv) from Zilien, Kenneth's software for Spectro Inlets
        'RGA': text output from Residual Gas Analysis program for mass spec
    '''
    if verbose:
        print('\n\nfunction \'text_to_data\' at your service!\n')

    #disect header
    N_lines = len(file_lines)        #number of header lines
    N_head = N_lines                 #this will change when I find the line that tells me how ling the header is
    header_string = ''

    dataset = {}
    commacols = []                   #will catch if data is recorded with commas as decimals.

    loop = False

    if data_type == 'SPEC' or data_type == 'ULM':
        N_head = 1 #the column headers are the first line
        if sep is None:
            sep = ','
    elif data_type == 'SI' or data_type == 'MKS':  # Spectro Inlets data
        sep = '\t' # despite it being a .csv, the separator is a tab.
    elif data_type == 'RGA':
        sep = ','
        N_blank = 2
        dataset['channels'] = {}
    elif data_type == 'CHI': # CH Instruments potentiostat
        N_blank = 2
        sep = ','
    elif data_type == 'MS':
        N_blank = 10

    if sep is None:  #EC and MS data all work with '\t'
        sep = '\t'

    print('N_head = ' + str(N_head)) # debugging

    n_blank = 0
    got_col_headers = False
    for nl, line in enumerate(file_lines):
        l = line.strip()
        if nl < N_head - 1:            #we're in the header

            if data_type == 'EC':
                if title is None:
                    if re.search('File :',line):
                        title_object = re.search(r'[\S]*\Z',line.strip())
                        title = title_object.group()
                        if verbose:
                            print('name \'' + title + '\' found in line ' + str(nl))
                if re.search(r'[Number ]*header lines',line):
                    N_head_object = re.search(r'[0-9][0-9]*',line)
                    N_head = int(N_head_object.group())
                    if verbose:
                        print('N_head \'' + str(N_head) + '\' found in line ' + str(nl))
                elif timestamp is None and re.search('Acquisition started',line):
                    timestamp_object = re.search(timestamp_match,l)
                    timestamp = timestamp_object.group()
                    date = parse_date(l)
                    if verbose:
                        print('timestamp \'' + timestamp + '\' found in line ' + str(nl))
                elif re.search('Number of loops', line):
                    #Then I want to add a loop number variable to data_cols
                    loop = True
                    dataset['loop number'] = []
                elif re.search('Loop', line):
                    n = int(re.search(r'^Loop \d+', line).group()[5:])
                    start = int(re.search(r'number \d+', line).group()[7:])
                    finish = int(re.search(r'to \d+', line).group()[3:])
                    N = finish - start + 1
                    dataset['loop number'] += N * [n]

            elif data_type == 'MS':
                if len(line.strip())==0:
                    n_blank += 1
                    if n_blank >= N_blank and len(file_lines[nl+1].strip())>0:
                        N_head = nl+2
                    continue
                else:
                    n_blank = 0
                if title is None:
                    object1 = re.search(r'"Comment"[\s]*"[^"]*',line)
                    if object1:
                        string1 = object1.group()
                        title_object = re.search(r'[\S]*\Z',string1.strip())
                        title = title_object.group()[1:]
                        if verbose:
                            print('name \'' + title + '\' found in line ' + str(nl))
                object2 = re.search(r'"Recorded at"[\s]*"[^"]*',line)
                if object2:
                    string2 = object2.group()
                    timestamp_object = re.search(timestamp_match, string2.strip())
                    timestamp = timestamp_object.group()
                    date = parse_date(l)
                    # ^convert yyyy-mm-dd to dd-mm-yyyy
                    if verbose:
                        print('timestamp \'' + timestamp + '\' found in line ' + str(nl))

            elif data_type == 'SI': # Spectro Inlets data format
                items = [item.strip() for item in line.split(sep) if len(item.strip())>0]
                if nl < 10:
                    #print(items) # debugging
                    pass
                if len(items) == 0:
                    continue
                if title is None and items[0] == 'name':
                    title = items[-1]
                    if verbose:
                        print('title \'' + str(title) + '\' found in line ' + str(nl))
                if items[0] == 'offset':
                    offset = float(items[-1])
                    dataset['SI offset'] = offset
                    if verbose:
                        print('SI offset \'' + str(offset) + '\' found in line ' + str(nl))
                if items[0] == 'data_start':
                    N_head = int(items[-1])
                    if verbose:
                        print('N_head \'' + str(N_head) + '\' found in line ' + str(nl))
                if nl == N_head - 2:
                    col_preheaders = [item.strip() for item in line.split(sep)]
                    for i, preheader in enumerate(col_preheaders):
                        if len(preheader) == 0:
                            col_preheaders[i] = col_preheaders[i-1]

            elif data_type == 'MKS': # old Spectro Inlets MS data format
                # this actually records absolute time (in a fucked up format),
                # so no need to read the timestring.
                if '[Scan Data' in line: # then the data is coming.
                    N_head = nl + 2

            elif data_type == 'RGA':
                if len(line.strip())==0:
                    n_blank += 1
                    if n_blank >= N_blank and len(file_lines[nl+1].strip())>0:
                        N_head = nl+2
                    continue
                else:
                    n_blank = 0
                if re.search('Start time', line):
                    tstamp, date, timestamp = timestring_to_epoch_time(l, tz=tz,
                                                    out='all', verbose=verbose)
                if re.search(r'\A[0-9]+\s', l): # lines starting with a number
                    items = [item.strip() for item in line.split(' ') if len(item.strip())>0]
                    channel = 'Channel#' + items[0]
                    mass = 'M' + items[1].split('.')[0]
                    dataset['channels'][channel] = mass
                if 'Analog Scan' in l:
                    col_headers = ['m/z', 'signal/A']
                    got_col_headers = True
                    print('got column headers! on line ' + str(nl))

            elif data_type == 'CHI':
                if len(line.strip())==0:
                    n_blank += 1
                    if n_blank >= N_blank and len(file_lines[nl+1].strip())>0:
                        N_head = nl+2
                    continue
                else:
                    n_blank = 0
                if nl == 0: # record time (measurement finish time) on top line
                    if verbose:
                        print('finding tstamp from line: ' + l)
                    tstamp, date, timestamp = timestring_to_epoch_time(l, tz=tz,
                                                    out='all', verbose=verbose)
                if 'Segment = ' in line:
                    dataset['segments'] = line.split(' = ')[-1].strip()
                    last_segment_line = 'Segment ' + dataset['segments'] + ':'
                if 'segments' in dataset and last_segment_line in line:
                    N_blank = 1
                if 'Scan Rate (V/s)' in line:
                    dataset['scan rate'] = eval(line.split(' = ')[-1].strip())*1e3 # in mV/s
                if 'Time/s' in line: # then it's actually the column header line.
                    N_head = nl + 2 # the next line is a blank line, during which we handle the column headers
                    col_headers = l.split(sep)
                    got_col_headers = True # to be used on next line (nl=N_head-1)


            header_string = header_string + line

        elif nl == N_head - 1:      #then it is the column-header line
               #(EC-lab includes the column-header line in header lines)
            #col_header_line = line
            if data_type == 'RGA':  # there's no damn commas on the column header lines!
                if not got_col_headers:
                    col_headers = [col.strip() for col in l.split(' ') if len(col.strip())>0]
            elif data_type == 'CHI' and got_col_headers:
                pass
            else:
                col_headers = [col.strip() for col in l.split(sep=sep)]

            if data_type == 'MKS':
                col_headers = [col.strip('"') for col in col_headers]

            if data_type == 'SI':
                for i, col in enumerate(col_headers):
                    col_headers[i] = col_preheaders[i] +' - ' + col

            #print(col_headers) # debugging

            dataset['N_col'] = len(col_headers)
            dataset['data_cols'] = set(col_headers.copy())  #will store names of columns containing data
            if not len(col_headers) == len(dataset['data_cols']):
                print('WARNING: repeated column headers!!!')
                print('col_headers = ' + str(col_headers))

            dataset['col_types'] = dict([(col, data_type) for col in col_headers])

            for col in col_headers:
                dataset[col] = []              #data will go here
            header_string = header_string + line #include this line in the header
            if verbose:
                print('Data starting on line ' + str(N_head) + '\n')

        elif len(l)==0:
            # rga and chi text files skip a line after the column header
            continue

        else:                   # data, baby!
            line_data = [dat.strip() for dat in l.split(sep=sep)]

            if data_type == 'MKS':
                timestring = line_data[0].replace('.', ':')[1:-1]
                if 'Annotations' in timestring: # last line actually doesn't have data
                    continue
                yyyy, dd, mm = timestring[6:10], timestring[0:2], timestring[3:5]
                timestring = yyyy + '/' + mm + '/' + dd + timestring[-9:]
                t = timestring_to_epoch_time(timestring)
                line_data[0] = str(t)

            if not len(line_data) == len(col_headers):
                #print('Mismatch between col_headers and data on line ' + str(nl) + ' of ' + title) #debugging
                pass
            for col, x in zip(col_headers, line_data):
                if not col in dataset['data_cols']:
                    # don't try adding data to a column that has already been determined not to have data!
                    continue
                try:
                    x = float(x)
                except ValueError:
                    if x == '':
                        continue        #added 17C22 to deal with data acquisition crashes.
                    try:
                        x = x.replace('.','')
                        # ^ in case there's also '.' as thousands separator, just get rid of it.
                        x = x.replace(',','.')       #put '.' as decimals
                        x = float(x)
                    except ValueError:
                        if verbose :
                            print(list(zip(col_headers,line_data)))
                            print(title + ' in text_to_data: \nRemoved \'' + str(col) +
                                  '\' from data columns because of value \'' +
                                str(x) + '\' at line ' + str(nl) +'\n')
                        dataset['data_cols'].remove(col)
                    else:
                        if verbose and not col in commacols:
                            print('ValueError on value ' + str(x) + ' in column ' + col + ' line ' + str(nl) +
                                  '\n Checking if you''re using commas as decimals in that column... ')
                        if not col in commacols:
                            if verbose:
                                print('... and you were, dumbass. I''ll fix it.')
                            commacols += [col]
                dataset[col].append(x)

    if data_type == 'MKS':
        tstamp = dataset['Time'][0]
        dataset['Time'] -= np.array(dataset['Time']) - tstamp
        tstamp = epoch_time_to_timestamp(tstamp)
        date = None
    if loop:
        dataset['data_cols'].add('loop number')
    dataset['title'] = title
    dataset['header'] = header_string
    dataset['timestamp'] = timestamp
    dataset['date'] = date
    if tstamp is None:
        tstamp = timestring_to_epoch_time(timestamp, date, tz=tz, verbose=verbose, out='tstamp')
    dataset['timezone'] = tz
    dataset['tstamp'] = tstamp
    #UNIX epoch time, for proper synchronization!
    dataset['data_type'] = data_type

    if data_type == 'EC':           #so that synchronize can combine current data from different EC-lab techniques
        if '<I>/mA' in dataset['data_cols'] and 'I/mA' not in dataset['data_cols']:
            #so that synchronize can combine current data from different EC-lab techniques
            dataset['data_cols'].add('I/mA')
            dataset['I/mA'] = dataset['<I>/mA'].copy()
        if '<Ewe>/V' in dataset['data_cols'] and 'Ewe/V' not in dataset['data_cols']:
            dataset['data_cols'].add('Ewe/V')
            dataset['Ewe/V'] = dataset['<Ewe>/V'].copy()

    if verbose:
        print('\nfunction \'text_to_data\' finished!\n\n')
    return dataset


def import_data(*args, **kwargs):
    print('\'import_data\' is now called \'load_from_file\'!\n' +
          'Remember that next time, goof.')
    return load_from_file(*args, **kwargs)

def load_from_file(full_path_name='current', title='file', tstamp=None, timestamp=None,
                 data_type='EC', tz=None, name=None, verbose=True):
    '''
    This method will organize the data in a file useful for
    electropy into a dictionary as follows (plus a few more keys)
    {'title':title, 'header':header, 'timestamp':timestamp,
    'data_cols':[colheader1, colheader2, ...],
    colheader1:[data1], colheader2:[data2]...}
    '''
    if verbose:
        print('\n\nfunction \'load_from_file\' at your service!\n')
    if title == 'file':
        folder, title = os.path.split(full_path_name)
    if folder == '':
        folder = '.'
    file_lines = import_text(full_path_name, verbose)
    dataset = text_to_data(file_lines=file_lines, title=title, data_type=data_type,
                           timestamp=timestamp, tz=tz, tstamp=tstamp,
                           verbose=verbose)
    if tstamp is not None: #then it overrides whatever text_to_data came up with.
        dataset['tstamp'] = tstamp
    elif dataset['tstamp'] is None:
        print('WARNING: no tstamp found in ' + full_path_name + '. Using file timestamp.')
        dataset['tstamp'] = get_creation_time(full_path_name, verbose=verbose)
    if 'data_cols' not in dataset or len(dataset['data_cols']) == 0:
        print('WARNING! empty dataset')
        dataset['empty'] = True
    else:
        numerize(dataset)
        dataset['empty'] = False
    if name is None:
        name = dataset['title']
    dataset['name'] = name

    if dataset['empty']:
        print('WARNING! load_from_file is returning an empty dataset')
    elif data_type == 'SI':
        from .Combining import rename_SI_cols
        rename_SI_cols(dataset)
    elif data_type == 'RGA':
        from .Combining import rename_RGA_cols
        rename_RGA_cols(dataset)
    elif data_type == 'CHI':
        from .Combining import parse_CHI_header, rename_CHI_cols, timeshift
        parse_CHI_header(dataset)
        rename_CHI_cols(dataset)
        dt = dataset['time/s'][-1] - dataset['time/s'][0]
        timeshift(dataset, dt)
    elif data_type == 'ULM':
        from .Combining import rename_ULM_cols
        rename_ULM_cols(dataset)

    if verbose:
        print('\nfunction \'load_from_file\' finished!\n\n')
    return dataset


def load_EC_set(directory, EC_files=None, tag='01', suffix=None, data_type='EC',
                  verbose=True, tz=None, exclude=[], fix_CP=False):
    '''
    inputs:
        directory - path to folder containing your data, string

        EC_file - list of EC_files, list
            OR
        tag - shared start of EC files you want to load and combine, str AND
        suffix - ending of files, by default .mpt

        data_type - type of EC data. By default 'EC', meaning Biologic EC-Lab files
        tz - timezone, usually not needed
        verbose - makes the function talk to you.
    output
        EC_data - a dataset with the data from all specified EC files combined
            and sorted based on time. Additional columns loop_number and
            file_number are added to the dataset if relevant.
    '''
    if verbose:
        print('\n\nfunction \'load_EC_set\' at your service!\n')
    from .Combining import synchronize, sort_time

    if suffix is None:
        if data_type == 'EC':
            suffix = '.mpt'
        elif data_type == 'CHI':
            suffix = '.txt'

    lslist = os.listdir(directory)

    if EC_files is None:
        EC_files = [f for f in lslist if f[:len(tag)] == tag and f[-4:] == suffix]
        if type(exclude) is str:
            exclude = [exclude]
        for excl in exclude:
            EC_files = [f for f in EC_files if not excl in f]
    elif type(EC_files) is str:
        EC_files = [EC_files]
    EC_datas = []
    for f in EC_files:
        try:
            data = load_from_file(directory + os.sep + f,
                                        data_type=data_type, tz=tz,
                                        verbose=verbose)
        except OSError:
            print('WARNING: problem importing ' + f + '. Continuing.')
            continue
        if fix_CP and 'CP' in f:
            try:
                data['Ewe/V'] = data['Ewe-Ece/V'] + data['<Ece>/V']
            except KeyError:
                print('WARNING! Could not fix CP for ' + f + ' because missing ' +
                      ' either Ece/V or Ewe-Ece/V')
        EC_datas += [data]
    EC_data = synchronize(EC_datas, verbose=verbose, append=True, t_zero='first', tz=tz)
    if 'loop number' in EC_data['data_cols']:
        sort_time(EC_data, verbose=verbose) #note, sort_time no longer returns!

    if verbose:
         print('\nfunction \'load_EC_set\' finished!\n\n')
    return EC_data

def import_EC_set(*args, **kwargs):
    '''
    See EC_MS.load_EC_set
    '''
    print('import_EC_set has been renamed load_EC_set')
    return load_EC_set(*args, **kwargs)


def download_cinfdata_set(setup='sniffer', group_id=None, grouping_column=None, **kwargs):

    if grouping_column is None:
        grouping_column, group_id = kwargs.popitem()

    from .Combining import synchronize

    try:
        from cinfdata import Cinfdata
    except ImportError:
        print('the cinfdata module must be on your python path. It\'s here: \n' +
              'https://github.com/CINF/cinf_database/blob/master/cinfdata.py')

    try:
        cinfd = Cinfdata(setup, grouping_column=grouping_column,
                         allow_wildcards=True,
                         label_column='mass_label')
    except:
        raise  #untill I know exactly which error I'm trying to catch.
        print('couldn\'t connect. You should run gstm')
        #os.system('gstm')
        raise RuntimeError('Couldn\'t connect to cinfdata!')

    #obj = cinfd.get_metadata_group('2018-03-30 14:13:17')

    #all_datasets = cinfd.get_metadata_group('%')
    #the_list = [(ID, d['time'], d['comment']) for ID, d in all_datasets.items()]
    #print(the_list)

    obj = cinfd.get_metadata_group(group_id)
    #print(str(obj)) #

    idlists = {} # keys will be time as string. values will be corresponding id's

    for key, value in obj.items():
        #label = value['mass_label']
        #print(label)
        timestamp = str(value['time'])
        if timestamp not in idlists:
            idlists[timestamp] = []
        idlists[timestamp] += [value['id']]

    datasets = {}
    for timestamp, idlist in idlists.items():

        if len(idlist) == 0:
            print('No data associated with timestamp \'' + timestamp + '\'.')
            continue

        dataset = {'title':timestamp, 'data_type':'MS'}

        metadatas = dict([(i, cinfd.get_metadata(i)) for i in idlist])

        unixtimes = [metadatas[i]['unixtime'] for i in idlist]
        if len(set(unixtimes)) > 1:
            msg = 'unix times don\'t match for timestamp \'' + timestamp + '\'!'
            raise ValueError(msg)

        dataset['tstamp'] = unixtimes[0]
        dataset['timestamp'] = metadatas[idlist[0]]['time'].strftime('%H:%M:%S')

        labels = [metadatas[i]['mass_label'] for i in idlist]
        if 'Mass Scan' in labels:
            dataset['scan_type'] = 'mass'
        else:
            dataset['scan_type'] = 'time'

        dataset['data_cols'] = set()
        dataset['timecols'] = {}
        for i in idlist: #avoiding id since it's got a builtin meaning
            data = cinfd.get_data(i)
            label = metadatas[i]['mass_label']
            if len(data.shape) == 1:
                dataset[label] = data
                dataset['data_cols'].add(label)
            elif data.shape[1] == 2:
                x = data[:, 0]
                y = data[:, 1]
                x_label = label + '-x'
                y_label = label + '-y'
                dataset['timecols'][x_label] = y_label
                dataset[x_label] = x * 1e-3 # cinfdata saves time in ms!!!
                dataset[y_label] = y

                dataset['data_cols'].add(x_label)
                dataset['data_cols'].add(y_label)

        datasets[timestamp] = dataset


    timescans = [dataset for dataset in datasets.values() if dataset['scan_type'] == 'time']


    combined = synchronize(timescans, t_zero='first')

    return combined

def get_xy(data, xcol=None, ycol=None, label=None, ):
    '''
    '''
    if xcol is None:
        xcol = label + '-x'
    if ycol is None:
        ycol = label + '-y'
    return data[xcol], data[ycol]

def set_xy(data, x, y, xcol=None, ycol=None, label=None, ):
    '''
    '''
    if xcol is None:
        xcol = label + '-x'
    if ycol is None:
        ycol = label + '-y'
    data[xcol] = x
    data[ycol] = y

def remove_repeats(data, xcol=None, ycol=None, label=None):
    '''
    '''
    x_0, y_0 = get_xy(data, xcol, ycol, label)
    x, y = only_while_increasing(x_0, y_0)
    set_xy(data, x=x, y=y, xcol=xcol, ycol=ycol, label=label)

def only_while_increasing(x=None, y=None):
    '''
    removes the repeats if a dataset goes back and repeats, as happens in
    the Analog In anomoly first observed 18D05.
    Does so in a vectorized way (only loops over "cliff points" where x falls)
    x is monotonically increasing in the returned data
    '''

    x_up = np.append(x[1:], x[-1]+1) # x shifted up one, so that x_up[i] = x[i+1]
    cliff_points = np.where(x_up < x)[0]      # points right before a drop in x
    mask = np.tile(True, np.size(x))

    for point in cliff_points:
        x_cliff = x[point]
        mask[point:] = np.logical_and(mask[point:], x[point:] > x_cliff)

    return x[mask], y[mask]


def import_set(directory, MS_file='QMS.txt', MS_data=None, t_zero='start',
               EC_file=None, tag='01',
               cutit=False, cut_buffer=60,
               verbose=True, override=False):
    from .Combining import synchronize, sort_time

    if verbose:
        print('\n\nfunction import_set at your service!\n')


    lslist = os.listdir(directory)

    if MS_data is None:
        if type(MS_file) is str:
            MS_file = [MS_file]
        MS_datas = [load_from_file(directory + os.sep + f,
                                data_type='MS', verbose=verbose)
                    for f in MS_file]
        MS_data = synchronize(MS_datas, verbose=verbose)
        if len(MS_datas) > 1:
            sort_time(MS_data)

    if EC_file is None:
        EC_file = [f for f in lslist if f[:2] == tag and f[-4:] == '.mpt']
    elif type(EC_file) is str:
        EC_file = [EC_file]
    EC_datas = [load_from_file(directory + os.sep + f, verbose=verbose, data_type='EC')
                for f in EC_file]
    EC_data = synchronize(EC_datas, verbose=verbose)
    if 'loop number' in EC_data['data_cols']:
        sort_time(EC_data, verbose=verbose) #note, sort_time no longer returns!

    data = synchronize([MS_data, EC_data], t_zero=t_zero, verbose=verbose,
                       override=override, cutit=cutit, cut_buffer=cut_buffer)
    if verbose:
         print('\nfunction import_set finished!\n\n')
    return data


def save_as_text(filename, dataset, cols=[], mols=[], tspan='all', header=None,
                 N_chars=None, timecols={}, **kwargs):
    '''
    kwargs is fed directly to Molecule.get_flux()
    '''
    from .Combining import get_timecol, cut

    lines = []
    if type(header) is list:
        lines += header
    elif type(header) is str:
        lines += [header]

    if N_chars is None:
        N_chars = max([len(col) for col in cols])

    col_header = ''
    i_col = 0
    columns = []
    datas = {}
    for col in cols:
        if col in timecols:
            tcol = timecols[col]
        else:
            tcol = get_timecol(col)
        if tcol in dataset and tcol not in columns: # don't want same tcol twice
            col_header += ('{0:>' + str(N_chars) + 's},\t').format(tcol)
            columns += [tcol]
            i_col += 1
        if col in dataset and col not in columns: # don't want same tcol twice
            col_header += ('{0:>' + str(N_chars) + 's},\t').format(col)
            columns += [col]
            i_col += 1
        else:
            print(col + ' not in dataset. ignoring it.')
            continue
        if tcol in columns:
            x, y = dataset[tcol].copy(), dataset[col].copy()
            if tspan is not False and not tspan=='all':
                x, y = cut(x, y, tspan=tspan)
            datas[tcol], datas[col] = x, y
        else:
            print('timecol \'' + tcol + '\' for col \'' + col +
                  '\' is not in dataset, so can\'t cut it.')
            datas[col] = dataset[col].copy()

    for mol in mols:
        tcol = mol.name + '_' + mol.primary + '-x'
        col = mol.name + '_' + mol.primary + '-y'
        x, y = mol.get_flux(dataset, tspan=tspan, **kwargs)
        datas[tcol] = x
        datas[col] = y
        col_header += ('{0:>' + str(N_chars) + 's},\t').format(tcol)
        columns += [tcol]
        col_header += ('{0:>' + str(N_chars) + 's},\t').format(col)
        columns += [col]

    lines += [col_header + '\n']

    i_data = 0
    finished = False
    while not finished:
        N_unfinished = 0
        line = ''
        for col in columns:
            try:
                d = datas[col][i_data]
                line += ('{0:>' + str(N_chars) + '.6g},\t').format(d)
                N_unfinished += 1
            except IndexError:
                line += ' '*N_chars + ',\t'
        if N_unfinished == 0:
            finished = True
        else:
            lines += [line + '\n']
            i_data += 1

    with open(filename, 'w') as f:
        f.writelines(lines)


def save_results_as_text(name, cols='all', **kwargs):
    if cols == 'all':
        cols = list(kwargs.keys())
    header_line =  ''.join([(col + ', \t') for col in cols])
    header_line = header_line[:-3] + '\n'
    lines = [header_line]

    N = len(kwargs[cols[0]])

    for i in range(N):
        l = ''
        for col in cols:
            try:
                v = kwargs[col][i]
            except IndexError:
                s = ', \t'
            else:
                s = '{:6.4g}'.format(v) + ', \t'
            l += s
        l = l[:-3] + '\n'
        lines += [l]

    with open(name, 'w') as f:
        f.writelines(lines)


def import_folder(directory, tags=None, MS_file=None, verbose=True):
    '''
    Copined 19G24 from commit  Submitting Trimarco2018 e12b8e9 on Dec 19, 2017

    import everything you need from directory at once.
    tags = None imports as one dataset
    tags = 'all' separates by EC file tag, imports evertything
    tags = ['01','02'] imports two datasets, one for each tag
    '''
    from .Combining import synchronize

    if verbose:
        print('\n\nfunction \'imoprt_folder\' at your service!\n')
        print('Importing from \'' + directory + '\'')

    if directory[-1] == os.sep:
        directory = directory[:-1] #import_set adds the os.sep

    lslist = os.listdir(directory)

    if MS_file is None:
        MS_file = [f for f in lslist if 'QMS' in f]

    #importing MS data here rather than in import_set to avoid redundant importing
    MS_datas = [import_data(directory + os.sep + f,
                            data_type='MS', verbose=verbose)
                for f in MS_file]
    MS_data = synchronize(MS_datas, verbose=verbose)
    #if len(MS_datas) > 1:          #not necessary, as synchronize sorts by recstart
        #sort_time(MS_data)

    if tags is None:
        EC_file = [f for f in lslist if '.mpt' in f]
        Datasets = import_set(directory, MS_data=MS_data, EC_file=EC_file, verbose=verbose)
       # sort_time(Datasets)  #probably not necessary, as synchronize sorts by recstart

    else:
        if tags == 'all':
            taglist = {f[0:2] for f in lslist if f[-4:]=='.mpt'}
        else:
            taglist = tags #Renamed so I keep info on what tags originally was
        Datasets = dict([(t, import_set(directory, MS_data=MS_data,
                                        tag=t, verbose=verbose))
                         for t in taglist])


    if verbose:
        print('\n\nfunction \'imoprt_folder\' finished!\n')
    return Datasets


def download_data(IDs='today',
                  timestamps=None,
                  data_type='fullscan',
                  timestamp_interval=None,
                  comment=None,
                  connect={},
                  verbose=True,
                  ):
    '''
    Copied 19G25 from commit   17G28 better combining and plotting b70b43b on Jul 28, 2017
    ... but it seems to be broken :( Not wasting time on this now.


    Returns data columns matching a certain set of ID's.

    '''
    import sys
    try:
        import MySQLdb # known to pip as mysqlclient
        #CONNECT_EXCEPTION = MySQLdb.OperationalError
        #LOG.info('Using MySQLdb as the database module')
        print('imported MySQLdb no problem!')
    except ImportError:
        try:
            # .. if that fails, try with pymysql
            import pymysql as MySQLdb
            MySQLdb.install_as_MySQLdb()
            #CONNECT_EXCEPTION = MySQLdb.err.OperationalError
            #LOG.info('Using pymysql as the database module')
            if sys.version_info.major > 2:
                #LOG.info('pymysql is known to be broken with Python 3. Consider '
                 #        'installing mysqlclient!')
                pass
        except:
            print('Error, can\'t connect to database!')


    connect_0 = dict(host='servcinf-sql',  # your host, usually localhost, servcinf would also work, but is slower (IPv6)
                           #    port=9995,  # your forwording port
                               user='cinf_reader',  # your username
                               passwd='cinf_reader',  # your password
                               db='cinfdata')  # name of the data base

    for key, val in connect_0.items():
        if key not in connect:
            connect[key] = val

    if data_type == 'fullscan':
        data_string_template = 'SELECT x,y FROM xy_values_sniffer where measurement = {0} order by id'


 #       try:
    print('Connecting to CINF database...')
    cnxn =  MySQLdb.connect(**connect)
    cursor = cnxn.cursor()
    print('Connection successful!')
  #      except:
   #         print('Connection failed!')

    if type(IDs) is int:
        IDs = [IDs]

    datasets = {}
    for ID in IDs:
        data_string = data_string_template.format(str(ID))
        cursor.execute(data_string)
        raw_data = cursor.fetchall()
        list_data = np.array(raw_data)
        xy_data = np.swapaxes(list_data, 0, 1)
        datasets[ID] = xy_data

    return datasets


