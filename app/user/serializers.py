from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the users object
    """
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update the authenticated user data """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication object """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    """ any field that makes up the serializer will be passed into the validate
    function as attrs dictionary.
    retrieve the fields,
    validate the fields.
    """

    def validate(self, attrs):
        """ Validate and authenticate the user """
        email = attrs.get('email')
        password = attrs.get('password')
        """
            we will pass the serializer into our view set
            what the django rest framework viewset does ->
            when a request is made, it passes the context into the
            serializer in this context class variable.
            from that we can get hold of the request that was made.
        """
        user = authenticate(request=self.context.get('request'),
                            username=email, password=password)

        if not user:
            msg = _('Unable to Authenticate with provided credential')
            """
            Django rest framework knows how to handle this error.
            it handles it by passing error as 400 response
            and display this msg.
            """
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user

        return attrs
