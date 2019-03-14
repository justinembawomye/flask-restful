from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel
from flask_jwt_extended import(create_access_token, create_refresh_token, jwt_required,jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":f"User {data['username']} already exists!"}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username']) 
            return {
                "message":f"user {data['username']} has successfully created an account!",
                "access_token":access_token,
                "refresh_token":refresh_token
            },201
        except:
            return {"message":"Failed to create user"}, 500    
        return data

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return{"message":f"User {data['username']} doesnot exist"}
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token= create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                "message":f"You are logged in as {data['username']}",
                "access_token":access_token,
                "refresh_token":refresh_token
      } 
        else:
            return {"message":"Wrong credentials! Please check your username and password!"}   

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message":"Access token has been revoked"}
        except:
            return {"message":"Something went wrong"}, 500

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message":"Refresh token has been revoked"}
        except:
            return {"message":"Something went wrong"}, 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token":access_token}

class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    def delete(self):
        return UserModel.delete_all()   

class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            "answer":42
        }

parser = reqparse.RequestParser()
parser.add_argument('username', help="This field cannot be blank", required=True)
parser.add_argument("password", help="This field cannot be blank", required=True)

