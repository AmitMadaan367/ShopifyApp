class Config(object):
    HOST = 'influencersclub.herokuapp.com/'

    SHOPIFY_CONFIG = {
        'API_KEY': 'd6ec9af939c5a44627d94b3b02a2ef34',
        'API_SECRET': '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',
        'APP_HOME': 'https://' + HOST,
        'CALLBACK_URL': 'https://' + HOST + '/install',
        'REDIRECT_URI': 'https://influencersclub.herokuapp.com/connect',
        'SCOPE': 'read_products, read_orders, read_all_orders'
    }
