import time
from locust import FastHttpUser, task, between

class QuickstartUser(FastHttpUser):
    wait_time = between(5, 20)

    @task(10)
    def homepage(self):
        self.client.get("/dataverse/harvard")

    @task
    def random_search1(self):
        self.client.get("/api/search?q=*")

    @task
    def random_search2(self):
        self.client.get("/dataverse/harvard/?q=fileName%3Aselfrecovery.tab")

    @task
    def random_dataset1(self):
        self.client.get("/dataset.xhtml?persistentId=doi:10.7910/DVN/29669")

    @task
    def random_dataset2(self):
        self.client.get("/dataset.xhtml?persistentId=doi:10.7910/DVN/55LJ9P")

    @task
    def random_dataset3(self):
        self.client.get("/dataset.xhtml?persistentId=doi:10.7910/DVN/27079")

    @task
    def random_dataset4(self):
        self.client.get("/dataset.xhtml?persistentId=doi:10.7910/DVN/MPU019")

    @task
    def random_dataset5(self):
        self.client.get("/dataset.xhtml?persistentId=doi:10.7910/DVN/27883")

    @task
    def random_dataset6(self):
        self.client.get("/dataset.xhtml?persistentId=doi:10.7910/DVN/OJZKKP")

    @task
    def random_dataset7(self):
        self.client.get("/dataset.xhtml?persistentId=doi:10.7910/DVN/29236")

    @task
    def random_dataset8(self):
        self.client.get("/dataset.xhtml?persistentId=doi:10.7910/DVN/26134")

    @task
    def random_dataset9(self):
        self.client.get("/dataset.xhtml?persistentId=doi:10.7910/DVN/27626")

    @task
    def get_version_dif1(self):
        self.client.get("/api/datasets/:persistentId/versions/compareSummary?persistentId=doi:10.7910/DVN/29236")
