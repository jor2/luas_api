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

        message += '\n==============================\n'
        message += 'Inbound'
        message += '\n==============================\n'
        for luas in self.trams_inbound:
            if len(luas) > 1:
                message += '{} - {}\n'.format(luas['@destination'], luas['@dueMins'])
            else:
                message += '{} - {}\n'.format(self.trams_inbound['@destination'], self.trams_inbound['@dueMins'])

        message += '\n==============================\n'
        message += 'Outbound'
        message += '\n==============================\n'
        for luas in self.trams_outbound:
            message += '{} - {}\n'.format(luas['@destination'], luas['@dueMins'])
        return message


if __name__ == '__main__':
    rti = Luas('central park')
    print(rti.schedule)
