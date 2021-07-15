from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from superhero import serializers
from superhero.models import Superhero 

# Create your views here.

class SuperheroeApi(APIView):
    serializer_class = serializers.SuperheroSerializer

    def get(self, req):
        superheroes = Superhero.objects.all()
        serializer = self.serializer_class(superheroes, many=True)
        return Response({'superheroes': serializer.data}, status=status.HTTP_200_OK)
        
    def post(self, req):
        serializer = self.serializer_class(data=req.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            publisher =  serializer.validated_data.get('publisher')
            public = serializer.validated_data.get('public')

            superhero = Superhero(
                name = name,
                publisher = publisher,
                public = public
            )
            superhero.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

    def put(self, req, id=None):
        serializer = self.serializer_class(data=req.data)

        if serializer.is_valid() and id:
            name = serializer.validated_data.get('name')
            publisher =  serializer.validated_data.get('publisher')
            public = serializer.validated_data.get('public')
            
            superhero = Superhero.objects.get(pk=id)
            superhero.name = name
            superhero.publisher = publisher
            superhero.public = public
            superhero.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
    def delete(self, req, id=None):
        serializer = self.serializer_class(data=req.data)

        if serializer.is_valid() and id:
            superhero = Superhero.objects.get(pk=id)
            superhero.delete()

            serializer = self.serializer_class(superhero)
            
            return Response({'superheroes': serializer.data, 'status': 'deleted'}, status=status.HTTP_200_OK)
        
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
