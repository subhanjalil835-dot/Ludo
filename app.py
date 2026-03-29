# ========================= app.py =========================
import streamlit as st
import random
from PIL import Image
import time

st.set_page_config(page_title="Real Ludo Pro", layout="centered")

BOARD_IMG = "ludo.png"

PATH = [
(6,1),(6,2),(6,3),(6,4),(6,5),(5,6),(4,6),(3,6),(2,6),(1,6),(0,6),(0,7),(0,8),
(1,8),(2,8),(3,8),(4,8),(5,8),(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),(7,14),(8,14),
(8,13),(8,12),(8,11),(8,10),(8,9),(9,8),(10,8),(11,8),(12,8),(13,8),(14,8),(14,7),(14,6),
(13,6),(12,6),(11,6),(10,6),(9,6),(8,5),(8,4),(8,3),(8,2),(8,1),(8,0),(7,0),(6,0)
]

START_INDEX = {"red":0, "green":13, "yellow":26, "blue":39}
SAFE = [0,8,13,21,26,34,39,47]

if "init" not in st.session_state:
    st.session_state.init=True
    st.session_state.players=2
    st.session_state.turn=0
    st.session_state.dice=0
    st.session_state.started=False
    st.session_state.pos={c:[-1]*4 for c in ["red","green","blue","yellow"]}

COLORS_2=["red","green"]
COLORS_4=["red","green","blue","yellow"]

st.title("🎲 REAL LUDO PRO")

if not st.session_state.started:
    p=st.selectbox("Players",[2,4])
    if st.button("Start"):
        st.session_state.players=p
        st.session_state.started=True
        st.rerun()

if st.session_state.started:

    COLORS = COLORS_2 if st.session_state.players==2 else COLORS_4
    player = COLORS[st.session_state.turn % len(COLORS)]

    st.subheader(f"Turn: {player.upper()}")

    if st.button("Roll Dice 🎲"):
        st.session_state.dice=random.randint(1,6)

    st.write("Dice:", st.session_state.dice)

    if st.session_state.dice>0:
        token=st.selectbox("Token",[0,1,2,3])

        if st.button("Move"):
            dice=st.session_state.dice
            pos=st.session_state.pos[player][token]

            if pos==-1 and dice==6:
                st.session_state.pos[player][token]=START_INDEX[player]

            elif pos>=0:
                for _ in range(dice):
                    pos=(pos+1)%52
                    st.session_state.pos[player][token]=pos
                    draw_board(COLORS)
                    time.sleep(0.1)

                if pos not in SAFE:
                    for p in COLORS:
                        if p!=player:
                            for i in range(4):
                                if st.session_state.pos[p][i]==pos:
                                    st.session_state.pos[p][i]=-1

            if dice!=6:
                st.session_state.turn+=1

            st.session_state.dice=0
            st.rerun()

    def draw_board(colors_list):
        img = Image.open(BOARD_IMG).convert("RGB")
        img = img.resize((600,600))
        pixels = img.load()

        cell = 600//15

        color_map={
            "red":(255,0,0),
            "green":(0,255,0),
            "blue":(0,0,255),
            "yellow":(255,255,0)
        }

        for c in colors_list:
            for p in st.session_state.pos[c]:
                if p>=0:
                    (r,cx)=PATH[p]
                    x=cx*cell+cell//2
                    y=r*cell+cell//2

                    for i in range(-8,9):
                        for j in range(-8,9):
                            if 0<=x+i<600 and 0<=y+j<600:
                                pixels[x+i,y+j]=color_map[c]

        st.image(img, use_container_width=True)

    draw_board(COLORS)

    for c in COLORS:
        if all(p>=50 for p in st.session_state.pos[c]):
            st.success(f"🏆 {c.upper()} WINS!")
            if st.button("Restart"):
                st.session_state.clear()
                st.rerun()


