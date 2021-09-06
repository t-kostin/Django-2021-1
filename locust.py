from locust import HttpUser, TaskSet, task


def login(l):
    l.client.post('auth/login', {'username':'admin', 'password':'cirijifi'})


def logout(l):
    l.client.post('auth/logout', {'username':'admin', 'password':'cirijifi'})


def index(l):
    l.client.get('/')


def products(l):
    l.client.get('/products/')



@task
class UserBegavior(TaskSet):
    tasks = {index: 2, products: 5}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)



@task
class WebsiteUser(HttpUser):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 900
