from .fixtures import *
from tenable.errors import *
import uuid, io

def test_configure_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.configure('nope', dict())

def test_configure_policy_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.configure(1, 'nope')

def test_configure_policy_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.configure(1, dict())

def test_configure_policy(api, policy):
    details = api.policies.details(policy['policy_id'])
    details['settings']['name'] = str(uuid.uuid4())
    api.policies.configure(policy['policy_id'], details)
    updated = api.policies.details(policy['policy_id'])
    assert details['settings']['name'] == updated['settings']['name']

def test_copy_policy_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.copy('nope')

def test_copy_policy_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.copy(1)

def test_copy_policy(api, policy):
    new = api.policies.copy(policy['policy_id'])
    assert 'Copy of' in new['name']
    api.policies.delete(new['id'])

def test_create_policy(api, policy):
    assert isinstance(policy, dict)

def test_delete_policy_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.delete('nope')

def test_delete_policy_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.delete(1)

def test_delete_policy(api, policy):
    api.policies.delete(policy['policy_id'])

def test_policy_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.details('nope')

def test_policy_details_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.details(1)

def test_policy_details(api, policy):
    check = api.policies.details(policy['policy_id'])
    assert isinstance(check, dict)

def test_policy_export_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.policy_export('nope')

def test_policy_export_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.policy_export(1)

def test_policy_export(api, policy):
    pobj = api.policies.policy_export(policy['policy_id'])
    assert isinstance(pobj, io.BytesIO)

def test_policy_import(api, policy):
    pobj = api.policies.policy_export(policy['policy_id'])
    resp = api.policies.policy_import(pobj)
    assert isinstance(resp['id'], int)

def policy_list(api):
    assert isinstance(api.policies.list(), list)