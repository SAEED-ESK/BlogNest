from locust import HttpUser, task

class QuickstartUser(HttpUser):
    """
    Simulates an authenticated user for load testing API endpoints.
    Retrieves a JWT token on start and uses it for subsequent requests.
    """

    def on_start(self):
        """
        Authenticate once at the beginning of the test
        and attach the JWT token to all future requests.
        """
        url = "/accounts/api/v1/jwt/create/"
        data = {
            "email": "kia@gmail.com",
            "password": "Zz12345@",
        }
        response = self.client.post(url, data=data).json()
        self.client.headers = {
            "Authorization": f"Bearer {response.get('access')}"
        }

    @task
    def post_list(self):
        """
        Fetch list of blog posts.
        """
        self.client.get("/blog/api/v2/post/")

    @task
    def category_list(self):
        """
        Fetch list of categories.
        """
        self.client.get("/blog/api/v2/category/")