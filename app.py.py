# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 10:50:57 2025

@author: Ivano
"""

# app.py

import streamlit as st
import pandas as pd

# Optional imports (uncomment later when ready)
import praw  # for Reddit API
import openai  # for LLM summarization

# ------------------------------
# 🔧 App Configuration
# ------------------------------
st.set_page_config(
    page_title="Brand Sentiment Explorer",
    page_icon="👗",
    layout="centered"
)

# ------------------------------
# 🎨 Title and Description
# ------------------------------
st.title("👗 Brand Sentiment Explorer")
st.markdown("""
Get a quick summary of what Reddit thinks about your favorite clothing brands.  
Type a brand name (like *Zara*, *Shein*, or *H&M*) and see what the community is saying.
""")

# ------------------------------
# 🧩 User Input
# ------------------------------
brand_name = st.text_input("Enter a clothing brand name:", placeholder="e.g., Zara")

if st.button("Analyze"):
    if not brand_name.strip():
        st.warning("Please enter a brand name.")
    else:
        # ------------------------------------
        # 🧠 Step 1: Fetch Reddit data (placeholder)
        # ------------------------------------
        st.write("🔍 Searching Reddit for posts about:", brand_name)
        
        
        # Example placeholder
        #posts_data = [
         #   {"title": f"What do you think of {brand_name}?", "comments": ["Love their style!", "Too expensive lately."]},
         #   {"title": f"Is {brand_name} sustainable?", "comments": ["Not really sure", "They’re trying..."]},
        #]

        # Later, replace this section with actual Reddit API code:
        reddit = praw.Reddit(client_id=st.secrets["REDDIT_CLIENT_ID"],
                              client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
                              user_agent="BrandSentimentApp")
        subreddit = reddit.subreddit("all")
        posts_data = []
        for post in subreddit.search(brand_name, limit=10):
             posts_data.append({
                 "title": post.title,
                "comments": [comment.body for comment in post.comments[:5] if hasattr(comment, 'body')]
             })

        # ------------------------------------
        # 🤖 Step 2: Summarize using OpenAI (placeholder)
        # ------------------------------------
        st.write("🧠 Generating summary...")

        # Example placeholder summary
        #summary = f"People have mixed feelings about {brand_name}. Some love their fashion sense, while others criticize quality and pricing."

        # When ready, replace with actual OpenAI call:
         
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        text_to_summarize = "\n".join([p['title'] + ' ' + ' '.join(p['comments']) for p in posts_data])
        response = openai.ChatCompletion.create(
             model="gpt-4o-mini",
             messages=[{"role": "user", "content": f"Summarize Reddit opinions about {brand_name}: {text_to_summarize}"}],
             max_tokens=200
         )
        summary = response["choices"][0]["message"]["content"]

        # ------------------------------------
        # 📊 Step 3: Display results
        # ------------------------------------
        st.subheader(f"📝 Summary of Reddit Opinions on {brand_name}")
        st.success(summary)

        # Optional: Show fetched posts
        with st.expander("See sample Reddit posts"):
            df = pd.DataFrame(posts_data)
            st.dataframe(df)

# ------------------------------
# 🪪 Footer
# ------------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Reddit API, and OpenAI")
