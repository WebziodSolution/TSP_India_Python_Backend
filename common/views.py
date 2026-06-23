from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from common.response.api_response import ApiResponse
from common.service import CommonService
from common.swagger_utils import (
    get_api_response_serializer,
    StartUploadSerializer,
    UploadChunkSerializer,
    CompleteUploadSerializer
)

common_service = CommonService()

@extend_schema(
    summary="Start Chunked Upload",
    description="Initiate a chunked file upload sequence.",
    request=StartUploadSerializer,
    responses={
        200: get_api_response_serializer(name="StartUploadResponse"),
        400: get_api_response_serializer(name="InvalidRequest"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def start_upload(request):
    try:
        # Check both POST data and query params
        folder_name = request.data.get('folderName') or request.query_params.get('folderName')
        user_id = request.data.get('userId') or request.query_params.get('userId')
        file_name = request.data.get('fileName') or request.query_params.get('fileName')
        
        if not folder_name or not file_name:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "folderName and fileName are required", None)
            
        u_id = int(user_id) if user_id else None
        res = common_service.start_upload(folder_name, u_id, file_name)
        return ApiResponse(status.HTTP_200_OK, "Upload started", res)
    except Exception as e:
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), None)

@extend_schema(
    summary="Upload Chunk",
    description="Upload an individual file chunk.",
    request=UploadChunkSerializer,
    responses={
        200: get_api_response_serializer(name="UploadChunkResponse"),
        400: get_api_response_serializer(name="InvalidRequest"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_chunk(request):
    try:
        folder_name = request.data.get('folderName')
        user_id = request.data.get('userId')
        upload_id = request.data.get('uploadId')
        chunk_index = request.data.get('chunkIndex')
        total_chunks = request.data.get('totalChunks')
        original_file_name = request.data.get('originalFileName')
        chunk = request.FILES.get('chunk')
        
        if not all([folder_name, upload_id, chunk_index, total_chunks, original_file_name, chunk]):
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Missing required parameters", None)
            
        u_id = int(user_id) if user_id else None
        c_idx = int(chunk_index)
        t_chunks = int(total_chunks)
        
        res = common_service.upload_chunk(
            folder_name, u_id, upload_id,
            c_idx, t_chunks, original_file_name, chunk
        )
        return ApiResponse(status.HTTP_200_OK, "Chunk uploaded", res)
    except Exception as e:
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), None)

@extend_schema(
    summary="Complete Chunked Upload",
    description="Complete a chunked upload sequence and merge the uploaded chunks.",
    request=CompleteUploadSerializer,
    responses={
        200: get_api_response_serializer(name="CompleteUploadResponse"),
        400: get_api_response_serializer(name="InvalidRequest"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def complete_upload(request):
    try:
        folder_name = request.data.get('folderName') or request.query_params.get('folderName')
        user_id = request.data.get('userId') or request.query_params.get('userId')
        upload_id = request.data.get('uploadId') or request.query_params.get('uploadId')
        total_chunks = request.data.get('totalChunks') or request.query_params.get('totalChunks')
        original_file_name = request.data.get('originalFileName') or request.query_params.get('originalFileName')
        
        if not all([folder_name, upload_id, total_chunks, original_file_name]):
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Missing required parameters", None)
            
        u_id = int(user_id) if user_id else None
        t_chunks = int(total_chunks)
        
        res = common_service.complete_upload(
            folder_name, u_id, upload_id, t_chunks, original_file_name
        )
        return ApiResponse(status.HTTP_200_OK, "File merged successfully", res)
    except Exception as e:
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), None)

@extend_schema(
    summary="Get Timezones",
    description="Retrieve a list of all supported timezones.",
    responses={
        200: get_api_response_serializer(serializers.ListField(child=serializers.CharField()), name="TimezonesList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_timezones(request):
    try:
        timezone_list = [
            "Asia/Kolkata",
            "Asia/Dubai",
            "Europe/London",
            "Australia/Sydney",
            "America/Adak",
            "America/Anchorage",
            "America/Anguilla",
            "America/Antigua",
            "America/Araguaina",
            "America/Argentina/Buenos_Aires",
            "America/Argentina/Catamarca",
            "America/Argentina/ComodRivadavia",
            "America/Argentina/Cordoba",
            "America/Argentina/Jujuy",
            "America/Argentina/La_Rioja",
            "America/Argentina/Mendoza",
            "America/Argentina/Rio_Gallegos",
            "America/Argentina/Salta",
            "America/Argentina/San_Juan",
            "America/Argentina/San_Luis",
            "America/Argentina/Tucuman",
            "America/Argentina/Ushuaia",
            "America/Aruba",
            "America/Asuncion",
            "America/Atikokan",
            "America/Atka",
            "America/Bahia",
            "America/Bahia_Banderas",
            "America/Barbados",
            "America/Belem",
            "America/Belize",
            "America/Blanc-Sablon",
            "America/Boa_Vista",
            "America/Bogota",
            "America/Boise",
            "America/Buenos_Aires",
            "America/Cambridge_Bay",
            "America/Campo_Grande",
            "America/Cancun",
            "America/Caracas",
            "America/Catamarca",
            "America/Cayenne",
            "America/Cayman",
            "America/Chicago",
            "America/Chihuahua",
            "America/Ciudad_Juarez",
            "America/Coral_Harbour",
            "America/Cordoba",
            "America/Costa_Rica",
            "America/Creston",
            "America/Cuiaba",
            "America/Curacao",
            "America/Danmarkshavn",
            "America/Dawson",
            "America/Dawson_Creek",
            "America/Denver",
            "America/Detroit",
            "America/Dominica",
            "America/Edmonton",
            "America/Eirunepe",
            "America/El_Salvador",
            "America/Ensenada",
            "America/Fort_Nelson",
            "America/Fort_Wayne",
            "America/Fortaleza",
            "America/Glace_Bay",
            "America/Godthab",
            "America/Goose_Bay",
            "America/Grand_Turk",
            "America/Grenada",
            "America/Guadeloupe",
            "America/Guatemala",
            "America/Guayaquil",
            "America/Guyana",
            "America/Halifax",
            "America/Havana",
            "America/Hermosillo",
            "America/Indiana/Indianapolis",
            "America/Indiana/Knox",
            "America/Indiana/Marengo",
            "America/Indiana/Petersburg",
            "America/Indiana/Tell_City",
            "America/Indiana/Vevay",
            "America/Indiana/Vincennes",
            "America/Indiana/Winamac",
            "America/Indianapolis",
            "America/Inuvik",
            "America/Iqaluit",
            "America/Jamaica",
            "America/Jujuy",
            "America/Juneau",
            "America/Kentucky/Louisville",
            "America/Kentucky/Monticello",
            "America/Knox_IN",
            "America/Kralendijk",
            "America/La_Paz",
            "America/Lima",
            "America/Los_Angeles",
            "America/Louisville",
            "America/Lower_Princes",
            "America/Maceio",
            "America/Managua",
            "America/Manaus",
            "America/Marigot",
            "America/Martinique",
            "America/Matamoros",
            "America/Mazatlan",
            "America/Mendoza",
            "America/Menominee",
            "America/Merida",
            "America/Metlakatla",
            "America/Mexico_City",
            "America/Miquelon",
            "America/Moncton",
            "America/Monterrey",
            "America/Montevideo",
            "America/Montreal",
            "America/Montserrat",
            "America/Nassau",
            "America/New_York",
            "America/Nipigon",
            "America/Nome",
            "America/Noronha",
            "America/North_Dakota/Beulah",
            "America/North_Dakota/Center",
            "America/North_Dakota/New_Salem",
            "America/Nuuk",
            "America/Ojinaga",
            "America/Panama",
            "America/Pangnirtung",
            "America/Paramaribo",
            "America/Phoenix",
            "America/Port_of_Spain",
            "America/Port-au-Prince",
            "America/Porto_Acre",
            "America/Porto_Velho",
            "America/Puerto_Rico",
            "America/Punta_Arenas",
            "America/Rainy_River",
            "America/Rankin_Inlet",
            "America/Recife",
            "America/Regina",
            "America/Resolute",
            "America/Rio_Branco",
            "America/Rosario",
            "America/Santa_Isabel",
            "America/Santarem",
            "America/Santiago",
            "America/Santo_Domingo",
            "America/Sao_Paulo",
            "America/Scoresbysund",
            "America/Shiprock",
            "America/Sitka",
            "America/St_Barthelemy",
            "America/St_Johns",
            "America/St_Kitts",
            "America/St_Lucia",
            "America/St_Thomas",
            "America/St_Vincent",
            "America/Swift_Current",
            "America/Tegucigalpa",
            "America/Thule",
            "America/Thunder_Bay",
            "America/Tijuana",
            "America/Toronto",
            "America/Tortola",
            "America/Vancouver",
            "America/Virgin",
            "America/Whitehorse",
            "America/Winnipeg",
            "America/Yakutat"
        ]
        return ApiResponse(
            status.HTTP_200_OK,
            "Time Zones fetched successfully",
            timezone_list
        )
    except Exception as e:
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), [])
