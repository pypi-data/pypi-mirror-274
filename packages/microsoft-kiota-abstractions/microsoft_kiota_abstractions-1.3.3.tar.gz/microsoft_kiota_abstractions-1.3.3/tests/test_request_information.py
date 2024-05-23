from datetime import datetime
import uuid
import pytest
from dataclasses import dataclass
from typing import Optional
from unittest.mock import Mock

from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.headers_collection import HeadersCollection
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.method import Method


from .conftest import TestEnum, QueryParams



def test_initialization():
    """Tests initialization of the RequestInformation objects
    """
    request_info = RequestInformation()
    assert request_info
    assert not request_info.path_parameters
    assert not request_info.query_parameters
    assert not request_info.request_options
    assert not request_info.url_template
    assert not request_info.http_method
    assert not request_info.content
    assert request_info.headers
    assert request_info.RAW_URL_KEY == 'request-raw-url'
    assert request_info.BINARY_CONTENT_TYPE == 'application/octet-stream'
    assert request_info.CONTENT_TYPE_HEADER == 'Content-Type'


def test_add_request_headers(mock_request_information):
    """Tests adding a request header with a string value
    """
    headers = HeadersCollection()
    headers.add("header1", "value1")
    headers.add("header2", "value2")
    mock_request_information.headers.add_all(headers)
    assert {"value1"} <= mock_request_information.headers.get("header1")
    assert {"value2"} <= mock_request_information.headers.get("header2")
    header2 = HeadersCollection()
    header2.add("header1", "value3")
    mock_request_information.headers.add_all(header2)
    assert {"value1", "value3"} <= mock_request_information.headers.get("header1")


def test_request_headers(mock_request_information):
    """Test the final request headers
    """
    headers = HeadersCollection()
    headers.add("header1", ["value1", "value2"])
    headers.add("header2", ["value3", "value4"])
    mock_request_information.headers.add_all(headers)
    assert "value1" in mock_request_information.request_headers["header1"]
    assert "value2" in mock_request_information.request_headers["header1"]
    assert "value3" in mock_request_information.request_headers["header2"]
    assert "value4" in mock_request_information.request_headers["header2"]
    headers2 = HeadersCollection()
    headers2.add("header1", ["value1", "value2", "value5", "value6"])
    mock_request_information.headers.add_all(headers2)
    assert "value5" in mock_request_information.request_headers["header1"]
    assert "value6" in mock_request_information.request_headers["header1"]

    # Ensure duplicates are removed
    assert len(mock_request_information.request_headers["header1"]
               ) == len("value1, value2, value5, value6")
    assert len(mock_request_information.request_headers["header2"]) == len("value3, value4")
    assert "value1" in mock_request_information.request_headers["header1"]
    assert "value1" not in mock_request_information.request_headers["header2"]
    assert "value3" in mock_request_information.request_headers["header2"]
    assert "value4" in mock_request_information.request_headers["header2"]

def test_remove_request_headers(mock_request_information):
    """Tests removing a request header
    """
    headers = HeadersCollection()
    headers.add("header1", "value1")
    headers.add("header2", "value2")
    mock_request_information.headers.add_all(headers)
    assert mock_request_information.headers.get("header1") == {"value1"}
    assert mock_request_information.headers.get("header2") == {"value2"}
    mock_request_information.headers.remove("header1")
    mock_request_information.headers.remove("header3")
    assert 'header1' not in mock_request_information.request_headers
    assert mock_request_information.headers.try_get("header2") == {"value2"}


def test_set_stream_content(mock_request_information):
    """Tests setting the stream content
    """
    mock_request_information.set_stream_content(b'stream')
    assert mock_request_information.content == b'stream'
    assert mock_request_information.headers.get("content-type") == {"application/octet-stream"}
    
def test_configure_empty_configuration(mock_request_information):
    """Tests configuring the request information
    """
    request_config = RequestConfiguration()
    mock_request_information.configure(request_config)
    assert not mock_request_information.headers.get_all()
    assert not mock_request_information.request_options
    assert not mock_request_information.query_parameters
    
def test_configure_request_configuration(mock_request_information):
    """Tests configuring the request information
    """
    
    @dataclass
    class CustomParams:
        filter: Optional[str] = None
        
        def get_query_parameter(self,original_name: Optional[str] = None) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if not original_name:
                raise TypeError("original_name cannot be null.")
            if original_name == "filter":
                return "%24filter"
    
    query_params = CustomParams(filter="query1")
    headers = HeadersCollection()
    headers.add("header1", "value1")
    headers.add("header2", "value2")
    
    request_config = RequestConfiguration(headers=headers, query_parameters=query_params)

    mock_request_information.configure(request_config)
    assert mock_request_information.headers.get("header1") == {"value1"}
    assert mock_request_information.headers.get("header2") == {"value2"}
    assert mock_request_information.query_parameters == {"%24filter": "query1"}
    assert not mock_request_information.request_options
    
def test_sets_boundary_on_multipart_request_body(
    mock_request_information,
    mock_request_adapter,
    mock_multipart_body,
    mock_serialization_writer,
    mock_serialization_writer_factory
    ):
    """Tests setting the boundary on a multipart request
    """
    mock_request_information.http_method = Method.POST
    mock_serialization_writer_factory.get_serialization_writer = Mock(return_value=mock_serialization_writer)
    mock_request_adapter.get_serialization_writer_factory = Mock(return_value=mock_serialization_writer_factory)
    mock_multipart_body.request_adapter = mock_request_adapter
    mock_request_information.set_content_from_parsable(mock_request_adapter, "multipart/form-data", mock_multipart_body)
    assert mock_multipart_body.boundary
    assert mock_request_information.headers.get("content-type") == {"multipart/form-data; boundary=" + mock_multipart_body.boundary}


def test_sets_enum_value_in_query_parameters():
    """Tests setting enum values in query parameters
    """
    
    request_info = RequestInformation(Method.GET, "https://example.com/me{?dataset}")
    request_info.set_query_string_parameters_from_raw_object(QueryParams(TestEnum.VALUE1))
    assert request_info.url == "https://example.com/me?dataset=value1"
    
def test_sets_enum_values_in_query_parameters():
    """Tests setting enum values in query parameters
    """
    
    request_info = RequestInformation(Method.GET, "https://example.com/me{?dataset}")
    request_info.set_query_string_parameters_from_raw_object(QueryParams([TestEnum.VALUE1, TestEnum.VALUE2]))
    assert request_info.url == "https://example.com/me?dataset=value1%2Cvalue2"
    
def test_sets_enum_value_in_path_parameters():
    """Tests setting enum values in path parameters
    """
    request_info = RequestInformation(Method.GET, "https://example.com/{dataset}")
    request_info.path_parameters["dataset"] = TestEnum.VALUE1
    assert request_info.url == "https://example.com/value1"
    
def test_sets_enum_values_in_path_parameters():
    """Tests setting enum values in path parameters
    """
    request_info = RequestInformation(Method.GET, "https://example.com/{dataset}")
    request_info.path_parameters["dataset"] = [TestEnum.VALUE1, TestEnum.VALUE2]
    assert request_info.url == "https://example.com/value1%2Cvalue2"

def test_sets_uuid_values_in_path_parameters():
    """Tests setting uuid values in path parameters
    """
    request_info = RequestInformation(Method.GET, "https://example.com/values/{id}")
    request_info.path_parameters["id"] = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    assert request_info.url == "https://example.com/values/123e4567-e89b-12d3-a456-426614174000"

def test_sets_bool_values_in_path_parameters():
    """Tests setting uuid values in path parameters
    """
    request_info = RequestInformation(Method.GET, "https://example.com/isTrue/{bool}")
    request_info.path_parameters["bool"] = True
    assert request_info.url == "https://example.com/isTrue/true"

def test_sets_datetime_values_in_path_parameters():
    """Tests setting datetime values in path parameters
    """
    request_info = RequestInformation(Method.GET, "https://example.com/daysFrom/{startDate}")
    request_info.path_parameters["startDate"] = datetime(year=2020, month=8, day=1, hour=0, minute=20, second=0, microsecond=0)
    assert request_info.url == "https://example.com/daysFrom/2020-08-01T00%3A20%3A00Z"

def test_sets_int_values_in_path_parameters():
    """Tests setting int values values in path parameters
    """
    request_info = RequestInformation(Method.GET, "https://example.com/valuesFromZero/{number}")
    request_info.path_parameters["number"] = 7
    assert request_info.url == "https://example.com/valuesFromZero/7"

def test_sets_date_only_values_in_path_parameters():
    """Tests setting date only values in path parameters
    """
    request_info = RequestInformation(Method.GET, "https://example.com/daysFrom/{startDate}")
    request_info.path_parameters["startDate"] = datetime(year=2020, month=8, day=1, hour=0, minute=20, second=0, microsecond=0).date()
    assert request_info.url == "https://example.com/daysFrom/2020-08-01"

def test_sets_time_only_values_in_path_parameters():
    """Tests setting time only values in path parameters
    """
    request_info = RequestInformation(Method.GET, "https://example.com/daysFrom/{startDate}")
    request_info.path_parameters["startDate"] = datetime(year=2020, month=8, day=1, hour=0, minute=20, second=0, microsecond=0).time()
    assert request_info.url == "https://example.com/daysFrom/00%3A20%3A00"
    

    