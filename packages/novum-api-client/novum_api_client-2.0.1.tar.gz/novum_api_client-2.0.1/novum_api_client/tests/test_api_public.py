# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=W0105
# flake8: noqa

import os
from datetime import datetime
import json
import pytest

from ..base_client import NovumAPIError
from ..client import NovumAPIClient
from ..api_type import (
    TUser,
    TReport,
    TVersion,
    TAnalysis,
    TEISSetup,
    TMeasured,
    TChargeCycle,
    TChargeTypes,
    TDatasetMeta,
    ReportStates,
    TTimedMeasure,
    TMeasurementCycle,
    TReportEssentials,
    TAPIInfoEssentials,
    TDatasetEssentials,
    TBatteryEssentials,
    TDeviceMetaParticle,
    TBatteryTypeEssentials,
    TCapacityMeasurementEssentials,
)


API_HOST = os.getenv("NOVUM_API_URL", "localhost")
SSL_VERIFY = False if os.getenv("SSL_VERIFY", "true").lower() == "false" else True


class TestNovumAPIClient:
    @pytest.fixture(scope="class")
    def unauthenticated_api_client(self):
        """Check if authenticated before login."""
        api_client = NovumAPIClient(host=API_HOST, check_ssl_certification=SSL_VERIFY)
        yield api_client

    @pytest.fixture(scope="class")
    def ada_logged_client(self):
        """Fixture API client logged in."""
        client = NovumAPIClient(host=API_HOST, check_ssl_certification=SSL_VERIFY)
        client.login(
            email="ada.lovelace@novum-engineering.com", password="5TkbQuVEx4v2GVqJ"
        )
        yield client

    @pytest.mark.run(order=1)
    def test_ping(self, unauthenticated_api_client: NovumAPIClient):
        """Check ping message."""
        response = unauthenticated_api_client.ping()

        assert (
            response["message"]
            == "Hello user this is the Novum batman API server. All routes begin with /api/{api_type}/{api_version}/{resource}. You have to identify using your credentials and /api/batman/v1/login to obtain a token"
        )

    @pytest.mark.run(order=2)
    def test_get_info(self, unauthenticated_api_client: NovumAPIClient):
        """Check info root."""
        info = unauthenticated_api_client.get_info()

        assert isinstance(info, TAPIInfoEssentials)
        assert info.name == "Novum Base API"
        assert info.dbName == "batman"

    @pytest.mark.run(order=3)
    def test_get_version(self, unauthenticated_api_client: NovumAPIClient):
        """Check version"""
        version = unauthenticated_api_client.get_version()

        assert isinstance(version, TVersion)
        assert version.name == "novum-api"

    @pytest.mark.run(order=4)
    def test_login_ada(self, unauthenticated_api_client: NovumAPIClient):
        """Check Ada login."""
        response = unauthenticated_api_client.login(
            email="ada.lovelace@novum-engineering.com", password="5TkbQuVEx4v2GVqJ"
        )
        assert isinstance(response, TUser)
        assert "user" in response.roles

    @pytest.mark.run(order=5)
    def test_login_ada_with_wrong_credentials(
        self, unauthenticated_api_client: NovumAPIClient
    ):
        """Check if login with wrong password gets authenticated."""
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.login(
                email="ada.lovelace@novum-engineering.com", password="WrongPassword"
            )

        error_details = json.loads(str(excinfo.value))

        expected_error_message = "Wrong email or password."
        assert expected_error_message in error_details["details"]

    @pytest.mark.run(order=6)
    def test_check_current_user_still_authenticated(
        self, ada_logged_client: NovumAPIClient
    ):
        """Check authentication."""
        response = ada_logged_client.check_current_user_still_authenticated()
        assert response["authenticated"] is True

    @pytest.mark.run(order=7)
    def test_logout(self, ada_logged_client: NovumAPIClient):
        """Check logout function."""
        response = ada_logged_client.logout()
        assert response == {"message": "Logout successful"}

    # ********************************************************
    # Section for the Battery Type
    # ********************************************************

    @pytest.fixture(scope="class")
    def sample_battery_type(self):
        """Fixture: Battery Type"""
        sample_battery_type = TBatteryTypeEssentials(
            name="Test Battery Type",
            manufacturer="The Tester",
            nominal_voltage=3.7,
            nominal_capacity=2500,
        )
        return sample_battery_type

    @pytest.fixture(scope="class")
    def created_battery_type(
        self,
        ada_logged_client: NovumAPIClient,
        sample_battery_type: TBatteryTypeEssentials,
    ):
        """Fixture: sample of battery type."""
        response = ada_logged_client.create_battery_type(sample_battery_type)

        yield response

        # Add cleanup code here to delete the created battery type
        ada_logged_client.remove_battery_types_by_id(response.id)

    @pytest.mark.run(order=8)
    def test_get_battery_type(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery_type: TBatteryTypeEssentials,
    ):
        """Check if the created battery type can be fetched."""
        response = ada_logged_client.get_battery_types()

        assert response[0].id == created_battery_type.id

    @pytest.mark.run(order=9)
    def test_get_battery_type_with_fields(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery_type: TBatteryTypeEssentials,
    ):
        """Check if the created battery type can be fetched with fields."""
        fields = {"name": 1}
        response = ada_logged_client.get_battery_types(fields=fields)

        assert response[0].id == created_battery_type.id
        assert response[0].name == created_battery_type.name
        assert response[0].manufacturer is None

    @pytest.mark.run(order=10)
    def test_get_battery_type_without_fields(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery_type: TBatteryTypeEssentials,
    ):
        """Check if the created battery type can be fetched without fields."""
        fields = {"name": 0}
        response = ada_logged_client.get_battery_types(fields=fields)

        assert response[0].id == created_battery_type.id
        assert response[0].name is None

    @pytest.mark.run(order=11)
    def test_get_battery_type_count(self, ada_logged_client: NovumAPIClient):
        """Check number of battery types created."""
        response = ada_logged_client.get_battery_types_count()
        assert response == 1

    @pytest.mark.run(order=12)
    def test_get_battery_type_by_id(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery_type: TBatteryTypeEssentials,
    ):
        """Check fetching battery type by id"""
        response = ada_logged_client.get_battery_types_by_id(created_battery_type.id)
        assert response.id == created_battery_type.id

    @pytest.mark.run(order=13)
    def test_create_battery_type(self, created_battery_type: TBatteryTypeEssentials):
        """Check info of created battery type."""
        assert created_battery_type.name == "Test Battery Type"
        assert created_battery_type.nominal_voltage == 3.7
        assert created_battery_type.nominal_capacity == 2500

    @pytest.fixture(scope="class")
    def sample_battery_type_without_name(
        self, sample_battery_type: TBatteryTypeEssentials
    ):
        """Fixture: battery type without name."""
        sample_battery_type.name = None  # type: ignore
        return sample_battery_type

    @pytest.mark.run(order=14)
    def test_create_battery_type_missing_required_field_name(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_battery_type_without_name: TBatteryTypeEssentials,
    ):
        """Check if attempt to create a battery type without name raises an error."""
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_battery_type(
                sample_battery_type_without_name
            )

        assert '{"error":"Failed to validate battery type data","details":' in str(
            excinfo.value
        )

    @pytest.fixture(scope="class")
    def sample_battery_type_without_manufacturer(
        self, sample_battery_type: TBatteryTypeEssentials
    ):
        """Fixture: battery type without manufacturer."""
        sample_battery_type.manufacturer = None  # type: ignore
        return sample_battery_type

    @pytest.mark.run(order=16)
    def test_create_battery_type_missing_required_field_manufacturer(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_battery_type_without_manufacturer: TBatteryTypeEssentials,
    ):
        """Check if attempt to create a battery type without manufacturer raises an error."""
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_battery_type(
                sample_battery_type_without_manufacturer
            )

        assert '{"error":"Failed to validate battery type data","details":' in str(
            excinfo.value
        )

    @pytest.fixture(scope="class")
    def sample_battery_type_without_capacity(
        self, sample_battery_type: TBatteryTypeEssentials
    ):
        """Fixture: battery type without nominal capacity."""
        sample_battery_type.nominal_capacity = ""  # type: ignore
        return sample_battery_type

    @pytest.mark.run(order=17)
    def test_create_battery_type_missing_required_field_capacity(
        self,
        ada_logged_client: NovumAPIClient,
        sample_battery_type_without_capacity: TBatteryTypeEssentials,
    ):
        """Check if attempt to create a battery type without nominal capacity raises an error."""
        with pytest.raises(NovumAPIError) as excinfo:
            ada_logged_client.create_battery_type(sample_battery_type_without_capacity)

        assert '{"error":"Failed to decode battery type data"' in str(excinfo.value)

    @pytest.fixture(scope="class")
    def sample_battery_type_without_voltage(
        self, sample_battery_type: TBatteryTypeEssentials
    ):
        """Fixture: battery type without nominal voltage."""
        sample_battery_type.nominal_voltage = ""  # type: ignore
        return sample_battery_type

    @pytest.mark.run(order=18)
    def test_update_battery_type(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery_type: TBatteryTypeEssentials,
    ):
        """Check if attempt to create a battery type without nominal voltage raises an error."""
        update_data = TBatteryTypeEssentials(
            name="Updated Battery Type",
            manufacturer="Updated",
            nominal_voltage=3.8,
            nominal_capacity=3200,
            description="There is an update",
        )

        updated_response = ada_logged_client.update_battery_type_by_id(
            created_battery_type.id, update_data
        )

        assert updated_response.name == "Updated Battery Type"
        assert updated_response.manufacturer == "Updated"
        assert updated_response.nominal_voltage == 3.8
        assert updated_response.nominal_capacity == 3200
        assert updated_response.description == "There is an update"

    @pytest.mark.run(order=19)
    def test_delete_battery_type(
        self,
        ada_logged_client: NovumAPIClient,
        sample_battery_type: TBatteryTypeEssentials,
    ):
        """Check battery type deletion."""
        sample_battery_type.name = "to be deleted"
        sample_battery_type.manufacturer = "broken manufacture"
        sample_battery_type.nominal_capacity = 1
        sample_battery_type.nominal_voltage = 220

        to_be_deleted_sample = sample_battery_type
        to_be_deleted = ada_logged_client.create_battery_type(to_be_deleted_sample)

        response = ada_logged_client.remove_battery_types_by_id(to_be_deleted.id)

        assert "was removed" in response

    # # ********************************************************
    # # Section for the Battery
    # # ********************************************************

    @pytest.fixture(scope="class")
    def sample_battery(self, created_battery_type: TBatteryTypeEssentials):
        """Fixture: sample of battery."""
        return TBatteryEssentials(
            name="Test Battery", battery_type=created_battery_type
        )

    @pytest.fixture(scope="class")
    def created_battery(
        self, ada_logged_client: NovumAPIClient, sample_battery: TBatteryEssentials
    ):
        """Fixture: sample of battery."""

        response = ada_logged_client.create_battery(sample_battery)

        yield response

        # Add cleanup code here to delete the created battery type
        ada_logged_client.remove_battery_by_id(response.id)

    @pytest.mark.run(order=20)
    def test_create_battery(self, created_battery: TBatteryEssentials):
        """Check battery creation."""

        assert created_battery.name == "Test Battery"

    @pytest.mark.run(order=21)
    def test_get_battery(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery: TBatteryEssentials,
    ):
        """Check if the created battery can be fetched."""
        response = ada_logged_client.get_batteries()

        assert response[0].id == created_battery.id

    @pytest.mark.run(order=22)
    def test_get_battery_with_fields(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery: TBatteryEssentials,
    ):
        """Check if the created battery can be fetched with fields."""
        fields = {"name": 1}
        response = ada_logged_client.get_batteries(fields=fields)

        assert response[0].id == created_battery.id
        assert response[0].name == created_battery.name
        assert response[0].description is None

    @pytest.mark.run(order=23)
    def test_get_battery_without_fields(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery: TBatteryEssentials,
    ):
        """Check if the created battery can be fetched without fields."""
        fields = {"name": 0}
        response = ada_logged_client.get_batteries(fields=fields)

        assert response[0].id == created_battery.id
        assert response[0].name is None
        assert response[0].description is None

    @pytest.fixture(scope="class")
    def sample_battery_without_name(self, sample_battery: TBatteryEssentials):
        """Fixture: battery without name."""
        sample_battery.name = None  # type: ignore

        return sample_battery

    @pytest.mark.run(order=24)
    def test_create_battery_missing_required_field_name(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_battery_without_name: TBatteryEssentials,
    ):
        """Check if attempt to create a battery without name raises an error."""
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_battery(sample_battery_without_name)

        assert '{"error":"Failed to validate ' in str(excinfo.value)

    @pytest.mark.run(order=25)
    def test_update_battery(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery: TBatteryEssentials,
        created_battery_type: TBatteryTypeEssentials,
    ):
        """Check battery updating."""
        update_data = TBatteryEssentials(
            name="Updated Battery",
            battery_type=created_battery_type,
            description="There is an update",
        )

        updated_response = ada_logged_client.update_battery_by_id(
            created_battery.id, update_data
        )

        assert updated_response.name == "Updated Battery"
        assert updated_response.description == "There is an update"

    @pytest.mark.run(order=26)
    def test_delete_battery(
        self,
        ada_logged_client: NovumAPIClient,
        created_battery_type: TBatteryTypeEssentials,
    ):
        """Check battery deletion."""
        to_be_deleted_sample = TBatteryEssentials(
            name="Test Battery Delete", battery_type=created_battery_type
        )
        to_be_deleted = ada_logged_client.create_battery(to_be_deleted_sample)

        response = ada_logged_client.remove_battery_by_id(to_be_deleted.id)

        assert "was removed" in response

    # ********************************************************
    # Section for the DataSet
    # ********************************************************

    @pytest.fixture(scope="class")
    def sample_eis_dataset(self):
        """Fixture: EIS measurement."""
        sample_eis = TDatasetEssentials(
            measured=TMeasured(
                start_time=datetime(2023, 11, 10, 5, 5, 5),
                end_time=datetime(2023, 11, 10, 5, 5, 5),
                eis_setup=TEISSetup(
                    start_frequency=4000,
                    end_frequency=0.1,
                    number_of_frequencies=21,
                    excitation_current_offset=0.06,
                    excitation_current_amplitude=0.05,
                    excitation_mode=None,
                ),
                voltage=TTimedMeasure(
                    before=2.853627920150757, after=2.8368048667907715
                ),
                ambient_temperature=TTimedMeasure(
                    before=23.423852920532227,
                    after=0,
                ),
                battery_temperature=TTimedMeasure(
                    before=0,
                    after=0,
                ),
                measurement_cycles=[
                    TMeasurementCycle(
                        frequency=3906.25,
                        amplitude=0.03961149351980206,
                        phase_shift=10.600752397202513,
                        voltage=3.4,
                        temperature=None,
                        time_delta=None,
                        quality=None,
                        current_raw_values=None,
                        voltage_raw_values=None,
                    )
                ],
            ),
            analysis=TAnalysis(),
            meta=TDatasetMeta(
                tags=["tag1", "tag2"],
                client_software=TVersion(
                    tag="test_tag",
                    name="test",
                    hash=None,
                    branch=None,
                    build_date=None,
                    error=None,
                    details=None,
                ),
                device=TDeviceMetaParticle(
                    cpu_id="test123456789",
                    serial="1235654321",
                    name=None,
                    description=None,
                    firmware=TVersion(
                        tag="test_tag",
                        name="test",
                        hash=None,
                        branch=None,
                        build_date=None,
                        error=None,
                        details=None,
                    ),
                ),
            ),
        )
        return sample_eis

    @pytest.fixture(scope="class")
    def created_eis_dataset(
        self, ada_logged_client: NovumAPIClient, sample_eis_dataset: TDatasetEssentials
    ):
        """Fixture: created EIS measurement."""

        response = ada_logged_client.create_dataset(sample_eis_dataset)

        yield response

        # Add cleanup code here to delete the created battery type
        ada_logged_client.remove_dataset_by_id(response.id)

    @pytest.mark.run(order=27)
    def test_create_eis_dataset(self, created_eis_dataset: TDatasetEssentials):
        """Check EIS creation."""

        assert isinstance(created_eis_dataset, TDatasetEssentials)

    @pytest.fixture(scope="class")
    def sample_dataset_without_name(self, sample_eis_dataset: TDatasetEssentials):
        """Fixture: EIS measurement without name"""
        sample_eis_dataset.measured.start_time = None  # type : ignore
        return sample_eis_dataset

    @pytest.mark.run(order=28)
    def test_create_dataset_missing_required_field_start_time(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_dataset_without_name: TDatasetEssentials,
    ):
        """Check if attempt to create a EIS measurement without name raises an error."""
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_dataset(sample_dataset_without_name)

        assert '{"error":"Failed to validate dataset","details":' in str(excinfo.value)

    @pytest.mark.run(order=29)
    def test_get_dataset(
        self, ada_logged_client: NovumAPIClient, created_eis_dataset: TDatasetEssentials
    ):
        """Check created EIS measurement."""
        response = ada_logged_client.get_datasets()

        assert response[0].id == created_eis_dataset.id

    @pytest.mark.run(order=30)
    def test_get_dataset_with_fields(
        self, ada_logged_client: NovumAPIClient, created_eis_dataset: TDatasetEssentials
    ):
        """Check created EIS measurement with fields."""
        fields = {"context_id": 1}
        response = ada_logged_client.get_datasets(fields=fields)

        assert response[0].id == created_eis_dataset.id
        assert response[0].context_id == created_eis_dataset.context_id
        assert response[0].show_in_chart is None

    @pytest.mark.run(order=31)
    def test_get_dataset_without_fields(
        self, ada_logged_client: NovumAPIClient, created_eis_dataset: TDatasetEssentials
    ):
        """Check created EIS measurement without fields."""
        fields = {"context_id": 0}
        response = ada_logged_client.get_datasets(fields=fields)

        assert response[0].id == created_eis_dataset.id
        assert response[0].context_id is None
        assert response[0].show_in_chart is None

    @pytest.mark.run(order=31)
    def test_get_datasets_count(self, ada_logged_client: NovumAPIClient):
        """Check amount of EIS measurements."""
        response = ada_logged_client.get_datasets_count()

        assert response == 1

    @pytest.mark.run(order=32)
    def test_get_dataset_by_id(
        self, ada_logged_client: NovumAPIClient, created_eis_dataset: TDatasetEssentials
    ):
        """Check created dataset by id."""
        response = ada_logged_client.get_dataset_by_id(created_eis_dataset.id)

        assert response.id == created_eis_dataset.id

    @pytest.mark.run(order=33)
    def test_update_dataset(
        self, ada_logged_client: NovumAPIClient, created_eis_dataset: TDatasetEssentials
    ):
        """Check EIS measurement update."""
        response = ada_logged_client.get_dataset_by_id(created_eis_dataset.id)
        response.context_id = "new_context_id"
        ada_logged_client.update_dataset_by_id(created_eis_dataset.id, response)
        response_updated = ada_logged_client.get_dataset_by_id(created_eis_dataset.id)

        assert response_updated.context_id == "new_context_id"

    @pytest.mark.run(order=34)
    def test_delete_dataset(
        self, ada_logged_client: NovumAPIClient, sample_eis_dataset: TDatasetEssentials
    ):
        """Check EIS measurement deletion."""
        to_be_deleted_sample = sample_eis_dataset
        to_be_deleted_sample.measured.start_time = datetime(2023, 11, 10, 5, 5, 6)
        to_be_deleted = ada_logged_client.create_dataset(to_be_deleted_sample)

        response = ada_logged_client.remove_dataset_by_id(to_be_deleted.id)

        assert "was removed" in response

    # ********************************************************
    # Section for the Capacity Measurement
    # ********************************************************
    @pytest.fixture(scope="class")
    def sample_capacity_measurement(self):
        """Fixture: sample capacity measurement."""
        sample_capacity = TCapacityMeasurementEssentials(
            start_time=datetime(2023, 11, 10, 5, 5, 5),
            end_time=None,
            current_setpoint=1,
            voltage_setpoint=2,
            charge_type=TChargeTypes.CC,
            charge_cycles=[
                TChargeCycle(
                    timestamp=datetime(2023, 11, 10, 5, 5, 5),
                    voltage=3,
                    current=1,
                    charge=1,
                )
            ],
            tags=["test0 only test"],
            ambient_temperature=22.3,
            device_name="NOVUM Testing Device",
            device_info="Firmware: v1.02",
            voltage_min=2.14,
            voltage_max=3.14,
            state_of_health=0.94,
            grade="D",
        )
        return sample_capacity

    @pytest.fixture(scope="class")
    def created_capacity_measurement(
        self,
        ada_logged_client: NovumAPIClient,
        sample_capacity_measurement: TCapacityMeasurementEssentials,
    ):
        """Fixture: capacity measurement creation."""

        response = ada_logged_client.create_capacity_measurement(
            sample_capacity_measurement
        )

        yield response

        # Add cleanup code here to delete the created battery type
        ada_logged_client.remove_capacity_measurement_by_id(response.id)

    @pytest.mark.run(order=35)
    def test_create_capacity_measurement(
        self, created_capacity_measurement: TCapacityMeasurementEssentials
    ):
        """Check capacity measurement creation."""

        assert created_capacity_measurement.current_setpoint == 1

    @pytest.fixture(scope="class")
    def sample_capacity_measurement_without_start_time(
        self, sample_capacity_measurement: TCapacityMeasurementEssentials
    ):
        """Fixture: sample of capacity measurement without start time."""
        sample_capacity_measurement.start_time = None  # type: ignore
        return sample_capacity_measurement

    @pytest.mark.run(order=36)
    def test_create_capacity_measurement_missing_required_field_start_time(
        self,
        ada_logged_client: NovumAPIClient,
        sample_capacity_measurement_without_start_time: TCapacityMeasurementEssentials,
    ):
        """Check if attempt to create a capacity measurement without start time raises an error."""
        with pytest.raises(NovumAPIError) as excinfo:
            ada_logged_client.create_capacity_measurement(
                sample_capacity_measurement_without_start_time
            )

        assert '{"error":"Failed to validate capacity measurement",' in str(
            excinfo.value
        )

    @pytest.mark.run(order=37)
    def test_get_capacity_measurements(
        self,
        ada_logged_client: NovumAPIClient,
        created_capacity_measurement: TCapacityMeasurementEssentials,
    ):
        """Check capacity measurements fetching."""
        response = ada_logged_client.get_capacity_measurements()

        assert response[0].id == created_capacity_measurement.id

    @pytest.mark.run(order=38)
    def test_get_capacity_measurements_with_fields(
        self,
        ada_logged_client: NovumAPIClient,
        created_capacity_measurement: TCapacityMeasurementEssentials,
    ):
        """Check capacity measurements fetching with fields."""
        fields = {"device_name": 1}
        response = ada_logged_client.get_capacity_measurements(fields=fields)

        assert response[0].id == created_capacity_measurement.id
        assert response[0].device_name == created_capacity_measurement.device_name
        assert response[0].grade is None

    @pytest.mark.run(order=39)
    def test_get_capacity_measurements_without_fields(
        self,
        ada_logged_client: NovumAPIClient,
        created_capacity_measurement: TCapacityMeasurementEssentials,
    ):
        """Check capacity measurements fetching without fields."""
        fields = {"device_name": 0}
        response = ada_logged_client.get_capacity_measurements(fields=fields)

        assert response[0].id == created_capacity_measurement.id
        assert response[0].device_name is None

    @pytest.mark.run(order=40)
    def test_get_capacity_measurements_count(self, ada_logged_client: NovumAPIClient):
        """Check created capacity measurement."""
        response = ada_logged_client.get_capacity_measurements_count()

        assert response == 1

    @pytest.mark.run(order=41)
    def test_get_capacity_measurement_by_id(
        self,
        ada_logged_client: NovumAPIClient,
        created_capacity_measurement: TCapacityMeasurementEssentials,
    ):
        """Check created capacity measurement by id."""
        response = ada_logged_client.get_capacity_measurement_by_id(
            created_capacity_measurement.id
        )

        assert response.id == created_capacity_measurement.id

    @pytest.mark.run(order=42)
    def test_update_capacity_measurement(
        self,
        ada_logged_client: NovumAPIClient,
        created_capacity_measurement: TCapacityMeasurementEssentials,
    ):
        """Check capacity measurement updating."""
        response = ada_logged_client.get_capacity_measurement_by_id(
            created_capacity_measurement.id
        )
        response.context_id = "new_context_id"
        ada_logged_client.update_capacity_measurement_by_id(
            created_capacity_measurement.id, response
        )
        response_updated = ada_logged_client.get_capacity_measurement_by_id(
            created_capacity_measurement.id
        )

        assert response_updated.context_id == "new_context_id"

    @pytest.mark.run(order=43)
    def test_delete_capacity_measurement(
        self,
        ada_logged_client: NovumAPIClient,
        sample_capacity_measurement: TCapacityMeasurementEssentials,
    ):

        """Check capacity measurement deletion."""
        to_be_deleted_sample = sample_capacity_measurement
        to_be_deleted_sample.start_time = datetime(2023, 11, 10, 5, 5, 6)
        to_be_deleted = ada_logged_client.create_capacity_measurement(
            to_be_deleted_sample
        )

        response = ada_logged_client.remove_capacity_measurement_by_id(to_be_deleted.id)

        assert "was removed" in response

    # ********************************************************
    # Section for Reports
    # ********************************************************

    @pytest.fixture
    def sample_report(self):
        return TReportEssentials(
            state=ReportStates.Unread,
            origin_id="test_report_origin_id",
            title="test_report_title",
            description="test_report_description",
            meta={},
            context_id="test_report_context_id",
            user_doc_ids=["test_report_doc_id"],
        )

    @pytest.fixture
    def created_report(
        self,
        ada_logged_client: NovumAPIClient,
        sample_report: TReportEssentials,
    ):

        response = ada_logged_client.create_report(sample_report)

        yield response

        # Add cleanup code here to delete the created battery type
        ada_logged_client.remove_report_by_id(response.id)

    @pytest.mark.run(order=44)
    def test_create_report(self, created_report: TReport):
        assert created_report.origin_id == "test_report_origin_id"
        assert created_report.title == "test_report_title"
        assert created_report.description == "test_report_description"
        assert created_report.context_id == "test_report_context_id"

    @pytest.fixture
    def sample_report_without_title(self, sample_report: TReportEssentials):
        sample_report.title = None  # type: ignore
        return sample_report

    @pytest.mark.run(order=45)
    def test_create_report_missing_required_field_title(
        self,
        unauthenticated_api_client: NovumAPIClient,
        sample_report_without_title: TReportEssentials,
    ):
        with pytest.raises(NovumAPIError) as excinfo:
            unauthenticated_api_client.create_report(sample_report_without_title)

        assert '{"error":"Failed to validate report data","details":"Key:' in str(
            excinfo.value
        )

    @pytest.mark.run(order=46)
    def test_get_reports(
        self,
        ada_logged_client: NovumAPIClient,
        created_report: TReport,
    ):
        response = ada_logged_client.get_reports()

        assert response[0].id == created_report.id

    @pytest.mark.run(order=47)
    def test_get_reports_count(self, ada_logged_client: NovumAPIClient):
        response = ada_logged_client.get_reports_count()

        assert response == 0

    @pytest.mark.run(order=48)
    def test_get_report_by_id(
        self,
        ada_logged_client: NovumAPIClient,
        created_report: TReport,
    ):
        response = ada_logged_client.get_report_by_id(created_report.id)

        assert response.id == created_report.id

    @pytest.mark.run(order=49)
    def test_update_report_by_id(
        self,
        ada_logged_client: NovumAPIClient,
        created_report: TReport,
    ):
        created_report.context_id = "new_context_id"
        ada_logged_client.update_report_by_id(created_report.id, created_report)
        response_updated = ada_logged_client.get_report_by_id(created_report.id)

        assert response_updated.context_id == "new_context_id"

    @pytest.mark.run(order=50)
    def test_delete_report_by_id(
        self,
        ada_logged_client: NovumAPIClient,
        sample_report: TReportEssentials,
    ):
        created_report = ada_logged_client.create_report(sample_report)
        response = ada_logged_client.remove_report_by_id(created_report.id)

        assert "was removed" in response

    #####  No test available because we dont have an delete function for this section

    # ********************************************************
    # Section for the Measurement
    # ********************************************************

    # @pytest.fixture
    # def sample_live_data(self, sample_battery :TBattery):
    #     uit_measurement = UITMeasurement(
    #     time=datetime.now(),
    #     voltage=3.5,
    #     current=1.2,
    #     temperature=25.0,
    #     charge=None,
    #     soc=75.0
    #     )

    #     device_measurement = TDeviceMeasurement(
    #         device_id=sample_battery.id,
    #         measurements=[uit_measurement]
    #     )

    #     # Creating a DeviceMeasurements variable
    #     device_measurements = [device_measurement]

    #     return device_measurements

    # @pytest.fixture
    # def created_live_data(
    #     self, ada_logged_client: NovumAPIClient, sample_live_data:List[TDeviceMeasurement]
    # ):

    #     response = ada_logged_client.write_device_measurements(
    #         sample_live_data
    #     )

    #     yield response

    #     # Add cleanup code here to delete the created battery type
    #     ada_logged_client.remove_______________by_id(response.id)


if __name__ == "__main__":
    pytest.main()
