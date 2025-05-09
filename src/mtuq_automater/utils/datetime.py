
import obspy


def _super(datetime):
    if isinstance(datetime, str):
        return UTCDateTime(datetime)

    elif isinstance(datetime, obspy.UTCDateTime):
        return UTCDateTime(str(datetime))

    else:
        print('Unrecognized datetime type: {type(datetime)}')
        raise TypeError


class UTCDateTime(obspy.UTCDateTime):
    def format_custom(utc):
        """ Returns  YYYY-DD-MM--HH-MM-DD

        Possible advantages:
         - it works for file and directory names
         - for me personally it is much easier to read than most others

        """
        year  = utc.year
        month = utc.month
        day   = utc.day

        hour   = utc.hour
        minute = utc.minute
        second = utc.second

        utc_str = f'{year:4d}-{month:02d}-{day:02d}--{hour:02d}-{minute:02d}-{second:02d}'
        return utc_str

    def format_iris(self, *args, **kwargs):
        """ Returns  YYYY-DD-MMTHH:MM:SS.SSS
        """
        return self.format_iris_web_service(*args, **kwargs)


