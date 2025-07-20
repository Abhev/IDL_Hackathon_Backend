import json
from datetime import datetime

# Get parameters
debate_topic = params['debate_topic']
user_stance = params['user_stance'].lower()
user_position = params['user_position']
user_speech = params['user_speech']

# Define Asian Parliamentary debate structure
DEBATE_POSITIONS = [
    {"position": "Prime Minister", "side": "government", "order": 1, "time_limit": "7 minutes"},
    {"position": "Leader of Opposition", "side": "opposition", "order": 2, "time_limit": "8 minutes"},
    {"position": "Deputy Prime Minister", "side": "government", "order": 3, "time_limit": "8 minutes"},
    {"position": "Deputy Leader of Opposition", "side": "opposition", "order": 4, "time_limit": "8 minutes"},
    {"position": "Member of Government", "side": "government", "order": 5, "time_limit": "8 minutes"},
    {"position": "Member of Opposition", "side": "opposition", "order": 6, "time_limit": "8 minutes"},
    {"position": "Opposition Whip", "side": "opposition", "order": 7, "time_limit": "4 minutes"},
    {"position": "Government Whip", "side": "government", "order": 8, "time_limit": "4 minutes"}
]

def call_llm(prompt, max_tokens=1500):
    """Call Relevance AI's LLM with the given prompt"""
    try:
        # Using Relevance AI's built-in LLM functionality
        response = llm_complete(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.8,
            model="gpt-4"
        )
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"

def get_position_info(position_name):
    """Get information about a debate position"""
    for pos in DEBATE_POSITIONS:
        if pos["position"] == position_name:
            return pos
    return None

def generate_ai_speech(position, side, topic, previous_speeches, is_whip=False):
    """Generate an AI speech for a given position"""
    
    # Create context from previous speeches
    context = ""
    if previous_speeches:
        context = "\n\nPrevious speeches in this debate:\n"
        for i, speech in enumerate(previous_speeches):
            context += f"\n{speech['position']} ({speech['side']}):\n{speech['content']}\n"
    
    # Different prompts based on position type
    if is_whip:
        prompt = f"""You are an expert debater participating in an Asian Parliamentary debate. You are the {position} speaking on the motion: "{topic}"

Your role as a whip is to:
1. Summarize and crystallize your side's key arguments
2. Identify the key clashes and explain why your side wins them
3. Provide a compelling conclusion to your side's case
4. Do NOT introduce new substantive arguments

You should be formal, articulate, and persuasive. Structure your speech clearly with signposting.
{context}

Please deliver a {position} speech (approximately 4 minutes worth of content):"""
    
    else:
        if position == "Prime Minister":
            prompt = f"""You are an expert debater participating in an Asian Parliamentary debate as the Prime Minister. The motion is: "{topic}"

As Prime Minister, you must:
1. Define the motion clearly and set the framework for the debate
2. Present 2-3 strong arguments supporting the motion
3. Be constructive and establish the government's case
4. Speak with authority and conviction

You should be formal, articulate, and persuasive. Structure your speech clearly with signposting.

Please deliver a Prime Minister speech (approximately 7 minutes worth of content):"""
        
        elif position == "Leader of Opposition":
            prompt = f"""You are an expert debater participating in an Asian Parliamentary debate as the Leader of Opposition. The motion is: "{topic}"

As Leader of Opposition, you must:
1. Accept or challenge the government's definition if problematic
2. Present 2-3 strong arguments opposing the motion
3. Directly rebut the Prime Minister's key points
4. Establish the opposition's case clearly

You should be formal, articulate, and persuasive. Structure your speech clearly with signposting.
{context}

Please deliver a Leader of Opposition speech (approximately 8 minutes worth of content):"""
        
        else:
            # For other positions (Deputy PM, Deputy Leader, Members)
            role_guidance = {
                "Deputy Prime Minister": "strengthen the government case, rebut opposition arguments, and add new substantive points",
                "Deputy Leader of Opposition": "strengthen the opposition case, rebut government arguments, and add new substantive points", 
                "Member of Government": "extend the government case with fresh analysis and rebut opposition points",
                "Member of Opposition": "extend the opposition case with fresh analysis and rebut government points"
            }
            
            prompt = f"""You are an expert debater participating in an Asian Parliamentary debate as the {position}. The motion is: "{topic}"

As {position}, you must:
1. {role_guidance.get(position, "Strengthen your side's case and rebut opposing arguments")}
2. Engage with the arguments made by previous speakers
3. Add value to the debate with new insights or analysis
4. Maintain your side's momentum

You should be formal, articulate, and persuasive. Structure your speech clearly with signposting.
{context}

Please deliver a {position} speech (approximately 8 minutes worth of content):"""
    
    return call_llm(prompt)

def generate_feedback(user_speech, user_position, all_speeches, topic):
    """Generate detailed feedback on the user's speech"""
    
    # Create context of all other speeches
    other_speeches = ""
    for speech in all_speeches:
        if speech['position'] != user_position:
            other_speeches += f"\n{speech['position']} ({speech['side']}):\n{speech['content']}\n"
    
    prompt = f"""You are an expert debate judge and coach evaluating a speech in an Asian Parliamentary debate. 

DEBATE MOTION: "{topic}"
SPEAKER POSITION: {user_position}

OTHER SPEECHES IN THE DEBATE:
{other_speeches}

USER'S SPEECH TO EVALUATE:
{user_speech}

Please provide comprehensive feedback covering:

1. **Content & Arguments** (25 points):
   - Strength and relevance of arguments
   - Logical reasoning and evidence
   - Fulfillment of positional role requirements

2. **Rebuttal & Engagement** (25 points):
   - How well they engaged with opposing arguments
   - Quality of rebuttals and refutations
   - Strategic response to the debate flow

3. **Structure & Organization** (25 points):
   - Clear signposting and speech structure
   - Logical flow of ideas
   - Effective use of time

4. **Style & Delivery** (25 points):
   - Persuasiveness and rhetoric
   - Language and tone appropriateness
   - Confidence and authority

Provide specific examples from their speech, suggest improvements, and give an overall score out of 100. Be constructive but honest in your assessment."""

    return call_llm(prompt, max_tokens=2000)

# Determine user's side
user_side = "government" if user_stance in ["government", "gov"] else "opposition"

# Find user's position info
user_pos_info = get_position_info(user_position)
if not user_pos_info:
    results = {"error": f"Invalid position: {user_position}"}
else:
    # Generate the complete debate
    debate_speeches = []
    
    print(f"🎭 **ASIAN PARLIAMENTARY DEBATE SIMULATION**")
    print(f"📋 **Motion:** {debate_topic}")
    print(f"👤 **Your Position:** {user_position} ({user_side.title()})")
    print(f"⏱️ **Time Limit:** {user_pos_info['time_limit']}")
    print("\n" + "="*80 + "\n")
    
    # Generate speeches in order, inserting user speech at appropriate time
    for position_info in DEBATE_POSITIONS:
        position = position_info["position"]
        side = position_info["side"]
        order = position_info["order"]
        
        if position == user_position:
            # This is the user's turn
            print(f"🎤 **{position} ({side.title()}) - YOUR TURN**")
            print(f"📝 Your Speech:")
            print(f"{user_speech}")
            print("\n" + "-"*60 + "\n")
            
            debate_speeches.append({
                "position": position,
                "side": side,
                "order": order,
                "content": user_speech,
                "speaker": "user"
            })
        else:
            # Generate AI speech
            print(f"🤖 **{position} ({side.title()}) - AI OPPONENT**")
            print("🔄 Generating speech...")
            
            is_whip = "whip" in position.lower()
            ai_speech = generate_ai_speech(position, side, debate_topic, debate_speeches, is_whip)
            
            print(f"📢 AI Speech:")
            print(f"{ai_speech}")
            print("\n" + "-"*60 + "\n")
            
            debate_speeches.append({
                "position": position,
                "side": side,
                "order": order,
                "content": ai_speech,
                "speaker": "ai"
            })
    
    print("🏁 **DEBATE COMPLETED**")
    print("\n" + "="*80 + "\n")
    
    # Generate feedback
    print("⚖️ **GENERATING JUDGE'S FEEDBACK**")
    print("🔄 Analyzing your performance...")
    
    feedback = generate_feedback(user_speech, user_position, debate_speeches, debate_topic)
    
    print("📊 **JUDGE'S FEEDBACK ON YOUR SPEECH:**")
    print(f"{feedback}")
    
    # Prepare results
    results = {
        "debate_topic": debate_topic,
        "user_position": user_position,
        "user_side": user_side,
        "debate_format": "Asian Parliamentary",
        "total_speeches": len(debate_speeches),
        "all_speeches": debate_speeches,
        "judge_feedback": feedback,
        "simulation_completed": True,
        "timestamp": datetime.now().isoformat()
    }

print("\n🎉 **Debate simulation completed successfully!**")
print("💡 **Tip:** Use the feedback to improve your debating skills for next time!")

results
return results