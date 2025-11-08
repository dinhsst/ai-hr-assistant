"""
Simplified FastAPI backend for Vercel deployment.
This version uses direct OpenAI API calls instead of LangChain/FAISS to fit within Vercel's 250MB limit.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="HR Assistant API (Vercel)",
    description="Lightweight HR Assistant for Vercel deployment",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    source_documents: list = []
    function_calls: list = []

# Sample HR FAQ data (embedded in code to avoid file dependencies)
HR_FAQ_DATA = [
    {"question": "How do I apply for annual leave?", "answer": "You can apply for annual leave through the HR portal. Log in, go to 'Leave Management', select 'Apply for Leave', choose the dates, and submit. Your manager will be notified for approval."},
    {"question": "What is the company's remote work policy?", "answer": "Employees can work remotely up to 2 days per week. Please coordinate with your manager and ensure you're available during core hours (10 AM - 3 PM)."},
    {"question": "How do I update my bank account for payroll?", "answer": "To update your bank account information, log into the HR portal, go to 'Personal Information', select 'Payment Details', and update your bank account number. Changes take effect from the next pay cycle."},
    {"question": "What are the company's working hours?", "answer": "Standard working hours are 9 AM to 6 PM, Monday to Friday. We have flexible hours with core hours from 10 AM to 3 PM when everyone should be available."},
    {"question": "How do I report sick leave?", "answer": "For sick leave, notify your manager as early as possible via email or phone. Submit a sick leave request through the HR portal within 24 hours. Medical certificates are required for absences longer than 3 days."}
]

# Simple function tools
def check_leave_balance(employee_name: str = "Alice") -> str:
    """Check employee leave balance."""
    return f"{employee_name} has 5 days of annual leave remaining."

def check_pay_date() -> str:
    """Get the next pay date."""
    return "Salaries are paid on the 25th of every month. Your next salary will be deposited in 10 days."

def get_employee_department(employee_name: str = "Alice") -> str:
    """Get employee department."""
    departments = {"Alice": "Engineering", "Bob": "Marketing", "Charlie": "HR"}
    return f"{employee_name} is in the {departments.get(employee_name, 'Unknown')} department."

def check_company_info() -> str:
    """Get general company information."""
    return "TechCorp Inc. Founded in 2010. Headquarters in San Francisco. 500+ employees worldwide."

# Simple keyword-based intent detection
def detect_intent(message: str) -> dict:
    """Detect user intent and find relevant FAQ."""
    message_lower = message.lower()
    
    # Check for function calls
    if any(word in message_lower for word in ["leave balance", "how many leave", "days left"]):
        return {"type": "function", "function": "check_leave_balance"}
    
    if any(word in message_lower for word in ["pay date", "salary", "when paid"]):
        return {"type": "function", "function": "check_pay_date"}
    
    if any(word in message_lower for word in ["department", "which team"]):
        return {"type": "function", "function": "get_employee_department"}
    
    if any(word in message_lower for word in ["company info", "about company"]):
        return {"type": "function", "function": "check_company_info"}
    
    # Search FAQ
    for faq in HR_FAQ_DATA:
        if any(word in message_lower for word in faq["question"].lower().split()):
            return {"type": "faq", "data": faq}
    
    return {"type": "general", "data": None}

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "HR Assistant API (Vercel Deployment)",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "HR Assistant API (Vercel)",
        "rag_ready": False,
        "deployment": "vercel"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with simple intent detection."""
    try:
        message = request.message
        intent = detect_intent(message)
        
        if intent["type"] == "function":
            # Execute function
            func_name = intent["function"]
            if func_name == "check_leave_balance":
                answer = check_leave_balance()
            elif func_name == "check_pay_date":
                answer = check_pay_date()
            elif func_name == "get_employee_department":
                answer = get_employee_department()
            elif func_name == "check_company_info":
                answer = check_company_info()
            else:
                answer = "Function not found."
            
            return ChatResponse(
                answer=answer,
                source_documents=[],
                function_calls=[func_name]
            )
        
        elif intent["type"] == "faq":
            # Return FAQ answer
            faq = intent["data"]
            return ChatResponse(
                answer=faq["answer"],
                source_documents=[{
                    "content": faq["answer"],
                    "source": "HR FAQ",
                    "question": faq["question"]
                }],
                function_calls=[]
            )
        
        else:
            # General response
            return ChatResponse(
                answer="I'm here to help with HR-related questions. You can ask about leave policies, pay dates, remote work, or company information.",
                source_documents=[],
                function_calls=[]
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/faq")
async def get_faq_stats():
    """Get FAQ statistics."""
    return {
        "total_faqs": len(HR_FAQ_DATA),
        "vector_store_ready": False,
        "deployment": "vercel-lightweight"
    }

@app.post("/api/init")
async def initialize():
    """Initialize endpoint (no-op for Vercel version)."""
    return {
        "status": "success",
        "message": "Lightweight version initialized (no RAG)."
    }

# For Vercel
handler = app
