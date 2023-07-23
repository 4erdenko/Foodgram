from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


class CreateDeleteMixin:
    """
    A mixin class that provides `create_item` and `delete_item` methods.
    These methods are used to create and delete instances of specified models.
    """

    def create_item(self, serializer_class, data, request):
        """
        Creates an instance of a specified model using the given serializer
        class and data.

        Args:
            serializer_class (Serializer): The serializer class to be used.
            data (dict): The data to be passed to the serializer.
            request (Request): The HTTP request object.

        Returns:
            Response: Response with a status of 201 (created).
        """
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete_item(self, model, **kwargs):
        """
        Deletes an instance of a specified model given its
        identifying attributes.

        Args:
            model (Model): The Django model class.
            **kwargs: The attributes identifying the model
            instance to be deleted.

        Returns:
            Response: Response with a status of 204 (no content).
        """
        get_object_or_404(model, **kwargs).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
