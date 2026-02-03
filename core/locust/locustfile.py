from locust import HttpUser, task

class QuickstartUser(HttpUser):
    def on_start(self):
        url = '/accounts/api/v1/jwt/create/'
        data = {
            "email": "kia@gmail.com",
            "password": "Zz12345@"
        }
        response = self.client.post(url, data=data).json()
        self.client.headers = {'Authorization': f"Bearer {response.get('access', None)}"}

    @task
    def post_list(self):
        self.client.get('/blog/api/v2/post/')

    @task
    def category_list(self):
        self.client.get('/blog/api/v2/category/')