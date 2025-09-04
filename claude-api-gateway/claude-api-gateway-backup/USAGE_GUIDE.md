# Claude API Gateway MCP Server - Usage Guide

## 🚀 **Comprehensive Claude 4 Sonnet Integration**

This MCP server provides a **secure front door** to Anthropic's Claude API with:
- **🔐 Secure API key storage** with encryption
- **👤 User registration and authentication** 
- **💬 Conversation history tracking**
- **🔑 Token-based access control**
- **📊 Usage monitoring and metrics**

## 🔧 **Quick Start**

### **1. Start the MCP Server**
```bash
cd claude-api-gateway
python3 claude-api-gateway_server.py
```

### **2. Register a User (Store Your API Key Securely)**
```python
# Using MCP client
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async with stdio_client(["python", "claude-api-gateway_server.py"]) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # Register with your Anthropic API key
        registration = await session.call_tool("claude-api-gateway_register_user", {
            "username": "your_username",
            "email": "your_email@example.com",
            "anthropic_api_key": "sk-ant-api03-your-actual-api-key-here"
        })
        
        print("Registration result:", registration)
        # Save the returned user_id and password securely!
```

**Result:**
```json
{
  "success": true,
  "data": {
    "user_id": "uuid-generated-user-id",
    "username": "your_username", 
    "password": "generated-secure-password",
    "message": "User registered successfully. Store your password securely - it cannot be recovered."
  }
}
```

### **3. Authenticate and Get Access Token**
```python
# Authenticate with your credentials
auth_result = await session.call_tool("claude-api-gateway_authenticate_user", {
    "username": "your_username",
    "password": "generated-secure-password"  # From registration
})

access_token = auth_result[0].text["data"]["access_token"]
print("Access token:", access_token)
```

### **4. Send Messages to Claude**
```python
# Send your first message
claude_response = await session.call_tool("claude-api-gateway_send_message", {
    "access_token": access_token,
    "message": "Hello Claude! Can you help me understand quantum computing?",
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 4096,
    "temperature": 0.7
})

print("Claude says:", claude_response[0].text)
```

### **5. Continue Conversations**
```python
# Get the conversation ID from the response
conversation_id = claude_response["data"]["conversation_id"]

# Continue the conversation
follow_up = await session.call_tool("claude-api-gateway_send_message", {
    "access_token": access_token,
    "message": "Can you give me a specific example?",
    "conversation_id": conversation_id  # This maintains conversation context
})
```

## 🔍 **API Endpoints (MCP Tools)**

### **User Management**

#### **`claude-api-gateway_register_user`**
Register a new user with encrypted API key storage.

**Input:**
```json
{
  "username": "string",
  "email": "string", 
  "anthropic_api_key": "string"
}
```

**Output:**
```json
{
  "success": true,
  "data": {
    "user_id": "uuid",
    "username": "string",
    "password": "generated-password"
  }
}
```

#### **`claude-api-gateway_authenticate_user`**
Authenticate and get access token.

**Input:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Output:**
```json
{
  "success": true,
  "data": {
    "access_token": "secure-token",
    "expires_at": "2024-01-01T12:00:00Z",
    "user_id": "uuid"
  }
}
```

### **Claude Integration**

#### **`claude-api-gateway_send_message`**
Send message to Claude with conversation tracking.

**Input:**
```json
{
  "access_token": "string",
  "message": "string",
  "conversation_id": "string (optional)",
  "model": "claude-3-5-sonnet-20241022 (optional)",
  "max_tokens": 4096,
  "temperature": 0.7,
  "system_prompt": "string (optional)"
}
```

**Output:**
```json
{
  "success": true,
  "data": {
    "conversation_id": "uuid",
    "message_id": "uuid", 
    "content": "Claude's response",
    "model": "claude-3-5-sonnet-20241022",
    "usage": {
      "input_tokens": 150,
      "output_tokens": 300
    }
  }
}
```

### **Conversation Management**

#### **`claude-api-gateway_get_conversations`**
Get user's conversation history.

**Input:**
```json
{
  "access_token": "string",
  "limit": 50,
  "offset": 0
}
```

**Output:**
```json
[
  {
    "id": "conversation-uuid",
    "title": "Conversation title",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:30:00Z",
    "message_count": 6,
    "is_active": true
  }
]
```

#### **`claude-api-gateway_get_conversation_history`**
Get full message history for a conversation.

**Input:**
```json
{
  "access_token": "string",
  "conversation_id": "string"
}
```

**Output:**
```json
[
  {
    "id": "message-uuid",
    "role": "user",
    "content": "Hello Claude!",
    "timestamp": "2024-01-01T10:00:00Z",
    "token_count": 3,
    "model_used": "claude-3-5-sonnet-20241022"
  },
  {
    "id": "message-uuid-2",
    "role": "assistant", 
    "content": "Hello! How can I help you today?",
    "timestamp": "2024-01-01T10:00:05Z",
    "token_count": 8,
    "model_used": "claude-3-5-sonnet-20241022"
  }
]
```

## 🔐 **Security Features**

### **API Key Protection**
- **Encrypted Storage**: API keys encrypted before database storage
- **No Plaintext**: API keys never stored in plaintext
- **User Isolation**: Each user's API key is isolated and secure

### **Authentication**
- **Password Hashing**: bcrypt for secure password storage
- **Session Tokens**: Secure, expiring access tokens
- **Token Validation**: Automatic token expiration and cleanup

### **Access Control**
- **User-Based**: Each user only accesses their own data
- **Conversation Ownership**: Users can only access their conversations
- **Rate Limiting**: Built-in rate limiting per user

## 💬 **Conversation Features**

### **Automatic Tracking**
- **Conversation IDs**: Each conversation gets a unique ID
- **Message History**: Complete message history stored
- **Context Preservation**: Claude receives full conversation context
- **Metadata**: Token counts, timestamps, model information

### **Conversation Management**
- **List Conversations**: Get all user conversations
- **Get History**: Retrieve full conversation history
- **Automatic Titles**: Conversations titled from first message
- **Message Counts**: Track conversation length

## 📊 **Monitoring & Metrics**

### **Health Monitoring**
```python
# Check server health
health = await session.call_tool("claude-api-gateway_health_check", {})
```

### **Usage Metrics**
```python
# Get detailed metrics
metrics = await session.read_resource("mcp://claude-api-gateway/metrics")
```

**Metrics Include:**
- Active users count
- Total conversations
- Messages in last 24 hours
- Performance statistics
- Security status

## 🤖 **AI Integration Example**

```python
import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def claude_conversation_example():
    """Complete example of using Claude API Gateway"""
    
    async with stdio_client(["python", "claude-api-gateway_server.py"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Register user (one time)
            registration = await session.call_tool("claude-api-gateway_register_user", {
                "username": "ai_researcher",
                "email": "researcher@example.com", 
                "anthropic_api_key": "your-anthropic-api-key"
            })
            
            user_password = registration[0].text["data"]["password"]
            print(f"🔑 Generated password: {user_password}")
            
            # 2. Authenticate
            auth = await session.call_tool("claude-api-gateway_authenticate_user", {
                "username": "ai_researcher",
                "password": user_password
            })
            
            access_token = auth[0].text["data"]["access_token"]
            print(f"🎫 Access token: {access_token[:20]}...")
            
            # 3. Start conversation with Claude
            response1 = await session.call_tool("claude-api-gateway_send_message", {
                "access_token": access_token,
                "message": "Explain the double-slit experiment in quantum physics",
                "system_prompt": "You are a physics professor explaining complex concepts clearly."
            })
            
            conversation_id = response1[0].text["data"]["conversation_id"]
            print(f"💬 Started conversation: {conversation_id}")
            print(f"🤖 Claude: {response1[0].text['data']['content'][:100]}...")
            
            # 4. Continue conversation
            response2 = await session.call_tool("claude-api-gateway_send_message", {
                "access_token": access_token,
                "message": "Can you give me a practical analogy for wave-particle duality?",
                "conversation_id": conversation_id
            })
            
            print(f"🤖 Claude: {response2[0].text['data']['content'][:100]}...")
            
            # 5. Get conversation history
            history = await session.call_tool("claude-api-gateway_get_conversation_history", {
                "access_token": access_token,
                "conversation_id": conversation_id
            })
            
            print(f"📚 Conversation has {len(history[0].text)} messages")
            
            # 6. List all conversations
            conversations = await session.call_tool("claude-api-gateway_get_conversations", {
                "access_token": access_token
            })
            
            print(f"💬 User has {len(conversations[0].text)} conversations")

# Run the example
asyncio.run(claude_conversation_example())
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Database configuration
export DATABASE_URL="sqlite:///claude_api_gateway.db"

# Security configuration  
export ENCRYPTION_KEY="your-32-byte-encryption-key"
export SESSION_TIMEOUT=3600

# Claude API configuration
export CLAUDE_MODEL="claude-3-5-sonnet-20241022"
export MAX_TOKENS=4096
export TEMPERATURE=0.7

# Rate limiting
export REQUESTS_PER_MINUTE=60
export MAX_CONVERSATION_LENGTH=100
```

### **Production Configuration**
For production deployment:

1. **Install security dependencies:**
   ```bash
   pip install cryptography bcrypt
   ```

2. **Generate encryption key:**
   ```python
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()
   print(f"Store this key securely: {key.decode()}")
   ```

3. **Use environment variables for sensitive data**
4. **Enable HTTPS transport for network access**
5. **Set up proper database (PostgreSQL recommended)**

## 🎯 **Use Cases**

### **Personal Claude Assistant**
- Register once with your API key
- Maintain conversation history across sessions
- Track usage and costs
- Secure API key storage

### **Team Claude Access**
- Multiple users with individual API keys
- Shared conversation access (if configured)
- Usage monitoring per user
- Cost tracking and allocation

### **AI Agent Integration**
- Other AI agents can discover and use Claude via this gateway
- Standardized MCP protocol for integration
- Automatic conversation management
- Built-in rate limiting and error handling

## 🛡️ **Security Best Practices**

1. **Store passwords securely** - The generated password cannot be recovered
2. **Protect access tokens** - Treat them like API keys
3. **Use HTTPS in production** - Never send credentials over HTTP
4. **Monitor usage** - Check metrics regularly for unusual activity
5. **Rotate tokens** - Implement token rotation for long-running applications

## 📈 **Benefits**

### **For Users**
- **One-time setup**: Register once, use everywhere
- **Conversation continuity**: Full conversation history preserved
- **Secure storage**: API keys encrypted and protected
- **Usage tracking**: Monitor your Claude API usage

### **For AI Agents**
- **Standardized access**: Same MCP protocol for all AI interactions
- **Automatic discovery**: AI agents find the service automatically
- **Context awareness**: Conversation history provides context
- **Error handling**: Robust error recovery and retry logic

### **For Organizations**
- **Centralized access**: Single point of access to Claude API
- **User management**: Multiple users with individual API keys
- **Usage monitoring**: Track usage across users and conversations
- **Cost control**: Monitor and limit API usage

---

**🎉 Your secure gateway to Claude 4 Sonnet is ready!**

This MCP server transforms Claude API access from individual API calls to a comprehensive, secure, conversation-aware service that AI agents can discover and use automatically.
