# Remember 
**Must regenerate another secret key in .env for production.**

```sh
openssl rand -hex 32
```

# How to use

1. create a virtual environment.
```sh
$ python3 -m venv env
```

2. activate it.
```sh
$ source ./env/bin/activate  
```

3. install the `requirements.txt`
```sh
(env) $ pip install -r requirements.txt
```

4. run the backend
```sh
(env) $ cd backend
(env) $ uvicorn app:app --reload
``` 

5. Open the Api Docs in the borwser http://127.0.0.1:8000/docs
