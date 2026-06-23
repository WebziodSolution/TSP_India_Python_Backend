from rest_framework import serializers

class CompanyReportResponseSerializer(serializers.Serializer):
    content = serializers.JSONField(required=False, allow_null=True)  # Nested: List<CompanyReportDto>
    totalPages = serializers.IntegerField(required=False, allow_null=True)
    currentPage = serializers.IntegerField(required=False, allow_null=True)
    nextPage = serializers.IntegerField(required=False, allow_null=True)
    numberOfElements = serializers.IntegerField(required=False, allow_null=True)
    last = serializers.BooleanField(default=False)
    sortDirection = serializers.CharField(required=False, allow_null=True)
