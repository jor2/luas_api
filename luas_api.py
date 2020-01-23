import requests
import xmltodict
import luas_stops


class Luas(object):
    def __init__(self, stop):
        self.url = 'https://luasforecasts.rpa.ie/xml/get.ashx'
        self.stop_info_json = luas_stops.stops['stations']
        self.stop_abbreviation = self.stop_names_abbreviation(stop.lower())
        self.response = self.stop_request_content

    def stop_names_abbreviation(self, stop):
        for stop_info in self.stop_info_json:
            if stop in stop_info['displayName'].lower():
                return stop_info['shortName']

    def request_stop_info(self):
        params = {
            'stop': self.stop_abbreviation,
            'action': 'forecast',
            'encrypt': 'false'
        }
        return requests.get(self.url, params=params)

    @property
    def stop_request_content(self):
        xml_text = self.request_stop_info().text
        return xmltodict.parse(xml_text)

    @property
    def time_of_request(self):
        return self.response['stopInfo']['@created']

    @property
    def stop(self):
        return self.response['stopInfo']['@stop']

    @property
    def message(self):
        return self.response['stopInfo']['message']

    @property
    def trams_inbound(self):
        return self.response['stopInfo']['direction'][0]['tram']

    @property
    def trams_outbound(self):
        return self.response['stopInfo']['direction'][1]['tram']

    def print_schedule(self):
        print(self.stop)
        print(self.message + "\n")

        print('Inbound')
        for luas in self.trams_inbound:
            print(luas['@destination'] + ' - ' + luas['@dueMins'])

        print('\nOutbound')
        for luas in self.trams_outbound:
            print(luas['@destination'] + ' - ' + luas['@dueMins'])


rti = Luas('harcourt')
rti.print_schedule()
