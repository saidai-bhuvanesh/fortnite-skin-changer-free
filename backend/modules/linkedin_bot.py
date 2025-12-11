"""
LinkedIn Bot - Generate professional LinkedIn content
"""

from typing import Dict, Optional, List
from loguru import logger
import sys
import random

# Configure logger
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("logs/linkedin_bot.log", rotation="10 MB")

class LinkedInBot:
    """LinkedIn content generation and formatting"""
    
    # Content style templates
    STYLES = {
        "corporate": "professional, formal, business-oriented",
        "motivational": "inspiring, uplifting, encouraging",
        "technical": "detailed, informative, educational",
        "storytelling": "narrative, personal, engaging",
        "thought_leadership": "insightful, analytical, forward-thinking"
    }
    
    # Popular hashtag categories
    HASHTAG_CATEGORIES = {
        "ai_ml": ["#ArtificialIntelligence", "#MachineLearning", "#DeepLearning", "#AI", "#DataScience"],
        "tech": ["#Technology", "#Innovation", "#DigitalTransformation", "#TechTrends", "#FutureTech"],
        "career": ["#CareerGrowth", "#ProfessionalDevelopment", "#Leadership", "#CareerAdvice", "#Success"],
        "productivity": ["#Productivity", "#TimeManagement", "#WorkLifeBalance", "#Efficiency", "#Skills"],
        "general": ["#LinkedIn", "#Networking", "#Learning", "#Growth", "#Motivation"]
    }
    
    def __init__(self, llm_chat):
        """
        Initialize LinkedIn bot
        
        Args:
            llm_chat: LLMChat instance for content generation
        """
        self.llm_chat = llm_chat
        logger.info("LinkedIn Bot initialized")
    
    def generate_post(
        self,
        topic: str,
        style: str = "corporate",
        length: str = "medium",
        include_hashtags: bool = True,
        hashtag_category: str = "general"
    ) -> Dict[str, str]:
        """
        Generate a LinkedIn post
        
        Args:
            topic: Post topic or prompt
            style: Writing style (corporate, motivational, technical, storytelling, thought_leadership)
            length: Post length (short: ~100 words, medium: ~200 words, long: ~300 words)
            include_hashtags: Whether to add hashtags
            hashtag_category: Category of hashtags to use
            
        Returns:
            Dict with post content and metadata
        """
        # Determine word count based on length
        word_counts = {"short": 100, "medium": 200, "long": 300}
        target_words = word_counts.get(length, 200)
        
        # Get style description
        style_desc = self.STYLES.get(style, self.STYLES["corporate"])
        
        # Create prompt for LLM
        system_prompt = f"""You are a professional LinkedIn content creator.
Create a {style} LinkedIn post about: {topic}

Requirements:
- Style: {style_desc}
- Length: approximately {target_words} words
- Use line breaks for readability (2-3 paragraphs or bullet points)
- Start with a hook to grab attention
- End with a call-to-action or question to encourage engagement
- Be authentic and valuable
- Do NOT include hashtags (they will be added separately)

Write the post now:"""
        
        post_content = self.llm_chat.generate_response(
            topic,
            system_prompt=system_prompt,
            temperature=0.8,
            max_tokens=500
        )
        
        # Add hashtags if requested
        hashtags = ""
        if include_hashtags:
            hashtags = self._generate_hashtags(topic, hashtag_category)
        
        # Combine post and hashtags
        full_post = post_content.strip()
        if hashtags:
            full_post += f"\n\n{hashtags}"
        
        logger.info(f"Generated {style} post about '{topic}'")
        
        return {
            "content": post_content.strip(),
            "hashtags": hashtags,
            "full_post": full_post,
            "style": style,
            "length": length,
            "word_count": len(post_content.split())
        }
    
    def rewrite_caption(
        self,
        original_caption: str,
        improvement: str = "make more engaging"
    ) -> Dict[str, str]:
        """
        Rewrite/improve an existing caption
        
        Args:
            original_caption: Existing caption to improve
            improvement: Specific improvement instruction
            
        Returns:
            Dict with improved caption
        """
        system_prompt = f"""You are a professional LinkedIn content editor.
Rewrite the following LinkedIn post to {improvement}.

Maintain:
- The core message
- Professional tone
- Authenticity

Improve:
- Clarity and readability
- Engagement potential
- Structure and flow

Original post:
{original_caption}

Rewritten post:"""
        
        improved = self.llm_chat.generate_response(
            "",
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=500
        )
        
        return {
            "original": original_caption,
            "improved": improved.strip(),
            "improvement_type": improvement
        }
    
    def _generate_hashtags(
        self,
        topic: str,
        category: str = "general",
        count: int = 5
    ) -> str:
        """
        Generate relevant hashtags
        
        Args:
            topic: Post topic
            category: Hashtag category
            count: Number of hashtags
            
        Returns:
            Hashtags string
        """
        # Get hashtags from category
        hashtags_pool = self.HASHTAG_CATEGORIES.get(category, self.HASHTAG_CATEGORIES["general"])
        
        # Randomly select hashtags
        selected = random.sample(hashtags_pool, min(count, len(hashtags_pool)))
        
        # Use LLM to generate custom hashtags based on topic
        system_prompt = f"""Generate 2-3 specific, relevant hashtags for a LinkedIn post about: {topic}
Return only the hashtags, each starting with #, separated by spaces.
Example: #CloudComputing #DevOps #Infrastructure"""
        
        custom_hashtags = self.llm_chat.generate_response(
            topic,
            system_prompt=system_prompt,
            temperature=0.6,
            max_tokens=50
        )
        
        # Combine selected and custom
        all_hashtags = selected + custom_hashtags.strip().split()
        
        # Deduplicate and limit
        unique_hashtags = []
        seen = set()
        for tag in all_hashtags:
            tag = tag.strip()
            if tag.startswith('#') and tag.lower() not in seen:
                unique_hashtags.append(tag)
                seen.add(tag.lower())
                if len(unique_hashtags) >= count:
                    break
        
        return " ".join(unique_hashtags[:count])
    
    def generate_comment(self, post_content: str, tone: str = "supportive") -> str:
        """
        Generate a professional comment for a LinkedIn post
        
        Args:
            post_content: The post to comment on
            tone: Comment tone (supportive, insightful, questioning)
            
        Returns:
            Generated comment text
        """
        system_prompt = f"""Generate a professional, {tone} LinkedIn comment for this post.

Requirements:
- Be genuine and add value
- Keep it concise (2-3 sentences)
- Encourage further discussion if appropriate
- Be professional but friendly

Post content:
{post_content}

Your comment:"""
        
        comment = self.llm_chat.generate_response(
            "",
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=150
        )
        
        return comment.strip()
    
    def get_post_ideas(self, industry: str = "technology", count: int = 5) -> List[str]:
        """
        Generate post topic ideas
        
        Args:
            industry: Industry/field for topics
            count: Number of ideas to generate
            
        Returns:
            List of post ideas
        """
        system_prompt = f"""Generate {count} engaging LinkedIn post topic ideas for someone in the {industry} industry.

For each idea, provide:
- A clear, specific topic
- Why it would resonate with a professional audience

Format as a numbered list."""
        
        ideas = self.llm_chat.generate_response(
            f"LinkedIn post ideas for {industry}",
            system_prompt=system_prompt,
            temperature=0.9,
            max_tokens=400
        )
        
        return ideas.strip()
