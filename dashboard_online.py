import streamlit as st
from PIL import Image
import io, requests

st.set_page_config(page_title="FC Constroi - ONLINE SEM LOGIN", layout="wide")
st.title("FC Constroi - PUXAR ONLINE @fc_constroi")
st.caption("SEM senha | SEM cookies.txt | SEM download | Modela e reposta 5 plataformas")

# TENTA 2 METODOS - sem travar com JSON
def puxar_online_v2(username):
    try:
        import instaloader
        L = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            quiet=True
        )
        # ANONIMO - sem login
        profile = instaloader.Profile.from_username(L.context, username)
        posts = []
        for post in profile.get_posts():
            if len(posts) >= 12:
                break
            posts.append({
                "shortcode": post.shortcode,
                "display_url": post.url,  # url direto da imagem
                "is_video": post.is_video,
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "caption": post.caption[:100] if post.caption else "",
                "likes": post.likes
            })
        return posts, None
    except Exception as ex:
        return None, str(ex)

if st.button("🔥 PUXAR @fc_constroi ONLINE - SEM LOGIN", type="primary"):
    with st.spinner("Puxando @fc_constroi online (anonimo)..."):
        posts, err = puxar_online_v2("fc_constroi")
        if err:
            st.error(f"Instagram bloqueou anonimo temporariamente: {err}")
            st.info("SOLUCAO RAPIDA: Roda no terminal -> instaloader fc_constroi --no-captions --no-metadata-json")
            st.code("instaloader fc_constroi --no-captions --no-metadata-json", language="powershell")
        else:
            st.session_state["posts"] = posts
            st.success(f"{len(posts)} posts puxados ONLINE sem baixar!")

if "posts" in st.session_state:
    cols = st.columns(3)
    for i, p in enumerate(st.session_state["posts"]):
        with cols[i%3]:
            try:
                st.image(p["display_url"], use_container_width=True)
            except:
                st.write(p["url"])
            st.caption(p["caption"])
            # AQUI SEUS 5 BOTOES DE REPOST
            if st.button(f"Modelar {p['shortcode']}", key=p["shortcode"]):
                st.session_state["selected"] = p
                st.toast(f"Modelando {p['shortcode']} -> thumbnail 1280x720 + remarketing + 5 plataformas")

if "selected" in st.session_state:
    p = st.session_state["selected"]
    st.divider()
    st.subheader(f"Pronto pra modelar e repostar: {p['url']}")
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.button("📸 Instagram", use_container_width=True)
    c2.button("📘 Facebook", use_container_width=True)
    c3.button("🎵 TikTok", use_container_width=True)
    c4.button("▶️ YouTube", use_container_width=True)
    c5.button("🟢 Kiwify", use_container_width=True)
    st.caption("Fluxo: thumbnail_generator.py -> remarketing_filter.py -> webhook_kiwify.py / youtube_pack.py")
    