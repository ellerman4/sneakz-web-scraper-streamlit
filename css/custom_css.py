import streamlit as st

def download_button_css():
    st.markdown(
    """
    <style>
    .css-1q8dd3e {
        width: 151px;
        position: absolute;
        top: 423px;
        left: 551px;
    </style>
    """,
    unsafe_allow_html=True
    )

def button_css():
    st.markdown(
    """
    <style>
    .css-wq85zr {
        display: inline-flex;
        -webkit-box-align: center;
        align-items: center;
        -webkit-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        margin: 0px;
        border-radius: 10px;
        line-height: 1.6;
        color: inherit;
        width: auto;
        user-select: none;
        background-color: rgb(43, 44, 54);
        border: 1px solid rgba(250, 250, 250, 0.2);
        width: 304px;
    }
    .css-wq85zr:before {
        content: '';
        background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
        position: absolute;
        top: -2px;
        left:-2px;
        background-size: 400%;
        z-index: -1;
        filter: blur(5px);
        width: calc(100% + 4px);
        height: calc(100% + 4px);
        animation: glowing 20s linear infinite;
        opacity: 0;
        transition: opacity .3s ease-in-out;
        border-radius: 10px;
    }
    .css-wq85zr:active {
        color: #000
    }
    .css-wq85zr:active:after {
        background: transparent;
    }
    .css-wq85zr:hover:before {
        opacity: 1;
    }

    .css-wq85zr:after {
        z-index: -1;
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        background: #111;
        left: 0;
        top: 0;
        border-radius: 10px;
    }

    @keyframes glowing {
        0% { background-position: 0 0; }
        50% { background-position: 400% 0; }
        100% { background-position: 0 0; }
    }
    </style>
    """,
    unsafe_allow_html=True
    )

def card():
    st.markdown(
    """
    <style>
    .card {
        width: 190px;
        height: 254px;
        top: 10px;
        right: 10px;
        position: absolute;
        border-radius: 20px;
        padding: 5px;
        box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
        background-image: linear-gradient(144deg,#AF40FF, #5B42F3 50%,#00DDEB);
        }

    .card__content {
        background: rgb(5, 6, 45);
        border-radius: 17px;
        position: absolute;
        top: 10px;
        right: 10px;
        width: 100%;
        height: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <div class="card">
    <div class="card__content">
    </div></div>
    """,
    unsafe_allow_html=True
    )