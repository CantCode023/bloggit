from src.agents.blogger import run
import streamlit as st
import asyncio
import nest_asyncio
nest_asyncio.apply()

async def generate_blog(prompt, style):
    return await run(prompt, style)

st.title("bloggit")
st.write("Made with ❤️ by [@bd.](https://github.com/CantCode023)")
st.markdown("---")

user_input = st.text_input("Enter your GitHub repository URL")
style = st.radio("Choose writing style:", ("Creative", "Logical"), horizontal=True)
generate_button = st.button("🚀 Blog it!")

if generate_button and user_input:
    chosen_style = style.lower()
    with st.spinner(f"Generating {chosen_style} blog..."):
        blog_content = asyncio.run(generate_blog(user_input, chosen_style))
        print(blog_content)
        st.markdown(blog_content)