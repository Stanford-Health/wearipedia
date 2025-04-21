"""Device registration module."""

from wearipedia import register_device

# Import all device classes
from .apple.healthkit import HealthKit
from .biostrap.evo import Evo
from .coros.pace_2 import Pace2
from .cronometer.cronometer import Cronometer
from .dexcom.pro_cgm import ProCGM
from .dreem.headband_2 import Headband2
from .fitbit.charge_4 import Charge4
from .fitbit.charge_6 import Charge6
from .fitbit.google_pixel_watch import GooglePixelWatch
from .fitbit.sense import Sense
from .garmin.fenix_7s import Fenix7S
from .google.googlefit import GoogleFit
from .myfitnesspal.myfitnesspal import MyFitnessPal
from .nutrisense.cgm import NutrisenseCGM
from .oura.ring3 import Ring3
from .polar.h10 import H10
from .polar.vantage import Vantage
from .polar.verity_sense import VeritySense
from .qualtrics.qualtrics import Qualtrics
from .strava.strava import Strava
from .whoop.whoop_4 import Whoop4
from .withings.bodyplus import BodyPlus
from .withings.scanwatch import ScanWatch
from .withings.sleepmat import SleepMat

ALL_DEVICES = [
    HealthKit,
    Evo,
    Pace2,
    Cronometer,
    ProCGM,
    Headband2,
    Charge4,
    Charge6,
    Sense,
    GooglePixelWatch,
    Fenix7S,
    GoogleFit,
    MyFitnessPal,
    NutrisenseCGM,
    Ring3,
    H10,
    Vantage,
    VeritySense,
    Qualtrics,
    Whoop4,
    ScanWatch,
    BodyPlus,
    SleepMat,
]
# Register all devices
for device in ALL_DEVICES:
    register_device(device.name, device)
