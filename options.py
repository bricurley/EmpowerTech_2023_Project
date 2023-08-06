GOOD_OPTIONS = {'Walk Outside': {
        'Mental Health': 2,
        'Physical Health': 5,
        'Social Standing': 5,
        'Description': 'You go on a walk to ease your stress, get some exercise, and make new friends'
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
    },
    'Journal Entry': {
        'Mental Health': 10,
        'Description': 'You write in your journal to destress from the comfort of your bedroom desk'
    }
    }

BAD_OPTIONS = {'Alcohol': {
        'Mental Health': -5,
        'Drug Independency': -15,
        'Money': -50,
        'Description': 'You turn to alcohol as a way to cope. But it is expensive and only a temporary solution'
    },
    'Burn Bridges': {
        'Mental Health': -5,
        'Social Standing': -10,
        'Description': 'You refuse to accept help and support from close friends'
    },
    'The Bar': {
        'Mental Health': -5,
        'Drug Independency': -5,
        'Physical Health': -5,
        'Social Standing': 5,
        'Money': -35,
        'Description': 'You go to the bar to loosen up and feel cool,\nbut spend money and the alcohol affects your health'
    },
    'No Exercise': {
        'Mental Health': -5,
        'Physical Health': -10,
        'Description': 'You skip exercising, leaving you feeling drained and out of energy'
    },
    'All Nighter Studying': {
        'Mental Health': -10,
        'Physical Health': -10,
        'Description': 'You are stressed for an exam and study too much, and perform poorly due to lack of sleep'
    },
    'Lose Temper': {
        'Mental Health': -10,
        'Social Standing': -15,
        'Description': 'You are feeling very overwhelmed and stressed and lash out at your friends'
    }
}

MIXED_OPTIONS = {'Therapy': {
        'Money': -100,
        'Mental Health': 10,
        'Social Standing': -5,
        'Drug Independency': 5,
        'Description': 'You open up through therapy and find help other than drugs.\nUnfortunately, there are costs and social stigma as well'
    },
    'Medication': {
        'Money': -35,
        'Mental Health': 10,
        'Drug Independency': -10,
        'Social Standing': -5,
        'Description': 'Medication helps, but can be expensive, increase drug dependency, and have social stigma\nassociated with it'
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
    },
    'Self Care Day': {
        'Mental Health': 10,
        'Money': -35,
        'Description': 'You take a day off you get your favorite ice cream but you spend money.'
    },
    'Healthy Boundaries': {
        'Social Standing': -10,
        'Mental Health': 10,
        'Description': 'You need to take care of yourself but people are upset you aren\'t there for them as much'
    },
    'No Boundaries': {
        'Social Standing': 10,
        'Mental Health': -10,
        'Description': 'You become a people pleaser, which makes you more popular but lets people take advantage of you'
    }
}

BIG_EVENTS = [['MAJOR EVENT:\nYou fall very ill',
               {'Work Anyway': {
                   'Description': 'You needed the money but could not take care of yourself at the same time\nYou also make your coworkers sick and mad at you',
                   'Mental Health': -20,
                   'Money': 150,
                   'Mental Health':-20,
                   'Social Standing': -10,
                   'Physical Health': -20
               }}, 
               {'Work at Home': {
                   'Description': 'You still need the money from your paycheck, but decide to take it easy for now\nYour coworkers are grateful you also aren\'t risking their health',
                   'Mental Health': 5,
                   'Money': 100,
                   'Social Standing': 10,
                   'Physical Health': 5
               }}, 
               {'Rest Day': {
                   'Description': 'You don\'t get paid, but know your health and the safety of your coworkers come first',
                   'Mental Health': 20,
                   'Physical Health': 20,
                   'Social Standing': 10,
                   'Money': -50
               }}], 
               ['MAJOR EVENT:\nYou have a panic attack', 
                {'Go to therapy': {
                    'Description': 'Despite the cost and feeling a little ashamed for seeking help, you decide to speak up and start getting help',
                    'Mental Health': 20,
                    'Physical Health': 15,
                    'Social Standing': -15,
                    'Money': -50
                }},
                {'Talk to a friend': {
                    'Description': 'You confide in a trusted friend who can help comfort you',
                    'Mental Health': 10,
                    'Physical Health': 10,
                    'Social Standing': 5
                }}, 
                {'Ignore and let pass': {
                    'Description': 'You do nothing, but this only causes it to keep happening',
                    'Mental Health': -20,
                    'Physical Health': -15
                }}],
                ['MAJOR EVENT:\nYou have a stressful week at work',
                 {'Take next week off': {
                     'Description': 'You feel better after resting even though you missed out on the week\'s pay.\nYour coworkers seem disappointed in you for taking time off',
                     'Mental Health': 20,
                     'Physical Health': 15,
                     'Social Standing': -15,
                     'Money': -75
                 }},
                 {'Work overtime': {
                     'Description': 'You make all of your deadlines at work and get paid, but it takes a toll on you.\nYour coworkers are also happy with you',
                     'Mental Health': -20,
                     'Money': 100,
                     'Physical Health': -15,
                     'Social Standing': 15
                 }},
                 {'Find a new job': {
                     'Description': 'You find a new job but it doesn\'t pay as well.\nYour coworkers and boss also seem disappointed with you for prioritizing your health',
                     'Money': 30,
                     'Mental Health': 15,
                     'Physical Health': 10,
                     'Social Standing': -20
                 }}]]

ALL_OPTIONS = GOOD_OPTIONS | BAD_OPTIONS | MIXED_OPTIONS

print(BIG_EVENTS)