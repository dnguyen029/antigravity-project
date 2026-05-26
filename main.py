import os
import sys
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from tools.sheets import SheetsClient
from tools.zendesk import ZendeskClient

# Set up standard logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("receptionist")

# Simple helper to load the .env file variables
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

# Load env variables immediately
load_env()

# ==========================================
# 🌐 WEBHOOK SERVER MODE (For CX Studio)
# ==========================================
class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to use standard logging instead of printing to stderr
        logger.info("%s - - %s" % (self.address_string(), format%args))

    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Antigravity Receptionist Webhook is LIVE")

    def do_POST(self):
        if self.path in ["/webhook/write-to-sheets", "/log_lead"]:
            try:
                # 1. Parse JSON body
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8'))
                
                logger.info(f"Received log_lead webhook request for session: {payload.get('session_id')}")

                # 2. Sync to Sheets (Upsert to prevent duplicates)
                sheets = SheetsClient()
                sheets_success = sheets.upsert_log(payload)

                # 3. Sync to Zendesk (Dual-PUT status update)
                zendesk_success = False
                ticket_id = payload.get("ticket_id")
                if ticket_id and payload.get("summary"):
                    zendesk = ZendeskClient()
                    urgency = payload.get("urgency", "low")
                    status = "open" if urgency == "high" else "pending"
                    zendesk_success = zendesk.update_ticket_with_summary(
                        ticket_id=ticket_id,
                        summary=payload.get("summary"),
                        status=status
                    )

                # 4. Respond to CX Studio
                sync_status = "synced_all" if (sheets_success and zendesk_success) else "synced_partial"
                response_data = {
                    "success": sheets_success,
                    "session_id": payload.get("session_id", "unknown"),
                    "sync_status": sync_status
                }
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))

            except Exception as e:
                logger.error(f"Error handling webhook request: {e}")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8080):
    server = HTTPServer(("0.0.0.0", port), WebhookHandler)
    logger.info(f"🚀 Decoupled Receptionist server listening on port {port}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down.")

# ==========================================
# 🤖 INTERACTIVE AGENT MODE (Antigravity SDK)
# ==========================================
async def run_interactive_agent():
    # Only import SDK inside this function to keep server startup fast and lightweight
    import asyncio
    from google.antigravity import Agent, LocalAgentConfig
    
    # 1. Load instructions from Phase 2
    instr_path = os.path.join(os.path.dirname(__file__), "instructions", "receptionist.txt")
    with open(instr_path, "r") as f:
        system_instructions = f.read()

    # 2. Define custom logger tool for the local SDK agent to call
    def log_lead_tool(name: str, phone: str, email: str, purchase_order: str = "", intent: str = "General Inquiry", summary: str = "", urgency: str = "low") -> str:
        """Logs the collected lead data into the Google Sheets database and Syncs to Zendesk."""
        payload = {
            "name": name,
            "phone": phone,
            "email": email,
            "purchase_order": purchase_order,
            "intent": intent,
            "summary": summary,
            "urgency": urgency,
            "session_id": "interactive-debug-session",
            "timestamp": "now"
        }
        
        # Write to sheets
        sheets = SheetsClient()
        sheets.upsert_log(payload)
        
        return json.dumps({"success": True, "message": "Lead logged successfully"})

    # 3. Configure the local agent
    config = LocalAgentConfig(
        system_instructions=system_instructions,
        tools=[log_lead_tool]
    )

    logger.info("🤖 Starting local Ariel Bath Receptionist. Talk to her below:")
    async with Agent(config) as agent:
        await agent.run_interactive_loop()

# ==========================================
# 🏁 MAIN ENTRY POINT
# ==========================================
if __name__ == "__main__":
    # If "--interactive" argument is passed, run local SDK loop
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        import asyncio
        asyncio.run(run_interactive_agent())
    else:
        # Default: Run the lightweight webhook server
        run_server(port=8080)
