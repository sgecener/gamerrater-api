from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game
from .categories import CategorySerializer


class GameSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)


    class Meta:
        model = Game
        fields = ['id', 'title', 'designer', 'year', 'number_of_players', 'play_time', 'age', 'categories']


class GameViewSet(viewsets.ViewSet):

    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        title = request.data.get('title')
        designer = request.data.get('designer')
        isbn_number = request.data.get('isbn_number')
        cover_image = request.data.get('cover_image')

        # Create a book database row first, so you have a
        # primary key to work with
        game = Game.objects.create(
            user=request.user,
            title=title,
            designer=designer,
            cover_image=cover_image,
            isbn_number=isbn_number)

        # Establish the many-to-many relationships
        category_ids = request.data.get('categories', [])
        game.categories.set(category_ids)

        serializer = GameSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:

            game = Game.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this book?
            self.check_object_permissions(request, book)

            serializer = GameSerializer(data=request.data)
            if serializer.is_valid():
                game.title = serializer.validated_data['title']
                game.author = serializer.validated_data['author']
                game.isbn_number = serializer.validated_data['isbn_number']
                game.cover_image = serializer.validated_data['cover_image']
                game.save()

                category_ids = request.data.get('categories', [])
                game.categories.set(category_ids)

                serializer = GameSerializer(game, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            self.check_object_permissions(request, game)
            game.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)