from logos_sdk.services import get_headers
from requests import request
from http import HTTPStatus
from dotenv import load_dotenv
import os


class DV360ServiceException(Exception):
    pass


class DV360Service:
    def __init__(self, url=None):
        load_dotenv()
        self._URL = url or os.environ.get("DV360_SERVICE_PATH")
        self._LIST_LINE_ITEMS = self._URL + "/line-items"
        self._BULK_LIST_LINE_ITEM_ASSIGNED_TARGETING_OPTIONS = (
                self._URL + "/bulk-list-line-item-assigned-targeting-options"
        )
        self._BULK_EDIT_LINE_ITEM_ASSIGNED_TARGETING_OPTIONS = (
                self._URL + "/bulk-edit-line-item-assigned-targeting-options"
        )
        self._CREATE_CHANNEL = self._URL + "/create-channel"
        self._LIST_CHANNELS = self._URL + "/list-channels"
        self._LIST_CHANNEL_SITES = self._URL + "/list-channel-sites"
        self._BULK_EDIT_CHANNEL_SITES = self._URL + "/bulk-edit-channel-sites"

    def list_line_items(self, advertiser_id, secret_id, filter_string=None):
        """
        Lists line items in an advertiser
        :param advertiser_id: The ID of the advertiser to list line items for
        :param secret_id: The ID (name) of the Logos Secret in Secret Manager to be used to access the account specified by account email
        :param filter_string: Allows filtering by line item fields
        :return List[Sites]
        """
        header = get_headers(self._LIST_LINE_ITEMS)
        body = {"advertiser_id": advertiser_id, "secret_id": secret_id}

        if filter_string is not None:
            body["filter"] = filter_string

        response = request("post", url=self._LIST_LINE_ITEMS, json=body, headers=header)

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise DV360ServiceException(response.content)

    def bulk_list_line_item_assigned_targeting_options(
            self,
            advertiser_id,
            secret_id,
            line_item_ids,
            filter_string,
    ):
        """
        Bulk lists targeting options under multiple line items
        :param advertiser_id: The ID of the advertiser the line items belong to
        :param secret_id: The ID (name) of the Logos Secret in Secret Manager to be used to access the account specified by account email
        :param line_item_ids: The ID of the line items whose targeting is being updated
        :param filter_string: Allows filtering by line item fields
        :return List of AssignedTargetingOption objects
        """
        header = get_headers(self._BULK_EDIT_LINE_ITEM_ASSIGNED_TARGETING_OPTIONS)
        body = {
            "advertiser_id": advertiser_id,
            "secret_id": secret_id,
            "line_item_ids": line_item_ids,
            "filter": filter_string,
        }

        response = request(
            "post",
            url=self._BULK_LIST_LINE_ITEM_ASSIGNED_TARGETING_OPTIONS,
            json=body,
            headers=header,
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise DV360ServiceException(response.content)


    def bulk_edit_line_item_assigned_targeting_options(
            self,
            advertiser_id,
            secret_id,
            line_item_ids,
            delete_requests=None,
            create_requests=None,
    ):
        """
        Bulk edits targeting options under multiple line items
        :param advertiser_id: The ID of the advertiser the line items belong to
        :param secret_id: The ID (name) of the Logos Secret in Secret Manager to be used to access the account specified by account email
        :param line_item_ids: The ID of the line items whose targeting is being updated
        :param delete_requests: The assigned targeting options to delete in batch, specified as a list of
        DeleteAssignedTargetingOptionsRequest
        :param create_requests: The assigned targeting options to create in batch, specified as a list of
        CreateAssignedTargetingOptionsRequest
        :return None
        """
        header = get_headers(self._BULK_EDIT_LINE_ITEM_ASSIGNED_TARGETING_OPTIONS)
        body = {
            "advertiser_id": advertiser_id,
            "secret_id": secret_id,
            "line_item_ids": line_item_ids,
        }

        if delete_requests is not None:
            body["delete_requests"] = delete_requests

        if create_requests is not None:
            body["create_requests"] = create_requests

        response = request(
            "post",
            url=self._BULK_EDIT_LINE_ITEM_ASSIGNED_TARGETING_OPTIONS,
            json=body,
            headers=header,
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise DV360ServiceException(response.content)

    def create_channel(self, advertiser_id, secret_id, name):
        """
        Lists channels for advertiser
        :param advertiser_id: The ID of the advertiser that owns the channels
        :param secret_id: The ID (name) of the Logos Secret in Secret Manager to be used to access the account specified by account email
        :param name: The display name of the channel. Must be UTF-8 encoded with a maximum length of 240 bytes
        :return Channel
        """
        header = get_headers(self._CREATE_CHANNEL)
        body = {"advertiser_id": advertiser_id, "secret_id": secret_id, "name": name}

        response = request("post", url=self._CREATE_CHANNEL, json=body, headers=header)

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise DV360ServiceException(response.content)

    def list_channels(self, advertiser_id, secret_id, filter_string=None):
        """
        Lists channels for advertiser
        :param advertiser_id: The ID of the advertiser that owns the channels
        :param secret_id: The ID (name) of the Logos Secret in Secret Manager to be used to access the account specified by account email
        :param filter_string: Allows filtering by channel fields
        :return List[Channels]
        """
        header = get_headers(self._LIST_CHANNELS)
        body = {"advertiser_id": advertiser_id, "secret_id": secret_id}

        if filter_string is not None:
            body["filter"] = filter_string

        response = request("post", url=self._LIST_CHANNELS, json=body, headers=header)

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise DV360ServiceException(response.content)

    def list_channel_sites(
        self, advertiser_id, secret_id, channel_id, filter_string=None
    ):
        """
        Lists channels for advertiser
        :param advertiser_id: The ID of the advertiser that owns the channels
        :param secret_id: The ID (name) of the Logos Secret in Secret Manager to be used to access the account specified by account email
        :param channel_id: The ID of the parent channel to which the sites belong
        :param filter_string: Allows filtering by channel fields
        :return List[Sites]
        """
        header = get_headers(self._LIST_CHANNEL_SITES)
        body = {
            "advertiser_id": advertiser_id,
            "secret_id": secret_id,
            "channel_id": channel_id,
        }

        if filter_string is not None:
            body["filter"] = filter_string

        response = request(
            "post", url=self._LIST_CHANNEL_SITES, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise DV360ServiceException(response.content)

    def bulk_edit_channels_sites(
            self,
            advertiser_id,
            secret_id,
            channel_id,
            deleted_sites=None,
            created_sites=None,
    ):
        """
        Bulk edits sites under a single channel
        :param advertiser_id: The ID of the advertiser that owns the parent channel
        :param secret_id: The ID (name) of the Logos Secret in Secret Manager to be used to access the account specified by account email
        :param channel_id: The ID of the parent channel to which the sites belong
        :param deleted_sites: The sites to delete in batch
        :param created_sites: The sites to create in batch
        :return None
        """
        header = get_headers(self._BULK_EDIT_CHANNEL_SITES)
        body = {
            "advertiser_id": advertiser_id,
            "secret_id": secret_id,
            "channel_id": channel_id,
        }

        if deleted_sites is not None:
            body["deleted_sites"] = deleted_sites

        if created_sites is not None:
            body["created_sites"] = created_sites

        response = request(
            "post",
            url=self._BULK_EDIT_CHANNEL_SITES,
            json=body,
            headers=header,
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise DV360ServiceException(response.content)
