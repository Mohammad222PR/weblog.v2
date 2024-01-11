from locust import HttpUser, task, between


class LoadTestingAPi(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/accounts/api/v1/register",
            data={
                "email": "admin@example.com",
                "username": "admin",
                "password": "asd@dqs1",
            },
        ).json()

        self.client.headers({"Authorization": f"Bearer {response.get('access', None)}"})

    @task
    def blog_get_post(self):
        self.client.get("/blog/api/v1/blog/list/")

    @task
    def blog_get_put_delete(self):
        self.client.get("/blog/api/v1/blog/list/2")

    @task
    def comment_get_put_post_path_delete(self):
        self.client.get("/blog/api/v1/blog/comment/")
