import importlib
import logging
import sys
import types
from pathlib import Path

import pytest


# Locate the application modules without changing production source code.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "src" / "text_to_sql_analytics"

if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))


# Provide lightweight stubs so tests do not initialize external services.
def create_stub_module(name, **attributes):
    module = types.ModuleType(name)

    for attribute_name, attribute_value in attributes.items():
        setattr(module, attribute_name, attribute_value)

    sys.modules[name] = module
    return module


def stub_setup_logger(logger_name, log_file=None):
    return logging.getLogger(logger_name)


create_stub_module(
    "llm_initialzation",
    create_llm=lambda *args, **kwargs: None,
    call_llm_string_response=lambda *args, **kwargs: "",
    call_llm_formatted_response=lambda *args, **kwargs: {},
)

create_stub_module(
    "utils",
    setup_logger=stub_setup_logger,
    load_configurations=lambda *args, **kwargs: None,
)

create_stub_module(
    "databaseQueryExecutor",
    fetch_user_workspaces=lambda *args, **kwargs: [],
)


# Import application functions after installing the stubs.
import global_vars

intent_module = importlib.import_module("intentClassifcationAndFilter")
query_module = importlib.import_module("processUserQuery")


def test_explicit_web_domain_is_detected_case_insensitively():
    result = intent_module.filter_testing_types(
        "Show failed WEB test executions"
    )

    assert result == ["web"]


def test_multiple_explicit_domains_are_detected():
    result = intent_module.filter_testing_types(
        "Compare API and PDF test failures"
    )

    assert result == ["api", "pdf"]


def test_all_explicit_domains_are_returned():
    result = intent_module.filter_testing_types(
        "Compare Web, API, PDF, and Package results"
    )

    assert result == ["web", "api", "pdf", "package"]


def test_missing_domain_defaults_to_all_domains():
    result = intent_module.filter_testing_types(
        "Show failed test execution results"
    )

    assert result == ["web", "api", "pdf", "package"]


def test_testing_type_globals_are_updated():
    try:
        intent_module.set_testing_type_globals(["API", " Package "])

        assert global_vars.is_web_selected is False
        assert global_vars.is_api_selected is True
        assert global_vars.is_pdf_selected is False
        assert global_vars.is_package_selected is True
    finally:
        intent_module.set_testing_type_globals([])


def test_markdown_json_fences_are_removed():
    raw_response = '```json\n{"status": "success"}\n```'

    cleaned = query_module.clean_llm_json_response(raw_response)

    assert cleaned == '{"status": "success"}'


def test_columns_are_derived_from_the_first_record():
    data = [
        {"run_id": 101, "status": "Fail", "duration": 12},
        {"run_id": 102, "status": "Pass", "duration": 8},
    ]

    result = query_module.derive_columns_from_data(data)

    assert result == ["run_id", "status", "duration"]


def test_empty_data_returns_no_columns():
    assert query_module.derive_columns_from_data([]) == []


def test_json_reader_returns_data_records(tmp_path):
    sample_file = tmp_path / "sample.json"
    sample_file.write_text(
        '{"data": [{"run_id": 101, "status": "Fail"}]}',
        encoding="utf-8",
    )

    result = query_module.read_data_from_json(str(sample_file))

    assert result == [{"run_id": 101, "status": "Fail"}]


def test_json_reader_returns_empty_list_when_data_is_absent(tmp_path):
    sample_file = tmp_path / "empty.json"
    sample_file.write_text('{"metadata": {}}', encoding="utf-8")

    result = query_module.read_data_from_json(str(sample_file))

    assert result == []