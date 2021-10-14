import requests
import json
from datetime import datetime, date

class Woffu:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.auth_headers = self._get_auth_headers()
        self.domain, self.user_id, self.company_id = self._get_domain_company_user_id()

    # aux functions
    def _get_auth_headers(self):
        access_token = requests.post(
            "https://app.woffu.com/token",
            data = f"grant_type=password&username={self.username}&password={self.password}"
        ).json()['access_token']

        return {
            'Authorization': 'Bearer ' + access_token,
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8'
        }

    def _get_domain_company_user_id(self):
        users = requests.get(
            "https://app.woffu.com/api/users", 
            headers = self.auth_headers
        ).json()
        company = requests.get(
            f"https://app.woffu.com/api/companies/{users['CompanyId']}", 
            headers = self.auth_headers
        ).json()
        return company['Domain'], users['UserId'], users['CompanyId']

    def sign_in(self):
        response = requests.post(
            f"https://{self.domain}/api/svc/signs/signs",
            json = {
                'StartDate': datetime.now().replace(microsecond=0).isoformat()+"+01:00",
                'EndDate': datetime.now().replace(microsecond=0).isoformat()+"+01:00",
                'TimezoneOffset': "-60",
                'UserId': self.user_id
            },
            headers = self.auth_headers
        )

        if response.status_code >= 400:
            raise Exception("Error trying to sign in or sign out.")

    def save_data(self):
        #Store user/password/id to make less network requests in next logins
        with open("data.json", "w") as login_info:
            json.dump(
                {
                    "username": self.username,
                    "password": self.password,
                    "user_id": self.user_id,
                    "company_id": self.company_id,
                    "domain": self.domain
                },
                login_info
            )

    def get_holidays(self):
        holidays = requests.get(
            f"https://{self.domain}/api/users/{self.user_id}/requests?pageSize=1000", 
            headers = self.auth_headers
        ).json()
        return holidays

    def get_pending_holidays(self):
        pending_holidays = [req for req in self.get_holidays()
            if req['RequestStatusId'] == 20 and req['RequestStatus'] == '_RequestStatusAcceptedAndPending']
        return pending_holidays

    def get_context(self):
        context = requests.get(
            f"https://{self.domain}/api/requests/context?id={self.user_id}",
            headers = self.auth_headers
        ).json()
        return context

    def get_bank_holidays(self, year=None):
        if year is None:
            year = date.today().year

        absence = requests.get(
            f"https://{self.domain}/api/users/{self.user_id}/diaries/absence/single_events?fromDate={year}-01-01T00:00:00.000Z&presence=false&toDate={year}-12-31T23:59:59.000Z",
            headers = self.auth_headers
        ).json()
        bank_holidays = [h for h in absence['Events'] if h['isHoliday'] and not h['isWeekend']]
        return bank_holidays

    def is_working_day_for_me(self, day=None):
        if day is None:
            day = date.today()
        is_weekend = day.weekday() >= 5
        if is_weekend:
            return False

        bank_holidays = self.get_bank_holidays()
        is_bank_holiday = any([datetime.fromisoformat(bh['start']).date() == day for bh in bank_holidays])
        if is_bank_holiday:
            return False

        pending_holidays = self.get_pending_holidays()
        if len(pending_holidays) == 0:
            return True

        is_pto = any([(day >= datetime.fromisoformat(h['StartDate']).date() and day <= datetime.fromisoformat(h['EndDate']).date()) for h in pending_holidays])
        return not is_pto
