from app.api.api_helper import enforce_param_existence, enforce_param_type, required_param, optional_param, prohibited_param_check
from tests import TestCase
from werkzeug.exceptions import HTTPException
import nose


class TestApiHelper(TestCase):
    def test_enforce_param_existence(self):
        enforce_param_existence(["testparam"], "testparam")

    def test_enforce_param_type(self):
        enforce_param_type({"string": "test"}, "string", str)
        enforce_param_type({"string": 3.14}, "string", float)
        enforce_param_type({"string": 42}, "string", int)
        enforce_param_type({"string": u"test"}, "string", unicode)
        enforce_param_type({"string": "test"}, "string", str, is_json=False)
        enforce_param_type({"string": 3.14}, "string", float, is_json=False)
        enforce_param_type({"string": 42}, "string", int, is_json=False)
        enforce_param_type({"string": u"test"}, "string", unicode, is_json=False)

    @nose.tools.raises(HTTPException)
    def test_enforce_param_type_abort1(self):
        enforce_param_type({"string": "42"}, "string", int)

    @nose.tools.raises(HTTPException)
    def test_enforce_param_type_abort2(self):
        enforce_param_type({"string": 3.14}, "string", str)

    def test_required_param(self):
        val = required_param({"string": "test"}, "string", str)
        assert val == "test"
        val = required_param({"string": 3.14}, "string", float)
        assert val == 3.14
        val = required_param({"string": 42}, "string", int)
        assert val == 42
        val = required_param({"string": u"test"}, "string", unicode)
        assert val == u"test"
        val = required_param({"string": "test"}, "string", str, is_json=False)
        assert val == "test"
        val = required_param({"string": 3.14}, "string", float, is_json=False)
        assert val == 3.14
        val = required_param({"string": 42}, "string", int, is_json=False)
        assert val == 42
        val = required_param({"string": u"test"}, "string", unicode, is_json=False)
        assert val == u"test"

    @nose.tools.raises(HTTPException)
    def test_required_param_abort1(self):
        required_param({"string": "42"}, "string", int)

    @nose.tools.raises(HTTPException)
    def test_required_param_abort2(self):
        required_param({"string": 3.14}, "string", str)

    def test_optional_param(self):
        val = optional_param({"string": "test"}, "string", str)
        assert val == "test"
        val = optional_param({"string": 3.14}, "string", float)
        assert val == 3.14
        val = optional_param({"string": 42}, "string", int)
        assert val == 42
        val = optional_param({"string": u"test"}, "string", unicode)
        assert val == u"test"
        val = optional_param({"string": "test"}, "string", str, is_json=False)
        assert val == "test"
        val = optional_param({"string": 3.14}, "string", float, is_json=False)
        assert val == 3.14
        val = optional_param({"string": 42}, "string", int, is_json=False)
        assert val == 42
        val = optional_param({"string": u"test"}, "string", unicode, is_json=False)
        assert val == u"test"
        val = optional_param({"string": u"test"}, "notexistskey", unicode, is_json=False)
        assert val is None
