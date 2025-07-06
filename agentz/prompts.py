"""
Strategic prompt templates for AgentZ - AI Co-founder Assistant
Inspired by successful founder insights and startup methodologies
"""

SYSTEM_PROMPT = """You are AgentZ, an experienced AI co-founder and startup advisor. You help entrepreneurs validate ideas, understand markets, and plan smarter business strategies.

Your expertise includes:
- Lean startup methodology
- Market research and validation
- Competitor analysis
- Business model design
- Go-to-market strategies
- Product-market fit assessment
- Fundraising guidance

You communicate in a direct, actionable way like a seasoned entrepreneur. You ask probing questions, challenge assumptions, and provide practical next steps. Always focus on data-driven insights and real-world execution.

Remember: Ideas are cheap, execution is everything. Help founders build something people actually want."""

IDEA_VALIDATION_PROMPT = """Let's validate this business idea step by step:

1. **Problem Definition**: What specific problem does this solve? How painful is this problem?
2. **Target Market**: Who exactly faces this problem? How big is this market?
3. **Current Solutions**: How do people solve this today? What are the gaps?
4. **Value Proposition**: Why would customers choose this over alternatives?
5. **Business Model**: How will this make money? What's the unit economics?

Based on the conversation history and your idea: {idea}

Ask 2-3 sharp questions to uncover the most critical assumptions that need testing."""

MARKET_RESEARCH_PROMPT = """As an experienced market researcher, analyze this market opportunity:

Target Market: {market}
Product/Service: {product}

Provide insights on:
1. **Market Size & Growth**: TAM, SAM, SOM estimates and growth trends
2. **Customer Segments**: Primary and secondary customer personas
3. **Competitive Landscape**: Direct and indirect competitors, market positioning
4. **Market Dynamics**: Key trends, regulatory factors, barriers to entry
5. **Opportunities**: Underserved segments or emerging needs

Be specific and actionable. Include potential red flags or challenges."""

COMPETITOR_ANALYSIS_PROMPT = """Conduct a strategic competitor analysis for:

Company/Product: {product}
Market: {market}

Analyze:
1. **Direct Competitors**: Head-to-head competitors and their positioning
2. **Indirect Competitors**: Alternative solutions customers might choose
3. **Competitive Advantages**: What could differentiate this offering?
4. **Market Gaps**: Underserved needs or customer segments
5. **Competitive Strategy**: How to position against competitors

Focus on actionable competitive intelligence and strategic positioning."""

BUSINESS_MODEL_PROMPT = """Let's design a robust business model for:

Product/Service: {product}
Target Market: {market}

Evaluate these business model components:
1. **Revenue Streams**: How will you make money? (subscriptions, one-time, marketplace, etc.)
2. **Cost Structure**: What are the main cost drivers? Fixed vs variable costs
3. **Unit Economics**: Customer acquisition cost (CAC) vs lifetime value (LTV)
4. **Pricing Strategy**: How should you price? What's the value-based pricing?
5. **Scalability**: How does this model scale? What are the leverage points?

Recommend the optimal business model with reasoning."""

GTM_STRATEGY_PROMPT = """Design a go-to-market strategy for:

Product: {product}
Target Market: {market}
Business Model: {business_model}

Create a strategic GTM plan covering:
1. **Market Entry**: Which segment to target first? Why this beachhead market?
2. **Customer Acquisition**: What channels will reach your customers most effectively?
3. **Sales Process**: How will you convert prospects to customers?
4. **Marketing Strategy**: What messaging and tactics will resonate?
5. **Launch Timeline**: What's the logical sequence of GTM activities?

Focus on practical, executable tactics with clear success metrics."""

FUNDRAISING_PROMPT = """Provide fundraising guidance for:

Company: {company}
Stage: {stage}
Market: {market}

Cover these fundraising essentials:
1. **Funding Need**: How much to raise? What will it accomplish?
2. **Investor Targeting**: Which investors align with this stage/sector?
3. **Valuation Strategy**: What's a reasonable valuation range?
4. **Pitch Strategy**: What's the compelling narrative?
5. **Due Diligence Prep**: What metrics and materials are needed?

Give specific, actionable fundraising advice."""

REFLECTION_PROMPT = """Based on our conversation, let me synthesize the key insights and next steps:

**Key Insights:**
- [Summarize main learning/validation points]

**Critical Assumptions to Test:**
- [List top 3 riskiest assumptions]

**Immediate Next Steps:**
- [Specific, actionable tasks for the next 2 weeks]

**Success Metrics:**
- [How to measure progress on these initiatives]

What's the one thing you should focus on this week to move the needle?"""

def get_context_prompt(conversation_history: str, tools_used: list = None) -> str:
    """Generate contextual prompt based on conversation history"""
    context_parts = [
        f"**Conversation Context:**\n{conversation_history}"
    ]
    
    if tools_used:
        context_parts.append(f"**Tools Used:** {', '.join(tools_used)}")
    
    return "\n\n".join(context_parts)