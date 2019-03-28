import os
import jenkins
import requests
import json
from datetime import datetime
from dateutil import tz
from config import (jid, 
                    jtoken, 
                    jaddr, 
                    slack_url)
from date_util import (convert_millisecond_to_time, 
                       convert_timedelta_to_millisecond, 
                       convert_timestamp_to_datetime)


class Notify:
    def __init__(self):
        jurl = 'https://%s:%s@%s' % (jid, jtoken, jaddr)
        self.jserver = jenkins.Jenkins(jurl)
    
    def run(self):
        """
        main method
        """
        running_jobs = self.jserver.get_running_builds()
        for job in running_jobs:
            job_name = job['name']
            job_no = job['number']

            build_info = self._get_build_info(job_name, job_no)

            start_time = convert_timestamp_to_datetime(build_info['timestamp'])

            running_time = self._get_running_time(start_time)
            running_time_millisecond = convert_timedelta_to_millisecond(running_time)

            avg_running_time_millisecond = build_info['estimatedDuration']
            avg_running_time = convert_millisecond_to_time(avg_running_time_millisecond)

            if running_time_millisecond > avg_running_time_millisecond :
                message = """
                [BATCH HANG ALERT] [%s] %s \n
                START TIME:\t%s
                RUNNING TIME:\t%s
                AVG RUNNING:\t%s
                URL:\t %s
                """ 
                message = message % (job_no, job_name, start_time.strftime("%Y-%m-%d %H:%M:%S"), str(running_time)[:-7], avg_running_time, job['url'])
                self._send_message(message)

    def _get_running_time(self, start_time):
        """
        Calculate duration time
        """
        local_now = datetime.now(tz=tz.gettz('Asia/Seoul'))
        duration = local_now - start_time
        return duration

    def _get_build_info(self, job_name, job_no):
        """
        Get Build info of specific job
        """
        return self.jserver.get_build_info(job_name, job_no)

    def _send_message(self, message):
        """
        Send Slack Message
        """
        data = {'text': message}
        headers = {'Content-type': 'application/json'}
        response = requests.post(slack_url, data=json.dumps(data), headers=headers)
        print('message', message, 'status_code', response.status_code)

if __name__ == "__main__":
    notify = Notify()
    notify.run()
