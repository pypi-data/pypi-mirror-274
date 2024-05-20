"""
quickscraper-sdk
~~~~~~
The quickscraper-sdk package - handles proxy servers, browsers, and
CAPTCHA so that you can get the HTML from any website with an easy API call!
"""

from .constant import BASE_URL, VERSION
from urllib.parse import urlencode
from base64 import b64decode
import requests


class QuickScraper:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.parse_url = BASE_URL + 'parse'
        self.account_url = BASE_URL + 'account'

    def getHtml(self, url: str,
                render: bool = None,
                session_number: str = None,
                country_code: str = None,
                premium: bool = None,
                keep_headers: bool = None,
                headers: dict = {},
                format: str = 'html',
                device_type: str = None,
                parserSubscriptionId: str = None,
                webhookRequestId: str = None,
                customSelectors:list = [],
                keepSelection: bool = None,
                formData: dict = {},
                isKeepFormDataSelection: bool  = None,
                isScroll: bool = None,
                scrollTimeout : int = None,
                isPabbly : bool = None,
                isZapier : bool = None,
                dynamicInputs :list = []
                ):
        
        if(customSelectors!=[] or formData != {} or (dynamicInputs !=[] and parserSubscriptionId)):
                request_data = self.__prepareRequestBodyOrUrl(
                url= url, render = render, session_number=session_number,country_code = country_code,
                premium = premium, keep_headers = keep_headers, format=format, device_type = device_type,
                parserSubscriptionId = parserSubscriptionId, webhookRequestId = webhookRequestId, 
                isScroll = isScroll, scrollTimeout = scrollTimeout, isPabbly = isPabbly, isZapier = isZapier, 
                customSelectors = customSelectors, keepSelection = keepSelection, formData = formData,
                isKeepFormDataSelection = isKeepFormDataSelection, dynamicInputs=dynamicInputs, requestType= 'POST')
        
        else:
            request_url = self.__prepareRequestBodyOrUrl(
            url=url, render=render, session_number=session_number,
            country_code=country_code,
            premium=premium, keep_headers=keep_headers, format=format,
            device_type=device_type, parserSubscriptionId=parserSubscriptionId,
            webhookRequestId=webhookRequestId, isScroll = isScroll, scrollTimeout = scrollTimeout, 
            isPabbly = isPabbly, isZapier = isZapier, keepSelection = None, isKeepFormDataSelection= None, requestType= 'GET')
        
        custom_headers = headers
        request_options = self.__prepareHeaders(custom_headers, keep_headers)
                
        try:
            if(customSelectors != [] or formData !={} or (dynamicInputs != [] and parserSubscriptionId)):
                response = requests.post(url= request_data["request_url"], json = request_data["request_body"], headers=request_options)
            else:
                response = requests.get(request_url, headers=request_options)
            
            if parserSubscriptionId is not None:
                response._content = response.json()
            else:
                response._content = response.text

        except ValueError:
            pass
        return response

    def writeHtmlToFile(self, url: str, file_path: str, render: bool = None,
                        session_number: str = None, country_code: str = None,
                        premium: bool = None, keep_headers: bool = None,
                        headers: dict = {}, format: str = None,
                        device_type: str = None,
                        parserSubscriptionId: str = None,
                        webhookRequestId: str = None, dynamicInputs :list = []):
        with open(file_path, 'w+') as file:
            response = self.getHtml(
                url, render, session_number, country_code, premium,
                keep_headers, headers, format, device_type, parserSubscriptionId,
                webhookRequestId, dynamicInputs=dynamicInputs)
            if format == 'images' or format == 'docx':
                try:
                    response._content = b64decode(response.text)
                except ValueError:
                    pass
            file.write(str(response._content))
        return response

    # def writeCSVFile(self, url: str, file_path: str, render: bool = None,
    #                  session_number: str = None, country_code: str = None,
    #                  premium: bool = None, keep_headers: bool = None,
    #                  headers: dict = {}):
    #     response = self.writeHtmlToFile(url, file_path, render,
    #                                     session_number,
    #                                     country_code, premium,
    #                                     keep_headers, headers,
    #                                     format='tables')
    #     return response

    # def getAllImagesInZip(self, url: str, file_path: str,
    #                       render: bool = None,
    #                       session_number: str = None,
    #                       country_code: str = None,
    #                       premium: bool = None, keep_headers: bool = None,
    #                       headers: dict = {}):
    #     response = self.writeHtmlToFile(url, file_path, render,
    #                                     session_number, country_code,
    #                                     premium, keep_headers,
    #                                     headers, format='images')
    #     return response

    # def writeDOCXFile(self, url: str, file_path: str, render: bool = None,
    #                   session_number: str = None, country_code: str = None,
    #                   premium: bool = None, keep_headers: bool = None,
    #                   headers: dict = {}):
    #     response = self.writeHtmlToFile(url, file_path, render,
    #                                     session_number, country_code,
    #                                     premium, keep_headers, headers,
    #                                     format='docx')
    #     return response

    # def post(self, url: str, render: bool = None,
    #          session_number: str = None, country_code: str = None,
    #          premium: bool = None, keep_headers: bool = None,
    #          headers: dict = {}):
    #     response = self.getHtml(
    #         url, render, session_number, country_code,
    #         premium, keep_headers, headers)
    #     return response

    # def put(self, url: str, render: bool = None,
    #         session_number: str = None, country_code: str = None,
    #         premium: bool = None, keep_headers: bool = None,
    #         headers: dict = {}):
    #     response = self.getHtml(
    #         url, render, session_number, country_code,
    #         premium, keep_headers, headers)
    #     return response

    def scrapyGet(self, url: str,
                  render: bool = None,
                  session_number: str = None,
                  country_code: str = None,
                  premium: bool = None,
                  keep_headers: bool = None,
                  format: str = 'html',
                  device_type: str = None,
                  parserSubscriptionId: str = None,
                  webhookRequestId: str = None):
        request_url = self.__prepareRequestBodyOrUrl(
            url=url, render=render, session_number=session_number,
            country_code=country_code,
            premium=premium, keep_headers=keep_headers, format=format,
            device_type=device_type, parserSubscriptionId=parserSubscriptionId,
            webhookRequestId=webhookRequestId, requestType = 'GET')
        return request_url

    def account(self):
        response = requests.get(self.account_url,
                                params={'access_token':
                                        self.access_token}).json()
        if response.get('message'):
            response = response.get('message')
        return response


    def __prepareHeaders(self, custom_headers={}, keep_headers=None):
        headers = {
            'Client': 'PYTHON_CLIENT_LIB',
            'Client-Version': VERSION
        }
        merged_headers = headers.copy()
        merged_headers.update(custom_headers)
        if keep_headers is True:
            return merged_headers
        return headers

    # This function is used for csv, json, excel
    def getData(self, url: str, render: bool = None, session_number: str = None,
                country_code: str = None,
                premium: bool = None, keep_headers: bool = None,
                headers: dict = {}, format: str = None,
                device_type: str = None,
                parserSubscriptionId: str = None, webhookRequestId: str = None, dynamicInputs :list = []):
        try:
            response = self.getHtml(url, render, session_number, country_code, premium,
                                    keep_headers, headers, format, device_type,
                                    parserSubscriptionId, webhookRequestId, dynamicInputs = dynamicInputs)
        except ValueError:
            pass
        return response

    def __prepareRequestBodyOrUrl(self, **kwargs):
         url_options = {
            'access_token': self.access_token,
            'URL': kwargs['url'],
            'render': kwargs.get('render', True),
            'session_number': kwargs['session_number'],
            'country_code': kwargs['country_code'],
            'premium': 'true' if kwargs['premium'] is True else None,
            'keep_headers': 'true' if kwargs['keep_headers'] is True else None,
            'format': kwargs['format'],
            'device_type': kwargs['device_type'],
            'isScroll' : 'true' if kwargs['isScroll'] is True else None,
            'scrollTimeout' : kwargs['scrollTimeout'],
            'isPabbly' : 'true' if kwargs['isPabbly'] is True else None,
            'isZapier' : 'true' if kwargs['isZapier'] is True else None,
            'keepSelection' : 'true' if kwargs['keepSelection'] is True else None,
            'isKeepFormDataSelection' : 'true' if kwargs['isKeepFormDataSelection'] is True else None,
        }
         if kwargs.get('parserSubscriptionId') is not None:
            url_options['parserSubscriptionRequestId'] = kwargs['parserSubscriptionId']  
         if kwargs.get('webhookRequestId') is not None:
            url_options['webhookRequestId'] = kwargs['webhookRequestId']
         if kwargs.get('customSelectors') is not None:
            url_options['customSelectors'] = kwargs['customSelectors']
         if kwargs.get('formData') is not None:
            url_options['formData'] = kwargs['formData']
         if kwargs.get('dynamicInputs') is not None:
            url_options['dynamicInputs'] = kwargs['dynamicInputs']

         if(kwargs['requestType'] == 'GET'):
            url_options_filtered = {
                key: value for key, value in 
                url_options.items() if value is not None
            }
            option_string = urlencode(url_options_filtered)
            request_url = self.parse_url + '?' + option_string
            return request_url
         requestData = { 'request_body':url_options, 'request_url': self.parse_url}
         return requestData
