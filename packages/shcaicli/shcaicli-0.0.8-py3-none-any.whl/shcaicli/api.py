from shcaicli.shcai_exc import SHCAIException
import requests
import json


class SHCAi:
  def __init__(self,
               api_root: str = 'https://apim.ihealthgroup.tec.br/api',
               api_name: str = 'shc-mtask',
               api_version: str = 'v1',
               api_key: str = None,
               tokens_mode: bool = False
               ):
    self._api_root = api_root
    self._api_name = api_name[1:] if api_name.startswith('/') else api_name
    self._api_name = f'{self._api_name}?output_type=tokens' if tokens_mode else self._api_name
    self.api_version = api_version
    self.api_key = api_key

  def infer(self, cns: [] = None):
    if cns is None or len(cns) == 0:
      raise ValueError('invalid value for cns parameter')

    headers = {
      'Content-Type': 'application/json',
      'X-Gravitee-Api-Key': self.api_key,
    }
    url = f'{self._api_root}/{self._api_name}'
    data = {
      'cns': cns
    }
    response = requests.post(url, json=data, headers=headers, timeout=30)
    if response.status_code == 200:
      return json.loads(response.text)
    else:
      raise SHCAIException(f'Request failed with status code {response.status_code}. Response: {response.text}')
