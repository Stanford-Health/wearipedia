import pandas as pd
import numpy as np


def create_syn_data(start_date, end_date):

    # Create a list of dates between start_date and end_date
    dates = pd.date_range(start_date, end_date, freq='D')

    # Create empty lists to store data
    goals = []
    daily_summary = []
    strength_exercises = []
    cardio_exercises = []
    breakfast = []
    lunch = []
    dinner = []
    snacks = []

    # Functions to generate synthetic data
    def syn_calories(x): return np.round(np.random.normal(2500, 200), 1)
    def syn_carbs(x): return np.round(np.random.normal(250, 75), 1)
    def syn_fat(x): return np.round(np.random.normal(75, 25), 1)
    def syn_protein(x): return np.round(max(0, np.random.normal(100, 25)), 1)

    def syn_sodium(x): return np.round(np.random.normal(2300, 500), 1)
    def syn_sugar(x): return np.round(np.random.normal(75, 25), 1)


# Scraped a list of all exercises from MyFitnessPal and used GPT3 to seperate them into strength and cardio exercises
    exercises_cardio = ['9Round',
                        'Aerobics',
                        'Aerobics, general',
                        'Aerobics, high impact',
                        'Aerobics, low impact',
                        'Aerobics, step, with 10-12 inch step',
                        'Aerobics, step, with 6-8 inch step',
                        'Aquathlon',
                        'Archery (non-hunting)',
                        'Automobile repair',
                        'Backpacking, general',
                        'Badminton, competitive',
                        'Badminton, social, general',
                        'Barre',
                        'Barre3',
                        "Barry's Bootcamp",
                        'Baseball',
                        'Basketball',
                        'Basketball, game',
                        'Basketball, nongame, general',
                        'Basketball, officiating',
                        'Basketball, shooting baskets',
                        'Basketball, wheelchair',
                        'Beat Saber',
                        'Belly dancing',
                        'Bench (Chest) Press, Machine',
                        'Bench Press, Barbell',
                        'Bicycling',
                        'Bicycling, 16-19 kph, light (cycling, biking, bike riding)',
                        'Bicycling, 19-23 kph, moderate (cycling, biking, bike riding)',
                        'Bicycling, 23-26 kph, vigorous (cycling, biking, bike riding)',
                        'Bicycling, 26-32 kph, very fast (cycling, biking, bike riding)',
                        'Bicycling, <16 kph, leisure (cycling, biking, bike riding)',
                        'Bicycling, >32 kph, racing (cycling, biking, bike riding)',
                        'Bicycling, BMX or mountain (cycling, biking, bike riding)',
                        'Bicycling, commuting, mountain biking',
                        'Bicycling, commuting, road cycling',
                        'Bicycling, cruiser bike',
                        'Bicycling, fixed gear',
                        'Bicycling, hybrid cycling',
                        'Bicycling, indoor',
                        'Bicycling, mountain',
                        'Bicycling, road cycle',
                        'Bicycling, stationary',
                        'Bicycling, touring bike',
                        'Bikram Yoga',
                        'Billiards',
                        'Bootcamp workout',
                        'Bowling',
                        'Brazilian Jiu Jitsu',
                        'Broomball',
                        'Calisthenics',
                        'Canoeing, on camping trip',
                        'Carpentry, general',
                        'Chair Yoga',
                        'Cheerleading',
                        'Chin-Ups',
                        'Chopping wood',
                        'Circuit training',
                        'Circuit training, Cardiovascular (CV)',
                        'Circuit training, Resistance',
                        'Circuit training, general',
                        'Class',
                        'Cleaning, heavy, vigorous effort',
                        'Cleaning, light',
                        'Cleaning, light, moderate effort',
                        'Club Pilates',
                        'Coaching: football, soccer, basketball, etc.',
                        'Cooking or food preparation',
                        'CorePower Yoga',
                        'Crew',
                        'Crewing',
                        'Cricket (batting, bowling)',
                        'Croquet',
                        'Cross Trainer',
                        'Cross trainer',
                        'CrossFit',
                        'Crossfit',
                        'Crunches and leg lifts',
                        'Curling',
                        'Curves Circuit Training',
                        'CycleBar',
                        'Dancing',
                        'Dancing, aerobic, ballet or modern, twist',
                        'Dancing, ballroom, fast',
                        'Dancing, ballroom, slow',
                        'Dancing, general',
                        'Darts, wall or lawn',
                        'Disc Golf',
                        'Diving, springboard or platform',
                        'Double Stroller, Bike',
                        'EverybodyFights',
                        'Fencing',
                        'Fhitting Room',
                        'Fishing',
                        'Fishing from boat, sitting',
                        'Fishing from river bank, standing',
                        'Fishing in stream, in waders',
                        'Fishing, general',
                        'Fishing, ice, sitting',
                        'Fitness band',
                        'Fixie Race/Event',
                        'Flywheel',
                        'Football',
                        'Football or baseball, playing catch',
                        'Football, competitive',
                        'Football, touch, flag, general',
                        'FreeLetics',
                        'Frisbee playing, general',
                        'Frisbee, ultimate',
                        'Gardening',
                        'Gardening, general',
                        'Generic',
                        'Golf, carrying clubs',
                        'Golf, miniature or driving range',
                        'Golf, pulling clubs',
                        'Golf, using power cart',
                        'Golfing',
                        'Gymnastics',
                        'Gymnastics, general',
                        'HIIT',
                        'Hacky sack',
                        'Handball, general',
                        'Handball, team',
                        'Heel Raise',
                        'Hiking',
                        'Hiking, climbing hills (carrying 4.5-9 kg load)',
                        'Hiking, climbing hills (carrying <4.5 kg load)',
                        'Hiking, cross country',
                        'Hockey',
                        'Hockey, field',
                        'Hockey, ice',
                        'Horse grooming',
                        'Horseback riding',
                        'Horseback riding, general',
                        'Horseback riding, trotting',
                        'Horseback riding, walking',
                        'Hunting',
                        'Hunting, general',
                        'Indoor bike trainer',
                        'Insanity',
                        'Jai alai',
                        'Jet skiing (riding jet ski, water ski-mobiling)',
                        'Judo, karate, kick boxing, tae kwan do',
                        'Jump roping',
                        'Jumping jacks, vigorous',
                        'Kangoo Jumps',
                        'Kayaking',
                        'Kickball',
                        'Kickboxing',
                        'Kickboxing (including Turbo Jam)',
                        'LES MILLS GRIT™',
                        'Lacrosse',
                        'Lagree Fitness™',
                        'Laps',
                        'Lawn mowing',
                        'Marching band, playing instrument(walking)',
                        'Marching, rapidly, military',
                        'Martial arts',
                        'Mild stretching',
                        'Mirror',
                        'Misc tasks, moderate',
                        'Motocross',
                        'Moving furniture, household',
                        'Moving household items, boxes, upstairs',
                        'Moving household items, carrying boxes',
                        'Mowing lawn, general',
                        'Mowing lawn, riding mower',
                        'Music playing, cello, flute, horn, woodwind',
                        'Music playing, drums',
                        'Music playing, guitar, classical, folk(sitting)',
                        'Music playing, guitar, rock/roll band(standing)',
                        'Music playing, piano, organ, violin, trumpet',
                        'Netball',
                        'November Project',
                        'Orangetheory',
                        'P90X',
                        'POP Tennis',
                        'PT session',
                        'Paddle Tennis',
                        'Paddleboat',
                        'Pedal Kayak',
                        'Peloton',
                        'Peloton Bike',
                        'Peloton Digital',
                        'Peloton Studio',
                        'Peloton Tread',
                        'Pelvic Lifts',
                        'Pickleball',
                        'Pilates',
                        'Pilates ProWorks',
                        'Pilates Reformer',
                        'Pilates video',
                        'Plank hold',
                        'Pole Dancing',
                        'Polo',
                        'Punching bag',
                        'Pure Barre',
                        'Race walking',
                        'Racquetball, casual, general',
                        'Racquetball, competitive',
                        'Raking lawn',
                        'Rappelling',
                        'Rear Deltoid Raise',
                        'Recumbant Trike',
                        'Rock climbing',
                        'Rock climbing, ascending rock',
                        'Rock climbing, rappelling',
                        'Roller blading (in-line skating)',
                        'Rollerblading',
                        'Rope jumping, fast',
                        'Rope jumping, moderate, general',
                        'Rope jumping, slow',
                        'Rucking, Heavy Pack',
                        'Rucking, Light Pack',
                        'Rucking, Medium Pack',
                        'Rugby',
                        'Rumble Boxing',
                        'Running',
                        'Running (jogging), 10.7 kph (5.6 min per km)',
                        'Running (jogging), 11.3 kph (5.3 min per km)',
                        'Running (jogging), 12 kph (5 min per km)',
                        'Running (jogging), 12.9 kph (4.6 min per km)',
                        'Running (jogging), 13.8 kph (4.3 min per km)',
                        'Running (jogging), 14.5 kph (4.1 min per km)',
                        'Running (jogging), 16 kph (3.7 min per km)',
                        'Running (jogging), 17.5 kph (3.4 min per km)',
                        'Running (jogging), 8 kph (7.5 min per km)',
                        'Running (jogging), 8.4 kph (7.2 min per km)',
                        'Running (jogging), 9.6 kph (6.2 min per km)',
                        'Running (jogging), in place',
                        'Running (jogging), indoor',
                        'Running (jogging), training, pushing wheelchair',
                        'Running (jogging), up stairs',
                        'Running, adventure race',
                        'Running, brick',
                        'Running, cross country',
                        'Running, elliptical',
                        'Running, general',
                        'Running, group',
                        'Running, hills',
                        'Running, interval training',
                        'Running, race/event',
                        'Running, sprints',
                        'Running, trail',
                        'Running, treadmill',
                        'Running, with dog',
                        'Running, with stroller',
                        'SLT',
                        'Sailing, boat/board, windsurfing, general',
                        'Sailing, in competition',
                        'Shoveling snow',
                        'Shred415',
                        'Shuffleboard, lawn bowling',
                        'Side Bends, Barbell',
                        'Side Leg Raises',
                        'Single Stroller, Bike',
                        'Skateboarding',
                        'Skating, ice, 4.1 min per km or less',
                        'Skating, ice, general',
                        'Skating, ice, rapidly, >4.1 min per km',
                        'Skating, ice, speed, competitive',
                        'Skating, roller (rollerblading, roller blading)',
                        'Ski jumping (climb up carrying skis)',
                        'Ski machine, general',
                        'Skiing, cross-country, 15 mins per km, slow or light effort',
                        'Skiing, cross-country, 4.5-7.5 mins per km, vigorous effort',
                        'Skiing, cross-country, 7.5-9 mins per km, moderate effort',
                        'Skiing, cross-country, >4.6 min per km, racing',
                        'Skiing, cross-country, uphill, maximum effort',
                        'Skiing, downhill, light effort',
                        'Skiing, downhill, moderate effort',
                        'Skiing, downhill, vigorous effort, racing',
                        'Skiing, snow, general',
                        'Skiing, water',
                        'Skin diving, scuba diving, general',
                        'Sledding, tobogganing, bobsledding, luge',
                        'Slimnastics, jazzercise',
                        'Snorkeling',
                        'Snow shoeing',
                        'Snow skiing',
                        'Snowboarding',
                        'Snowmobiling',
                        'Soccer',
                        'Soccer, casual, general',
                        'Soccer, competitive',
                        'Softball',
                        'Softball or baseball, fast or slow pitch',
                        'Softball, officiating',
                        'SoulCycle',
                        'Spinning',
                        'Spinning®',
                        'Sports',
                        'Squash',
                        'Squat',
                        'Stair-treadmill ergometer, general',
                        'Stationary bike, general (bicycling, cycling, biking)',
                        'Stationary bike, light effort (bicycling, cycling, biking)',
                        'Stationary bike, moderate effort (bicycling, cycling, biking)',
                        'Stationary bike, very light effort (bicycling, cycling, biking)',
                        'Stationary bike, very vigorous effort (bicycling, cycling, biking)',
                        'Stationary bike, vigorous effort (bicycling, cycling, biking)',
                        'Stretching, hatha yoga',
                        'Stretching, sculpting',
                        'Surfing',
                        'Surfing, body or board',
                        'Swimming',
                        'Swimming laps, freestyle, fast, vigorous effort',
                        'Swimming laps, freestyle, light/moderate effort',
                        'Swimming, backstroke, general',
                        'Swimming, breaststroke, general',
                        'Swimming, butterfly, general',
                        'Swimming, general',
                        'Swimming, laps',
                        'Swimming, leisurely, general',
                        'Swimming, meet/race',
                        'Swimming, open water',
                        'Swimming, sidestroke, general',
                        'Swimming, synchronized',
                        'Swimming, treading water, fast/vigorous',
                        'Swimming, treading water, moderate effort',
                        'Table tennis, ping pong',
                        'Tae Bo',
                        'Tae Kwon Do',
                        'Tai chi',
                        'Teaching aerobics class',
                        'Tennis',
                        'Tennis, doubles',
                        'Tennis, general',
                        'Tennis, singles',
                        'Title Boxing',
                        'Tonal',
                        'Traditional cross country skiing',
                        'Tricycle',
                        'Unicycling',
                        'Volleyball',
                        'Volleyball, beach',
                        'Volleyball, competitive, in gymnasium',
                        'Volleyball, noncompetitive; 6-9 member team',
                        'Wake Surfing',
                        'Walking',
                        'Walking, 10.5 mins per km, brisk pace',
                        'Walking, 10.5 mins per km, uphill',
                        'Walking, 12.5 mins per km, mod. pace',
                        'Walking, 12.5 mins per km, mod. pace, walking dog',
                        'Walking, 15 mins per km, downhill',
                        'Walking, 15 mins per km, leisurely pace',
                        'Walking, 18.5 mins per km, slow pace',
                        'Walking, 7.5 mins per km',
                        'Walking, 8 mins per km, very, very brisk pace',
                        'Walking, 9 mins per km, very brisk pace',
                        'Walking, brisk',
                        'Walking, carrying infant or 7 kg load',
                        'Walking, elliptical',
                        'Walking, general',
                        'Walking, power',
                        'Walking, stairs',
                        'Walking, treadmill',
                        'Walking, upstairs',
                        'Walking, using crutches',
                        'Walking, with dog',
                        'Walking, with stroller',
                        'Wallyball, general',
                        'Water aerobics, water calisthenics',
                        'Water jogging',
                        'Water polo',
                        'Water volleyball',
                        'Weight workout',
                        'Wheelchair Basketball',
                        'Wheelchair Downhill',
                        'Wheelchair Race',
                        'Wheelchair Rugby',
                        'Wheelchair Soccer',
                        'Wheelchair Softball',
                        'Wheelchair Tennis',
                        'Whitewater rafting, kayaking, or canoeing',
                        'Wii Fit Advanced Step',
                        'Wii Fit Free Run',
                        'Wii Fit Free Step',
                        'Wii Fit Island Run',
                        'Wii Fit Rhythm Boxing',
                        'Wii Fit Super Hula Hoop',
                        'Wii Fit exercise (advanced or high intensity)',
                        'Wii Fit exercise (beginner or low intensity)',
                        'Wii baseball',
                        'Wii bowling',
                        'Wii boxing',
                        'Wii golf',
                        'Wii tennis',
                        'Workout',
                        'Workout video',
                        'Wrestling',
                        'Wrist Curl',
                        'Wrist Roller',
                        'Yard Work',
                        'Yoga',
                        'Yoga Six',
                        'Yoga to the People',
                        'Yoga, Aerial',
                        'Yoga, Ashtanga',
                        'Yoga, bikram',
                        'Yoga, hot',
                        'Yoga, power',
                        'Yoga, vinyasa',
                        'YogaWorks',
                        'Zumba',
                        'Zumba® Fitness'
                        ]

    # List of exercises that are strength exercises scraped from myfitnesspal.com
    exercises_strength = [
        'Abdominal Crunches',
        'Abdominal Leg Raise',
        'Abdominal Twist, Seated, Machine',
        'Abs',
        'Activity tracker',
        'Adaptive Motion Trainer',
        'Back Butterfly',
        'Back Extension',
        'Bar Dip, Palms In, Neutral Grip',
        'Barbell Military Press',
        'Barbell Row, Bent-over',
        'Bent Arm Barbell Pullover',
        'Bent Arm Barbell Pullover and Press',
        'Bent-Arm Lateral',
        'Bent-Knee Sit-Up',
        'Bent-Leg Kickbacks',
        'Bent-Over Low-Pulley Side Lateral',
        'Biceps Curl',
        'Body Pump',
        'Body weight squats',
        'Boxing, in ring, general',
        'Boxing, punching bag',
        'Boxing, sparring',
        'Cable Crossover, High Pulley',
        'Calf Raises, Single-Leg',
        'Calisthenics (pushups, sit-ups), vigorous effort',
        'Calisthenics, home, light/moderate effort',
        'Camp Gladiator',
        'Canoeing, rowing, >10 kph, vigorous effort',
        'Canoeing, rowing, crewing, competition',
        'Canoeing, rowing, light effort',
        'Canoeing, rowing, moderate effort',
        'Combat class',
        'Concept2 BikErg',
        'Concept2 SkiErg',
        'Curves',
        'Cycling, stationary, general',
        'Cycling, stationary, 30-50 watts, very light to light effort',
        'Cycling, stationary, 90-100 watts, moderate to vigorous effort',
        'Dips', 'Deadlift, Straight Leg', 'Decline Bench Press', 'Decline Dumbbell Fly',
        'Dumbbell Press, One-Arm, Palm-In',
        'Dumbbell Press, Seated, Palms-In',
        'Dumbbell Row, One-Arm, Bent-Over',
        'Dumbbell Row, Two-Arm, Bent-Over',
        'Elliptical Trainer',
        'Elliptical, Under Desk', 'F45 Training', 'Flat Dumbbell Fly',
        'Flat Dumbbell Press', 'Front Barbell Raise, Standing, Medium-Grip',
        'Front Chin Up, Close-Grip, Palms Back',
        'Front Chin Up, Reverse Close-Grip',
        'Front Raises, Straight Arm',
        'Front Squats, Barbell, Arms Crossed', 'Gym',
        'Gym Workout',
        "Gym, Jacob's ladder",
        'Gym, TRX',
        'Gym, abs/core',
        'Gym, back',
        'Gym, chest',
        'Gym, exercise bike',
        'Gym, kettlebell',
        'Gym, legs',
        'Gym, misc',
        'Gym, other machine',
        'Gym, rowing machine',
        'Gym, stair machine',
        'Gym, total body',
        'Gym, total body',
        'Gym, treadmill',
        'Gym, upper body',
        'Gym, versa climber', 'Hack Squat', 'Hip Abduction, Machine, Seated',
        'Hip Flexor, Machine, Standing', 'Home Workout', 'Hyperextensions',
        'Incline Bench Press',
        'Incline Dumbbell Curl',
        'Incline Dumbbell Fly',
        'Incline Lateral, Dumbbells', 'Kickbacks, Bent, 1-Arm, Dumbbell',
        'Kickbacks, Bent, 2-Arm, Dumbbell', 'Lat Pulldown',
        'Lateral Arm Raise, Machine',
        'Lateral Raise, Dumbbell, Side', 'Leg Curls',
        'Leg Extension',
        'Leg Press',
        'Leg Pull-In, Seated Flat Bench',
        'Leg Raises, Hanging',
        'Les Mills BODYATTACK™',
        'Les Mills BODYBALANCE™/BODYFLOW®',
        'Les Mills BODYCOMBAT™',
        'Les Mills BODYPUMP™',
        'Les Mills BODYSTEP™',
        'Les Mills RPM™',
        'Line dancing',
        'Lower body',
        'Lunge',
        'Machine Fly',
        'Machine Squat', 'Mid Row, Chest Supported, Machine', 'Overhead Press, Barbell', 'Pec Dec Butterfly (Pectoral Fly)',
        'Overhead Press, Machine, Seated', 'Preacher Bench Medium-Grip Barbell Curl',
        'Pull Ups (pull-ups)',
        'Pull-ups, vigorous',
        'Pullover',
        'Pump', 'Push Ups (push-ups)',
        'Push-ups',
        'Push-ups, vigorous',
        'Pushing or pulling stroller with child', 'Reverse Sit-Up',
        'Reverse Trunk Twist', 'Rowing',
        'Rowing, stationary, light effort',
        'Rowing, stationary, moderate effort',
        'Rowing, stationary, very vigorous effort',
        'Rowing, stationary, vigorous effort', 'Seated Biceps Curl',
        'Seated Calf Raise',
        'Seated Row, Floor, Machine',
        'Seated, Low Lat Pull-In, Two-Arm',
        'Shoulder Press',
        'Shoulder Shrug', 'Sit-Ups',
        'Sit-ups',
        'Sit-ups, vigorous', 'Stand Up Paddling',
        'Standing Bar Curl, Machine',
        'Standing Biceps Curl, Dumbell',
        'Standing Calf Raises',
        'Standing Medium-Grip Barbell Curl',
        'Standing One-Arm Curl, Low Pulley',
        'Standing One-Arm Dumbbell Curl', 'Step-ups, vigorous',
        'Straight Arm Dumbbell Pullover',
        'Strength training',
        'Strength training (weight lifting, weight training)', 'Toe Press', 'Triceps Extension',
        'Triceps Pull-down',
        'Triceps Push Down', 'Upright Row', 'V-Bar Chin Up, Neutral Grip, Palms In', 'Vertical Leg Lift, Knees Bent (Dip Bars)',
        'Vertical Leg Lift, Knees Straight (Dip Bars)']

    # List of top 15 breakfast foods from the USDA
    breakfast_foods = {
        "Oatmeal": {"calories": 166, "protein": 4, "carbohydrates": 28, "fat": 3, "fiber": 4, "sodium": 4, "sugar": 1},
        "Scrambled eggs": {"calories": 71, "protein": 6, "carbohydrates": 0, "fat": 5, "fiber": 0, "sodium": 71, "sugar": 0},
        "Pancakes": {"calories": 69, "protein": 2, "carbohydrates": 13, "fat": 1, "fiber": 1, "sodium": 81, "sugar": 4},
        "Sausage": {"calories": 160, "protein": 8, "carbohydrates": 0, "fat": 14, "fiber": 0, "sodium": 536, "sugar": 0},
        "Bacon": {"calories": 174, "protein": 12, "carbohydrates": 1, "fat": 14, "fiber": 0, "sodium": 462, "sugar": 0},
        "Bagel": {"calories": 246, "protein": 10, "carbohydrates": 52, "fat": 1, "fiber": 3, "sodium": 439, "sugar": 5},
        "Cereal": {"calories": 109, "protein": 2, "carbohydrates": 22, "fat": 1, "fiber": 3, "sodium": 182, "sugar": 10},
        "Yogurt": {"calories": 149, "protein": 8, "carbohydrates": 27, "fat": 2, "fiber": 0, "sodium": 81, "sugar": 25},
        "Toast": {"calories": 69, "protein": 3, "carbohydrates": 12, "fat": 1, "fiber": 3, "sodium": 124, "sugar": 2},
        "Waffles": {"calories": 76, "protein": 2, "carbohydrates": 13, "fat": 2, "fiber": 1, "sodium": 136, "sugar": 6},
        "Muffin": {"calories": 322, "protein": 7, "carbohydrates": 45, "fat": 14, "fiber": 2, "sodium": 233, "sugar": 22},
        "Croissant": {"calories": 280, "protein": 8, "carbohydrates": 34, "fat": 14, "fiber": 2, "sodium": 256, "sugar": 9},
        "Donut": {"calories": 199, "protein": 4, "carbohydrates": 27, "fat": 10, "fiber": 1, "sodium": 179, "sugar": 16},
        "French toast": {"calories": 148, "protein": 6, "carbohydrates": 17, "fat": 5, "fiber": 1, "sodium": 196, "sugar": 8},
        "Smoothie": {"calories": 84, "protein": 2, "carbohydrates": 16, "fat": 0, "fiber": 1, "sodium": 15, "sugar": 14}}

    # List of top 15 lunch foods from the USDA
    lunch_foods = {
        "Sandwich": {"calories": 267, "protein": 14, "carbohydrates": 32, "fat": 9, "fiber": 3, "sodium": 668, "sugar": 6},
        "Salad": {"calories": 47, "protein": 2, "carbohydrates": 7, "fat": 0, "fiber": 2, "sodium": 73, "sugar": 4},
        "Soup": {"calories": 75, "protein": 3, "carbohydrates": 12, "fat": 2, "fiber": 1, "sodium": 579, "sugar": 5},
        "Pizza": {"calories": 285, "protein": 11, "carbohydrates": 35, "fat": 10, "fiber": 2, "sodium": 621, "sugar": 5},
        "Burger": {"calories": 248, "protein": 17, "carbohydrates": 28, "fat": 8, "fiber": 3, "sodium": 526, "sugar": 8},
        "Taco": {"calories": 153, "protein": 8, "carbohydrates": 17, "fat": 8, "fiber": 3, "sodium": 526, "sugar": 2},
        "Pasta": {"calories": 221, "protein": 8, "carbohydrates": 41, "fat": 2, "fiber": 3, "sodium": 135, "sugar": 3},
        "Fried rice": {"calories": 289, "protein": 8, "carbohydrates": 41, "fat": 9, "fiber": 2, "sodium": 879, "sugar": 3},
        "Noodles": {"calories": 200, "protein": 8, "carbohydrates": 35, "fat": 4, "fiber": 2, "sodium": 579, "sugar": 3},
        "Sushi": {"calories": 239, "protein": 11, "carbohydrates": 38, "fat": 4, "fiber": 3, "sodium": 579, "sugar": 8},
        "Grilled chicken": {"calories": 180, "protein": 36, "carbohydrates": 0, "fat": 3, "fiber": 0, "sodium": 77, "sugar": 0},
        "Tofu stir-fry": {"calories": 189, "protein": 13, "carbohydrates": 14, "fat": 11, "fiber": 2, "sodium": 579, "sugar": 4},
        "Beans and rice": {"calories": 239, "protein": 13, "carbohydrates": 38, "fat": 4, "fiber": 8, "sodium": 579, "sugar": 5},
        "Grilled cheese": {"calories": 333, "protein": 14, "carbohydrates": 30, "fat": 20, "fiber": 1, "sodium": 774, "sugar": 5},
        "Deli meat wrap": {"calories": 246, "protein": 15, "carbohydrates": 30, "fat": 8, "fiber": 3, "sodium": 997, "sugar": 7}}

    # List of top 15 dinner foods from the USDA
    dinner_foods = {
        "Roast beef": {"calories": 273, "protein": 37, "carbohydrates": 0, "fat": 14, "fiber": 0, "sodium": 77, "sugar": 0},
        "Steak": {"calories": 287, "protein": 37, "carbohydrates": 0, "fat": 16, "fiber": 0, "sodium": 77, "sugar": 0},
        "Lamb chops": {"calories": 344, "protein": 37, "carbohydrates": 0, "fat": 22, "fiber": 0, "sodium": 77, "sugar": 0},
        "Pork chops": {"calories": 290, "protein": 37, "carbohydrates": 0, "fat": 16, "fiber": 0, "sodium": 77, "sugar": 0},
        "Grilled chicken": {"calories": 180, "protein": 36, "carbohydrates": 0, "fat": 3, "fiber": 0, "sodium": 77, "sugar": 0},
        "Baked chicken": {"calories": 187, "protein": 31, "carbohydrates": 0, "fat": 9, "fiber": 0, "sodium": 77, "sugar": 0},
        "Fried chicken": {"calories": 365, "protein": 31, "carbohydrates": 19, "fat": 21, "fiber": 0, "sodium": 579, "sugar": 1},
        "Fish and chips": {"calories": 607, "protein": 31, "carbohydrates": 59, "fat": 28, "fiber": 3, "sodium": 997, "sugar": 3},
        "Grilled salmon": {"calories": 208, "protein": 37, "carbohydrates": 0, "fat": 9, "fiber": 0, "sodium": 77, "sugar": 0},
        "Baked salmon": {"calories": 207, "protein": 37, "carbohydrates": 0, "fat": 9, "fiber": 0, "sodium": 77, "sugar": 0},
        "Fried rice": {"calories": 310, "protein": 8, "carbohydrates": 43, "fat": 10, "fiber": 2, "sodium": 997, "sugar": 2},
        "Spaghetti and meatballs": {"calories": 358, "protein": 22, "carbohydrates": 41, "fat": 13, "fiber": 3, "sodium": 997, "sugar": 6},
        "Pizza": {"calories": 285, "protein": 11, "carbohydrates": 33, "fat": 12, "fiber": 2, "sodium": 622, "sugar": 3},
        "Hamburger": {"calories": 354, "protein": 28, "carbohydrates": 34, "fat": 14, "fiber": 3, "sodium": 682, "sugar": 6},
        "Taco": {"calories": 275, "protein": 13.5, "carbohydrates": 27.5, "fat": 12.5, "fiber": 3, "sodium": 350, "sugar": 3}}

    # List of top 15 snack foods from the USDA
    snack_foods = {
        "potato chips": {
            "serving size": "1 oz",
            "calories": 160,
            "carbohydrates": 20,
            "fat": 10,
            "protein": 2,
            "sodium": 170,
            "sugar": 1
        },
        "pretzels": {
            "serving size": "1 oz",
            "calories": 110,
            "carbohydrates": 22,
            "fat": 0.5,
            "protein": 3,
            "sodium": 390,
            "sugar": 0
        },
        "cheese crackers": {
            "serving size": "1 oz",
            "calories": 140,
            "carbohydrates": 20,
            "fat": 7,
            "protein": 3,
            "sodium": 200,
            "sugar": 2
        },
        "chex mix": {
            "serving size": "1 oz",
            "calories": 140,
            "carbohydrates": 20,
            "fat": 7,
            "protein": 3,
            "sodium": 260,
            "sugar": 1
        },
        "peanut butter sandwich crackers": {
            "serving size": "2 crackers",
            "calories": 140,
            "carbohydrates": 20,
            "fat": 8,
            "protein": 3,
            "sodium": 120,
            "sugar": 5
        },
        "goldfish crackers": {
            "serving size": "1 oz",
            "calories": 140,
            "carbohydrates": 20,
            "fat": 6,
            "protein": 3,
            "sodium": 240,
            "sugar": 0
        },
        "cheez-its": {
            "serving size": "1 oz",
            "calories": 150,
            "carbohydrates": 20,
            "fat": 8,
            "protein": 3,
            "sodium": 250,
            "sugar": 0
        },
        "animal crackers": {
            "serving size": "1 oz",
            "calories": 120,
            "carbohydrates": 20,
            "fat": 3,
            "protein": 2,
            "sodium": 90,
            "sugar": 8
        },
        "graham crackers": {
            "serving size": "2 crackers",
            "calories": 70,
            "carbohydrates": 20,
            "fat": 2,
            "protein": 2,
            "sodium": 120,
            "sugar": 6
        },
        "fruit snacks": {
            "serving size": "1 package",
            "calories": 80,
            "carbohydrates": 20,
            "fat": 0,
            "protein": 0,
            "sodium": 15,
            "sugar": 11
        },
        "raisins": {
            "serving size": "1/4 cup",
            "calories": 130,
            "carbohydrates": 20,
            "fat": 0.5,
            "protein": 1,
            "sodium": 0,
            "sugar": 28
        },
        "peanuts": {
            "serving size": "1 oz",
            "calories": 170,
            "carbohydrates": 20,
            "fat": 14,
            "protein": 7,
            "sodium": 140,
            "sugar": 2
        },
        "sunflower seeds": {
            "serving size": "1 oz",
            "calories": 160,
            "carbohydrates": 20,
            "fat": 14,
            "protein": 6,
            "sodium": 240,
            "sugar": 1
        },
        "trail mix": {
            "serving size": "1 oz",
            "calories": 150,
            "carbohydrates": 20,
            "fat": 8,
            "protein": 5,
            "sodium": 70,
            "sugar": 6
        }, "popcorn": {
            "serving size": "3 cups",
            "calories": 150,
            "carbohydrates": 20,
            "fat": 8,
            "protein": 4,
            "sodium": 300,
            "sugar": 0
        }
    }

    for day in dates:

        # Creating a randomly generated summary of the day's food goal
        goals.append({'calories': syn_calories(day), 'carbohydrates': syn_carbs(day), 'fat': syn_fat(day), 'protein': syn_protein(day), 'sodium': syn_sodium(day), 'sugar': syn_sugar(day),
                      'date': pd.Timestamp(day)})

        # Creating a randomly generated summary of the day's food intake
        daily_summary.append({'calories': syn_calories(day), 'carbohydrates': syn_carbs(day), 'fat': syn_fat(day), 'protein': syn_protein(day), 'sodium': syn_sodium(day), 'sugar': syn_sugar(day),
                              'date': pd.Timestamp(day)})

        # Creating a randomly generated list of cardio exercises for the day
        cardio = [{'day': pd.Timestamp(day)}]

        # We will randomly select between 1 and 3 cardio exercises
        cardio_count = np.random.randint(1, 3)

        # We will randomly select between 1 and 3 cardio exercises
        random_exercises = np.random.choice(
            exercises_cardio, cardio_count, replace=False)

        # Adding each exercise to the list of cardio exercises for that day
        for exercise in random_exercises:
            minutes = np.random.randint(10, 60)
            syn_exercise = {
                'name': exercise,
                'nutrition_information': {
                    'minutes': minutes,
                    'calories burned': minutes * max(2, np.random.uniform(3, 5)),
                }
            }

            # Adding the exercise to the list of cardio exercises for that day
            cardio.append(syn_exercise)

        # Adding the list of cardio exercises for that day to the list of all cardio exercises
        cardio_exercises.append(cardio)

        # Creating a randomly generated list of strength exercises for the day
        strength = []

        # Adding the date to the list of strength exercises for that day
        strength.append({
            'date': pd.Timestamp(day)
        })

        # We will randomly select between 1 and 10 strength exercises
        exercise_count = np.random.randint(1, 10)

        # We will randomly select between 1 and 10 strength exercises
        random_exercises = np.random.choice(
            exercises_strength, exercise_count, replace=False)

        # Adding each exercise to the list of strength exercises for that day
        for exercise in random_exercises:
            syn_exercise = {
                'name': exercise,
                'nutrition_information': {
                    'sets': float(np.random.randint(2, 5)),
                    'reps/set': float(np.round(np.random.uniform(10, 2))),
                    'weight/set': float(np.random.randint(5, 100))
                }
            }
            strength.append(syn_exercise)
        strength_exercises.append(strength)

        # Creating a randomly generated list of breakfast foods for the day
        breakfast_item_name = np.random.choice(list(breakfast_foods.keys()))
        breakfast_item = breakfast_foods[breakfast_item_name]

        # Adding the breakfast food to the list of breakfast foods for that day
        breakfast.append([{'day': pd.Timestamp(day)},
                          {
            'name': breakfast_item_name,
            'nutrition_information': {
                'calories': float(breakfast_item['calories']),
                'carbohydrates': float(breakfast_item['carbohydrates']),
                'fat': float(breakfast_item['fat']),
                'protein': float(breakfast_item['protein']),
                'sodium': float(breakfast_item['sodium']),
                'sugar': float(breakfast_item['sugar'])
            },
            "totals": {
                'calories': float(breakfast_item['calories']),
                'carbohydrates': float(breakfast_item['carbohydrates']),
                'fat': float(breakfast_item['fat']),
                'protein': float(breakfast_item['protein']),
                'sodium': float(breakfast_item['sodium']),
                'sugar': float(breakfast_item['sugar'])
            },
        }])

        # Creating a randomly generated list of lunch foods for the day
        lunch_item_name = np.random.choice(list(lunch_foods.keys()))
        lunch_item = lunch_foods[lunch_item_name]

        # Adding the lunch food to the list of lunch foods for that day
        lunch.append([{'day': pd.Timestamp(day)},
                      {
            'name': lunch_item_name,
            'nutrition_information': {
                'calories': float(lunch_item['calories']),
                'carbohydrates': float(lunch_item['carbohydrates']),
                'fat': float(lunch_item['fat']),
                'protein': float(lunch_item['protein']),
                'sodium': float(lunch_item['sodium']),
                'sugar': float(lunch_item['sugar'])
            },
            "totals": {
                'calories': float(lunch_item['calories']),
                'carbohydrates': float(lunch_item['carbohydrates']),
                'fat': float(lunch_item['fat']),
                'protein': float(lunch_item['protein']),
                'sodium': float(lunch_item['sodium']),
                'sugar': float(lunch_item['sugar'])
            },
        }])

        # Creating a randomly generated list of dinner foods for the day
        dinner_item_name = np.random.choice(list(dinner_foods.keys()))
        dinner_item = dinner_foods[dinner_item_name]

        # Adding the dinner food to the list of dinner foods for that day
        dinner.append([{'day': pd.Timestamp(day)},
                       {
            'name': dinner_item_name,
            'nutrition_information': {
                'calories': float(dinner_item['calories']),
                'carbohydrates': float(dinner_item['carbohydrates']),
                'fat': float(dinner_item['fat']),
                'protein': float(dinner_item['protein']),
                'sodium': float(dinner_item['sodium']),
                'sugar': float(dinner_item['sugar'])
            },
            'totals': {
                'calories': float(dinner_item['calories']),
                'carbohydrates': float(dinner_item['carbohydrates']),
                'fat': float(dinner_item['fat']),
                'protein': float(dinner_item['protein']),
                'sodium': float(dinner_item['sodium']),
                'sugar': float(dinner_item['sugar'])
            },
        }])

        # Creating a randomly generated list of snack foods for the day
        snack_item_name = np.random.choice(list(snack_foods.keys()))
        snack_item = snack_foods[snack_item_name]

        # Adding the snack food to the list of snack foods for that day
        snacks.append([{'day': pd.Timestamp(day)},
                       {
            'name': snack_item_name,
            'nutrition_information': {
                'calories': float(snack_item['calories']),
                'carbohydrates': float(snack_item['carbohydrates']),
                'fat': float(snack_item['fat']),
                'protein': float(snack_item['protein']),
                'sodium': float(snack_item['sodium']),
                'sugar': float(snack_item['sugar'])
            },
            'totals': {
                'calories': float(snack_item['calories']),
                'carbohydrates': float(snack_item['carbohydrates']),
                'fat': float(snack_item['fat']),
                'protein': float(snack_item['protein']),
                'sodium': float(snack_item['sodium']),
                'sugar': float(snack_item['sugar'])
            }
        }])

    return goals, daily_summary, cardio_exercises, strength_exercises, breakfast, lunch, dinner, snacks
