import os
import base64
import requests
import logging

logger = logging.getLogger("google.antigravity.tools.zendesk")

class ZendeskClient:
    def __init__(self):
        self.subdomain = os.getenv("ZENDESK_SUBDOMAIN")
        self.email = os.getenv("ZENDESK_EMAIL")
        self.token = os.getenv("ZENDESK_TOKEN") or os.getenv("ZENDESK_API_KEY")
        
        if not self.subdomain or not self.email or not self.token:
            logger.error("Zendesk configuration missing (SUBDOMAIN/EMAIL/TOKEN)")
            self.auth_header = None
            return

        # Handle formatting token credentials
        formatted_email = self.email if self.email.endswith('/token') else f"{self.email}/token"
        auth_str = f"{formatted_email}:{self.token}"
        auth_bytes = auth_str.encode("utf-8")
        auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")
        self.auth_header = f"Basic {auth_b64}"
        self.base_url = f"https://{self.subdomain}.zendesk.com/api/v2"

    def update_ticket_with_summary(self, ticket_id, summary, status="open"):
        """Performs a Dual-PUT update on Zendesk tickets:
        1. Appends an internal (private) comment with the summary.
        2. Updates the ticket status.
        """
        if not self.auth_header:
            logger.error("Zendesk credentials not configured")
            return False

        headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            # Step 1: PUT Private Note (comment)
            private_note_payload = {
                "ticket": {
                    "comment": {
                        "body": f"AI RECEPTIONIST SUMMARY:\n{summary}",
                        "public": False
                    }
                }
            }
            url = f"{self.base_url}/tickets/{ticket_id}.json"
            logger.info(f"Writing Private Note to Zendesk Ticket {ticket_id}")
            r1 = requests.put(url, headers=headers, json=private_note_payload)
            r1.raise_for_status()

            # Step 2: PUT Status Update
            status_payload = {
                "ticket": {
                    "status": status
                }
            }
            logger.info(f"Setting Zendesk Ticket {ticket_id} status to '{status}'")
            r2 = requests.put(url, headers=headers, json=status_payload)
            r2.raise_for_status()

            logger.info("Successfully completed Dual-PUT Zendesk Sync")
            return True
        except Exception as e:
            logger.error(f"Zendesk sync failed for ticket {ticket_id}: {e}")
            return False

    def search_tickets_by_po(self, po_number):
        """Searches for tickets matching the given purchase order number."""
        if not self.auth_header:
            logger.error("Zendesk credentials not configured")
            return None

        headers = {
            "Authorization": self.auth_header,
            "Accept": "application/json"
        }

        url = f"{self.base_url}/search.json"
        params = {"query": f'type:ticket "{po_number}"'}
        try:
            logger.info(f"Searching Zendesk tickets for PO {po_number}")
            r = requests.get(url, headers=headers, params=params)
            r.raise_for_status()
            data = r.json()
            return data.get("results", [])
        except Exception as e:
            logger.error(f"Zendesk search failed for PO {po_number}: {e}")
            return None

