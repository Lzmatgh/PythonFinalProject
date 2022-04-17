import webbrowser
import requests
import json
# can import the API Key from a module file to make the program safe.
import secrets


# weather API
def weather_API(location):
    url_weather = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q":location,"days":"3"}
    apikey = secrets.apikey_weatherapi

    headers = {
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
        "X-RapidAPI-Key": apikey
    }
    # caching
    request_key = construct_unique_key(url_weather, querystring)
    if request_key in CACHE_DICT_weather.keys():
        print("cache hit!", request_key)
        # return CACHE_DICT_weather[request_key]
    else:
        print("cache miss!", request_key)
        # CACHE_DICT_weather[request_key] = make_request(baseurl, params)
        weather_response = requests.request("GET", url_weather, headers=headers, params=querystring)
        weather_json = weather_response.json()
        CACHE_DICT_weather[request_key] = weather_json
        save_cache(CACHE_DICT_weather, cache_weather_name)

    print(CACHE_DICT_weather[request_key]['location']['name'])
    return CACHE_DICT_weather[request_key]


def covid_API(coordinates):
    # covid API
    url_covid = "https://geocovid-19.p.rapidapi.com/geocovid"
    querystring = {"coordinates": coordinates}

    headers = {
        "X-RapidAPI-Host": "geocovid-19.p.rapidapi.com",
        "X-RapidAPI-Key": secrets.apikey_covidapi
    }

    # caching
    request_key = construct_unique_key(url_covid, querystring)
    if request_key in CACHE_DICT_covid.keys():
        print("cache hit!", request_key)
    else:
        print("cache miss!", request_key)
        covid_response = requests.request("GET", url_covid, headers=headers, params=querystring)
        covid_json = covid_response.json()
        CACHE_DICT_covid[request_key] = covid_json
        save_cache(CACHE_DICT_covid, cache_covid_name)


    print(CACHE_DICT_covid[request_key]['response']['data']['place_name'])
    print(CACHE_DICT_covid[request_key]['response']['data']['last_7_days_trend'])

    return CACHE_DICT_covid[request_key]


def yelp_API(params):
    apikey = secrets.apikey_yelpfusionapi
    headers = {'Authorization': 'Bearer ' + apikey}
    baseurl = 'https://api.yelp.com/v3/businesses/search?'


    # caching
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT_yelp.keys():
        print("cache hit!", request_key)
    else:
        print("cache miss!", request_key)
        yelp_response = requests.get(baseurl, params, headers=headers)
        print('yelp response code', yelp_response.status_code)
        yelp_json = yelp_response.json()
        CACHE_DICT_yelp[request_key] = yelp_json
        save_cache(CACHE_DICT_yelp, cache_yelp_name)


    print(CACHE_DICT_yelp[request_key])
    return CACHE_DICT_yelp[request_key]


###########################################################################################
# the caching part
def open_cache(cache_filename):
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(cache_filename, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}

    return cache_dict


def save_cache(cache_dict, cache_filename):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(cache_filename,"w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and
    repeatably identify an API request by its baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the unique key as a string
    '''
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector + connector.join(param_strings)
    return unique_key


# def make_request(baseurl, params):
#     '''Make a request to the Web API using the baseurl and params
#     Parameters
#     ----------
#     baseurl: string
#         The URL for the API endpoint
#     params: dictionary
#         A dictionary of param: param_value pairs
#     Returns
#     -------
#     string
#         the results of the query as a Python object loaded from JSON
#     '''
#     response = requests.get(endpoint_url, params=params, auth=oauth)
#     return response.json()


# def make_request_with_cache(baseurl, params):
#     '''Check the cache for a saved result for this baseurl+params
#     combo. If the result is found, return it. Otherwise send a new
#     request, save it, then return it.
#     Parameters
#     ----------
#     baseurl: string
#         The URL for the API endpoint
#     params: dictionary
#         A dictionary of param: param_value pairs
#     Returns
#     -------
#     string
#         the results of the query as a Python object loaded from JSON
#     '''
#     request_key = construct_unique_key(baseurl, params)
#     if request_key in CACHE_DICT.keys():
#         print("cache hit!", request_key)
#         return CACHE_DICT[request_key]
#     else:
#         print("cache miss!", request_key)
#         CACHE_DICT[request_key] = make_request(baseurl, params)
#         save_cache(CACHE_DICT)
#         return CACHE_DICT[request_key]




if __name__ == "__main__":

    # call the weather api
    CACHE_DICT_weather = {}
    cache_weather_name = 'cache_weather.json'
    CACHE_DICT_weather = open_cache(cache_weather_name)

    zipcode = '48105'
    weather_content = weather_API(zipcode)
    wind_kph = weather_content['current']['wind_kph']
    print(weather_content['current']['condition']['text'])
    print(f'the wind is: {wind_kph} kph')


    # call the covid api
    CACHE_DICT_covid = {}
    cache_covid_name = 'cache_covid.json'
    CACHE_DICT_covid = open_cache(cache_covid_name)

    coordinates = '37.381315,-122.046148'
    covid_content = covid_API(coordinates)

    # call the yelp api
    CACHE_DICT_yelp = {}
    cache_yelp_name = 'cache_yelp.json'
    CACHE_DICT_yelp = open_cache(cache_yelp_name)

    # params = {'term': 'delis', 'latitude': '37.786882', 'longitude': '-122.399972'}
    params = {'term': 'food', 'location': 'Ann Arbor'}
    content_yelp = yelp_API(params)

    # preprocess the data from the yelp API
    list_businesses = content_yelp['businesses']
    list_businesses.sort(key=lambda x: x['rating'], reverse=True)
    print('sort', list_businesses)
    high_rate_list = list_businesses[0:5]
    print(high_rate_list[-1])

    # build a tree #############################################################################
    finalTree = \
        ("Would you like to sort by rating or price?",
         ("Do you like (weather today) or (weather tomorrow)",
          (['I suggest go today, this is the 5 shop sorted by rating:[12345]'], None, None),
          (['I suggest go tomorrow, this is the 5 shop:[12345]'], None, None)),
         ("Do you like (weather today) or (weather tomorrow)",
          (['I suggest go today, this is the 5 shop sorted by price:[12345]'], None, None),
          (['I suggest go tomorrow, this is the 5 shop:[12345]'], None, None)))

    weather_today = weather_content['current']['condition']['text']
    print('test', weather_content['forecast']['forecastday'][1]['day']['condition']['text'])
    weather_tomorrow = weather_content['forecast']['forecastday'][1]['day']['condition']['text']
    weather_qst = f'Do you like {weather_today} or {weather_tomorrow}? former or latter?'

    list_businesses_rating = content_yelp['businesses']
    list_businesses_rating.sort(key=lambda x: x['rating'], reverse=True)
    list_businesses_rating = list_businesses_rating[0:5]

    list_businesses_price = content_yelp['businesses']
    list_businesses_price.sort(key=lambda x: x['rating'], reverse=False)
    list_businesses_price = list_businesses_price[0:5]


    finalTree = \
        ("Would you like to sort by rating or price? former or latter?",
         (weather_qst,
          (['I suggest you go today, this is the 5 restaurants sorted by rating:', list_businesses_rating], None, None),
          (['I suggest  you go tomorrow, this is the 5 restaurants sorted by rating:', list_businesses_rating], None, None)),
         (weather_qst,
          (['I suggest you go today, this is the 5 restaurants sorted by price:', list_businesses_price], None, None),
          (['I suggest you go tomorrow, this is the 5 restaurants sorted by price:', list_businesses_price], None, None)))


    def yes(prompt):
        while True:
            content = input(prompt)
            if content in ['yes', 'y', 'yup', 'sure']:
                return True
            elif content in ['no', 'n', 'nope']:
                return False
            else:
                print("Not a valid input, please enter \"yes\" or \"no\": ")


    def simplePlay(tree):
        """DOCSTRING!"""
        # 1. If the tree is a leaf, ask whether the object is the object named in the leaf.
        # Return True or False appropriately.
        # 2. If the tree is not a leaf, ask the question in the tree, that is tree[0]
        # If the user answers "yes", call yourself recursively on the subtree that is the second element in the triple.
        # If the user answers "no", recur on the subtree that is the third element in the triple.
        if isLeaf(tree):
            businesses_name = [x['name'] for x in tree[0][1]]
            businesses_details = [[x['name'], x['url']] for x in tree[0][1]]  # check format
            print([tree[0][0], businesses_name])
            ans = yes('Do you want to explore the details? ')
            if ans:
                print(businesses_details)
            else:
                print('Thank you!')



        else:
            content = input(f'{tree[0]} Enter \"former\" or \"latter\": ')
            while True:
                if content == 'former':
                    tree = tree[1]
                    return simplePlay(tree)  # there is no return value when recursively call the function itself, so return the function
                elif content == 'latter':
                    tree = tree[2]
                    return simplePlay(tree)
                else:
                    content = input(f'Not a valid input, {tree[0]} Enter \"former\" or \"latter\": ')


    def isLeaf(tree):
        if (tree[1] == None) and (tree[2] == None):
            return True
        else:
            return False


    # def playLeaf(node, weather_content, covid_content):
    #     # if isLeaf(node):
    #     #     ans = yes(f'I guess it is {node[0]}, am I correct? Enter \"yes\" or \"no\": ')
    #     #     if ans:
    #     #         print("I got it!")
    #     #         return node
    #     #     else:
    #     #         ans = input('Drats! What was it? ')
    #     #         qst = input(f'What\'s a question that distinguisheds between {ans} and {node[0]}? ')
    #     #         question_tf = yes(f"and what\'s the answer for {ans}? Please enter \"yes\" or \"no\"")
    #     #         if question_tf:
    #     #             new_leaf = (qst, (ans, None, None), (node[0], None, None))
    #     #         else:
    #     #             new_leaf = (qst, (node[0], None, None), (ans, None, None))
    #     #
    #     #         return new_leaf
    #     # else:
    #     #     ans = yes(f'{node[0]} Enter \"yes\" or \"no\": ')
    #     #     if ans:
    #     #         return tuple((node[0], playLeaf(node[1]), node[2]))
    #     #     else:
    #     #         return tuple((node[0], node[1], playLeaf(node[2])))
    #     ans = input('Would you like to sort the restaurant by rating (high to low) or price (low to high)? ')
    #     if ans == 'rating':
    #         weather_today = weather_content['current']['text']
    #         weather_tomorrow = weather_content['forecast']['forecastday'][1]['text']  # check format
    #         weather_qst = f'Do you like {weather_today} or {weather_tomorrow}?'
    #         new_leaf = (weather_qst, )




    # def play(tree):
    #     """DOCSTRING!"""
    #
    #     while True:
    #         tree = playLeaf(tree)
    #         # print('This is the new tree: ')
    #         # printTree(tree)
    #         ans = yes('Would you like to play again? ')
    #         if not ans:
    #             return tree

    newtree = simplePlay(finalTree)






