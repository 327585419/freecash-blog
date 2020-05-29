# -*- coding: utf-8 -*-

import os
import streamlit as st
from PIL import Image
import pandas as pd

# Database Functions
from db_fxns import *

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# from freetx import Key

import requests
from MyQR import myqr


import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


# Reading Time
def readingTime(mytext):
    total_words = len([token for token in mytext.split(" ")])
    estimatedTime = total_words / 200.0
    return estimatedTime


# def analyze_text(text):
# 	return nlp(text)


# Layout Templates
title_temp = """
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar2.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<h6>Author:{}</h6>
	<br/>
	<br/>	
	<p style="text-align:justify">{}</p>
	</div>
	"""

article_temp = """
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<h6>Author:{}</h6> 
	<h6>Post Date: {}</h6>
	<img src="https://www.w3schools.com/howto/img_avatar2.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>
	<p style="text-align:justify">{}</p>
	</div>
	"""

head_message_temp = """
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar2.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
	<h6>Author:{}</h6> 		
	<h6>Post Date: {}</h6>		
	</div>
	"""

full_message_temp = """
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<p style="text-align:justify;color:black;padding:10px">{}</p>
	</div>
	"""

HTML_WRAPPER = """<div style="overflow-x: auto; border: 3px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


def main():
    """A Simple FCH Blog App"""
    html_temp = """
		<div style="background-color:{};padding:10px;border-radius:10px">
		<img src="http://fch.world/images/logo.png" style="vertical-align: middle;float:left;width: 80px;height: 80px;border-radius: 50%;">
		<h1 style="color:{};text-align:center;">FreeCash Community Blog </h1>
		</div>
		"""
    st.markdown(html_temp.format('royalblue','white'), unsafe_allow_html=True)

    # Display a picture
    image = Image.open('sunrise.png')
    st.image(image, caption='Freecash:A Free-Evolved Electronic Currency System!',
             use_column_width=True)


    # Display audio
    # video_file = open('satoshi.mp4','rb')
    # video_bytes = video_file.read()
    # st.video(video_bytes,format='video/mp4',start_time=0)


    menu2 = ["Home", "View Post", "Add Post", "Search", "Manage Blog"]
    choice2 = st.sidebar.selectbox("Main Menu", menu2)

    if choice2 == "Home":
        st.subheader("Home")
        result = view_all_notes()
        for i in result:
            # short_article = str(i[2])[0:int(len(i[2])/2)]
            short_article = str(i[2])[0:100]
            st.write(title_temp.format(i[1], i[0], short_article), unsafe_allow_html=True)


    elif choice2 == "View Post":
        st.subheader("View Post")

        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("All Posts", all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
            st.markdown(head_message_temp.format(i[1], i[0], i[3]), unsafe_allow_html=True)
            # st.markdown(full_message_temp.format(i[2]), unsafe_allow_html=True)
            st.markdown(i[2])

            reward_number = st.slider("Select a reward number(satoshi)",0,10000000)
            st.write("You will reward:",reward_number)

            # Reward blog_author(CID),
            # CID from the Li Ming API(http://39.104.79.176:8989/fc/info/cid/cid/pageSize/1/pageNum/1),
            # Generate QR code of the FCH address

            blog_author = str(i[0])
            r = requests.get('http://39.104.79.176:8989/fc/info/cid/{}/pageSize/0/pageNum/0'.format(blog_author))
            blog_author_address = r.json()['data']['address']
            if st.button("Reward(satoshi)"):
                myqr.run(words= blog_author_address,
                         version = 5,  # 设置容错率
                         level = 'H',  # 控制纠错水平，范围是L、M、Q、H，从左到右依次升高
                         picture = 'myqr1.png',
                         colorized = True,
                         contrast = 2.0,  # 调节图片的对比度，1.0 表示原始图片,默认为1.0。
                         brightness = 1.0,  # 调节图片的亮度，1.0 表示原始图片,默认为1.0。
                         save_name = 'myqr2.png')
                qr_image = Image.open('myqr2.png')
                st.image(qr_image, caption = 'Reward FreeCash Address:{}'.format(blog_author_address),
                         use_column_width = True)
                st.success('Thank you very much for your reward!')


    elif choice2 == "Add Post":
        st.subheader("Add Your Article")
        create_table()
        blog_title = st.text_input('Enter Post Title')
        blog_author = st.text_input("Enter Author Name(FCH_CID)", max_chars=30)
        blog_article = st.text_area("Enter Your Message", height=300)
        blog_post_date = st.date_input("Post Date")
        if st.button("Add"):
            add_data(blog_author, blog_title, blog_article, blog_post_date)
            st.success("Post::'{}' Saved".format(blog_title))


    elif choice2 == "Search":
        st.subheader("Search Articles")
        search_term = st.text_input("Enter Term")
        search_choice = st.radio("Field to Search", ("title", "author"))
        if st.button('Search'):
            if search_choice == "title":
                article_result = get_blog_by_title(search_term)
            elif search_choice == "author":
                article_result = get_blog_by_author(search_term)

        # Preview Articles
        for i in article_result:
            st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
            st.write(head_message_temp.format(i[1], i[0], i[3]), unsafe_allow_html=True)
            # st.write(full_message_temp.format(i[2]), unsafe_allow_html=True)


    elif choice2 == "Manage Blog":
        st.subheader("Manage Blog")
        result = view_all_notes()
        clean_db = pd.DataFrame(result, columns=["Author", "Title", "Article", "Date", "Index"])
        st.table(clean_db)

        unique_list = [i[0] for i in view_all_titles()]
        delete_by_title = st.selectbox("Select Title", unique_list)
        if st.button("Delete"):
            delete_data(delete_by_title)
            st.warning("Deleted: '{}'".format(delete_by_title))

        if st.checkbox("Metrics"):
            new_df = clean_db
            new_df['Length'] = new_df['Article'].str.len()

            st.table(new_df['Author'].value_counts())
            st.subheader("Author Stats")
            new_df['Author'].value_counts().plot(kind='bar',figsize=(10, 5))
            st.pyplot()

            new_df['Author'].value_counts().plot.pie(autopct="%1.1f%%",figsize=(10, 10))
            st.pyplot()


        if st.checkbox("WordCloud"):
            text = ','.join(clean_db['Article'])
            # Create and generate a word cloud image
            wordcloud = WordCloud().generate(text)

            # Display the generated image
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot()

        if st.checkbox("BarH Plot"):
            st.subheader("Length of Articles")
            new_df = clean_db
            new_df['Length'] = new_df['Article'].str.len()
            barh_plot = new_df.plot.barh(x='Author', y='Length', figsize=(8, 5))
            st.pyplot()


if __name__ == '__main__':
    main()
