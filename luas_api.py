import requests
import xmltodict
import luas_stops


class Luas(object):
    def __init__(self, stop):
        self.url = 'https://luasforecasts.rpa.ie/xml/get.ashx'
        self.stop_info_json = luas_stops.stops['stations']
        self.stop_abbreviation = self.stop_names_abbreviation(stop.lower())
        self.response = self.request_stop_info
        self.response_content = self.stop_request_content
        self.mapping = {
            "Inbound": self.trams_inbound,
            "Outbound": self.trams_outbound
        }

    def stop_names_abbreviation(self, stop):
        for stop_info in self.stop_info_json:
            if stop in stop_info['displayName'].lower():
                return stop_info['shortName']

    @property
    def request_stop_info(self):
        params = {
            'stop': self.stop_abbreviation,
            'action': 'forecast',
            'encrypt': 'false'
        }
        return requests.get(self.url, params=params)

    @property
    def stop_request_content(self):
        xml_text = self.response.text
        return xmltodict.parse(xml_text)

    @property
    def time_of_request(self):
        return self.response_content['stopInfo']['@created']

    @property
    def stop(self):
        return self.response_content['stopInfo']['@stop']

    @property
    def message(self):
        return self.response_content['stopInfo']['message']

    @property
    def trams_inbound(self):
        return self.response_content['stopInfo']['direction'][0]['tram']

    @property
    def trams_outbound(self):
        return self.response_content['stopInfo']['direction'][1]['tram']

    @property
    def schedule(self):
        message = '{}\n{}\n'.format(self.stop, self.message)
        message = self.direction_trams_message("Inbound", message)
        message = self.direction_trams_message("Outbound", message)
        return message

    def direction_trams_message(self, direction, message):
        message += '\n==============================\n'
        message += f'{direction}'
        message += '\n==============================\n'
        for luas in self.mapping[direction]:
            try:
                message += '{} - {}\n'.format(luas['@destination'], luas['@dueMins'])
            except TypeError:
                message += '{} - {}\n'.format(self.mapping[direction]['@destination'], self.mapping[direction]['@dueMins'])
        return message


if __name__ == '__main__':
    rti = Luas('central park')
    print(rti.schedule)
