#!-*- coding: utf-8 -*-
"""
Authentication backend for handling firebase user.idToken from incoming
Authorization header, verifying, and locally authenticating

This package are published as free software under the terms of the Apache License, Version 2.0. Is developed by
Dirección de Gobierno Digital of the Secretaría de Innovación y Gobierno Abierto of Municipality of Monterrey.

Authors: ['Gary Burgmann', 'César Benjamín García Martínez <mathereall@gmail.com>']
Email: gobierno.digital@monterrey.gob.mx
GitHub: https://github.com/gobiernodigitalmonterrey/gdmty-drf-firebase-auth
Package: gdmty_drf_firebase_auth
PyPi: https://pypi.org/project/gdmty-drf-firebase-auth/
"""

from typing import Tuple, Dict
import logging
import firebase_admin
from firebase_admin import auth as firebase_auth
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication, exceptions
from .settings import api_settings
from django.conf import settings
from .models import FirebaseUser, FirebaseUserProvider
from .utils import get_firebase_user_email
from . import __title__
import json

log = logging.getLogger(__title__)
User = get_user_model()

firebase_instances = {}

for index, project in enumerate(api_settings.FIREBASE_AUTH_PROJECTS):
    log.info(index, project)
    if index == 0:
        default_credentials = firebase_admin.credentials.Certificate(project['SERVICE_ACCOUNT'])
        firebase_admin.initialize_app(credential=default_credentials)
    credentials = firebase_admin.credentials.Certificate(project['SERVICE_ACCOUNT'])
    firebase_instances[project['PROJECT_ID']] = firebase_admin.initialize_app(credentials,
                                                                              {'projectId': project['PROJECT_ID']},
                                                                              name=project['PROJECT_ID']
                                                                              )


class FirebaseAuthentication(authentication.TokenAuthentication):
    """
    Token based authentication using firebase.
    """
    keyword = api_settings.FIREBASE_AUTH_HEADER_PREFIX
    current_firebase_user_app = None

    def authenticate_credentials(self, token: str) -> Tuple[AnonymousUser, Dict]:
        try:
            decoded_token = self._decode_token(token)
            firebase_user = self._authenticate_token(decoded_token)
            local_user = self._get_or_create_local_user(firebase_user)
            self._create_local_firebase_user(local_user, firebase_user)
            return local_user, decoded_token
        except Exception as e:
            if settings.DEBUG:
                raise exceptions.AuthenticationFailed(e)

    def _decode_token(self, token: str) -> Dict:
        """
        Attempt to verify JWT from Authorization header with Firebase and return the decoded token
        """
        for account in api_settings.FIREBASE_AUTH_PROJECTS:
            try:
                self.current_firebase_user_app = firebase_instances[account['PROJECT_ID']]
                decoded_token = firebase_auth.verify_id_token(token, app=self.current_firebase_user_app, check_revoked=api_settings.FIREBASE_CHECK_JWT_REVOKED)
                log.info(f'_decode_token - decoded_token: {decoded_token}')
                return decoded_token
            except Exception as e:
                log.error(f'_decode_token - Exception: {e}')
                # Continuar con el siguiente intento de verificación
        if settings.DEBUG:
            log.error(f'Invalid AccessToken')
            raise Exception("Invalid AccessToken")

    def _authenticate_token(self, decoded_token: Dict) -> firebase_auth.UserRecord:
        """ Returns firebase user if token is authenticated """
        try:
            uid = decoded_token.get('uid')
            log.info(f'_authenticate_token - uid: {uid}')
            firebase_user = firebase_auth.get_user(uid, app=self.current_firebase_user_app)
            log.info(f'_authenticate_token - firebase_user: {firebase_user}')
            if api_settings.FIREBASE_AUTH_EMAIL_VERIFICATION:
                if not firebase_user.email_verified:
                    if settings.DEBUG:
                        raise Exception('Email address of this user has not been verified.')
            return firebase_user
        except Exception as e:
            log.error(f'_authenticate_token - Exception: {e}')
            if settings.DEBUG:
                raise Exception(e)

    @staticmethod
    def _get_or_create_local_user(firebase_user: firebase_auth.UserRecord) -> User:
        """
        Attempts to return or create a local User from Firebase user data
        """
        email = get_firebase_user_email(firebase_user)
        log.info(f'_get_or_create_local_user - email: {email}')
        try:
            user = User.objects.get(email=email)
            log.info(
                f'_get_or_create_local_user - user.is_active: {user.is_active}'
            )
            if not user.is_active:
                if settings.DEBUG:
                    raise Exception('User account is not currently active.')
            user.last_login = timezone.now()
            user.save()
        except User.DoesNotExist:
            log.error(
                f'_get_or_create_local_user - User.DoesNotExist: {email}'
            )
            if not api_settings.FIREBASE_CREATE_LOCAL_USER:
                if settings.DEBUG:
                    raise Exception('User is not registered to the application.')
            username = api_settings.FIREBASE_USERNAME_MAPPING_FUNC(firebase_user)
            log.info(f'_get_or_create_local_user - username: {username}')
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email
                )
                user.last_login = timezone.now()
                if (
                        api_settings.FIREBASE_ATTEMPT_CREATE_WITH_DISPLAY_NAME
                        and firebase_user.display_name is not None
                ):
                    display_name = firebase_user.display_name.split(' ')
                    if len(display_name) == 2:
                        user.first_name = display_name[0]
                        user.last_name = display_name[1]
                user.save()
            except Exception as e:
                if settings.DEBUG:
                    raise Exception(e)
        return user

    @staticmethod
    def _create_local_firebase_user(user: User, firebase_user: firebase_auth.UserRecord):
        """ Create a local FireBase model if one does not already exist """
        # pylint: disable=no-member
        local_firebase_user = FirebaseUser.objects.filter(
            user=user
        ).first()

        if not local_firebase_user:
            new_firebase_user = FirebaseUser(
                uid=firebase_user.uid,
                user=user
            )
            new_firebase_user.save()
            local_firebase_user = new_firebase_user

        if local_firebase_user.uid != firebase_user.uid:
            local_firebase_user.uid = firebase_user.uid
            local_firebase_user.save()

        # store FirebaseUserProvider data
        for provider in firebase_user.provider_data:
            local_provider = FirebaseUserProvider.objects.filter(
                provider_id=provider.provider_id,
                firebase_user=local_firebase_user
            ).first()
            if not local_provider:
                new_local_provider = FirebaseUserProvider.objects.create(
                    provider_id=provider.provider_id,
                    uid=provider.uid,
                    firebase_user=local_firebase_user,
                )
                new_local_provider.save()

        # catch locally stored providers no longer associated at Firebase
        local_providers = FirebaseUserProvider.objects.filter(
            firebase_user=local_firebase_user
        )
        if len(local_providers) != len(firebase_user.provider_data):
            current_providers = \
                [x.provider_id for x in firebase_user.provider_data]
            for provider in local_providers:
                if provider.provider_id not in current_providers:
                    FirebaseUserProvider.objects.filter(
                        id=provider.id
                    ).delete()
