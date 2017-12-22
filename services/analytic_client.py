"""Reporting Analytic API V4."""

from django.conf import settings

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = settings.GA_KEY_FILE_LOCATION
SERVICE_ACCOUNT_EMAIL = settings.GA_SERVICE_ACCOUNT_EMAIL
VIEW_ID = settings.GA_VIEW_ID


def initialize_analytics_reporting():
    """Initializes an analyticsreporting service object.

    Returns:
        analytics an authorized analyticsreporting service object.
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(
        SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    analytics = build(
        'analytics',
        'v4',
        http=http,
        discoveryServiceUrl=DISCOVERY_URI
    )

    return analytics


def get_most_visited_files(analytics):
    '''
    Use the Analytics Service Object to query the Analytics Reporting API V4.
    '''

    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [
                        {'startDate': '7daysAgo', 'endDate': 'today'}
                    ],
                    'metrics': [
                        {'expression': 'ga:pageviews'},
                        {'expression': 'ga:uniquePageviews'},
                        {'expression': 'ga:entrances'},
                        {'expression': 'ga:bounces'}
                    ],
                    'dimensions': [
                        {'name': 'ga:pagePath'},
                    ],
                    'orderBys': [
                        {
                            'fieldName': 'ga:pageviews',
                            'sortOrder': 'DESCENDING'
                        }
                    ],
                    'dimensionFilterClauses': [{
                        'filters': [{
                            'dimensionName': 'ga:pagePath',
                            'operator': 'BEGINS_WITH',
                            'expressions': [
                                '/fichas/'
                            ]
                        }]
                    }]
                }]
        }
    ).execute()


def get_analytic_data():

    analytics = initialize_analytics_reporting()
    response = get_most_visited_files(analytics)
    return response
