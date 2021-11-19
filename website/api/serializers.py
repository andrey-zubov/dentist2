from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from website.models import MessageModel, Administrator, Client

from rest_framework import serializers


class MessageModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    recipient = serializers.CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user)
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')


class ClientModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Client
        fields = ('username',)


class AdministratorModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Administrator
        fields = ('username',)
