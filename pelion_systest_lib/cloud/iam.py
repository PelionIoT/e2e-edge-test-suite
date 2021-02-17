"""
IAM related helper functions
"""

import logging

log = logging.getLogger(__name__)


def create_api_key(cloud, group_name=None):
    """
    Create api key for a group
    :param cloud: Cloud API object
    :param group_name: Policy group name
    :return: Api key creation response
    """
    group_id = ''
    if group_name is not None:
        make_new_group = True
        r = cloud.iam.get_policy_groups(expected_status_code=200)
        resp = r.json()
        for group in resp['data']:
            if group['name'] == group_name:
                group_id = group['id']
                make_new_group = False
                break

        if make_new_group:
            payload = {'name': group_name}
            r = cloud.iam.create_policy_group(payload, expected_status_code=200)
            group = r.json()
            group_id = group['id']

    r = cloud.iam.create_api_key(group_id, expected_status_code=201)
    return r


def get_policy_group_id(cloud, group_name):
    """
    Gets the policy group id with group name
    :param cloud: Cloud API object
    :param group_name: Policy group name
    :return: Group id
    """
    group_id = None
    r = cloud.iam.get_policy_groups(expected_status_code=200)
    resp = r.json()
    for group in resp['data']:
        if group['name'] == group_name:
            group_id = group['id']
            break

    return group_id


def get_auth_token(cloud, account, username, password, expected_status_code=None):
    """
    Get auth token from user login
    :param cloud: Cloud API object
    :param account: Account id
    :param username: User id
    :param password: Password
    :param expected_status_code: Asserts the result in the function
    :return: Auth token
    """
    r = cloud.iam.authenticate_user(account=account, username=username, password=password,
                                    expected_status_code=expected_status_code).json()['token']

    return r
