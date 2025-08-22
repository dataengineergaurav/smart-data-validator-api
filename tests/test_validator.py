import pytest
from unittest.mock import patch
from app.services.dify_connector import call_dify
from app.services.validator import validate_csv
from app.models.schema import ValidationRequest, ColumnRule

# Mocked response from Dify
MOCK_FIXES = {
    "fixes": [
        {"error": "Missing column: age", "suggestion": "Add an 'age' column with integers."},
        {"error": "Null values in required column: salary", "suggestion": "Impute missing salaries with median."}
    ]
}

def test_call_dify_mocked():
    error_summary = "Missing column: age\nNull values in required column: salary"

    with patch("app.services.dify_connector.requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "data": {
                "outputs": {
                    "result": MOCK_FIXES
                }
            }
        }
        mock_post.return_value.raise_for_status = lambda: None

        response = call_dify(error_summary)
        assert "fixes" in response
        assert response["fixes"][0]["error"] == "Missing column: age"


def test_validate_csv(tmp_path):
    # Create sample CSV with missing column 'age'
    csv_file = tmp_path / "dummy_data.csv"
    csv_file.write_text("name,salary\nJohn,50000\nJane,\n")


    rules = ValidationRequest(rules=[
        ColumnRule(name="name", dtype="string"),
        ColumnRule(name="age", dtype="int"),
        ColumnRule(name="salary", dtype="float", required=True)
    ])

    result = validate_csv(str(csv_file), rules)
    assert not result.is_valid
    assert "Missing column: age" in result.errors
    assert "Null values in required column: salary" in result.errors
