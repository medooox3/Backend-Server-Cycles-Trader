from fastapi.routing import APIRouter 

router = APIRouter()

@router.get("/login")
async def login():
    '''login and redirect the user to the dashboard'''
    pass

@router.get("/logout")
async def logout():
    '''logout and redirect the user to the login route'''
    pass

# ! Todo: is this realy necessary in case of using react ?
@router.get("/dashboard")
async def dashboard():
    '''show the dashboard'''
    pass

# ----- Users Management -------
@router.post("/addUser")
async def add_user():
    '''create a new user and store him in the DB'''
    pass

@router.delete("/deleteUsers")
async def remove_users(users_id: list[int]):
    '''remove user completely from the DB'''
    pass

@router.put("/updateUser")
async def update_user():
    '''update user info'''
    pass


@router.get("/user/{id}")
async def get_user(id):
    '''return user using his id'''
    pass

@router.get("/users")
async def get_all_users():
    '''return all users from the DB.
    results will be sent to the front-end to filer them'''
    pass


async def create_api_key():
    '''generate an api key for a user'''
    pass

# ----- Strategy Management -------

