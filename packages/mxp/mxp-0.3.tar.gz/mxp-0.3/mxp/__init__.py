"""Support to read the .mxp file format used by Stratagenes qPCR machines.

It tries it's best to extract the actual amplification parts (segments 1 or 2),
but offers nothing for later segments (such as melting curves) right now.

There is quite a bit of sanity checking,
changing the allowed_cycles seems to be fairly safe now.


read_mxp(filename) is the basic function you need, returns
a DataFrame containing the amplification curves (xy cycles, <=96 wells...)
    with the following columns:
    Well: 0..96
    Well Key A1..H12
    Assay - the assay in this well - exported as 'Dye' by MxPro'
    Well Name - the name the user assigned
    Fluorescence - the raw measurement at this cyle/well
    Temperature - temperature at this cycle/well
    Cycle - 0..xy

Currently only tested for 96 well plates on Mx3000P and Mx3005P machines.


"""
import pandas as pd
import olefile
import numpy as np
import natsort
import sys
import collections

__version__ = "0.3"

try:
    xrange
except NameError:
    xrange = range


def ord3(x):
    if sys.version_info[0] >= 3:
        if isinstance(x, int):
            return x
        else:
            raise ValueError(x, type(x))
    else:
        return ord(x)


class EmptyFile(ValueError):
    pass


def read_mxp(
    filename,
    allowed_cycles=(
        2,
        4,
        7,
        13,
        14,
        25,
        28,
        30,
        34,
        35,
        36,
        40,
        41,
        43,
        44,
        45,
        49,
        50,
        55,
        60,
        65,
        120,
    ),
    empty_assays_ok=False,
):
    """Read an MXP file and return a dataframe with the annotated amplification curves"""
    try:
        ole = olefile.OleFileIO(filename)
        fileformat = discover_fileformat(ole)
        # print 'fileformat', fileformat
        well_names, assay_names, well_types, set_ids = np.array(
            extract_well_names_and_assay_names(ole, fileformat, empty_assays_ok)
        )
        well_numbers = np.array(xrange(0, 96))
        # empty wells that were not read, and are not in the amplification curve file...
        ok_wells_by_name = (well_names != b"") | (assay_names != b"")
        ok_wells_by_type = well_types != b""
        # A dirty hack because I can't tell which wells were actually measured
        if ok_wells_by_type.sum() < ok_wells_by_name.sum():
            ok_wells = ok_wells_by_type
        else:
            ok_wells = ok_wells_by_name
        well_names = [x for x in well_names[ok_wells]]
        assay_names = [x for x in assay_names[ok_wells]]
        set_ids = [x for x in set_ids[ok_wells]]
        well_numbers = well_numbers[ok_wells]

        amplification_data = extract_amplification_curves(
            ole, fileformat, allowed_cycles, len(assay_names)
        )

        # melting_data = extract_melting_curves(ole)

        cycle_count = len(amplification_data[0][0])
        well_count = sum(ok_wells)
        amp_data = {
            "Well": [],
            "Well Key": [],
            "Assay": [],
            "Well Name": [],
            'Set id': [],
            "Fluorescence": [],
            "Temperature": [],
            "Cycle": [],
        }
        for ii in xrange(0, well_count):
            amp_data["Cycle"].extend(list(xrange(1, cycle_count + 1)))
            amp_data["Well"].extend([well_numbers[ii]] * cycle_count)
            amp_data["Well Key"].extend(
                [well_no_to_code(well_numbers[ii] + 1)] * cycle_count
            )
            amp_data["Assay"].extend([assay_names[ii]] * cycle_count)
            amp_data["Well Name"].extend([well_names[ii]] * cycle_count)
            amp_data["Set id"].extend([set_ids[ii]] * cycle_count)
            amp_data["Fluorescence"].extend(amplification_data[0][ii])
            amp_data["Temperature"].extend(amplification_data[1][ii])
        res = pd.DataFrame(amp_data)
        res.insert(len(res.columns), "Filename", filename)
        res["Well Key"] = pd.Categorical(
            res["Well Key"],
            natsort.humansorted(set([well_no_to_code(x) for x in xrange(1, 97)])),
        )
        if (res["Temperature"] > 120).any():
            raise ValueError(
                "Temperature above 120 degrees observed. Most likely a parsing error"
            )
    finally:
        # only if ole is defined
        if 'ole' in locals():
            ole.close()
    return res


def extract_date(filename, debug=False):
    """Read an MXP file and return a the (bytes) date in the file.
    For us that's either b'Unknown'
    or a string like b'January 07, 2018'
    """
    ole = olefile.OleFileIO(filename)
    with ole.openstream("Storage4/Stream4") as op:
        raw = op.read()
    parts = raw.split(b"\x00")
    if debug:
        for ii, p in enumerate(parts):
            print(ii, p)
    idx = 16
    date_part = parts[16]
    while not date_part:
        idx += 1
        date_part = parts[idx]
    if debug:
        print("date_part", date_part)
    date_len = ord3(date_part[0])
    if debug:
        print("date_len", date_len)
    date = date_part[1 : 1 + date_len]
    return date


def well_no_to_code(well_no):
    """1 -> A1, 2 -> A2, 96 -> H12"""
    well_no = well_no - 1
    first = well_no // 12
    second = well_no % 12
    return chr(ord(b"A") + first) + str(second + 1)


def code_to_well_no(code):
    """A1 -> 1, H12 -> 96"""
    if len(code) not in (2, 3):
        raise ValueError("Invalid code - wrong length")
    first = ord3(code[0]) - ord("A")
    if not (0 <= first <= 8):
        raise ValueError(
            "Invalid code: wrong first letter: %s, code:%s" % (first, code)
        )
    second = int(code[1:])
    if not (0 <= second <= 12):
        raise ValueError("Invalid code: wrong number")

    return 12 * first + second


def discover_fileformat(ole):
    with ole.openstream("Storage2/Stream2") as op:
        x = op.read()
    with ole.openstream("Storage0/Stream0") as op:
        y = op.read()
    if len(x) <= 10814:
        raise EmptyFile("No amplification was performed in this file")

    parts = y.split(b"\xf0\xe7i\xa5")

    if len(parts) == 1058 or len(parts) == 1074:
        return 0
    if len(parts) == 1154:
        return 1
    if ord3(x[0xF32]) != 0:
        return 0
    else:
        return 1


def extract_well_names_and_assay_names(ole, fileformat, empty_assays_ok=False):
    """Read well and assay names from an MXP file"""
    # print 'using fileformat', fileformat
    if isinstance(ole, olefile.OleFileIO):
        path = "Storage0/Stream0"
        with ole.openstream(path) as op:
            d = op.read()
    else:
        path = os.path.join(ole, "Storage0_Stream0")
        with open(path, "rb") as op:
            d = op.read()
    parts = d.split(b"\xf0\xe7i\xa5")
    if fileformat == 1:
        # starting at 0, it's allways \x01\x00\x00\x00
        well_parts = [parts[x] for x in xrange(2, len(parts), 12)]
        well_type_parts = [parts[x] for x in xrange(3, len(parts), 12)]
        # 4 is 1 0 0 0's again...
        # so is 5
        # so is 6, 7, 8
        start = 9
        assay_parts = [parts[x] for x in xrange(start, len(parts), 12)]
        lengths = np.array([ord3(part[8]) for part in assay_parts])
        if (lengths == 0).all():
            start = 7
            assay_parts = [parts[x] for x in xrange(start, len(parts), 12)]
            lengths = np.array([ord3(part[8]) for part in assay_parts])
            if (lengths == 0).all():
                start = 8
                assay_parts = [parts[x] for x in xrange(start, len(parts), 12)]
                lengths = np.array([ord3(part[8]) for part in assay_parts])
                if (lengths == 0).all():
                    start = 6
                    assay_parts = [parts[x] for x in xrange(start, len(parts), 12)]
                    lengths = np.array([ord3(part[8]) for part in assay_parts])
                    if (lengths == 0).all() and not empty_assays_ok:
                        import pprint

                        pprint.pprint(list(enumerate(parts[:20])))
                        raise ValueError("Could not read assay names in this file")
        set_id_parts = [parts[x] for x in xrange(10, len(parts), 12)]
    elif fileformat == 0:
        if len(parts) == 866:  # must be an older file format...
            well_parts = [parts[x] for x in xrange(2, len(parts), 9)]
            well_type_parts = [parts[x] for x in xrange(3, len(parts), 9)]
            assay_parts = [parts[x] for x in xrange(7, len(parts), 9)]
        else:
            well_parts = [parts[x] for x in xrange(2, len(parts), 11)]
            well_type_parts = [parts[x] for x in xrange(3, len(parts), 11)]
            assay_parts = [parts[x] for x in xrange(8, len(parts), 11)]
            if len(parts) == 1074:
                if len(well_parts) == 98:
                    well_parts = well_parts[:96]
                if len(assay_parts) == 97:
                    assay_parts = assay_parts[:96]
        fileformat = 0
    else:
        raise ValueError("fileformat")
    if len(well_parts) != 96:
        raise ValueError(
            "Did not find 96 well parts in Storage0 - was %i" % len(well_parts)
        )
    well_names = []
    for part in well_parts:
        length = ord3(part[4])
        name = part[5 : 5 + length]
        well_names.append(name)
    assay_names = []
    for part in assay_parts:
        length = ord3(part[8])
        name = part[9 : 9 + length]
        assay_names.append(name)
    well_types = []
    for part in well_type_parts:
        length = ord3(part[4])
        name = part[5 : 5 + length]
        well_types.append(name)
    set_ids = []
    if fileformat == 1:
        for part in set_id_parts:
            length = ord3(part[4])
            name = part[5 : 5 + length]
            set_ids.append(name)
    else:
        set_ids = [b''] * len(assay_names)

    well_names = np.array(well_names, dtype=object)
    assay_names = np.array(assay_names, dtype=object)
    well_types = np.array(well_types, dtype=object)
    set_ids = np.array(set_ids, dtype=object)
    # if (well_names == '').all(): # I have seen files without well names asigned...
    # raise ValueError("Could not find a single well name in that file!")
    if (assay_names == b"").all() and not empty_assays_ok:
        raise ValueError("Could not find a single assay name in that file!")
    return well_names, assay_names, well_types, set_ids


def to_16_bit(letters):
    """Convert the internal (little endian) number format to an int"""
    a = ord3(letters[0])
    b = ord3(letters[1])
    return (b << 8) + a


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def split_aligned(to_split, splitter):
    all_positions = find_all(to_split, splitter)
    filtered = [x for x in all_positions if (x % 2) == 0]
    if filtered[0] != 0:
        filtered.insert(0, 0)
    filtered.append(len(to_split))
    for start, stop in zip(filtered, filtered[1::]):
        yield to_split[start + len(splitter) : stop]


def no_of_different_values(text):
    c = collections.Counter()
    for char in text:
        c[char] += 1
    return len(c)


def extract_amplification_curves(ole, fileformat, allowed_cycles, supposed_wells=96):
    """extract amplification curves (40 cycles, 96 wells...) from an mxp file"""
    path = "Storage2/Stream2"
    with ole.openstream(path) as op:
        x = op.read()
    # if len(x) <= 10814:
    # raise EmptyFile("No amplification was performed in this file")
    x = x.split(b"\x00\x00\x00\x60")  # 96...

    # we first have to determine which segment we're reading
    offset = 3  # this is where the segments start...
    if no_of_different_values(x[offset]) < 10:
        offset += 1
    if no_of_different_values(x[offset]) < 10:
        offset += 1
    if no_of_different_values(x[offset]) < 10:
        raise EmptyFile("Could not find amplification data in this file")

    if fileformat == 0:  # I really which I had a smarter way to do this
        no_of_cycles = -1
        for c in x[offset]:
            if c != chr(0).encode("ascii")[0]:
                no_of_cycles = ord3(c)
                break
    elif fileformat == 1:
        no_of_cycles = -1
        for c in x[offset]:
            if c != chr(0).encode("ascii")[0]:
                no_of_cycles = ord3(c)
                break
        if no_of_cycles == -1:
            offset = offset - 1
            no_of_cycles = ord3(x[offset][9])
    else:
        raise ValueError("Unknown fileformat")
    if no_of_cycles not in allowed_cycles:
        print(b"%x" % x[4].find(b"("), fileformat)
        # raise ValueError(
        # "File contained an unexpected number of cycles: %i. Allowed: %s" %
        # (no_of_cycles, allowed_cycles))
    seperator = b"\x00\x00\x00" + chr(no_of_cycles).encode("latin1")
    y = x[offset]
    while y.count(seperator) < supposed_wells:
        offset += 1
        y = y + b"\x00\x00\x00\x60" + x[offset]
    y = y.split(seperator)
    y = y[1:]  # some kind of header maybe? seems pretty empty
    # we assume the most common length to be the block length.
    org = y[:]
    length_counts = collections.Counter()
    for x in y:
        length_counts[len(x)] += 1
    block_len = length_counts.most_common(1)[0][0]

    y[-1] = y[-1][
        :block_len
    ]  # there is a different seperator after the last one, so we set it to the first length

    if max(set([len(a) for a in y])) > 966:  # 816: #572: #476: #466: #428:
        # for ii, a in enumerate(y):
        # print ii, len(a)
        raise ValueError("Seen a very large chunk: %i " % max(set([len(a) for a in y])))
    result_fluorescence = []
    result_temperatures = []

    # patch together broken blocks
    for block_id, block in enumerate(y):
        if block is False:
            continue
        start_id = block_id
        while len(y[start_id]) < block_len and (
            block_id + 1 < len(y) - 1
        ):  # sometimes the splitter appers in the data. then we patch it up.
            y[start_id] = y[start_id] + seperator + y[block_id + 1]
            y[block_id + 1] = False
            block_id += 1
    y = [x for x in y if x is not False]
    if block_len < 724:
        for block_id, block in enumerate(y):
            if block is not False:
                if block_id > supposed_wells:
                    break
                numbers = [
                    to_16_bit(block[3 + offset * 10 : 3 + 2 + offset * 10])
                    for offset in xrange(0, no_of_cycles)
                ]
                if len(numbers) != no_of_cycles:
                    raise ValueError("Not exactly 40 datapoints in amplification curve")
                result_fluorescence.append(numbers)
                temperatures = np.array(
                    [
                        to_16_bit(block[3 + 4 + offset * 10 : 3 + 4 + 2 + offset * 10])
                        / 10.0
                        for offset in xrange(0, no_of_cycles)
                    ]
                )
                if (temperatures > 120).any():
                    raise ValueError(
                        "Temperature above 120 degrees obsereved. Most likely a parsing error"
                    )
                result_temperatures.append(temperatures)
    elif block_len in (724, 726, 748, 796):  # blocks with two samples per cycle
        for block_id, block in enumerate(y):
            if block is not False:
                if block_id > supposed_wells:
                    break

                all_numbers = [
                    to_16_bit(block[3 + offset * 2 : 3 + 2 + offset * 2])
                    for offset in xrange(0, no_of_cycles * 9)
                ]
                numbers = [all_numbers[x * 9] for x in xrange(0, no_of_cycles)]
                if len(numbers) != no_of_cycles:
                    raise ValueError("Not exactly 40 datapoints in amplification curve")
                result_fluorescence.append(numbers)
                temperatures = np.array(
                    [all_numbers[x * 9 + 2] / 10.0 for x in xrange(0, no_of_cycles)]
                )
                if (temperatures > 120).any():
                    raise ValueError(
                        "Temperature above 120 degrees obsereved. Most likely a parsing error"
                    )
                result_temperatures.append(temperatures)
    elif block_len == 806:
        for block in y:
            all_numbers = [
                to_16_bit(block[3 + offset * 2 : 3 + 2 + offset * 2])
                for offset in xrange(0, no_of_cycles * 9)
            ]
            numbers = [all_numbers[x * 5] for x in xrange(0, no_of_cycles)]
            result_fluorescence.append(numbers)
            temperatures = np.array(
                [all_numbers[x * 5 + 2] / 10.0 for x in xrange(0, no_of_cycles)]
            )
            result_temperatures.append(temperatures)
            if (temperatures > 120).any():
                raise ValueError(
                    "Temperature above 120 degrees obsereved. Most likely a parsing error"
                )
    elif block_len in (816,):
        for block in y:
            all_numbers = [
                to_16_bit(block[3 + offset * 2 : 3 + 2 + offset * 2])
                for offset in xrange(0, no_of_cycles * 9)
            ]
            numbers = [all_numbers[x * 6] for x in xrange(0, no_of_cycles)]
            result_fluorescence.append(numbers)
            temperatures = np.array(
                [all_numbers[x * 6 + 2] / 10.0 for x in xrange(0, no_of_cycles)]
            )
            result_temperatures.append(temperatures)
            if (temperatures > 120).any():
                raise ValueError(
                    "Temperature above 120 degrees obsereved. Most likely a parsing error"
                )
    else:
        raise ValueError("unexpected block length: %i" % block_len)

    if len(result_fluorescence) != supposed_wells:
        raise ValueError(
            "Not exactly the supposed %i wells - was %i"
            % (supposed_wells, len(result_fluorescence))
        )
    return result_fluorescence, result_temperatures
