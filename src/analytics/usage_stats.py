import streamlit as st


def initialize_stats():

    if "usage_stats" not in st.session_state:

        st.session_state.usage_stats = {

            "repository_loaded": 0,

            "questions_asked": 0,

            "reports_generated": 0,

            "agents_used": 0
        }


def increment_stat(
    stat_name
):

    initialize_stats()

    if stat_name in st.session_state.usage_stats:

        st.session_state.usage_stats[
            stat_name
        ] += 1


def get_usage_stats():

    initialize_stats()

    return st.session_state.usage_stats