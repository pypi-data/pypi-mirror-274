from tls_client import Session

class DCHcaptcha:
    def __init__(self, api_key:str) -> None:
        self.session = Session(
            random_tls_extension_order=True
        )

        self.api_key =api_key
    
    def create_task(self, site_key:str, link:str, proxy:str, rqdata:str=None) -> str:
        """
            Create a task and return his id ( str ).

            site_key: str -> HCaptcha site key of your website
            link: str -> Link of the page where you are solving it
            proxy: str -> HTTP Proxy, format: user:pass@ip:port or ip:port
            Optional: rqdata: str -> used for silent captcha, ex: discord join
        """
        data = {
            "apiKey": self.api_key,
            "TaskType": "Hcaptcha",
            "Data": {
                "link": link,
                "sitekey": site_key,
                "proxy": proxy
            }
        }
        
        if rqdata is not None:
            data["Data"]["rqdata"] = rqdata

        response = self.session.post(
            'https://api.dchcaptcha.com/api/CreateTask',
            json=data
        ).json()

        if response['error'] == 1:
            raise Exception(response['reason'])
        
        return response['data']['taskid']
    
    def get_task_data(self, task_id:str) -> str:
        """
            Return the corresponding task data.

            task_id: str -> your task_id
        """
        response = self.session.post(
            'https://api.dchcaptcha.com/api/GetTask',
            json={
                "apiKey": self.api_key,
                "taskid": task_id
            }
        ).json()

        if response['error'] == 1:
            raise Exception("Failed to solve ( get_task_data ): mainly proxy issue.")
        
        return response['data']
    
    def solve(self, site_key:str, link:str, proxy:str, rqdata:str=None) -> str:
        """
            Solve a captcha and return his solved key ( str ).

            site_key: str -> HCaptcha site key of your website
            link: str -> Link of the page where you are solving it
            proxy: str -> HTTP Proxy, format: user:pass@ip:port or ip:port
            Optional: rqdata: str -> used for silent captcha, ex: discord join
        """
                
        task_id = self.create_task(site_key, link, proxy, rqdata)

        for i in range(120):
            if i == 120:
                raise Exception('Failed to solve: too slow.')
            
            response = self.get_task_data(task_id)
            if response['state'] == "completed":
                return response['response_key']