# from django.shortcuts import render

# Create your views here.
# example of api endpoint documentation


# class Random(APIView):

#     @swagger_auto_schema(
#         operation_description=""" This API view contains a get function that displays all books.

#             Attributes:
#                 refresh_token (string): This is a valid user refresh token that provided on login.

#             Handles GET requests and returns a Response.
#                 Args:
#                     request (Request): The HTTP request object.

#                 Returns:
#                     Response: A JsonResponse and a status code indicating the successful query of books or 
                        # any other error.""",
#         responses={
#             200: openapi.Response(
#                 description="Get books successful",
#                 schema=  BookSerializer(),
#                 examples={
#                     "application/json": 
#                     BookSerializer(Book.objects.first()).data,                  
#                 },
#             ),
#               404: openapi.Response(
#                 description="Get books failed",
#                 examples={
#                     "application/json":
#                    {"message":"Books not found"}
#                 },
#             )
#         },
#         operation_summary="Getting Books list",
#     )
#     def get(self, request, *args, **kwargs):

#         data= Book.objects.all().values()
#         serializer = BookSerializer(data=Book.objects.first())
#         serializer.is_valid(raise_exception=True)

#         return Response(data, status=status.HTTP_200_OK
#         )
