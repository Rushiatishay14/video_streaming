from rest_framework import serializers
from .models import UserMaster



class UserSerializers(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def create_or_update_instance(self, validated_data):
        first_name = validated_data.get("first_name", None)
        last_name = validated_data.get("last_name", None)
        password = validated_data.get("password", None)
        email = validated_data.get("email", None)

        user_obj, created = UserMaster.objects.get_or_create(email=email, defaults={"first_name": first_name, "last_name": last_name})
        
        # Update the user's first name and last name
        if not created:
            user_obj.first_name = first_name
            user_obj.last_name = last_name

        # Set the password and save the user object
        user_obj.set_password(password)
        user_obj.save()

        return validated_data
            