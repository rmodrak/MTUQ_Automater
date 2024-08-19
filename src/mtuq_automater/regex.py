
def regex_patterns(event):
    #
    # To generate event-specific MTUQ scripts, we apply a regular expression
    # substitution (similar to a sed command) to every of one of the existing
    # template files below.
    #
    # The following gets applied to every line of the template file:
    #
    #   value = format % value
    #   re.sub(pattern+'.*', pattern+value, line)
    #

    return [
        # pattern, format, value
        ['event_id=    ',  '\'%s\'',       event['event_tag']],
        ['path_data=    ',  '\'%s\'',      event['path_data']],
        ['path_weights= ',  '\'%s\'',      event['path_weights']],
        ['\'time\':',       '\'%s\',',     event['origin_time']],
        ['\'latitude\':',   '%f,',         event['event_latitude']],
        ['\'longitude\':',  '%f,',         event['event_longitude']],
        ['\'depth_in_m\':', '%f,',   (1.e3*event['event_depth_km'])],
        ['magnitude=',      '%f',          event['event_magnitude']],
        ['magnitudes=',     '[%f],',        event['event_magnitude']],
        ]

