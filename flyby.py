import requests
import datetime
import json


def flyby(latitude, longitude):
    """
    Queries NASA's public API to get the data for when pictures of a particular
    location were taken
    :param latitude: latitude value for a location
    :param longitude: longitude value for a location
    """

    # make sure the values passed are floats
    if type(latitude) is not float or type(longitude) is not float:
        raise ValueError('Please enter float values')

    # Throw an error if latitude and longitude are not in expected range
    if latitude > 90 or latitude < -90 or longitude > 180 or longitude < -180:
        raise ValueError('Please check the value of co-ordinates entered')
        return

    # Set parameters for API request
    api_url = 'https://api.nasa.gov/planetary/earth/assets'
    coordinates = {
        'lat': latitude,
        'lon': longitude,
        'api_key': '9Jz6tLIeJ0yY9vjbEUWaH9fsXA930J9hspPchute'
    }

    # Query the API to get the results for a location
    result = requests.get(api_url, params=coordinates)

    # full json data of GET request
    data = result.json()
    # print(result.json())

    # Check the HTTP status code for failures
    if result.status_code is not 200:
        print('!!ERROR!! API call returned an unexpected status ' % result.status_code)
        return

    calculateTime(data)


def calculateTime(data):
    """
    Accepts the JSON format of data returned by NASA's API and calculates and prints time
    the next picture will be taken
    :param data: NASA's returned data in JSON format
    """

    # If NASA does not provide at least 2 values to calculate 1 time delta, no predictions can be made
    if data['count'] < 2:
        print('!!ERROR!!Not enough data to make a prediction.')
        return

    # parse unicode dates to datetime dates
    dates = [datetime.datetime.strptime(i['date'], '%Y-%m-%dT%H:%M:%S') for i in data['results']]

    dates.sort()

    # compute time deltas between each image
    time_deltas = [(dates[i + 1] - dates[i]) for i in range(0, len(dates) - 1)]

    # calculate the average time between images
    avg_time_delta = sum(time_deltas, datetime.timedelta()) / len(time_deltas)

    # print(avg_time_delta)
    # print(dates[len(dates)-1])

    # print the next average date and time of the picture that will be taken for provided location
    # by adding the average delta time to the last date a picture was taken
    currentDate = datetime.datetime.now()
    calculatedDate = dates[len(dates) - 1] + avg_time_delta
    #print(currentDate)
    #print(calculatedDate)

    while(currentDate > calculatedDate):
        #print(calculatedDate)
        #print(avg_time_delta)
        calculatedDate = calculatedDate + avg_time_delta

    print(calculatedDate)
    #print('Next time: ' + str(dates[len(dates) - 1] + avg_time_delta))


def main():
    flyby(37.7937007, -122.4039064)


if __name__ == "__main__":
    main()
