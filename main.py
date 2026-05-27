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
    
    # 1. Load instructions for all agents
    def read_instr(name):
        path = os.path.join(os.path.dirname(__file__), "instructions", name)
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        return ""

    router_instr = read_instr("router.txt")
    after_hours_instr = read_instr("receptionist.txt")
    faq_instr = read_instr("faq_receptionist.txt")
    wismo_instr = read_instr("wismo_receptionist.txt")

    logger.info("🤖 Starting Decoupled Ariel Bath Receptionist Router Loop...")
    print("\n=======================================================")
    print("Welcome to Ariel Bath AI Receptionist Routing Simulator")
    print("=======================================================\n")
    
    while True:
        try:
            user_input = input("Caller: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Simulated intent routing logic based on router directives
            lower_input = user_input.lower()
            if any(word in lower_input for word in ["order", "tracking", "po", "where is my"]):
                target_agent = "WISMO Receptionist"
                agent_instr = wismo_instr
            elif any(word in lower_input for word in ["return", "policy", "faq", "spec", "vanity", "tub", "mirror", "faucet"]):
                target_agent = "FAQ Receptionist"
                agent_instr = faq_instr
            else:
                target_agent = "After Hours Receptionist"
                agent_instr = after_hours_instr
                
            print(f"\n[Router] -> Detected query intent. Routing to: {target_agent}")
            
            # Simple simulation of agent response using prompt constraints
            if target_agent == "WISMO Receptionist":
                response = "[WISMO] I would be happy to help check your order status. Could you please provide your Purchase Order number?"
            elif target_agent == "FAQ Receptionist":
                response = f"[FAQ] For details on specs, policies, or returns, please visit www.ArielBath.com or let me know what specific product you are asking about."
            else:
                response = f"[After Hours] You've reached us after hours, but I can take your info for a callback. What is your phone number?"
                
            print(f"Agent: {response}\n")
            
        except (KeyboardInterrupt, EOFError):
            break

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
