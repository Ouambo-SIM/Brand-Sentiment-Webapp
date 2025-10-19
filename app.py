# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 10:50:57 2025

@author: Ivano
"""

# app.py

import streamlit as st
import pandas as pd
import cohere 

import praw 


# App Configuration
st.set_page_config(
    page_title="Brand Sentiment Explorer",
    page_icon="👗",
    layout="centered"
)


# Title and Description
st.title("👗 Brand Sentiment Explorer")
st.markdown("""
Get a quick summary of what Reddit thinks about your favorite clothing brands.  
Type a brand name (like *Zara*, *Shein*, or *H&M*) and see what the community is saying.
""")


# User Input
brand_name = st.text_input("Enter a clothing brand name:", placeholder="e.g., Zara")

if st.button("Analyze"):
    if not brand_name.strip():
        st.warning("Please enter a brand name.")
    else:    
        
        st.write("🔍 Searching Reddit for posts about:", brand_name)
    

        # Reddit Interaction
        
        reddit = praw.Reddit(client_id=st.secrets["REDDIT_CLIENT_ID"],
                              client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
                              user_agent="BrandSentimentApp")
        subreddit = reddit.subreddit("all")
        posts_data = []
        for post in subreddit.search(brand_name, limit=20):
             posts_data.append({
                 "title": post.title,
                "comments": [comment.body for comment in post.comments[:5] if hasattr(comment, 'body')]
             })

        
        st.write("🧠 Generating summary...")

        # LLM interaction
        cohere_api_key = st.secrets["COHERE_API_KEY"]
        co = cohere.Client(cohere_api_key)
        
        top_posts=posts_data[:20]
        text_to_summarize = "\n".join([p['title'] + ' ' + ' '.join(p['comments']) for p in top_posts])
        
        response = co.chat(
             model="command-xlarge-nightly",
             message=f"Summarize the following text and tell me what people think of the clothing brand in question's Quality, and Affordability': {text_to_summarize}",
             max_tokens=500
         )
        
        summary = response.text

        # result display
        st.subheader(f"📝 Summary of Reddit Opinions on {brand_name}")
        st.success(summary)

       
        with st.expander("See sample Reddit posts"):
            df = pd.DataFrame(posts_data)
            st.dataframe(df)


# Footer

st.markdown("---")
st.markdown("Built using Streamlit, Reddit API, and Cohere")
