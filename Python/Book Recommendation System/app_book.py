import streamlit as st
import pickle
import numpy as np
import math
import time

book_data=pickle.load(open('artifact_f/book_data.pkl','rb'))
popular_books=pickle.load(open('artifact_f/top_50_books.pkl','rb'))
user_data=pickle.load(open('artifact_f/user_pivot.pkl','rb'))
user_similarity=user_data.T.corr()

def recommend_books_by_user(user,n=5):
    temp=user_similarity.drop(index=user)
    similar_users=temp[temp[user]>0.3][user]
    user_watched_movies=user_data.loc[user].dropna().index
    similar_users_watched=user_data.loc[similar_users.index].dropna(axis=1,how='all')
    unwatched=similar_users_watched.drop(columns=user_watched_movies,errors='ignore')
    weighted_score={}
    for i in unwatched:
        cleaned_movie=unwatched[i].dropna()
        scores=np.array([similar_users[j]*cleaned_movie[j] for j in cleaned_movie.index]).mean()
        weighted_score[i]=scores
    return list(dict(sorted(weighted_score.items(),key=lambda x:x[1],reverse=True)).keys())[:n]




def get_book_details(book):
    book_details=np.array(book_data[book_data['Book-Title']==book])[0]
    return book_details

st.set_page_config(layout="wide")

trending,user=st.tabs(['Trending','User'])

with trending:
    _,center,_=st.columns([1,7,1])
    with center: 
        st.title('Popular Books',anchor=False)    
        st.title('') 
        
    cols=st.columns(5,gap='medium')
    for r in range(10):
        for i,j in enumerate(cols):
            st.title('')
            with j:
                    # st.title('')
                with st.container(border=True,height=300):
                    temp=get_book_details(popular_books[i+(r*5),0])
                    st.image(temp[4])
                    st.write(popular_books[i,0])
                    st.write('Rating ',np.round(popular_books[i+(r*5),1],2))
                    
        st.write('')
        st.title('')
        st.title('')    

with user:
    _,c,_=st.columns([1,5,1])   
    with c:
        with st.form('form'):
            user,number,btn=st.columns(3,gap='medium')
            with user:
                user_id=st.selectbox('Enter User ID',options=user_similarity.index,index=None)
            with number:
                number=st.number_input('Number Of Books',max_value=50,value=5)
            with btn:
                st.write('')
                st.write('')
                submit=st.form_submit_button('submit')
    if submit:
        if user_id==None:
            st.warning('Input User ID')
        else:
            # time.sleep(1)
            books=recommend_books_by_user(user_id,number)
            st.header(f'Recommended books for {user_id}',anchor=False)
            cols=st.columns(5,gap='medium')
            for r in range(math.ceil(number/5)):
                for i,j in enumerate(cols):
                    st.title('')
                    with j:
                    # st.title('')
                        if i+r*5<number:
                            with st.container(border=True,height=300):
                                temp=get_book_details(books[i+r*5])
                                st.image(temp[4])
                                st.write(books[i+r*5])
                                st.write('rating : ',np.round(temp[-1],2))


