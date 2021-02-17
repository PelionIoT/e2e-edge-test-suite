# pylint: disable=too-many-public-methods
"""
This module is for cloud's Admin API functions
"""


class AdminAPI:
    """
    A class that provides Admin Rest API related functionality.
    Endpoint list here:
    https://github.com/ArmMbedCloud/auth/blob/master/documentation/swagger/iam-identity-r1.3-internal-swagger.json
    https://github.com/ArmMbedCloud/mbed-billing/blob/master/docs/server/swagger-api-server.yaml
    """

    def __init__(self, rest_api):
        """
        Initializes the Admin Rest API library
        :param rest_api: RestAPI object
        """
        self.cloud_api = rest_api
        self.api_version = 'v3'

    def get_account_templates(self, rt_token, query_params=None, expected_status_code=None):
        """
        Get all account templates
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/account-templates
        """
        api_url = '/admin/{}/account-templates'.format(self.api_version)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_account_template_info(self, rt_token, template_id, query_params=None, expected_status_code=None):
        """
        Get account template info
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param rt_token: Reference token
        :param template_id: Template id
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/account-templates/{template_id}
        """
        api_url = '/admin/{}/account-templates/{}'.format(self.api_version, template_id)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def create_account_template(self, rt_token, template_data, expected_status_code=None):
        """
        Create account template
        :param template_data: Template payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/account-templates
        """
        api_url = '/admin/{}/account-templates'.format(self.api_version)

        r = self.cloud_api.post(api_url, rt_token, payload=template_data, expected_status_code=expected_status_code)
        return r

    def update_account_template(self, rt_token, template_id, template_data, expected_status_code=None):
        """
        Update account template
        :param template_data: Template payload
        :param rt_token: Reference token
        :param template_id: Template id
        :param expected_status_code: Asserts the result in the function
        :return: PUT /admin/v3/account-templates/{template_id}
        """
        api_url = '/admin/{}/account-templates/{}'.format(self.api_version, template_id)

        r = self.cloud_api.put(api_url, rt_token, payload=template_data, expected_status_code=expected_status_code)
        return r

    def delete_account_template(self, rt_token, template_id, expected_status_code=None):
        """
        Delete account template
        :param rt_token: Reference token
        :param template_id: Template id
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /admin/v3/account-templates/{template_id}
        """
        api_url = '/admin/{}/account-templates/{}'.format(self.api_version, template_id)

        r = self.cloud_api.delete(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_accounts(self, rt_token, query_params=None, expected_status_code=None):
        """
        Get all accounts
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/accounts
        """
        api_url = '/admin/{}/accounts'.format(self.api_version)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def create_account(self, rt_token, account_data, expected_status_code=None):
        """
        Create account
        :param account_data: Account payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/accounts
        """
        api_url = '/admin/{}/accounts'.format(self.api_version)

        r = self.cloud_api.post(api_url, rt_token, account_data, expected_status_code=expected_status_code)
        return r

    def update_account(self, rt_token, account_id, account_data, expected_status_code=None):
        """
        Update account
        :param account_id: Account id
        :param account_data: Account payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: PUT /admin/v3/accounts/{account_id}
        """
        api_url = '/admin/{}/accounts{}'.format(self.api_version, account_id)

        r = self.cloud_api.put(api_url, rt_token, account_data, expected_status_code=expected_status_code)
        return r

    def delete_account(self, rt_token, account_id, payload=None, expected_status_code=None):
        """
        Delete account
        :param account_id: Account id
        :param rt_token: Reference token
        :param payload: Delete payload
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /admin/v3/accounts/{account_id}
        """
        api_url = '/admin/{}/accounts/{}'.format(self.api_version, account_id)

        r = self.cloud_api.delete(api_url, rt_token, payload, expected_status_code=expected_status_code)
        return r

    def get_account_info(self, rt_token, account_id, expected_status_code=None):
        """
        Get account info
        :param account_id: Account id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/accounts/account_id
        """
        api_url = '/admin/{}/accounts/{}'.format(self.api_version, account_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_account_features(self, rt_token, account_id, expected_status_code=None):
        """
        Get account features
        :param account_id: Account id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/features/{account_id}
        """
        api_url = '/admin/{}/features/{}'.format(self.api_version, account_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def set_account_limitations(self, rt_token, account_id, limitation_data, expected_status_code=None):
        """
        Set account features
        :param account_id: Account id
        :param limitation_data: Limitation policies payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/accounts/{account_id}/limitations/set
        """
        api_url = '/admin/{}/accounts/{}/limitations/set'.format(self.api_version, account_id)

        return self.cloud_api.post(api_url, rt_token, limitation_data, expected_status_code=expected_status_code)

    def set_account_features(self, rt_token, account_id, feature_data, expected_status_code=None):
        """
        Set account features
        :param account_id: Account id
        :param feature_data: Feature policies payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: PUT /admin/v3/features/{account_id}
        """
        api_url = '/admin/{}/features/{}'.format(self.api_version, account_id)

        r = self.cloud_api.put(api_url, rt_token, feature_data, expected_status_code=expected_status_code)
        return r

    def delete_account_features(self, rt_token, account_id, feature_data, expected_status_code=None):
        """
        Delete account features
        :param account_id: Account id
        :param feature_data: Feature policies payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /admin/v3/features/{account_id}
        """
        api_url = '/admin/{}/features/{}'.format(self.api_version, account_id)

        r = self.cloud_api.delete(api_url, rt_token, feature_data, expected_status_code=expected_status_code)
        return r

    def update_account_tier_level(self, rt_token, account_id, tier_data, expected_status_code=None):
        """
        Update account tier level
        :param account_id: Account id
        :param tier_data: Tier data payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: PUT /admin/v3/accounts/{account_id}/tier
        """
        api_url = '/admin/{}/accounts/{}/tier'.format(self.api_version, account_id)

        r = self.cloud_api.put(api_url, rt_token, tier_data, expected_status_code=expected_status_code)
        return r

    def get_account_sessions(self, rt_token, account_id, expected_status_code=None):
        """
        Get account sessions
        :param account_id: Account id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/accounts/{account_id}/sessions
        """
        api_url = '/admin/{}/accounts/{}/sessions'.format(self.api_version, account_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_agreements(self, rt_token, query_params=None, expected_status_code=None):
        """
        Get all agreements
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/agreements
        """
        api_url = '/admin/{}/agreements'.format(self.api_version)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def upload_new_agreement(self, rt_token, agreement_data, expected_status_code=None):
        """
        Upload new agreement
        :param agreement_data: Agreement payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/agreements
        """
        api_url = '/admin/{}/agreements'.format(self.api_version)

        r = self.cloud_api.post(api_url, rt_token, agreement_data, expected_status_code=expected_status_code)
        return r

    def get_agreement_info(self, rt_token, agreement_id, expected_status_code=None):
        """
        Get agreement info
        :param agreement_id: Agreement id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/agreements/agreement_id
        """
        api_url = '/admin/{}/agreements/{}'.format(self.api_version, agreement_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def update_agreement(self, rt_token, agreement_id, agreement_data, expected_status_code=None):
        """
        Update agreement
        :param agreement_id: Agreement id
        :param agreement_data: Agreement payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: PUT /admin/v3/agreements/{agreement_id}
        """
        api_url = '/admin/{}/agreements{}'.format(self.api_version, agreement_id)

        r = self.cloud_api.put(api_url, rt_token, agreement_data, expected_status_code=expected_status_code)
        return r

    def delete_agreement(self, rt_token, agreement_id, expected_status_code=None):
        """
        Delete agreement
        :param agreement_id: Agreement id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /admin/v3/agreements/{agreement_id}
        """
        api_url = '/admin/{}/agreements{}'.format(self.api_version, agreement_id)

        r = self.cloud_api.delete(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_signed_agreements(self, rt_token, query_params=None, expected_status_code=None):
        """
        Get all signed agreements
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/signed-agreements
        """
        api_url = '/admin/{}/signed-agreements'.format(self.api_version)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_signed_agreement_info(self, rt_token, signed_agreement_id, expected_status_code=None):
        """
        Get signed agreement info
        :param signed_agreement_id: Signed agreement id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/signed-agreements/signed_agreement_id
        """
        api_url = '/admin/{}/signed-agreements/{}'.format(self.api_version, signed_agreement_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_trusted_certificates(self, rt_token, query_params=None, expected_status_code=None):
        """
        Get all accounts' trusted certificates
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/trusted-certificates
        """
        api_url = '/admin/{}/trusted-certificates'.format(self.api_version)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_api_keys(self, rt_token, query_params=None, expected_status_code=None):
        """
        Get all API keys
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/api-keys
        """
        api_url = '/admin/{}/api-keys'.format(self.api_version)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_api_key_info(self, rt_token, api_key_id, expected_status_code=None):
        """
        Get API key info
        :param api_key_id: API key id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/api-keys/api-key_id
        """
        api_url = '/admin/{}/api-keys/{}'.format(self.api_version, api_key_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def update_api_key(self, rt_token, api_key_id, api_key_data, expected_status_code=None):
        """
        Update api key
        :param api_key_id: Api_key id
        :param rt_token: Reference token
        :param api_key_data: New api key attributes
        :param expected_status_code: Asserts the result in the function
        :return: PUT /admin/v3/api_keys/{api_key_id}
        """
        api_url = '/admin/{}/api_keys/{}'.format(self.api_version, api_key_id)

        r = self.cloud_api.put(api_url, rt_token, api_key_data, expected_status_code=expected_status_code)
        return r

    def delete_api_key(self, rt_token, api_key_id, expected_status_code=None):
        """
        Delete api key
        :param api_key_id: Api_key id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /admin/v3/api_keys/{api_key_id}
        """
        api_url = '/admin/{}/api_keys/{}'.format(self.api_version, api_key_id)

        r = self.cloud_api.delete(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def reset_api_key_secret_key(self, rt_token, api_key_id, expected_status_code=None):
        """
        Reset api key secret key
        :param api_key_id: Api_key id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/api_keys/{api_key_id}/reset-secret
        """
        api_url = '/admin/{}/api_keys/{}/reset-secret'.format(self.api_version, api_key_id)

        r = self.cloud_api.post(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_api_key_count(self, rt_token, expected_status_code=None):
        """
        Get environment's API key count
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: API key count
        """
        api_url = '/admin/{}/api-keys'.format(self.api_version)
        query_params = {'limit': '5', 'include': 'total_count'}

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        api_keys = r.json()
        return api_keys['total_count']

    def get_admin_features(self, rt_token, query_params=None, expected_status_code=None):
        """
        Get admin features
        :param rt_token: Reference token
        :param query_params: e.g.{'filter': 'packages'}
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/features
        """
        api_url = '/admin/{}/features'.format(self.api_version)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_users(self, rt_token, query_params=None, expected_status_code=None):
        """
        Get all users
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/users
        """
        api_url = '/admin/{}/users'.format(self.api_version)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_user_info(self, rt_token, user_id, expected_status_code=None):
        """
        Get user info
        :param user_id: User id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/user/{user_id}
        """
        api_url = '/admin/{}/user/{}'.format(self.api_version, user_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_user_invitations(self, rt_token, query_params=None, expected_status_code=None):
        """
        Get all user invitations
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/user-invitations
        """
        api_url = '/admin/{}/user-invitations'.format(self.api_version)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_user_invitation_info(self, rt_token, invitation_id, expected_status_code=None):
        """
        Get user invitation info
        :param invitation_id: Invitation id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/user-invitations/{invitation_id}
        """
        api_url = '/admin/{}/user-invitations/{}'.format(self.api_version, invitation_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def change_user_password(self, rt_token, user_id, new_password_data, expected_status_code=None):
        """
        Change the password for a user
        :param user_id: User id
        :param rt_token: Reference token
        :param new_password_data: New password
        :param expected_status_code: Asserts the result in the function
        :return: PUT /admin/v3/users/{user_id}/password
        """
        api_url = '/admin/{}/users/{}/password'.format(self.api_version, user_id)

        r = self.cloud_api.put(api_url, rt_token, new_password_data, expected_status_code=expected_status_code)
        return r

    def reset_user_password(self, rt_token, user_id, expected_status_code=None):
        """
        Reset the password for a user
        :param user_id: User id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/users/{user_id}/reset-password
        """
        api_url = '/admin/{}/users/{}/reset-password'.format(self.api_version, user_id)

        r = self.cloud_api.post(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def send_email_notification_for_account(self, rt_token, account_id, email_data, expected_status_code=None):
        """
        Test email notification sending with the given account
        :param account_id: Account_id
        :param email_data: Email payload
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/emails/{account_id}
        """
        api_url = '/admin/{}/emails/{}'.format(self.api_version, account_id)

        r = self.cloud_api.post(api_url, rt_token, email_data, expected_status_code=expected_status_code)
        return r

    def get_billing_report(self, rt_token, month, query_params=None, expected_status_code=None):
        """
        Get billing report for all commercial accounts
        :param month: Report month in format {'month': 'YYYY-MM'}
        :param query_params: e.g.{'format': 'json', 'final': 'false', parent_id: '<account_id>',
         'account_id__in': '<account_id>', 'after': '<report_id>}
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing-report
        """
        api_url = '/admin/{}/billing-report'.format(self.api_version)

        # Add month to query parameters
        if isinstance(query_params, dict):
            query_params.update(month)
        else:
            query_params = month

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_billing_report_active_devices(self, rt_token, month, account_id, query_params=None,
                                          expected_status_code=None):
        """
        Get billing report for active devices for a certain account
        :param month: Report month in format {'month': 'YYYY-MM'}
        :param account_id: Account id in format {'account': '<account_id>'}
        :param query_params: e.g.{'final': 'false'}
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing/report/activedevices
        """
        api_url = '/admin/{}/billing/report/activedevices'.format(self.api_version)

        # Add month and account id to query parameters
        if isinstance(query_params, dict):
            query_params.update(month)
            query_params.update(account_id)
        else:
            query_params = month
            query_params.update(account_id)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_billing_report_firmware_updates(self, rt_token, month, account_id, query_params=None,
                                            expected_status_code=None):
        """
        Get billing report for updated devices for a certain account
        :param month: Report month in format {'month': 'YYYY-MM'}
        :param account_id: Account id in format {'account': '<account_id>'}
        :param query_params: e.g.{'final': 'false'}
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing/report/firmwareupdates
        """
        api_url = '/admin/{}/billing/report/firmwareupdates'.format(self.api_version)

        # Add month and account id to query parameters
        if isinstance(query_params, dict):
            query_params.update(month)
            query_params.update(account_id)
        else:
            query_params = month
            query_params.update(account_id)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_billing_service_packages(self, rt_token, account_id, expected_status_code=None):
        """
        Get info for all billing service packages for a certain commercial account
        :param account_id: Account id
        :param rt_token: Reference token
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing/accounts/{account_id}/servicepackages
        """
        api_url = '/admin/{}/billing/accounts/{}/servicepackages'.format(self.api_version, account_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_billing_active_service_package(self, rt_token, account_id, expected_status_code=None):
        """
        Get info about current active package for commercial account
        :param account_id: Account id
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing/accounts/{account_id}/servicepackages/active
        """
        api_url = '/admin/{}/billing/accounts/{}/servicepackages/active'.format(self.api_version, account_id)

        r = not self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_billing_service_package_quota(self, rt_token, account_id, expected_status_code=None):
        """
        Get available billing service package total quota for a certain commercial account
        :param account_id: Account id
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing/accounts/{account_id}/servicepackages/quota
        """
        api_url = '/admin/{}/billing/accounts/{}/servicepackages/quota'.format(self.api_version, account_id)

        r = self.cloud_api.get(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def get_billing_service_package_quota_history(self, rt_token, account_id, query_params=None,
                                                  expected_status_code=None):
        """
        Get available billing service package quota history for a certain commercial account
        :param account_id: Account id
        :param query_params: e.g. {'limit': '100', 'order': 'ASC'}
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing/accounts/{account_id}/servicepackages/quota/history
        """
        api_url = '/admin/{}/billing/accounts/{}/servicepackages/quota/history'.format(self.api_version, account_id)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def create_billing_service_package(self, rt_token, account_id, service_package_data, expected_status_code=None):
        """
        Create a new service package for commercial account
        :param account_id: Account id
        :param service_package_data: Service package payload
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/billing/accounts/{account_id}/servicepackages
        """
        api_url = '/admin/{}/billing/accounts/{}/servicepackages'.format(self.api_version, account_id)

        r = self.cloud_api.post(api_url, rt_token, service_package_data, expected_status_code=expected_status_code)
        return r

    def confirm_billing_service_package(self, rt_token, account_id, confirmation_id, expected_status_code=None):
        """
        Confirm the creation of a new service package for commercial account
        :param account_id: Account id
        :param confirmation_id: Confirmation id
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/billing/accounts/{account_id}/servicepackages/confirm/{confirmation_id}
        """
        api_url = '/admin/{}/billing/accounts/{}/servicepackages/confirm/{}'.format(self.api_version, account_id,
                                                                                    confirmation_id)

        r = self.cloud_api.post(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def reject_billing_service_package(self, rt_token, account_id, confirmation_id, expected_status_code=None):
        """
        Reject the creation of a new service package for commercial account
        :param account_id: Account id
        :param confirmation_id: Confirmation id
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /admin/v3/billing/accounts/{account_id}/servicepackages/confirm/{confirmation_id}
        """
        api_url = '/admin/{}/billing/accounts/{}/servicepackages/confirm/{}'.format(self.api_version, account_id,
                                                                                    confirmation_id)

        r = self.cloud_api.delete(api_url, rt_token, expected_status_code=expected_status_code)
        return r

    def modify_billing_service_package_quota(self, rt_token, account_id, quota_data, expected_status_code=None):
        """
        Modify active service package quota for commercial account
        :param account_id: Account id
        :param quota_data: New quota for package in format {'firmware_update_count': '<new_quota>'}
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: PATCH /admin/v3/billing/accounts/{account_id}/servicepackages/active
        """
        api_url = '/admin/{}/billing/accounts/{}/servicepackages/active'.format(self.api_version, account_id)

        r = self.cloud_api.patch(api_url, rt_token, quota_data, expected_status_code=expected_status_code)
        return r

    def renew_billing_service_package(self, rt_token, account_id, service_package_renew_data,
                                      expected_status_code=None):
        """
        Renew currently active service package for commercial account
        :param account_id: Account id
        :param service_package_renew_data: Service package renew payload
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: POST /admin/v3/billing/accounts/{account_id}/servicepackages/renew
        """
        api_url = '/admin/{}/billing/accounts/{}/servicepackages/renew'.format(self.api_version, account_id)

        r = self.cloud_api.post(api_url, rt_token, service_package_renew_data,
                                expected_status_code=expected_status_code)
        return r

    def get_billing_free_tier_usage(self, rt_token, account_id, month, expected_status_code=None):
        """
        Get reservation details for free tier account
        :param account_id: Account id
        :param month: Month in format {'month': 'YYYY-MM'}
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing/accounts/{account_id}/free-tier-usage
        """
        api_url = '/admin/{}/billing/accounts/{}/free-tier-usage'.format(self.api_version, account_id)

        r = self.cloud_api.get(api_url, rt_token, params=month, expected_status_code=expected_status_code)
        return r

    def get_billing_stats(self, rt_token, month, account_id=None, expected_status_code=None):
        """
        Get billing stats for all / certain commercial account(s)
        :param month: Month in format {'month': 'YYYY-MM'}
        :param account_id: Account id in format {'account': '<account_id>'}
        :param rt_token: Authorization token, either Reference token or Root API key
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing/stats
        """
        api_url = '/admin/{}/billing/stats'.format(self.api_version)

        # Build query parameters
        query_params = month
        if account_id is not None:
            query_params.update(account_id)

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_billing_statistics(self, rt_token, account_id, interval, query_params=None, expected_status_code=None):
        """
        Get billing statistics for an account for certain time period
        :param rt_token: Authorization token, either Reference token or Root API key
        :param account_id: Account id
        :param interval: Desired interval e.g. 5m, 2h, 3d, 4w, 1mo in format {'interval': '5m'}
        :param query_params: Either period or start & end times need to be defined, additionally
        e.g. {'limit': '100', 'order': 'ASC'}
        :param expected_status_code: Asserts the result in the function
        :return: GET /admin/v3/billing/accounts/{account_id}/statistics
        """
        api_url = '/admin/{}/billing/accounts/{}/statistics'.format(self.api_version, account_id)

        # Add interval to query params
        if isinstance(query_params, dict):
            query_params.update(interval)
        else:
            query_params = interval

        r = self.cloud_api.get(api_url, rt_token, params=query_params, expected_status_code=expected_status_code)
        return r
