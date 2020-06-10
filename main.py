class NMEA:
    def __init__(self, data):
        self.data = data
        self.error = False
        self.error_msg = ''

        if len(data) < 6:
            self.__error('Sentence is too short!')
            return

        if len(data) > 82:
            self.__error('Sentence is too long! It may contain up to 80 characters plus `$` and CR/LF.')
            return

            # $ - hex 24
        # ! - hex 21
        if data[0] == '$':
            self.hex = 24
        elif data[0] == '!':
            self.hex = 21
        else:
            self.hex = None
            self.__error('Wrong format! Sentence must start with `$` or `!`!')
            return

        data = data.split(',')

        # GP - GPS
        # GL - GLONASS
        # GN - GLONASS + GPS
        if data[0][1:-3] in ['GP', 'GL', 'GN']:
            self.talker_identifier = data[0][1:-3]
        elif data[0][1:-3] in ['AG', 'AP', 'CD', 'CR', 'CS', 'CT', 'CV', 'CX', 'DF', 'EC',
                               'EP', 'ER', 'GP', 'HC', 'HE', 'HN', 'II', 'IN', 'LC', 'P',
                               'RA', 'SD', 'SN', 'SS', 'TI', 'VD', 'DM', 'VW', 'WI', 'YX',
                               'ZA', 'ZC', 'ZQ', 'ZV']:
            self.talker_identifier = data[0][1:-3]
            self.__error('Talker identifier `' + data[0][1:-3] + '` is not supported!')
            return
        else:
            self.talker_identifier = None
            self.__error('Unknown talker identifier `' + data[0][1:-3] + '`!')
            return

        # GSV - Satellites in view
        # RMC - Recommended Minimum Navigation Information
        # VTG - Track Made Good and Ground Speed
        if data[0][-3:] in ['GSV', 'RMC', 'VTG']:
            self.sentence_identifier = data[0][-3:]
        else:
            self.sentence_identifier = None
            self.__error('Unknown or unsupported sentence identifier `' + data[0][-3:] + '`!')
            return

        if self.sentence_identifier == 'GSV':
            self.__parse_GSV(data[1:])

    def __parse_GSV(self, data):
        self.number_of_messages = int(data[0])
        self.message_number = int(data[1])
        self.satellites_in_view = int(data[2])
        self.satellite_number = data[3]
        self.elevation = data[4]  # in degrees
        self.azimuth = data[5]  # in degrees

    def __error(self, msg):
        self.error = True
        self.error_msg = msg

    def __str__(self):
        if self.error:
            return 'error: True\n' \
                   'error_msg: ' + self.error_msg
        else:
            out = 'error: False\n'
            out += 'talker_identifier: ' + str(self.talker_identifier) + '\n'
            out += 'sentence_identifier: ' + str(self.sentence_identifier) + '\n'
            if self.sentence_identifier == 'GSV':
                out += 'number_of_messages: ' + str(self.number_of_messages) + '\n'
                out += 'message_number: ' + str(self.message_number) + '\n'
                out += 'satellites_in_view: ' + str(self.satellites_in_view) + '\n'
                out += 'satellite_number: ' + str(self.satellite_number) + '\n'
                out += 'elevation: ' + str(self.elevation) + '\n'
                out += 'azimuth: ' + str(self.azimuth) + '\n'
            out += 'hex: ' + str(self.hex)
            return out


a = NMEA('$GLGSV,2,1,06,74,03,356,23,66,56,033,25,82,66,331,46,83,17,324,2563')
print(a)
