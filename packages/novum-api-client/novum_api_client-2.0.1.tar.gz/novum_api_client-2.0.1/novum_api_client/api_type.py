# pylint: disable=C0115

import datetime
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Union
from dataclasses_json import dataclass_json, Undefined


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TStats:
    last_login: Union[str, int]
    logins_count: int
    last_ip: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TProfile:
    name: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool]
    picture: Optional[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TServiceCenterSettings:
    showAdvancedOptions: Optional[bool]
    invertAxis: Optional[bool]
    onlyShowTopLevelBatteries: Optional[bool]
    favoriteBatteriesIds: Optional[List[str]]
    batteryTableColumns: Optional[List[str]]
    dashboardTableColumns: Optional[List[str]]
    eisDatasetTableColumns: Optional[List[str]]
    capacityMeasurementTableColumns: Optional[List[str]]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TUserSettings:
    ServiceCenterSettings: Optional[TServiceCenterSettings]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TIDAndTimes:
    id: Optional[str] = None
    created_at: Optional[Union[datetime.datetime, str]] = None
    updated_at: Optional[Union[datetime.datetime, str]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TUserEssentials:
    jwt: Optional[str] = None
    refresh_token: Optional[str] = None
    auth0_id: Optional[str] = None
    roles: Optional[List[str]] = None
    profile: Optional[TProfile] = None
    settings: Optional[TUserSettings] = None
    permissions: Optional[List[str]] = None
    stats: Optional[TStats] = None
    meta_data: Optional[dict] = None
    scope: Optional[str] = None
    expires_at: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TUser(TUserEssentials, TIDAndTimes):
    "TUser"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TMinMax:
    min: Optional[float] = None
    max: Optional[float] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TGeometricDimension:
    height: Optional[float] = None
    width: Optional[float] = None
    depth: Optional[float] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TEISSetup:
    start_frequency: Optional[float] = None
    end_frequency: Optional[float] = None
    number_of_frequencies: Optional[int] = None
    excitation_current_offset: Optional[float] = None
    excitation_current_amplitude: Optional[float] = None
    excitation_mode: Optional[int] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TChargeSetup:
    discharge_rate: Optional[float] = None
    charge_rate: Optional[float] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TUserDocument:
    originalFileName: Optional[str] = None
    fileName: Optional[str] = None
    fileURL: Optional[str] = None
    fileMD5: Optional[str] = None
    fileType: Optional[Dict[str, Any]] = None
    fileSize: Optional[int] = None
    aws_file_url: Optional[str] = None
    aws_file_name: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TBaseDocModel(TIDAndTimes):
    id: Optional[str] = None
    creator_id: Optional[str] = None
    updater_id: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TDetails:
    statusCode: Optional[int]
    headers: Optional[Dict[str, str]]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TAPIError:
    error: Optional[str] = None
    details: Optional[TDetails] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TLatLng:
    planet: str
    lat: float
    lng: float


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TAddress:
    country: str
    country_code: str
    city: str
    state: str
    postal_code: str
    street: str
    street_number: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TLocation:
    geo: TLatLng
    address: TAddress


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TMetrics:
    measured_at: datetime.datetime
    state_of_health: float
    state_of_charge: float
    temperature: float


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TIndicatorProperty:
    scale: float
    top: float
    left: float


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TIndicatorProperties:
    indicator_properties: Dict[str, TIndicatorProperty]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TInsights:
    enabled: Optional[bool] = None
    image: Optional[str] = None
    image_styles: Optional[str] = None
    indicator_properties: Optional[TIndicatorProperties] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TAtomicState:
    updated_at: Union[datetime.datetime, str]
    value: float
    origin_id: Optional[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TBatteryState:
    state_of_health: Optional[TAtomicState] = None
    state_of_charge: Optional[TAtomicState] = None
    current: Optional[TAtomicState] = None
    voltage: Optional[TAtomicState] = None
    temperature: Optional[TAtomicState] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TTreeProperties:
    is_leaf: Optional[bool] = None
    enabled: Optional[bool] = None
    parent: Optional[str] = None
    ancestors: Optional[List[str]] = None
    children_topology: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TEstimatorOverview:
    file_name: Optional[str]
    description: Optional[str]
    time: Optional[Union[str, datetime.datetime]]
    last_valid_time: Optional[Union[str, datetime.datetime]]
    model_state: Optional[List[float]]
    last_valid_model_state: Optional[List[float]]
    report: Optional[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TEstimators:
    soc_estimator: Optional[TEstimatorOverview]


TBatteryGrade = Literal[
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "?",
]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TLowerSoHLimit:
    soh: float
    grade: TBatteryGrade


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TBatteryTypeReading(TBaseDocModel):
    """Reading TBattery Type"""

    name: Optional[str] = None
    manufacturer: Optional[str] = None
    nominal_voltage: Optional[float] = None
    nominal_capacity: Optional[float] = None
    description: Optional[str] = None
    cell_chemistry: Optional[str] = None
    battery_design: Optional[str] = None
    allowed_voltage_range_single_cell: Optional[TMinMax] = None
    allowed_voltage_range_battery_pack: Optional[TMinMax] = None
    allowed_peak_charge_current_range: Optional[TMinMax] = None
    allowed_peak_discharge_current_range: Optional[TMinMax] = None
    allowed_continuous_charge_current_range: Optional[TMinMax] = None
    allowed_temperature_range_for_charging: Optional[TMinMax] = None
    allowed_temperature_range_for_storage: Optional[TMinMax] = None
    allowed_temperature_range_for_use: Optional[TMinMax] = None
    internal_resistance: Optional[float] = None
    self_discharge_rate_per_month: Optional[float] = None
    allowed_cycles_for_100_depth_of_discharge: Optional[int] = None
    mass_based_power_density: Optional[float] = None
    cell_mass: Optional[float] = None
    outer_geometric_dimension: Optional[TGeometricDimension] = None
    default_eis_setup: Optional[TEISSetup] = None
    default_charge_setup: Optional[TChargeSetup] = None
    image: Optional[str] = None
    user_docs: Optional[List[TUserDocument]] = None
    user_doc_ids: Optional[List[str]] = None
    public: Optional[bool] = None
    tags: Optional[List[str]] = None
    grade_lookup_table: Optional[List[TLowerSoHLimit]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TBatteryTypeEssentials(TBatteryTypeReading):
    """Writing TBattery"""

    name: str
    manufacturer: str
    nominal_voltage: float
    nominal_capacity: float


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TBatteryReading(TBaseDocModel):
    name: Optional[str] = None
    battery_type: Optional[TBatteryTypeEssentials] = None
    serial_number: Optional[str] = None
    description: Optional[str] = None
    location: Optional[TLocation] = None
    image: Optional[str] = None
    tags: Optional[List[str]] = None
    metrics: Optional[TMetrics] = None
    insights: Optional[TInsights] = None
    state: Optional[TBatteryState] = None
    tree: Optional[TTreeProperties] = None
    estimators: Optional[TEstimators] = None
    user_doc_ids: Optional[List[str]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TBatteryEssentials(TBatteryReading):
    "TBattery with required fields"
    name: str
    battery_type: TBatteryTypeEssentials


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TChargeTypes:
    UNKNOWN = "UNKNOWN"
    CC = "CC"
    CCCV = "CCCV"
    CCPulse = "CCPulse"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TChargeCycle:
    timestamp: Optional[Union[str, datetime.datetime]]
    voltage: Optional[float]  # in Voltage (V)
    current: Optional[float]  # in Ampere (A)
    charge: Optional[float]  # in AmpereHours (Ah)
    temperature: Optional[float] = None  # in °C (K)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TCapacityMeasurementReading(TBaseDocModel):
    tags: Optional[List[str]] = None
    charge_cycles: Optional[List[TChargeCycle]] = None
    start_time: Optional[datetime.datetime] = None
    charge_type: Optional[TChargeTypes] = None
    context_id: Optional[str] = None
    battery: Optional[TBatteryEssentials] = None
    end_time: Optional[datetime.datetime] = None
    current_setpoint: Optional[float] = None  # in Ampere (A)
    voltage_setpoint: Optional[float] = None  # in Voltage (V)
    ambient_temperature: Optional[float] = None  # in °C (K)
    device_name: Optional[str] = None
    device_info: Optional[str] = None
    voltage_min: Optional[float] = None  # in Voltage (V)
    voltage_max: Optional[float] = None  # in Voltage (V)
    capacity: Optional[float] = None  # in AmpereHours (Ah)
    state_of_health: Optional[float] = None
    internal_resistance: Optional[float] = None  # in Ohm (Ω)
    grade: Optional[str] = None
    is_preview: Optional[bool] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TCapacityMeasurementEssentials(TCapacityMeasurementReading):
    """TCapacityMeasurement"""

    tags: List[str]
    charge_cycles: List[TChargeCycle]
    start_time: datetime.datetime
    charge_type: TChargeTypes


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TTimedMeasure:
    before: Optional[float]
    after: Optional[float]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TVersionReading(TAPIError):
    tag: Optional[str] = None
    name: Optional[str] = None
    hash: Optional[str] = None
    branch: Optional[str] = None
    build_date: Optional[datetime.datetime] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TVersion(TVersionReading):
    "TVersion"
    tag: str
    name: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TMeasurementCycle:
    frequency: float  # frequency of the periodic excitation in Hz
    amplitude: float  # amplitude of the oscillation current in A
    phase_shift: float  # phase shift of the oscillation current
    temperature: Optional[float]
    voltage: Optional[float]  # voltage measured before the excitation in V
    time_delta: Optional[float]  # in seconds
    quality: Optional[float]  # a quality indicator
    voltage_raw_values: Optional[List[float]]
    current_raw_values: Optional[List[float]]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TRemoteProcedureReport:
    success: bool
    report: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TDeviceMetaParticle:
    cpu_id: str
    serial: str
    firmware: TVersion
    name: Optional[str]
    description: Optional[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TProduct(TBaseDocModel):
    gtin: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TDeviceMeta(TBaseDocModel, TDeviceMetaParticle):
    product: Optional[TProduct] = None
    revision: Optional[str] = None
    description: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TAPIInfoEssentials:
    name: Optional[str] = None
    dbName: Optional[str] = None
    version: Optional[TVersion] = None
    description: Optional[str] = None
    dev_container_mode: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TAPIInfo(TAPIInfoEssentials, TAPIError):
    "Info"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TMeasured:
    start_time: Optional[Union[datetime.datetime, str]] = None
    end_time: Optional[Union[datetime.datetime, str]] = None
    eis_setup: Optional[TEISSetup] = None
    voltage: Optional[TTimedMeasure] = None
    ambient_temperature: Optional[TTimedMeasure] = None
    battery_temperature: Optional[TTimedMeasure] = None
    measurement_cycles: Optional[List[TMeasurementCycle]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TAnalysis:
    grade: Optional[str] = None
    state_of_health: Optional[float] = None
    state_of_charge: Optional[float] = None
    temperature: Optional[float] = None
    enforce_capacity_test: Optional[bool] = None
    reports: Optional[Dict[str, TRemoteProcedureReport]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TDatasetMeta:
    tags: List[str]
    device: TDeviceMetaParticle
    client_software: TVersion
    comment: Optional[str] = None
    battery: Optional[TBatteryEssentials] = None
    user_defined: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TDatasetReading(TBaseDocModel):
    measured: Optional[TMeasured] = None
    analysis: Optional[TAnalysis] = None
    meta: Optional[TDatasetMeta] = None
    show_in_chart: Optional[bool] = None
    context_id: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TDatasetEssentials(TDatasetReading):
    """TDataset"""

    measured: TMeasured
    analysis: TAnalysis
    meta: TDatasetMeta


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class UITMeasurement:
    time: datetime.datetime
    voltage: Optional[float]
    current: Optional[float]
    temperature: Optional[float]
    charge: Optional[float]
    soc: Optional[float]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class UITMeasurements(List[UITMeasurement]):
    pass


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TDeviceMeasurement:
    device_id: str
    measurements: UITMeasurements


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TDeviceMeasurementsResult:
    results: List[UITMeasurement]
    rejectedDeviceIds: List[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ReportStates:
    Unread = "unread"
    Viewed = "viewed"
    Acknowledged = "acknowledged"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TReportEssentials:
    state: ReportStates
    origin_id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    context_id: Optional[str]
    meta: Optional[dict] = None
    user_doc_ids: Optional[List[str]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TReport(TBaseDocModel, TReportEssentials):
    """TReport"""
