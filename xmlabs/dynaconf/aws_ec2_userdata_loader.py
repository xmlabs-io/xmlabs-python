from .base import ConfigSource
import logging
import requests

logger = logging.getLogger()
class ConfigSourceAwsEc2UserData(ConfigSource):
    def load(self):
        if self._running_in_ec2():
            #TODO: fetch EC2 USERDATA
            raise Exception("ConfigSourceEC2UserData Load Unimplemented")
        
    def _running_in_ec2(self):
        try:
            # Based on https://gist.github.com/dryan/8271687
            instance_ip_url = "http://169.254.169.254/latest/meta-data/local-ipv4"
            requests.get(instance_ip_url, timeout=0.01)
            return True
        except requests.exceptions.RequestException:
            return False
