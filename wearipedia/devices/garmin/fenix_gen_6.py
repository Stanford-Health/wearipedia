import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm


def get_device_settings_data(num_devices):
    """Generate synthetic device settings data for the specified number of devices.

    This function generates synthetic device settings data for the specified number of devices. Each device"s settings
    include various configuration options such as time format, units of measurement, activity tracking settings, alarm modes,
    language preferences, and more. The generated data is structured as a list of dictionaries.

    :param num_devices: The number of devices for which to generate settings data.
    :type num_devices: int

    :return: A list of dictionaries containing synthetic device settings data for the specified number of devices.
    :rtype: List[Dict]
    """
    device_settings = []

    # Generate random data for two devices
    for _ in range(num_devices):
        device_data = {
            "deviceId": random.randint(1000000000, 9999999999),
            "timeFormat": random.choice(["time_twelve_hr", "time_twenty_four_hr"]),
            "dateFormat": "date_month_day",
            "measurementUnits": random.choice(["statute_us", "metric"]),
            "allUnits": "statute_us" if random.choice([True, False]) else "metric",
            "visibleScreens": None,
            "enabledScreens": {},
            "screenLists": None,
            "isVivohubEnabled": None,
            "alarms": [],
            "supportedAlarmModes": [
                "ON",
                "OFF",
                "DAILY",
                "WEEKDAYS",
                "WEEKENDS",
                "ONCE",
            ],
            "multipleAlarmEnabled": True,
            "maxAlarm": random.randint(0, 10),
            "activityTracking": {
                "activityTrackingEnabled": True,
                "moveAlertEnabled": True,
                "moveBarEnabled": None,
                "pulseOxSleepTrackingEnabled": random.choice([True, False]),
                "spo2Threshold": None,
                "lowSpo2AlertEnabled": None,
                "highHrAlertEnabled": random.choice([True, False]),
                "highHrAlertThreshold": random.randint(80, 130),
                "pulseOxAcclimationEnabled": random.choice([True, False]),
                "lowHrAlertEnabled": random.choice([True, False]),
                "lowHrAlertThreshold": random.randint(30, 70),
                "bloodEfficiencySleepTrackingEnabled": None,
                "bloodEfficiencyAcclimationEnabled": None,
            },
            "keyTonesEnabled": None,
            "keyVibrationEnabled": None,
            "alertTonesEnabled": None,
            "userNoticeTonesEnabled": None,
            "glonassEnabled": None,
            "turnPromptEnabled": None,
            "segmentPromptEnabled": None,
            "supportedLanguages": [{"id": i, "name": "lang_{i}"} for i in range(40)],
            "language": random.randint(0, 39),
            "supportedAudioPromptDialects": [
                "AR_AE",
                "CS_CZ",
                "DA_DK",
                "DE_DE",
                "EL_GR",
                "EN_AU",
                "EN_GB",
                "EN_US",
                "ES_ES",
                "ES_MX",
                "FI_FI",
                "FR_CA",
                "FR_FR",
                "HE_IL",
                "HR_HR",
                "HU_HU",
                "ID_ID",
                "IT_IT",
                "JA_JP",
                "KO_KR",
                "MS_MY",
                "NL_NL",
                "NO_NO",
                "PL_PL",
                "PT_BR",
                "RO_RO",
                "RU_RU",
                "SK_SK",
                "SV_SE",
                "TH_TH",
                "TR_TR",
                "VI_VI",
                "ZH_CN",
                "ZH_TW",
            ],
            "defaultPage": None,
            "displayOrientation": None,
            "mountingSide": "RIGHT",
            "backlightMode": "AUTO_BRIGHTNESS",
            "backlightSetting": "ON",
            "customWheelSize": None,
            "gestureMode": None,
            "goalAnimation": "NOT_IN_ACTIVITY",
            "autoSyncStepsBeforeSync": 2000,
            "autoSyncMinutesBeforeSync": 240,
            "bandOrientation": None,
            "screenOrientation": None,
            "duringActivity": {
                "screens": None,
                "defaultScreen": None,
                "smartNotificationsStatus": "SHOW_ALL",
                "smartNotificationsSound": None,
                "phoneNotificationPrivacyMode": None,
            },
            "phoneVibrationEnabled": None,
            "connectIQ": {"autoUpdate": True},
            "opticalHeartRateEnabled": True,
            "autoUploadEnabled": True,
            "bleConnectionAlertEnabled": None,
            "phoneNotificationMode": None,
            "lactateThresholdAutoDetectEnabled": None,
            "wiFiAutoUploadEnabled": None,
            "blueToothEnabled": None,
            "smartNotificationsStatus": "SHOW_ALL",
            "smartNotificationsSound": None,
            "dndEnabled": random.choice([True, False]),
            "distanceUnit": None,
            "paceSpeedUnit": None,
            "elevationUnit": None,
            "weightUnit": None,
            "heightUnit": None,
            "temperatureUnit": None,
            "runningFormat": None,
            "cyclingFormat": None,
            "hikingFormat": None,
            "strengthFormat": None,
            "cardioFormat": None,
            "xcSkiFormat": None,
            "otherFormat": None,
            "startOfWeek": "SUNDAY",
            "dataRecording": "SMART",
            "soundVibrationEnabled": None,
            "soundInAppOnlyEnabled": None,
            "backlightKeysAndAlertsEnabled": None,
            "backlightWristTurnEnabled": None,
            "backlightTimeout": "MEDIUM",
            "supportedBacklightTimeouts": None,
            "screenTimeout": None,
            "colorTheme": None,
            "autoActivityDetect": {
                "autoActivityDetectEnabled": True,
                "autoActivityStartEnabled": False,
                "runningEnabled": True,
                "cyclingEnabled": True,
                "swimmingEnabled": True,
                "walkingEnabled": True,
                "ellipticalEnabled": True,
                "drivingEnabled": True,
            },
            "sleep": None,
            "screenMode": None,
            "watchFace": None,
            "watchFaceItemList": None,
            "multipleSupportedWatchFace": {},
            "supportedScreenModes": None,
            "supportedWatchFaces": None,
            "supportedWatchFaceColors": None,
            "autoSyncFrequency": None,
            "supportedBacklightSettings": [
                "AUTO_INTERACTION_ONLY",
                "AUTO_INTERACTION_GESTURE",
                "OFF",
            ],
            "supportedColorThemes": None,
            "disableLastEnabledScreen": None,
            "nickname": None,
            "avatar": None,
            "controlsMenuList": [
                {"id": "POWER_OFF", "index": 0, "required": True},
                {"id": "PAYMENTS", "index": 1, "required": None},
                {"id": "MUSIC_CONTROLS", "index": 2, "required": None},
                {"id": "FIND_MY_PHONE", "index": 3, "required": None},
                {"id": "SAVE_LOCATION", "index": 4, "required": None},
                {"id": "DO_NOT_DISTURB", "index": 5, "required": None},
                {"id": "BLUETOOTH", "index": 6, "required": None},
                {"id": "STOPWATCH", "index": 7, "required": None},
                {"id": "BRIGHTNESS", "index": 8, "required": None},
                {"id": "LOCK_DEVICE", "index": 9, "required": None},
                {"id": "SYNC", "index": None, "required": None},
                {"id": "SET_TIME", "index": None, "required": None},
                {"id": "ALARMS", "index": None, "required": None},
                {"id": "TIMER", "index": None, "required": None},
                {"id": "FLASHLIGHT", "index": None, "required": None},
            ],
            "customUserText": None,
            "metricsFileTrueupEnabled": True,
            "relaxRemindersEnabled": True,
            "smartNotificationTimeout": "MEDIUM",
            "intensityMinutesCalcMethod": "AUTO",
            "moderateIntensityMinutesHrZone": 3,
            "vigorousIntensityMinutesHrZone": 4,
            "keepUserNamePrivate": None,
            "audioPromptLapEnabled": False,
            "audioPromptSpeedPaceEnabled": False,
            "audioPromptSpeedPaceType": "AVERAGE",
            "audioPromptSpeedPaceFrequency": "INVALID",
            "audioPromptSpeedPaceDuration": 180,
            "audioPromptHeartRateEnabled": False,
            "audioPromptHeartRateType": "HEART_RATE",
            "audioPromptHeartRateFrequency": "INVALID",
            "audioPromptHeartRateDuration": 180,
            "audioPromptDialectType": None,
            "audioPromptActivityAlertsEnabled": False,
            "audioPromptPowerEnabled": False,
            "audioPromptPowerType": "AVERAGE",
            "audioPromptPowerFrequency": "INVALID",
            "audioPromptPowerDuration": 180,
            "weightOnlyModeEnabled": None,
            "phoneNotificationPrivacyMode": "OFF",
            "diveAlerts": None,
            "liveEventSharingEnabled": None,
            "liveTrackEnabled": None,
            "liveEventSharingEndTimestamp": None,
            "liveEventSharingMsgContents": None,
            "liveEventSharingTargetDistance": None,
            "liveEventSharingMsgTriggers": None,
            "liveEventSharingTriggerDistance": None,
            "liveEventSharingTriggerTime": None,
            "dbDrivenDefaults": None,
            "schoolMode": None,
            "customMeasurementDate": None,
            "customBodyFatPercent": None,
            "customMuscleMass": None,
            "customDeviceWeight": None,
            "customDeviceBodyFatPercent": None,
            "customDeviceMuscleMass": None,
            "vivohubEnabled": None,
        }

        device_settings.append(device_data)

    return device_settings


def get_weigh_ins_data(start_date, num_days):
    """Generate synthetic weigh-ins data for a specified number of days.

    This function generates synthetic weigh-ins data for a specified number of days. It includes daily weight summaries,
    total average values, and information about the previous and next date's weight. The generated data structure is a
    dictionary with placeholders for various attributes. You can customize this function to provide specific values for
    weigh-ins data.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which weigh-ins data should be generated.
    :type num_days: int
    :return: A dictionary containing synthetic weigh-ins data with placeholder values.
    :rtype: dict
    """
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    from_timestamp = int(start_date_obj.timestamp() * 1000)
    end_date = start_date_obj + timedelta(days=num_days)
    end_timestamp = int(end_date.timestamp() * 1000)

    weigh_ins_data = {
        "dailyWeightSummaries": [],
        "totalAverage": {
            "from": from_timestamp,
            "until": end_timestamp,
            "weight": None,
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
        },
        "previousDateWeight": {
            "samplePk": 1658540493286,
            "date": from_timestamp,
            "calendarDate": start_date,
            "weight": random.randint(20000, 100000),
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
            "sourceType": "CHANGE_LOG",
            "timestampGMT": None,
            "weightDelta": None,
        },
        "nextDateWeight": {
            "samplePk": None,
            "date": None,
            "calendarDate": None,
            "weight": None,
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
            "sourceType": None,
            "timestampGMT": None,
            "weightDelta": None,
        },
    }

    return weigh_ins_data


def get_weigh_ins_daily_data(start_date, num_days):
    """Generate synthetic daily weigh-ins data for a specified number of days.

    This function generates synthetic daily weigh-ins data for a specified number of days. Each day includes a start date,
    end date, and a list of date-weight pairs. The generated data structure is a list of dictionaries containing
    weigh-ins information for each day.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which daily weigh-ins data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic daily weigh-ins data for the specified number of days.
    :rtype: List[Dict]
    """
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    weigh_ins_daily_data = []

    for i in range(num_days):
        current_date = start_date_obj + timedelta(days=i)
        current_date_str = current_date.strftime("%Y-%m-%d")
        timestamp = int(current_date.timestamp() * 1000)
        weight = random.randint(50000, 100000)

        weigh_ins_daily_entry = {
            "startDate": current_date_str,
            "endDate": current_date_str,
            "dateWeightList": [
                {
                    "samplePk": random.randint(1000000, 9999999),
                    "date": timestamp,
                    "calendarDate": current_date_str,
                    "weight": weight,
                    "bmi": None,
                    "bodyFat": None,
                    "bodyWater": None,
                    "boneMass": None,
                    "muscleMass": None,
                    "physiqueRating": None,
                    "visceralFat": None,
                    "metabolicAge": None,
                    "sourceType": "CHANGE_LOG",
                    "timestampGMT": timestamp,
                    "weightDelta": None,
                },
            ],
            "totalAverage": {
                "from": timestamp,
                "until": timestamp + 86400000,
                "weight": weight,
                "bmi": None,
                "bodyFat": None,
                "bodyWater": None,
                "boneMass": None,
                "muscleMass": None,
                "physiqueRating": None,
                "visceralFat": None,
                "metabolicAge": None,
            },
        }
        weigh_ins_daily_data.append(weigh_ins_daily_entry)

    return weigh_ins_daily_data


def get_hill_score_data(start_date, end_date):
    """Generate synthetic hill score data for a specified date range.

    This function generates synthetic hill score data for a specified start and end date. The generated data structure
    includes user profile information, the date range, period average score, maximum score, and a list of hill score DTOs.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param end_date: The end date in the format "YYYY-MM-DD".
    :type end_date: str
    :return: A dictionary containing synthetic hill score data for the specified date range.
    :rtype: Dict
    """

    hill_score_data = {
        "userProfilePK": random.randint(10000000, 99999999),
        "startDate": start_date,
        "endDate": end_date,
        "periodAvgScore": {},
        "maxScore": None,
        "hillScoreDTOList": [],
    }

    return hill_score_data


def get_available_badges_data(start_date, num_days):
    available_badges_data = []

    for i in range(100):
        start_date = datetime.now() + timedelta(days=random.randint(0, 30))
        end_date = start_date + timedelta(days=random.randint(1, 30))

        badge_id = random.randint(1000, 2000)
        badge_uuid = "NA".upper()
        challenge_name = f"Challenge {badge_id}"

        available_badges_entry = {
            "uuid": badge_uuid,
            "badgeChallengeName": challenge_name,
            "challengeCategoryId": random.randint(1, 10),
            "badgeChallengeStatusId": random.randint(1, 3),
            "startDate": start_date.strftime("%Y-%m-%dT00:00:00.0"),
            "endDate": end_date.strftime("%Y-%m-%dT23:59:59.0"),
            "createDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.0"),
            "updateDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.0"),
            "badgeId": badge_id,
            "badgeKey": f"challenge_key_{badge_id}",
            "badgeUuid": badge_uuid,
            "badgePoints": random.randint(1, 5),
            "badgeUnitId": random.randint(0, 5),
            "badgeProgressValue": None,
            "badgeEarnedDate": None,
            "badgeTargetValue": random.uniform(0.0, 10000.0),
            "badgeTypeIds": [random.randint(1, 10) for _ in range(2)],
            "userJoined": random.choice([True, False]),
            "challengeCategoryImageId": random.randint(1, 5),
            "badgePromotionCodeTypePk": None,
            "badgePromotionCode": None,
            "codeExpirationDate": None,
            "redemptionType": None,
            "partnerName": None,
            "partnerRewardUrl": None,
            "limitedCapacity": random.choice([True, False]),
            "joinDateLocal": None,
            "challengeGroupPk": None,
            "joinable": random.choice([True, False]),
            "approximateValue": None,
            "urlEmbeddedSupported": random.choice([True, False]),
        }

        available_badges_data.append(available_badges_entry)

    return available_badges_data
