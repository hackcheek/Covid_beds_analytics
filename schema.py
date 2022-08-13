import numpy as np

from dataclasses import dataclass


@dataclass(slots=True)
class DataSchema():
    state: str
    date: np.datetime64
    critical_staffing_shortage_today_yes: np.int32
    critical_staffing_shortage_today_no: np.int32
    critical_staffing_shortage_today_not_reported: np.int32
    critical_staffing_shortage_anticipated_within_week_yes: np.int32
    critical_staffing_shortage_anticipated_within_week_no: np.int32
    critical_staffing_shortage_anticipated_within_week_not_reported: np.int32
    hospital_onset_covid: np.int32
    hospital_onset_covid_coverage: np.int32
    inpatient_beds: np.int32
    inpatient_beds_coverage: np.int32
    inpatient_beds_used: np.int32
    inpatient_beds_used_coverage: np.int32
    inpatient_beds_used_covid: np.int32
    inpatient_beds_used_covid_coverage: np.int32
    previous_day_admission_adult_covid_confirmed: np.int32
    previous_day_admission_adult_covid_confirmed_coverage: np.int32
    previous_day_admission_adult_covid_suspected: np.int32
    previous_day_admission_adult_covid_suspected_coverage: np.int32
    previous_day_admission_pediatric_covid_confirmed: np.int32
    previous_day_admission_pediatric_covid_confirmed_coverage: np.int32
    previous_day_admission_pediatric_covid_suspected: np.int32
    previous_day_admission_pediatric_covid_suspected_coverage: np.int32
    staffed_adult_icu_bed_occupancy: np.int32
    staffed_adult_icu_bed_occupancy_coverage: np.int32
    staffed_icu_adult_patients_confirmed_and_suspected_covid: np.int32
    staffed_icu_adult_patients_confirmed_and_suspected_covid_coverage: np.int32
    staffed_icu_adult_patients_confirmed_covid: np.int32
    staffed_icu_adult_patients_confirmed_covid_coverage: np.int32
    total_adult_patients_hospitalized_confirmed_and_suspected_covid: np.int32
    total_adult_patients_hospitalized_confirmed_and_suspected_covid_coverage: np.int32
    total_adult_patients_hospitalized_confirmed_covid: np.int32
    total_adult_patients_hospitalized_confirmed_covid_coverage: np.int32
    total_pediatric_patients_hospitalized_confirmed_and_suspected_covid: np.int32
    total_pediatric_patients_hospitalized_confirmed_and_suspected_covid_coverage: np.int32
    total_pediatric_patients_hospitalized_confirmed_covid: np.int32
    total_pediatric_patients_hospitalized_confirmed_covid_coverage: np.int32
    total_staffed_adult_icu_beds: np.int32
    total_staffed_adult_icu_beds_coverage: np.int32
    inpatient_beds_utilization: np.float32
    inpatient_beds_utilization_coverage: np.int32
    inpatient_beds_utilization_numerator: np.int32
    inpatient_beds_utilization_denominator: np.int32
    percent_of_inpatients_with_covid: np.float32
    percent_of_inpatients_with_covid_coverage: np.int32
    percent_of_inpatients_with_covid_numerator: np.int32
    percent_of_inpatients_with_covid_denominator: np.int32
    inpatient_bed_covid_utilization: np.float32
    inpatient_bed_covid_utilization_coverage: np.int32
    inpatient_bed_covid_utilization_numerator: np.int32
    inpatient_bed_covid_utilization_denominator: np.int32
    adult_icu_bed_covid_utilization: np.int32
    adult_icu_bed_covid_utilization_coverage: np.int32
    adult_icu_bed_covid_utilization_numerator: np.int32
    adult_icu_bed_covid_utilization_denominator: np.int32
    adult_icu_bed_utilization: np.float32
    adult_icu_bed_utilization_coverage: np.int32
    adult_icu_bed_utilization_numerator: np.int32
    adult_icu_bed_utilization_denominator: np.int32
    previous_day_admission_adult_covid_confirmed_18_19: np.int32
    previous_day_admission_adult_covid_confirmed_18_19_coverage: np.int32
    previous_day_admission_adult_covid_confirmed_20_29: np.int32
    previous_day_admission_adult_covid_confirmed_20_29_coverage: np.int32
    previous_day_admission_adult_covid_confirmed_30_39: np.int32
    previous_day_admission_adult_covid_confirmed_30_39_coverage: np.int32
    previous_day_admission_adult_covid_confirmed_40_49: np.int32
    previous_day_admission_adult_covid_confirmed_40_49_coverage: np.int32
    previous_day_admission_adult_covid_confirmed_50_59: np.int32
    previous_day_admission_adult_covid_confirmed_50_59_coverage: np.int32
    previous_day_admission_adult_covid_confirmed_60_69: np.int32
    previous_day_admission_adult_covid_confirmed_60_69_coverage: np.int32
    previous_day_admission_adult_covid_confirmed_70_79: np.int32
    previous_day_admission_adult_covid_confirmed_70_79_coverage: np.int32
    previous_day_admission_adult_covid_confirmed_80_plus: np.int32
    previous_day_admission_adult_covid_confirmed_80_plus_coverage: np.int32
    previous_day_admission_adult_covid_confirmed_unknown: np.int32
    previous_day_admission_adult_covid_confirmed_unknown_coverage: np.int32
    previous_day_admission_adult_covid_suspected_18_19: np.int32
    previous_day_admission_adult_covid_suspected_18_19_coverage: np.int32
    previous_day_admission_adult_covid_suspected_20_29: np.int32
    previous_day_admission_adult_covid_suspected_20_29_coverage: np.int32
    previous_day_admission_adult_covid_suspected_30_39: np.int32
    previous_day_admission_adult_covid_suspected_30_39_coverage: np.int32
    previous_day_admission_adult_covid_suspected_40_49: np.int32
    previous_day_admission_adult_covid_suspected_40_49_coverage: np.int32
    previous_day_admission_adult_covid_suspected_50_59: np.int32
    previous_day_admission_adult_covid_suspected_50_59_coverage: np.int32
    previous_day_admission_adult_covid_suspected_60_69: np.int32
    previous_day_admission_adult_covid_suspected_60_69_coverage: np.int32
    previous_day_admission_adult_covid_suspected_70_79: np.int32
    previous_day_admission_adult_covid_suspected_70_79_coverage: np.int32
    previous_day_admission_adult_covid_suspected_80_plus: np.int32
    previous_day_admission_adult_covid_suspected_80_plus_coverage: np.int32
    previous_day_admission_adult_covid_suspected_unknown: np.int32
    previous_day_admission_adult_covid_suspected_unknown_coverage: np.int32
    deaths_covid: np.int32
    deaths_covid_coverage: np.int32
    all_pediatric_inpatient_bed_occupied: np.int32
    all_pediatric_inpatient_bed_occupied_coverage: np.int32
    all_pediatric_inpatient_beds: np.int32
    all_pediatric_inpatient_beds_coverage: np.int32
    staffed_pediatric_icu_bed_occupancy: np.int32
    staffed_pediatric_icu_bed_occupancy_coverage: np.int32
    total_staffed_pediatric_icu_beds: np.int32
    total_staffed_pediatric_icu_beds_coverage: np.int32

    @classmethod
    def structured(cls: type):
        return StructType(
            [
                StructField(features, dtype(), False)
                for features, dtype in cls.__annotations__.items()
            ]
        )
