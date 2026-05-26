import os
import requests
import google.auth
from google.auth.transport.requests import Request
import logging

logger = logging.getLogger("google.antigravity.tools.sheets")

class SheetsClient:
    def __init__(self, spreadsheet_id=None):
        self.spreadsheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID")
        self._credentials = None

    def get_auth_token(self):
        """Obtains Google Access Token using Application Default Credentials."""
        if not self._credentials:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file'
            ]
            self._credentials, _ = google.auth.default(scopes=scopes)
        
        # Refresh token if expired
        if not self._credentials.valid:
            self._credentials.refresh(Request())
        
        return self._credentials.token

    def append_log(self, data, range_name="Sheet1!A1"):
        """Appends a new row to Google Sheets."""
        try:
            token = self.get_auth_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Row mapping exactly like the old sheets_client.js
            row_values = [
                data.get("name", ""),
                data.get("phone", ""),
                data.get("email", ""),
                data.get("purchase_order", ""),
                data.get("intent", "General Inquiry"),
                data.get("summary", ""),
                data.get("urgency", "low"),
                data.get("timestamp", ""),
                data.get("call_duration_seconds", ""),
                data.get("ticket_id", ""),
                data.get("session_id", "N/A"),
                data.get("crm_sync_status", "processing"),
                data.get("error_message", ""),
                data.get("sentiment", "neutral"),
                data.get("product_type", "")
            ]
            
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/{range_name}:append"
            params = {
                "valueInputOption": "USER_ENTERED",
                "insertDataOption": "INSERT_ROWS"
            }
            payload = {
                "values": [row_values]
            }
            
            response = requests.post(url, headers=headers, params=params, json=payload)
            response.raise_for_status()
            logger.info("Successfully logged lead to Google Sheets")
            return True
        except Exception as e:
            logger.error(f"Failed to write to Google Sheets: {e}")
            return False

    def upsert_log(self, data):
        """Checks for existing session_id in Column K and updates or appends."""
        session_id = data.get("session_id")
        if not session_id:
            return self.append_log(data)

        try:
            token = self.get_auth_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # Get all session_ids from Column K (11th column)
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/Sheet1!K:K"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            rows = response.json().get("values", [])
            row_index = -1
            for idx, row in enumerate(rows):
                if row and row[0] == session_id:
                    row_index = idx
                    break

            if row_index != -1:
                sheet_row = row_index + 1
                logger.info(f"Existing session found at row {sheet_row}, updating...")
                
                # Perform update on specific row
                row_values = [
                    data.get("name", ""),
                    data.get("phone", ""),
                    data.get("email", ""),
                    data.get("purchase_order", ""),
                    data.get("intent", "General Inquiry"),
                    data.get("summary", ""),
                    data.get("urgency", "low"),
                    data.get("timestamp", ""),
                    data.get("call_duration_seconds", ""),
                    data.get("ticket_id", ""),
                    data.get("session_id", "N/A"),
                    data.get("crm_sync_status", "updated"),
                    data.get("error_message", ""),
                    data.get("sentiment", "neutral"),
                    data.get("product_type", "")
                ]
                
                update_url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadsheet_id}/values/Sheet1!A{sheet_row}"
                update_params = {
                    "valueInputOption": "USER_ENTERED"
                }
                update_payload = {
                    "values": [row_values]
                }
                
                update_response = requests.put(
                    update_url, 
                    headers={**headers, "Content-Type": "application/json"}, 
                    params=update_params, 
                    json=update_payload
                )
                update_response.raise_for_status()
                return True

            return self.append_log(data)
        except Exception as e:
            logger.error(f"Upsert failed, falling back to append: {e}")
            return self.append_log(data)

    def log_failure(self, data, error_message):
        """Logs failures to the DLQ (FAILURES tab)."""
        failure_data = {
            **data,
            "crm_sync_status": "failed",
            "error_message": error_message
        }
        return self.append_log(failure_data, range_name="FAILURES!A1")
