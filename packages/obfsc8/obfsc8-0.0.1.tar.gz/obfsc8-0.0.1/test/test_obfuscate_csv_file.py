import boto3
from moto import mock_aws
import polars as pl
import polars.testing as pt

from src.obfsc8.obfuscate_csv_file import obfuscate_csv_file
from src.obfsc8.get_file_object_from_s3_bucket \
    import get_file_object_from_s3_bucket
from test_data.test_dataframe import test_dataframe


@mock_aws
def test_that_csv_file_returned_is_not_equivalent_to_the_file_input():
    s3 = boto3.client('s3', region_name="eu-west-2")
    s3.create_bucket(Bucket="test_bucket",
                     CreateBucketConfiguration={
                            'LocationConstraint': "eu-west-2"
                     }
                     )

    test_csv_file_object = test_dataframe.write_csv()
    s3.put_object(
        Bucket="test_bucket",
        Key="test_csv.csv",
        Body=test_csv_file_object)

    csv_file_object_from_s3 = get_file_object_from_s3_bucket(
        bucket="test_bucket", key="test_csv.csv")
    columns_for_obfuscation = ["name", "email_address"]

    buffer = obfuscate_csv_file(
        csv_file_object_from_s3, columns_for_obfuscation, "***")
    obfuscated_dataframe = pl.read_csv(buffer)

    pt.assert_frame_not_equal(test_dataframe, obfuscated_dataframe)


@mock_aws
def test_that_all_values_in_non_target_columns_remain_unchanged():
    s3 = boto3.client('s3', region_name="eu-west-2")
    s3.create_bucket(Bucket="test_bucket",
                     CreateBucketConfiguration={
                            'LocationConstraint': "eu-west-2"
                     }
                     )

    test_csv_file_object = test_dataframe.write_csv()
    s3.put_object(
        Bucket="test_bucket",
        Key="test_csv.csv",
        Body=test_csv_file_object)

    csv_file_object_from_s3 = get_file_object_from_s3_bucket(
        bucket="test_bucket", key="test_csv.csv")
    columns_for_obfuscation = ["name", "email_address"]

    buffer = obfuscate_csv_file(
        csv_file_object_from_s3, columns_for_obfuscation, "***")
    obfuscated_dataframe = pl.read_csv(buffer)

    for column_name in obfuscated_dataframe.columns:
        if column_name not in columns_for_obfuscation:
            original_column_values = test_dataframe.get_column(column_name)
            obfuscated_column_values = (obfuscated_dataframe
                                        .get_column(column_name))

            (pt.assert_series_equal(original_column_values,
                                    obfuscated_column_values))


@mock_aws
def test_that_all_values_in_target_columns_made_equal_to_replacement_string():
    s3 = boto3.client('s3', region_name="eu-west-2")
    s3.create_bucket(Bucket="test_bucket",
                     CreateBucketConfiguration={
                            'LocationConstraint': "eu-west-2"
                     }
                     )

    test_csv_file_object = test_dataframe.write_csv()
    s3.put_object(
        Bucket="test_bucket",
        Key="test_csv.csv",
        Body=test_csv_file_object)

    csv_file_object_from_s3 = get_file_object_from_s3_bucket(
        bucket="test_bucket", key="test_csv.csv")
    columns_for_obfuscation = ["name", "email_address"]

    buffer = obfuscate_csv_file(
        csv_file_object_from_s3, columns_for_obfuscation, "***")
    obfuscated_dataframe = pl.read_csv(buffer)

    obfuscated_column_values_list = []
    for column_name in columns_for_obfuscation:
        obfuscated_column_values = (obfuscated_dataframe
                                    .get_column(column_name))
        obfuscated_column_values_list.append(obfuscated_column_values)

    for i in range(1, len(obfuscated_column_values_list)):
        (pt.assert_series_equal(obfuscated_column_values_list[0],
                                obfuscated_column_values_list[i],
                                check_names=False))
