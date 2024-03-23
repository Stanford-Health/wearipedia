import random
from datetime import datetime, timedelta


def get_metrics_data(start_date, num_days):
    """Generate synthetic "max_metrics" data for a specified number of days.

    This function generates synthetic "max_metrics" data for a specified number of days. It simulates various metrics like
    vo2MaxPreciseValue and vo2MaxValue for users with random values. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which "max_metrics" data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing "max_metrics" data for the specified number of days.
    :rtype: List[Dict]
    """
    max_metrics_data = []

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        date = (start_date_obj + timedelta(days=i)).strftime("%Y-%m-%d")

        max_metrics_entry = [
            {
                "userId": random.randint(10000000, 99999999),
                "generic": {
                    "calendarDate": date,
                    "vo2MaxPreciseValue": random.uniform(30.0, 50.0),
                    "vo2MaxValue": random.randint(30, 50),
                    "fitnessAge": random.randint(20, 50),
                    "fitnessAgeDescription": "MODERATE",
                    "maxMetCategory": random.randint(0, 3),
                },
                "cycling": None,
                "heatAltitudeAcclimation": {
                    "calendarDate": date,
                    "altitudeAcclimationDate": date,
                    "previousAltitudeAcclimationDate": date,
                    "heatAcclimationDate": date,
                    "previousHeatAcclimationDate": date,
                    "altitudeAcclimation": random.randint(0, 100),
                    "previousAltitudeAcclimation": random.randint(0, 100),
                    "heatAcclimationPercentage": random.randint(0, 100),
                    "previousHeatAcclimationPercentage": random.randint(0, 100),
                    "heatTrend": "STABLE",
                    "altitudeTrend": "STABLE",
                    "currentAltitude": random.randint(100, 1000),
                    "previousAltitude": random.randint(100, 1000),
                    "acclimationPercentage": random.randint(0, 100),
                    "previousAcclimationPercentage": random.randint(0, 100),
                    "altitudeAcclimationLocalTimestamp": f"{date}T23:55:52.0",
                },
            }
        ]

        max_metrics_data.append(max_metrics_entry)
    return max_metrics_data


def random_datetime(start_date, end_date):
    """
    Generate a random datetime within a specified date range.

    This function generates a random datetime within the specified start and end dates.

    :param start_date: The start date as a datetime object.
    :type start_date: datetime.datetime
    :param end_date: The end date as a datetime object.
    :type end_date: datetime.datetime
    :return: A random datetime between start_date (inclusive) and end_date (exclusive).
    :rtype: datetime.datetime
    """
    start_timestamp = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
    end_timestamp = datetime.strptime(end_date, "%Y-%m-%d").timestamp()
    random_timestamp = start_timestamp + random.random() * (
        end_timestamp - start_timestamp
    )
    return datetime.fromtimestamp(random_timestamp)


def get_personal_record_data(start_date, end_date, num_entries):
    """Generate synthetic personal record data for a specified date range.

    This function generates synthetic personal record data for a given date range. Each personal record entry contains
    information such as the type of record, activity details, start timestamps (GMT and local), and the recorded value.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param end_date: The end date in the format "YYYY-MM-DD".
    :type end_date: str
    :param num_entries: The number of personal record entries to generate.
    :type num_entries: int
    :return: A list of dictionaries, each containing personal record data, including type, activity details, timestamps, and recorded value.
    :rtype: List[Dict]
    """
    personal_record_data = []

    for _ in range(num_entries):
        personal_record_entry = {
            "id": random.randint(1000000000, 9999999999),
            "typeId": random.randint(1, 16),
            "activityId": 0,
            "activityName": None,
            "activityType": None,
            "activityStartDateTimeInGMT": None,
            "actStartDateTimeInGMTFormatted": None,
            "activityStartDateTimeLocal": None,
            "activityStartDateTimeLocalFormatted": None,
            "value": round(random.uniform(10, 1000000), 2),
            "prTypeLabelKey": None,
            "poolLengthUnit": None,
        }

        personal_record_entry["prStartTimeGmt"] = int(
            random_datetime(start_date, end_date).timestamp() * 1000
        )
        personal_record_entry["prStartTimeGmtFormatted"] = datetime.utcfromtimestamp(
            personal_record_entry["prStartTimeGmt"] / 1000
        ).strftime("%Y-%m-%dT%H:%M:%S.0")

        personal_record_entry["prStartTimeLocal"] = int(
            random_datetime(start_date, end_date).timestamp() * 1000
        )
        personal_record_entry["prStartTimeLocalFormatted"] = datetime.fromtimestamp(
            personal_record_entry["prStartTimeLocal"] / 1000
        ).strftime("%Y-%m-%dT%H:%M:%S.0")

        personal_record_data.append(personal_record_entry)

    return personal_record_data


def get_activities_data(start_date, num_days):
    """Generate synthetic activity data for a specified number of days.

    This function generates synthetic activity data for a specified number of days. It simulates activities with random
    start times, durations, distances, elevation gains, and other attributes. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which activity data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic activity data for the specified number of days.
    :rtype: List[Dict]
    """

    activities_data = []
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        activity_start_time = start_date_obj + timedelta(days=i)
        # Between 30 minutes and 3 hours
        activity_duration = random.randint(30 * 60, 3 * 60 * 60)
        distance = random.uniform(0.0, 15.0)  # Up to 15 km
        elevation_gain = random.uniform(0.0, 500.0)  # Up to 500 meters
        elevation_loss = random.uniform(0.0, 500.0)  # Up to 500 meters
        # Average speed in km/h
        avg_speed = distance / (activity_duration / 3600)

        activity_entry = {
            "activityId": random.randint(10000000, 99999999),
            "activityName": "Random Activity",
            "description": None,
            "startTimeLocal": activity_start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "startTimeGMT": activity_start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "activityType": {
                "typeId": random.randint(1, 20),
                "typeKey": "random_activity",
                "parentTypeId": random.randint(1, 20),
                "isHidden": False,
                "restricted": False,
                "trimmable": True,
            },
            "eventType": {
                "typeId": random.randint(1, 10),
                "typeKey": "uncategorized",
                "sortOrder": 10,
            },
            "comments": None,
            "parentId": None,
            "distance": distance,
            "duration": activity_duration,
            "elapsedDuration": activity_duration,
            "movingDuration": random.randint(20 * 60, activity_duration),
            "elevationGain": elevation_gain,
            "elevationLoss": elevation_loss,
            "averageSpeed": avg_speed,
            "maxSpeed": avg_speed + random.uniform(0.0, 5.0),
            "startLatitude": random.uniform(-90.0, 90.0),
            "startLongitude": random.uniform(-180.0, 180.0),
            "hasPolyline": True,
            "ownerId": random.randint(10000000, 99999999),
            "ownerDisplayName": "Random User",
            "ownerFullName": "Random User",
        }

        activities_data.append(activity_entry)

    return activities_data


def get_devices_data(start_date, num_days):
    """Generate synthetic device data for a specified number of days.

    This function generates synthetic device data for a specified number of days. It simulates various device attributes
    for multiple devices. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which device data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic device data for the specified number of days.
    :rtype: List[Dict]
    """
    devices_data = []

    devices_entry = {
        "userProfilePk": random.randint(10000000, 99999999),
        "unitId": random.randint(1000000000, 9999999999),
        "deviceId": random.randint(1000000000, 9999999999),
        "appSupport": True,
        "applicationKey": "fenix7s",
        "deviceTypePk": 36879,
        "bestInClassVideoLink": None,
        "bluetoothClassicDevice": False,
        "bluetoothLowEnergyDevice": True,
        "deviceCategories": ["FITNESS", "WELLNESS", "GOLF", "OUTDOOR"],
        "deviceEmbedVideoLink": None,
        "deviceSettingsFile": "RealTimeDeviceSettings_RANDOM.json",
        "gcmSettingsFile": "Fenix7S_RANDOM.json",
        "deviceVideoPageLink": None,
        "displayOrder": 0,
        "golfDisplayOrder": 0,
        "hasOpticalHeartRate": True,
        "highlighted": False,
        "hybrid": True,
        "imageUrl": "https://static.garmincdn.com/en/products/010-02539-00/v/cf-sm-2x3-d013b003-7e67-4db4-90c2-7fbd03f40a7c.png",
        "minGCMAndroidVersion": 6411,
        "minGCMWindowsVersion": 99999,
        "minGCMiOSVersion": 10320,
        "minGolfAppiOSVersion": 0,
        "minGolfAppAndroidVersion": 0,
        "partNumber": "006-B3905-00",
        "primary": True,
        "productDisplayName": "fenix 7S",
        "deviceTags": None,
        "productSku": "010-02539-00",
        "wasp": False,
        "weightScale": False,
        "wellness": False,
        "wifi": True,
        "hasPowerButton": True,
        "supportsSecondaryUsers": False,
        "primaryApplication": "UNSPECIFIED",
        "incompatibleApplications": [],
        "abnormalHeartRateAlertCapable": True,
        "activitySummFitFileCapable": True,
        "aerobicTrainingEffectCapable": True,
        "alarmDaysCapable": True,
        "allDayStressCapable": True,
        "anaerobicTrainingEffectCapable": True,
        "atpWorkoutCapable": True,
        "bodyBatteryCapable": True,
        "brickWorkoutCapable": True,
        "cardioCapable": True,
        "cardioOptionCapable": False,
        "cardioSportsCapable": False,
        "cardioWorkoutCapable": True,
        "cellularCapable": False,
        "changeLogCapable": True,
        "contactManagementCapable": True,
        "courseCapable": True,
        "courseFileType": "FIT",
        "coursePromptCapable": False,
        "customIntensityMinutesCapable": True,
        "customWorkoutCapable": True,
        "cyclingSegmentCapable": True,
        "cyclingSportsCapable": False,
        "cyclingWorkoutCapable": True,
        "defaultSettingCapable": True,
        "deviceSettingCapable": True,
        "deviceSettingFileType": None,
        "displayFieldsExtCapable": False,
        "divingCapable": False,
        "ellipticalOptionCapable": False,
        "floorsClimbedGoalCapable": True,
        "ftpCapable": True,
        "gcj02CourseCapable": False,
        "glonassCapable": True,
        "goalCapable": True,
        "goalFileType": "FIT",
        "golfAppSyncCapable": False,
        "gpsRouteCapable": True,
        "handednessCapable": True,
        "hrZoneCapable": True,
        "hrvStressCapable": True,
        "intensityMinutesGoalCapable": True,
        "lactateThresholdCapable": True,
        "languageSettingCapable": True,
        "languageSettingFileType": None,
        "lowHrAlertCapable": True,
        "maxHRCapable": True,
        "maxWorkoutCount": 200,
        "metricsFitFileReceiveCapable": True,
        "metricsUploadCapable": True,
        "militaryTimeCapable": True,
        "moderateIntensityMinutesGoalCapable": True,
        "nfcCapable": True,
        "otherOptionCapable": False,
        "otherSportsCapable": False,
        "personalRecordCapable": True,
        "personalRecordFileType": "FIT",
        "poolSwimOptionCapable": False,
        "powerCurveCapable": True,
        "powerZonesCapable": True,
        "pulseOxAllDayCapable": True,
        "pulseOxOnDemandCapable": True,
        "pulseOxSleepCapable": True,
        "remCapable": True,
        "reminderAlarmCapable": False,
        "reorderablePagesCapable": False,
        "restingHRCapable": True,
        "rideOptionsCapable": False,
        "runOptionIndoorCapable": False,
        "runOptionsCapable": False,
        "runningSegmentCapable": True,
        "runningSportsCapable": False,
        "runningWorkoutCapable": True,
        "scheduleCapable": True,
        "scheduleFileType": "FIT",
        "segmentCapable": True,
        "segmentPointCapable": True,
        "settingCapable": True,
        "settingFileType": "FIT",
        "sleepTimeCapable": True,
        "smallFitFileOnlyCapable": False,
        "sportCapable": True,
        "sportFileType": "FIT",
        "stairStepperOptionCapable": False,
        "strengthOptionsCapable": False,
        "strengthWorkoutCapable": True,
        "supportedHrZones": ["RUNNING", "CYCLING", "SWIMMING", "ALL"],
        "swimWorkoutCapable": True,
        "trainingPlanCapable": True,
        "trainingStatusCapable": True,
        "trainingStatusPauseCapable": True,
        "userProfileCapable": False,
        "userProfileFileType": None,
        "userTcxExportCapable": False,
        "vo2MaxBikeCapable": True,
        "vo2MaxRunCapable": True,
        "walkOptionCapable": False,
        "walkingSportsCapable": False,
        "weatherAlertsCapable": False,
        "weatherSettingsCapable": False,
        "workoutCapable": True,
        "workoutFileType": "FIT",
        "yogaCapable": True,
        "yogaOptionCapable": False,
        "heatAndAltitudeAcclimationCapable": True,
        "trainingLoadBalanceCapable": True,
        "indoorTrackOptionsCapable": False,
        "indoorBikeOptionsCapable": False,
        "indoorWalkOptionsCapable": False,
        "trainingEffectLabelCapable": True,
        "pacebandCapable": True,
        "respirationCapable": True,
        "openWaterSwimOptionCapable": False,
        "phoneVerificationCheckRequired": False,
        "weightGoalCapable": False,
        "yogaWorkoutCapable": True,
        "pilatesWorkoutCapable": True,
        "connectedGPSCapable": False,
        "diveAppSyncCapable": False,
        "golfLiveScoringCapable": True,
        "solarPanelUtilizationCapable": False,
        "sweatLossCapable": True,
        "diveAlertCapable": False,
        "requiresInitialDeviceNickname": False,
        "defaultSettingsHbaseMigrated": True,
        "sleepScoreCapable": True,
        "fitnessAgeV2Capable": True,
        "intensityMinutesV2Capable": True,
        "collapsibleControlMenuCapable": False,
        "measurementUnitSettingCapable": False,
        "onDeviceSleepCalculationCapable": True,
        "hiitWorkoutCapable": True,
        "runningHeartRateZoneCapable": True,
        "cyclingHeartRateZoneCapable": True,
        "swimmingHeartRateZoneCapable": True,
        "defaultHeartRateZoneCapable": True,
        "cyclingPowerZonesCapable": True,
        "xcSkiPowerZonesCapable": True,
        "swimAlgorithmCapable": True,
        "benchmarkExerciseCapable": True,
        "spectatorMessagingCapable": False,
        "ecgCapable": False,
        "lteLiveEventSharingCapable": False,
        "sleepFitFileReceiveCapable": True,
        "secondaryWorkoutStepTargetCapable": False,
        "assistancePlusCapable": False,
        "powerGuidanceCapable": True,
        "airIntegrationCapable": False,
        "healthSnapshotCapable": True,
        "racePredictionsRunCapable": True,
        "vivohubCompatible": False,
        "stepsTrueUpChartCapable": True,
        "sportingEventCapable": True,
        "solarChargeCapable": False,
        "realTimeSettingsCapable": True,
        "emergencyCallingCapable": False,
        "personalRepRecordCapable": False,
        "hrvStatusCapable": True,
        "trainingReadinessCapable": True,
        "publicBetaSoftwareCapable": True,
        "workoutAudioPromptsCapable": False,
        "actualStepRecordingCapable": True,
        "groupTrack2Capable": False,
        "golfAppPairingCapable": False,
        "localWindConditionsCapable": False,
        "multipleGolfCourseCapable": False,
        "beaconTrackingCapable": False,
        "batteryStatusCapable": False,
        "runningPowerZonesCapable": True,
        "acuteTrainingLoadCapable": True,
        "criticalSwimSpeedCapable": False,
        "primaryTrainingCapable": True,
        "dayOfWeekSleepWindowCapable": True,
        "golfCourseDownloadCapable": False,
        "launchMonitorEventSharingCapable": False,
        "lhaBackupCapable": True,
        "jetlagCapable": True,
        "bloodPressureCapable": False,
        "bbiRecordingCapable": False,
        "wheelchairCapable": False,
        "primaryActivityTrackerSettingCapable": True,
        "setBodyCompositionCapable": False,
        "acuteChronicWorkloadRatioCapable": True,
        "sleepNeedCapable": False,
        "wearableBackupRestoreCapable": True,
        "cyclingComputerBackupRestoreCapable": False,
        "descriptiveTrainingEffectCapable": False,
        "sleepSkinTemperatureCapable": False,
        "runningLactateThresholdCapable": False,
        "altitudeAcclimationPercentageCapable": True,
        "hillScoreAndEnduranceScoreCapable": True,
        "swimWorkout2Capable": False,
        "enhancedWorkoutStepCapable": False,
        "primaryTrainingBackupCapable": False,
        "hideSoftwareUpdateVersionCapable": False,
        "adaptiveCoachingScheduleCapable": False,
        "datasource": "C",
        "deviceStatus": "active",
        "registeredDate": 1658531394000,
        "actualProductSku": "010-02539-00",
        "vivohubConfigurable": None,
        "serialNumber": "70H001824",
        "shortName": None,
        "displayName": "fenix 7S",
        "wifiSetup": False,
        "currentFirmwareVersionMajor": 14,
        "currentFirmwareVersionMinor": 36,
        "activeInd": 1,
        "primaryActivityTrackerIndicator": True,
        "unRetirable": False,
        "corporateDevice": False,
        "prePairedWithHRM": False,
        "otherAssociation": False,
        "currentFirmwareVersion": "14.36",
        "isPrimaryUser": False,
    }

    for _ in range(3):
        devices_entry["userProfilePk"] = random.randint(10000000, 99999999)
        devices_entry["unitId"] = random.randint(1000000000, 9999999999)
        devices_entry["deviceId"] = random.randint(1000000000, 9999999999)
        devices_data.append(devices_entry)
    return devices_data
