from rest_framework.pagination import Cursor, CursorPagination

class TaskCursorPagination(CursorPagination):
    page_size = 2
    ordering = "-created_at"