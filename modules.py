from sol import CMV2, Launchpad, Nova, Monkelabs, MagicEdenSniper
from eth import ETH
from opensea import Sniper, OfferSender
_MODULES = {
    'SOL': {
        'cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ': CMV2,
        'CMZYPASGWeTz7RNGHaRJfCq2XQ5pYK6nDvVQxzkH51zb': Launchpad,
        'nva24Y1vHfhCrCLcqqFLXher9uZR4JjKP4D89MHhkmA': Nova,
        'Monkelabs': Monkelabs,
        'MagicEdenSniper': MagicEdenSniper },
    'ETH': {
        'ETH': ETH },
    'OpenSea': {
        'Sniper': Sniper,
        'OfferSender': OfferSender } }