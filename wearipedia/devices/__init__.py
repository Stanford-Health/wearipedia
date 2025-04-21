"""Device registration module."""

# Import all device classes
from .apple.healthkit import HealthKit
from .biostrap.evo import EVO
from .coros.coros_pace_2 import CorosPace2
from .cronometer.cronometer import Cronometer
from .dexcom.pro_cgm import DexcomProCGM
from .dreem.headband_2 import DreemHeadband2
from .fitbit.fitbit_charge_4 import FitbitCharge4
from .fitbit.fitbit_charge_6 import FitbitCharge6
from .fitbit.fitbit_sense import FitbitSense
from .fitbit.google_pixel_watch import GooglePixelWatch
from .garmin.fenix_7s import Fenix7S
from .google.googlefit import GoogleFit
from .myfitnesspal.myfitnesspal import MyFitnessPal
from .nutrisense.cgm import NutrisenseCGM
from .oura.oura_ring3 import OuraRing3
from .polar.h10 import H10
from .polar.vantage import PolarVantage
from .polar.verity_sense import VeritySense
from .qualtrics.qualtrics import Qualtrics
from .registry import register_device
from .strava.strava import Strava
from .whoop.whoop_4 import Whoop4
from .withings.bodyplus import BodyPlus
from .withings.scanwatch import ScanWatch
from .withings.sleepmat import SleepMat

ALL_DEVICES = [
    HealthKit,
    EVO,
    CorosPace2,
    Cronometer,
    DexcomProCGM,
    DreemHeadband2,
    FitbitCharge4,
    FitbitCharge6,
    FitbitSense,
    GooglePixelWatch,
    Fenix7S,
    GoogleFit,
    MyFitnessPal,
    NutrisenseCGM,
    OuraRing3,
    H10,
    PolarVantage,
    VeritySense,
    Qualtrics,
    Whoop4,
    ScanWatch,
    BodyPlus,
    SleepMat,
    Strava,
]

# Register all devices
for device in ALL_DEVICES:
    register_device(device)
