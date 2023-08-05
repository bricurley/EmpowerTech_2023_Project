GOOD_OPTIONS = {'Walk Outside': {
        'Mental Health': 2,
        'Physical Health': 5,
        'Social Standing': 5,
        'Desctiption': 'You go on a walk to ease your stress, get some exercise, and make new friends'
    },
    'Solid Sleep': {
        'Mental Health': 5,
        'Physical Health': 5,
        'Description': 'You get a good night\'s rest to recharge both your mental and physical health'
    }, 
    'Make Friends': {
        'Social Standing': 10,
        'Mental Health': 5,
        'Description': 'You are able to find people to open up to and connect with'
    }
    }

BAD_OPTIONS = {'Alcohol': {
        'Mental Health': -5,
        'Drug Dependency': 5,
        'Money': -50,
        'Description': 'You turn to alcohol as a way to cope. But it is expensive and only a temporary solution'
    },
    'Burn Bridges': {
        'Mental Health': 5,
        'Social Standing': -10,
        'Description': 'You refuse to accept help and support from close friends'
    },
    'The Bar': {
        'Mental Health': -5,
        'Drug Dependency': 5,
        'Physical Health': -5,
        'Social Standing': 5,
        'Money': -35,
        'Description': 'You go to the bar to loosen up and feel cool, but spend money and the alcohol affects your health'
    },
    'Skip Exercise for 1 Week': {
        'Mental Health': -5,
        'Physical Health': -10,
        'Description': 'You skip exercising, leaving you feeling drained and out of energy'
    }
}

MIXED_OPTIONS = {'Therapy': {
        'Money': -100,
        'Mental Health': 10,
        'Social Standing': -5,
        'Drug Dependency': -5,
        'Description': 'You open up through therapy and find help other than drugs. Unfortunately, there are costs and social stigma as well'
    },
    'Medication': {
        'Money': -35,
        'Mental Health': 10,
        'Drug Dependency': 5,
        'Social Standing': -5,
        'Description': 'Medication helps, but can be expensive, increase drug dependency, and have social stigma associated with it'
    },
    'Social Media': {
        'Mental Health': -5,
        'Social Standing': 5,
        'Description': 'You doomscroll tiktok, leaving you drained but found a friend doing the same'
    },
    'Work Extra Hours': {
        'Social Standing': 5,
        'Money': 100,
        'Mental Health': -5,
        'Description': 'You skip family time to work, leaving you feeling drained and alone with more money'
    },
    'Mental Health Day': {
        'Mental Health': 5,
        'Social Standing': -5,
        'Money': -100,
        'Description': 'You skip work to recharge, you couldn\'t work and people look down on you but you feel great'
    }
}

ALL_OPTIONS = GOOD_OPTIONS | BAD_OPTIONS | MIXED_OPTIONS
