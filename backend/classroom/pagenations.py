from rest_framework.pagination import PageNumberPagination


class ClassRoomSetPagination(PageNumberPagination):
    page_size = 20


class ChatHistorySetPagination(PageNumberPagination):
    page_size = 50

class DefaultSetPagination(PageNumberPagination):
    page_size = 15