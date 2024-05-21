# pylint: disable=C0103
# flake8: noqa
import json
from dataclasses import dataclass
from typing import Optional, Union, List
import warnings
import requests
from .base_client import BaseAPIClient, NovumAPIError
from .api_type import (
    TUser,
    TReport,
    TVersion,
    TUserDocument,
    TBatteryReading,
    TDatasetReading,
    TDeviceMeasurement,
    TReportEssentials,
    TAPIInfoEssentials,
    TDatasetEssentials,
    TBatteryEssentials,
    TBatteryTypeReading,
    TBatteryTypeEssentials,
    TDeviceMeasurementsResult,
    TCapacityMeasurementReading,
    TCapacityMeasurementEssentials,
)


@dataclass
class NovumAPIClient(BaseAPIClient):
    """NovumAPIClient class"""

    def __init__(
        self,
        user=None,
        host=None,
        check_ssl_certification=None,
        refresh_token_warning=None,
        refresh_interval_scale=None,
        _relogin_timer_handle=None,
        _authenticated=None,
    ):
        super().__init__(
            user=user if user is not None else self.user,
            host=host if host is not None else self.host,
            check_ssl_certification=check_ssl_certification
            if check_ssl_certification is not None
            else self.check_ssl_certification,
            refresh_token_warning=refresh_token_warning
            if refresh_token_warning is not None
            else self.refresh_token_warning,
            refresh_interval_scale=refresh_interval_scale
            if refresh_interval_scale is not None
            else self.refresh_interval_scale,
            _relogin_timer_handle=_relogin_timer_handle
            if _relogin_timer_handle is not None
            else self._relogin_timer_handle,
            _authenticated=_authenticated
            if _authenticated is not None
            else self._authenticated,
        )

    # ********************************************************
    # Section for the Service Center info
    # ********************************************************

    def ping(self) -> dict:
        """Ping API."""
        return self._get_json("/api/batman/v1/")

    def get_info(self) -> TAPIInfoEssentials:
        """Get info."""
        info = self._get_json("/api/batman/v1/info")
        return TAPIInfoEssentials(**info)

    def get_version(self) -> TVersion:
        """Check version."""
        version = self._get_json("/api/batman/v1/version")
        return TVersion(**version)

    # ********************************************************
    # Section for the users
    # ********************************************************

    def login(
        self, email: str, password: str, store_user=True, timeout: float = 4
    ) -> Union[TUser, None]:
        """Login function"""
        header = {"authorization": "auth", "content-type": "application/json"}
        payload = {"username": email, "password": password}
        response = requests.post(
            self.host + "/api/batman/v1/login",
            data=json.dumps(payload),
            headers=header,
            timeout=timeout,
            verify=self.check_ssl_certification,
        )
        if response.status_code == requests.codes.get("ok"):
            if store_user is True:
                user = response.json()
                self.user = TUser(**user)
                self._install_token_refresh_procedure()
                self.headers = dict(
                    {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + str(self.user.jwt),
                    }
                )

            return self.user

        raise NovumAPIError(response.text, response.status_code)

    def logout(self):
        """Log out."""
        return self._get_json("/api/batman/v1/logout")

    def check_current_user_still_authenticated(self) -> dict:
        """Check authentication."""

        return self._get_json("/api/batman/v1/check_token")

    # ********************************************************
    # Section for the Battery Types
    # ********************************************************

    def get_battery_types(
        self,
        filter_types: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBatteryTypeReading]:
        """Get battery types."""
        battery_types_list = self._get_json(
            "/api/batman/v1/batteryTypes",
            filter_json=filter_types,
            option=option,
            fields=fields,
            timeout=timeout,
        )

        battery_types = [
            TBatteryTypeReading(**battery_type) for battery_type in battery_types_list
        ]

        return battery_types

    def get_battery_types_count(
        self,
        filter_types: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> dict:
        """Get amount of battery types."""
        return self._get_json(
            "/api/batman/v1/batteryTypes/count",
            filter_json=filter_types,
            option=option,
            fields=fields,
            timeout=timeout,
        )  # type: ignore

    def get_battery_types_by_id(
        self, battery_type_id: str, timeout: float = 4.0
    ) -> TBatteryTypeReading:
        """Get battery type by id."""
        battery_type = self._get_json(
            f"/api/batman/v1/batteryTypes/{battery_type_id}", timeout=timeout
        )
        return TBatteryTypeReading(**battery_type)

    def remove_battery_types_by_id(self, battery_type_id: str, timeout: float = 4.0):
        """Delete battery type by id."""
        self._delete_json(
            f"/api/batman/v1/batteryTypes/{battery_type_id}", timeout=timeout
        )
        return "The battery type was removed."

    def create_battery_type(
        self,
        battery_type: TBatteryTypeEssentials,
        timeout: float = 4.0,
    ) -> TBatteryTypeEssentials:
        """Create battery type."""
        created_battery_type = self._post_json(
            "/api/batman/v1/batteryTypes", input_data=battery_type, timeout=timeout
        )
        return TBatteryTypeEssentials(**created_battery_type)

    def update_battery_type_by_id(
        self,
        battery_type_id: str,
        battery_type_update: TBatteryTypeReading,
        timeout: float = 4.0,
    ) -> TBatteryTypeEssentials:
        """Update battery type by id."""
        updated_battery_type = self._put_json(
            f"/api/batman/v1/batteryTypes/{battery_type_id}",
            input_data=battery_type_update,
            timeout=timeout,
        )
        return TBatteryTypeEssentials(**updated_battery_type)

    # ********************************************************
    # Section for the Datasets
    # ********************************************************

    def dataset_exists_on_remote(self, dataset_id: str, timeout: float = 4.0) -> bool:
        """Check remote data."""
        response = self._get_json(
            f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout
        )
        try:
            if len(response["measured"]["measurement_cycles"]) != 0:
                return True
            return False
        except KeyError:
            return False

    def create_dataset(
        self, dataset: TDatasetEssentials, timeout: float = 4.0
    ) -> TDatasetEssentials:
        """Create EIS measurement."""
        created_dataset = self._post_json(
            "/api/batman/v1/datasets", input_data=dataset, timeout=timeout
        )
        return TDatasetEssentials(**created_dataset)

    def get_dataset_by_id(
        self, dataset_id: str, timeout: float = 4.0
    ) -> TDatasetReading:
        """Get EIS measurement by id."""
        dataset = self._get_json(
            f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout
        )
        return TDatasetReading(**dataset)

    def get_datasets(
        self,
        filter_datasets: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TDatasetReading]:
        """Get EIS measurements."""
        dataset_list = self._get_json(
            "/api/batman/v1/datasets",
            filter_json=filter_datasets,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        datasets = [TDatasetReading(**dataset) for dataset in dataset_list]

        return datasets

    def get_datasets_count(
        self,
        filter_datasets: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> int:
        """Get amount of EIS measurements."""
        return self._get_json(
            "/api/batman/v1/datasets/count",
            filter_json=filter_datasets,
            option=option,
            fields=fields,
            timeout=timeout,
        )  # type: ignore

    def get_datasets_count_by_battery(
        self,
        battery: TBatteryReading,
        filter_datasets: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> int:
        """Get amount of EIS measurements by battery."""
        filter_with_id = {"meta.battery._id": battery.id}
        if filter_datasets is not None:
            filter_with_id.update(filter_datasets)
        response = self._get_json(
            "/api/batman/v1/datasets/count",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        return response  # type: ignore

    def update_dataset_by_id(
        self, dataset_id: str, dataset: TDatasetReading, timeout: float = 4.0
    ) -> TDatasetEssentials:
        """Update EIS measurement by id."""
        updated_dataset = self._put_json(
            f"/api/batman/v1/datasets/{dataset_id}",
            input_data=dataset,
            timeout=timeout,
        )
        return TDatasetEssentials(**updated_dataset)

    def remove_dataset_by_id(self, dataset_id: str, timeout: float = 4.0):
        """Delete EIS measurement by id."""
        self._delete_json(f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout)
        return "The data set was removed."

    # ********************************************************
    # Section for the Battery
    # ********************************************************

    def create_battery(
        self, battery: TBatteryEssentials, timeout: float = 4.0
    ) -> TBatteryEssentials:
        """Create a battery."""
        created_battery = self._post_json(
            "/api/batman/v1/batteries", input_data=battery, timeout=timeout
        )
        return TBatteryEssentials(**created_battery)

    def get_battery_by_id(
        self, battery_id: str, timeout: float = 4.0
    ) -> TBatteryReading:
        """Get battery by id."""
        battery = self._get_json(
            f"/api/batman/v1/batteries/{battery_id}", timeout=timeout
        )

        return TBatteryReading(**battery)

    def update_battery(
        self, battery: TBatteryReading, timeout: float = 4.0
    ) -> TBatteryEssentials:
        """Update a battery."""
        updated_battery = self._put_json(
            f"/api/batman/v1/batteries/{battery.id}",
            input_data=battery,
            timeout=timeout,
        )

        return TBatteryEssentials(**updated_battery)

    def update_battery_by_id(
        self, battery_id: str, battery_update: TBatteryReading, timeout: float = 4.0
    ) -> TBatteryEssentials:
        """Update a battery by id."""
        updated_battery = self._put_json(
            f"/api/batman/v1/batteries/{battery_id}",
            input_data=battery_update,
            timeout=timeout,
        )
        return TBatteryEssentials(**updated_battery)

    def remove_battery_by_id(self, battery_id: str, timeout: float = 4.0) -> str:
        """Delete a battery by id."""
        self._delete_json(f"/api/batman/v1/batteries/{battery_id}", timeout=timeout)
        return "The battery was removed."

    def get_batteries(
        self,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBatteryReading]:
        """Get batteries."""
        battery_list = self._get_json(
            "/api/batman/v1/batteries",
            filter_json=filter_batteries,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBatteryReading(**battery) for battery in battery_list]

        return batteries

    def get_batteries_count(
        self,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> int:
        """Get amount of batteries."""
        return self._get_json(
            "/api/batman/v1/batteries/count",
            filter_json=filter_batteries,
            option=option,
            fields=fields,
            timeout=timeout,
        )  # type: ignore

    def get_children_of_battery_by_id(
        self,
        parent_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBatteryReading]:
        """Get children of a battery using the id."""
        filter_with_id = {"tree.parent": parent_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBatteryReading(**battery) for battery in battery_list]

        return batteries

    def get_children_of_battery_by_id_count(
        self,
        parent_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> int:
        """Get amount of children by battery id."""
        filter_with_id = {"tree.parent": parent_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        response = self._get_json(
            "/api/batman/v1/batteries/count",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        return response  # type: ignore

    def get_leaves_of_battery_by_id(
        self,
        ancestor_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBatteryReading]:
        """Get all leaves of a tree of battery."""
        filter_with_id = {"tree.is_leaf": True, "tree.ancestors": ancestor_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBatteryReading(**battery) for battery in battery_list]
        return batteries

    def get_leaves_of_battery_by_id_count(
        self,
        ancestor_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBatteryReading]:
        """Get amount of leaves of a level top(accordingly on a tree) battery."""
        filter_with_id = {"tree.is_leaf": True, "tree.ancestors": ancestor_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries/count",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBatteryReading(**battery) for battery in battery_list]
        return batteries

    def get_descendants_of_battery_by_id(
        self,
        ancestor_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBatteryReading]:
        """Get all descendants on the tree by battery id."""
        filter_with_id = {"tree.ancestors": ancestor_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBatteryReading(**battery) for battery in battery_list]
        return batteries

    def get_descendants_of_battery_by_id_count(
        self,
        ancestor_battery_id: str,
        filter_batteries: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TBatteryReading]:
        """Get amount of descendants on the tree by battery id."""
        filter_with_id = {"tree.ancestors": ancestor_battery_id}
        if filter_batteries is not None:
            filter_with_id.update(filter_batteries)
        battery_list = self._get_json(
            "/api/batman/v1/batteries/count",
            filter_json=filter_with_id,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        batteries = [TBatteryReading(**battery) for battery in battery_list]
        return batteries

    # ********************************************************
    # Section for the CapacityMeasurement
    # ********************************************************

    def create_capacity_measurement(
        self, capacity_measurement: TCapacityMeasurementEssentials, timeout: float = 4.0
    ) -> TCapacityMeasurementEssentials:
        """Create a capacity measurement."""
        response = self._post_json(
            "/api/batman/v1/capacityMeasurements",
            input_data=capacity_measurement,
            timeout=timeout,
        )

        return TCapacityMeasurementEssentials(**response)

    def update_capacity_measurement_by_id(
        self,
        capacity_measurement_id: str,
        capacity_measurement: TCapacityMeasurementReading,
        timeout: float = 4.0,
    ) -> TCapacityMeasurementEssentials:
        """Update a capacity measurement by id."""
        updated_capacity_measurement = self._put_json(
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            input_data=capacity_measurement,
            timeout=timeout,
        )
        return TCapacityMeasurementEssentials(**updated_capacity_measurement)

    def remove_capacity_measurement_by_id(
        self, capacity_measurement_id: str, timeout: float = 4.0
    ):
        """Delete capacity measurement by id."""
        self._delete_json(
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            timeout=timeout,
        )
        return "Capacity measurement was removed."

    def get_capacity_measurement(
        self,
        filter_measurements: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TCapacityMeasurementReading]:
        """Get capacity measurements (deprecated)."""
        warnings.warn(
            "Function get_capacity_measurement is deprecated, use get_capacity_measurements instead.",
            DeprecationWarning,
        )

        capacity_measurements = self.get_capacity_measurements(
            filter_measurements=filter_measurements,
            option=option,
            fields=fields,
            timeout=timeout,
        )

        return capacity_measurements

    def get_capacity_measurements(
        self,
        filter_measurements: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TCapacityMeasurementReading]:
        """Get capacity measurements."""
        capacity_measurement_list = self._get_json(
            "/api/batman/v1/capacityMeasurements",
            filter_json=filter_measurements,
            option=option,
            fields=fields,
            timeout=timeout,
        )

        capacity_measurements = [
            TCapacityMeasurementReading(**capa) for capa in capacity_measurement_list
        ]

        return capacity_measurements

    def get_capacity_measurement_count(
        self,
        filter_measurements: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> int:
        """Get amount of capacity measurements (deprecated)."""
        warnings.warn(
            "Function get_capacity_measurement_count is deprecated, use get_capacity_measurements_count instead.",
            DeprecationWarning,
        )
        capacity_measurements_count = self.get_capacity_measurement_count(
            filter_measurements=filter_measurements,
            option=option,
            fields=fields,
            timeout=timeout,
        )

        return capacity_measurements_count

    def get_capacity_measurements_count(
        self,
        filter_measurements: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> int:
        """Get amount of capacity measurements."""
        response = self._get_json(
            "/api/batman/v1/capacityMeasurements/count",
            filter_json=filter_measurements,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        return response  # type: ignore

    def get_capacity_measurement_by_id(
        self, capacity_measurement_id: str, timeout: float = 4.0
    ) -> TCapacityMeasurementEssentials:
        """Get capacity measurement by id."""
        capacity_measurement = self._get_json(
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            timeout=timeout,
        )
        return TCapacityMeasurementEssentials(**capacity_measurement)

    def get_capacity_measurements_count_by_battery(
        self, battery_id: str, timeout: float = 4.0
    ) -> int:
        """Get amount of capacity measurement per battery using battery id."""
        filter_by_id = {"battery._id": battery_id}
        response = self._get_json(
            "/api/batman/v1/capacityMeasurements/count",
            filter_json=filter_by_id,
            timeout=timeout,
        )
        return response  # type: ignore

    def capacity_measurement_exists_on_remote(
        self, capacity_measurement_id: str, timeout: float = 4.0
    ) -> bool:
        """Check capacity measurement on remote."""
        response = self._get_json(
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            timeout=timeout,
        )
        return response["id"] == capacity_measurement_id

    # ********************************************************
    # Section for the Measurements
    # ********************************************************

    def get_latests_measurements(
        self, device_id: str, count: int = 1, timeout: float = 4.0
    ) -> TDeviceMeasurementsResult:
        """Get latest live measurement."""
        measurements_list = self._get_json(
            f"/api/time-series/v1/devices/{device_id}/measurements/last/{count}",
            timeout=timeout,
        )

        return measurements_list  # type: ignore

    def write_device_measurements(
        self, device_measurements: List[TDeviceMeasurement], timeout: float = 4.0
    ) -> TDeviceMeasurementsResult:
        """Write time series live measurement."""
        write_measurement = self._post_json(
            "/api/time-series/v1/measurements",
            input_data=device_measurements,
            timeout=timeout,
        )
        return write_measurement  # type: ignore

    def read_device_measurements(
        self,
        device_filter: Optional[dict],
        option=None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> TDeviceMeasurementsResult:
        """Get time series live measurement."""
        read_measurements = self._get_json(
            "/api/time-series/v1/measurements",
            filter_json=device_filter,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        return read_measurements  # type: ignore

    def read_device_measurements_by_id(
        self,
        battery_id,
        device_filter: Optional[dict],
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> TDeviceMeasurementsResult:
        """Get time series live measurement by battery id."""
        read_measurements_by_battery_id = self._get_json(
            f"/api/time-series/v1/measurements/{battery_id}",
            filter_json=device_filter,
            fields=fields,
            timeout=timeout,
        )
        return read_measurements_by_battery_id  # type: ignore

    # ********************************************************
    # Section for the Reports
    # ********************************************************

    def create_report(self, report: TReportEssentials, timeout: float = 4.0) -> TReport:
        """Create report."""
        report_post = self._post_json("/api/batman/v1/reports", report, timeout=timeout)
        return TReport(**report_post)

    def update_report_by_id(
        self, report_id: str, report: TReportEssentials, timeout: float = 4
    ) -> TReport:
        """Update report by id."""
        update_report = self._put_json(
            f"/api/batman/v1/reports/{report_id}", report, timeout=timeout
        )
        return TReport(**update_report)

    def get_reports(
        self,
        report_filter: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4,
    ) -> List[TReport]:
        """Get reports."""
        report_list = self._get_json(
            "/api/batman/v1/reports",
            filter_json=report_filter,
            fields=fields,
            option=option,
            timeout=timeout,
        )
        reports = [TReport(**report) for report in report_list]
        return reports

    def get_reports_count(
        self,
        report_filter: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4,
    ) -> int:
        """Get amount of reports."""
        response = self._get_json(
            "/api/batman/v1/reports/count",
            report_filter,
            option=option,
            fields=fields,
            timeout=timeout,
        )
        return response  # type: ignore

    def get_reports_count_by_battery(
        self, battery: TBatteryReading, timeout: float = 4
    ) -> int:
        """Get amount of reports by battery."""
        response = self._get_json(
            "/api/batman/v1/reports/count",
            filter_json={"origin_id": battery.id},
            timeout=timeout,
        )

        return response  # type: ignore

    def get_report_by_id(self, report_id: str, timeout: float = 4) -> TReport:
        """Get reports by id."""
        report = self._get_json(f"/api/batman/v1/reports/{report_id}", timeout=timeout)
        return TReport(**report)

    def get_reports_by_origin_id(
        self,
        origin_id: str,
        report_filter: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4,
    ) -> List[TReport]:
        """Get reports by origin id."""
        report_list = self._get_json(
            f"/api/batman/v1/reports/byOriginId/{origin_id}",
            report_filter,
            option=option,
            fields=fields,
            timeout=timeout,
        )

        reports = [TReport(**report) for report in report_list]

        return reports

    def get_reports_by_origin_id_count(
        self,
        origin_id: str,
        report_filter: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4,
    ) -> int:
        """Get amount of reports by origin id."""
        reports_count = self._get_json(
            f"/api/batman/v1/reports/byOriginId/{origin_id}/count",
            report_filter,
            option,
            fields=fields,
            timeout=timeout,
        )
        return reports_count  # type: ignore

    def remove_report_by_id(
        self, report_id: str, report_filter=None, option=None, timeout: float = 4
    ):
        """Delete reports by id."""
        self._delete_json(
            f"/api/batman/v1/reports/{report_id}",
            filter_json=report_filter,
            option=option,
            timeout=timeout,
        )
        return "The report was removed."

    # ********************************************************
    # Section for the userDocs
    # ********************************************************

    def get_user_documents(
        self,
        document_filter: Optional[dict] = None,
        option: Optional[dict] = None,
        fields: Optional[dict] = None,
        timeout: float = 4.0,
    ) -> List[TUserDocument]:
        """Gest user documents"""
        user_documents_list = self._get_json(
            "/api/batman/v1/userDocuments",
            filter_json=document_filter,
            option=option,
            fields=fields,
            timeout=timeout,
        )

        user_documents = [TUserDocument(**document) for document in user_documents_list]

        return user_documents

    def get_user_document_by_id(self, user_document_id: str) -> TUserDocument:
        """Get user document by document id."""
        document = self._get_json(f"/api/batman/v1/userDocuments/{user_document_id}")

        return TUserDocument(**document)
