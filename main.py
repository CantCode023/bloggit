from src.agents.blogger import run_tools, stream_blog
import streamlit as st
import asyncio
import nest_asyncio
nest_asyncio.apply()

async def generate_blog(prompt, style):
    blog_placeholder = st.empty()
    blog_placeholder.markdown("Generating blog image...")
    
    image_markdown, repo_contents = await run_tools(prompt)
    full_content = image_markdown + "\n\n"
    blog_placeholder.markdown(full_content)
    
    async for token in stream_blog(repo_contents, style):
        if isinstance(token, str):
            full_content += token
            blog_placeholder.markdown(full_content)
            await asyncio.sleep(0.01)
    
    blog_placeholder.empty()
    return full_content

st.title("bloggit")
st.write("Made with ❤️ by [@bd.](https://github.com/CantCode023)")
st.markdown("---")

user_input = st.text_input("Enter your GitHub repository URL")
style = st.radio("Choose writing style:", ("Creative", "Logical"), horizontal=True)
generate_button = st.button("🚀 Blog it!")

if generate_button and user_input:
    chosen_style = style.lower()
    blog_content = asyncio.run(generate_blog(user_input, chosen_style))
    st.markdown(blog_content)