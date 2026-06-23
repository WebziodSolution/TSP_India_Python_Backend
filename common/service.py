import os
import re
import uuid
import shutil
import pytz
import logging
from datetime import datetime
from PIL import Image
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

# Helper parameters
MAX_DIM = 1920

def get_file_directory():
    dir_path = getattr(settings, 'TIMESHEETPRO_DRIVE', '')
    if dir_path and not dir_path.endswith('/') and not dir_path.endswith('\\'):
        dir_path += '/'
    return dir_path

def get_image_context_path():
    path = getattr(settings, 'IMAGE_CONTEXT_PATH', '')
    if path and not path.endswith('/'):
        path += '/'
    return path

def sanitize_file_name(filename):
    return re.sub(r'[^a-zA-Z0-9\.\-]+', '_', filename)

def validate_extension(filename):
    dot = filename.rfind(".")
    if dot == -1:
        raise Exception("File has no extension")
    ext = filename[dot + 1:].lower()
    
    is_video = bool(re.match(r'^(mp4|mkv|avi|mov)$', ext))
    is_image = bool(re.match(r'^(jpg|jpeg|png)$', ext))
    
    if not (is_image or is_video):
        raise Exception(f".{ext} File type not supported")
    return is_image, is_video

def optimize_image(input_file_path):
    try:
        with Image.open(input_file_path) as img:
            ext = os.path.splitext(input_file_path)[1].lower()
            width, height = img.size
            max_side = max(width, height)
            
            # Do not upscale or resize if smaller
            if max_side <= MAX_DIM:
                return input_file_path
                
            scale = float(MAX_DIM) / max_side
            new_width = int(round(width * scale))
            new_height = int(round(height * scale))
            
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            out_file_path = os.path.join(
                os.path.dirname(input_file_path),
                "opt_" + os.path.basename(input_file_path)
            )
            
            if ext in [".jpg", ".jpeg"]:
                resized_img.convert("RGB").save(out_file_path, "JPEG", quality=60)
            elif ext == ".png":
                resized_img.save(out_file_path, "PNG")
            else:
                return input_file_path
                
            return out_file_path
    except Exception as e:
        logger.error(f"Error optimizing image: {e}")
        return input_file_path

# Service Operations
class CommonService:
    def start_upload(self, folder_name: str, user_id: int, file_name: str) -> dict:
        last_dot = file_name.rfind(".")
        if last_dot == -1:
            raise Exception("File has no extension")
            
        ext = file_name[last_dot + 1:].lower()
        if not re.match(r'^(jpg|jpeg|png)$', ext):
            raise Exception("Only JPG, JPEG, PNG images are allowed")
            
        safe_file_name = sanitize_file_name(file_name)
        upload_id = str(uuid.uuid4())
        
        file_dir = get_file_directory()
        chunk_dir_path = os.path.join(file_dir, str(user_id or "global"), "tempImage", folder_name, "chunks", upload_id)
        os.makedirs(chunk_dir_path, exist_ok=True)
        
        return {
            "uploadId": upload_id,
            "fileName": safe_file_name
        }

    def upload_chunk(self, folder_name: str, user_id: int, upload_id: str, chunk_index: int, total_chunks: int, original_file_name: str, chunk_file) -> dict:
        safe_name = sanitize_file_name(original_file_name)
        validate_extension(safe_name)
        
        file_dir = get_file_directory()
        chunk_dir_path = os.path.join(file_dir, str(user_id or "global"), "tempImage", folder_name, "chunks", upload_id)
        os.makedirs(chunk_dir_path, exist_ok=True)
        
        chunk_file_path = os.path.join(chunk_dir_path, f"{chunk_index}.part")
        try:
            with open(chunk_file_path, "wb+") as destination:
                for chunk in chunk_file.chunks():
                    destination.write(chunk)
        except Exception as e:
            raise Exception(f"Failed to save chunk {chunk_index}: {str(e)}")
            
        return {
            "chunkIndex": chunk_index,
            "totalChunks": total_chunks
        }

    def complete_upload(self, folder_name: str, user_id: int, upload_id: str, total_chunks: int, original_file_name: str) -> dict:
        safe_name = sanitize_file_name(original_file_name)
        validate_extension(safe_name)
        
        file_dir = get_file_directory()
        base_dir = os.path.join(file_dir, str(user_id or "global"), "tempImage", folder_name)
        os.makedirs(base_dir, exist_ok=True)
        
        chunk_dir_path = os.path.join(base_dir, "chunks", upload_id)
        if not os.path.exists(chunk_dir_path):
            raise Exception("Chunk directory not found")
            
        final_file_path = os.path.join(base_dir, safe_name)
        if os.path.exists(final_file_path):
            os.remove(final_file_path)
            
        # Merge chunks
        try:
            with open(final_file_path, "ab") as merged_file:
                for i in range(total_chunks):
                    part_path = os.path.join(chunk_dir_path, f"{i}.part")
                    if not os.path.exists(part_path):
                        raise Exception(f"Missing chunk: {i}")
                    with open(part_path, "rb") as part_file:
                        merged_file.write(part_file.read())
        except Exception as e:
            raise Exception(f"Failed to merge chunks: {str(e)}")
            
        # Optimize image
        optimized_path = optimize_image(final_file_path)
        if optimized_path != final_file_path:
            os.remove(final_file_path)
            os.rename(optimized_path, final_file_path)
            
        # Clean up chunk folder
        shutil.rmtree(chunk_dir_path, ignore_errors=True)
        
        # Build URL
        context_path = get_image_context_path()
        rel_url = f"{user_id or 'global'}/tempImage/{folder_name}/{safe_name}"
        file_url = context_path + rel_url
        
        return {
            "uploadedFiles": [
                {
                    "imageName": safe_name,
                    "imageURL": file_url
                }
            ]
        }

    def upload_files(self, files: list, login_user_id: int, folder_name: str) -> dict:
        uploaded_files = []
        try:
            file_dir = get_file_directory()
            dynamic_path = f"{login_user_id or 'global'}/tempImage/{folder_name}/"
            target_dir = os.path.join(file_dir, dynamic_path)
            os.makedirs(target_dir, exist_ok=True)
            
            for file in files:
                original_filename = sanitize_file_name(file.name)
                is_image, is_video = validate_extension(original_filename)
                
                full_path = os.path.join(target_dir, original_filename)
                with open(full_path, "wb+") as dest:
                    for chunk in file.chunks():
                        dest.write(chunk)
                        
                context_path = get_image_context_path()
                file_url = context_path + dynamic_path + original_filename
                
                uploaded_files.append({
                    "imageName": original_filename,
                    "imageURL": file_url,
                    "fileType": "video" if is_video else "image"
                })
                
            return {
                "uploadedFiles": uploaded_files,
                "status": 200
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def update_file_location_for_profile(self, image: str, login_user_id: int, folder_name: str) -> str:
        arr = image.split("/")
        original_file_name = arr[-1]
        
        file_dir = get_file_directory()
        temp_dir = os.path.join(file_dir, str(login_user_id or "global"), "tempImage", folder_name)
        dest_dir = os.path.join(file_dir, str(login_user_id or "global"), folder_name)
        
        os.makedirs(dest_dir, exist_ok=True)
        
        source_file = os.path.join(temp_dir, original_file_name)
        destination_file = os.path.join(dest_dir, original_file_name)
        
        if os.path.exists(source_file):
            try:
                shutil.copy2(source_file, destination_file)
                image_dynamic_path = f"{login_user_id or 'global'}/{folder_name}/{original_file_name}"
                shutil.rmtree(temp_dir, ignore_errors=True)
                
                context_path = get_image_context_path()
                return context_path + image_dynamic_path
            except Exception as e:
                raise Exception(f"File move error: {str(e)}")
        else:
            return "Error"

    def delete_directory_recursively(self, directory_path: str):
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path, ignore_errors=True)

    def convert_string_to_date(self, date_str: str) -> datetime:
        if not date_str or not date_str.strip():
            return None
            
        date_str = date_str.strip()
        
        # Handle ISO strings like 2026-01-31T08:34:45.622Z
        if "T" in date_str:
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            try:
                # Limit microsecond digits to 6
                parts = date_str.split('.')
                if len(parts) > 1 and '+' in parts[1]:
                    subparts = parts[1].split('+')
                    if len(subparts[0]) > 6:
                        parts[1] = subparts[0][:6] + '+' + subparts[1]
                        date_str = parts[0] + '.' + parts[1]
                return datetime.fromisoformat(date_str)
            except Exception:
                pass
                
        formats = [
            "%d/%m/%Y, %I:%M:%S %p",
            "%d/%m/%Y, %H:%M:%S",
            "%d/%m/%Y",
            "%Y-%m-%d"
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.replace(tzinfo=pytz.UTC)
            except ValueError:
                continue
                
        raise Exception(f"Error converting date: {date_str} - format not matched")

    def convert_utc_to_local(self, utc_time: str, time_zone: str) -> str:
        if not utc_time:
            return None
        try:
            fmt = "%d/%m/%Y, %I:%M:%S %p" if ("am" in utc_time.lower() or "pm" in utc_time.lower()) else "%d/%m/%Y, %H:%M:%S"
            dt = datetime.strptime(utc_time, fmt)
            dt_utc = pytz.utc.localize(dt)
            local_tz = pytz.timezone(time_zone)
            dt_local = dt_utc.astimezone(local_tz)
            return dt_local.strftime("%d/%m/%Y, %I:%M:%S %p")
        except Exception as e:
            logger.error(f"Error parsing time: {e}")
            return None

    def convert_local_to_utc(self, local_date: str, time_zone: str, has_time: bool) -> datetime:
        try:
            if has_time and ":" in local_date:
                fmt = "%d/%m/%Y, %H:%M:%S"
                dt = datetime.strptime(local_date, fmt)
                local_tz = pytz.timezone(time_zone)
                dt_local = local_tz.localize(dt)
                return dt_local.astimezone(pytz.utc)
            else:
                fmt = "%d/%m/%Y"
                dt = datetime.strptime(local_date, fmt)
                local_tz = pytz.timezone(time_zone)
                # At start of day
                dt_local = local_tz.localize(datetime.combine(dt.date(), datetime.min.time()))
                return dt_local.astimezone(pytz.utc)
        except Exception as e:
            raise Exception(f"Error converting local date time to UTC: {str(e)}")

    def convert_date_to_string(self, date_obj: datetime, time_zone: str = "UTC") -> str:
        if not date_obj:
            return None
        try:
            if not isinstance(date_obj, datetime):
                # If it's a date object and not datetime, format directly
                return date_obj.strftime("%d/%m/%Y")
            if date_obj.tzinfo is None:
                date_obj = pytz.utc.localize(date_obj)
            tz = pytz.timezone(time_zone)
            date_tz = date_obj.astimezone(tz)
            return date_tz.strftime("%d/%m/%Y, %I:%M:%S %p")
        except Exception as e:
            logger.error(f"Error converting date to string: {e}")
            return None


    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        try:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
            send_mail(
                subject=subject,
                message=body,
                from_email=from_email,
                recipient_list=[to_email],
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f"Email send error: {str(e)}")
            return False
