# ... [behoud alle vorige imports en functies] ...

# Voeg deze CSS styling toe bovenaan de Streamlit code
st.markdown("""
<style>
    /* Kleurenpalet */
    :root {
        --score-a: #2ecc71;
        --score-b: #27ae60;
        --score-c: #f39c12;
        --score-d: #e74c3c;
        --score-e: #c0392b;
    }
    
    .score-label {
        padding: 0.2em 0.5em;
        border-radius: 0.25em;
        font-weight: 600;
        font-size: 0.9em;
    }
    
    .score-A { background: var(--score-a); color: white; }
    .score-B { background: var(--score-b); color: white; }
    .score-C { background: var(--score-c); color: white; }
    .score-D { background: var(--score-d); color: white; }
    .score-E { background: var(--score-e); color: white; }
    
    /* Aangepaste progress bar */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, var(--score-a) 0%, var(--score-e) 100%);
    }
    
    /* Donkere modus compatibel */
    @media (prefers-color-scheme: dark) {
        .score-A { color: #111 !important; }
        .score-B { color: #111 !important; }
    }
</style>
""", unsafe_allow_html=True)

# Hulp functie voor score labels
def score_label(score):
    color_class = f"score-{score}"
    return f'<span class="score-label {color_class}">{score}</span>'

# Pas de resultatenpagina aan
elif st.session_state.page == 2:
    st.title("📈 Analyse Resultaten")
    
    # Score berekening
    score_values = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1}
    total = sum(score_values[s] for s in st.session_state.scores.values())
    avg_score = total / len(st.session_state.scores)
    final_score = chr(ord('A') + int(4 - (avg_score - 1)))
    
    # Header met kleurcodering
    col1, col2 = st.columns([1,3])
    with col1:
        st.markdown(f"### Totale Futri-Score\n"
                    f"{score_label(final_score)}", 
                    unsafe_allow_html=True)
        st.caption(f"Gemiddelde: {avg_score:.1f}/5.0")
        
    with col2:
        st.progress(avg_score/5)
        st.caption("""
        **Interpretatie:**  
        🟢 A = Uitmuntend | 🟡 C = Gemiddeld | 🔴 E = Kritiek
        """)
    
    st.divider()
    
    # Detailrapport met kleuren
    for criterion, score in st.session_state.scores.items():
        with st.expander(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                {criterion} 
                {score_label(score)}
            </div>
        """, expanded=True, unsafe_allow_html=True):
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.subheader("📋 Analyse")
                st.markdown(f'<div style="line-height:1.8">{CRITERIA_FEEDBACK[criterion][score]}</div>', 
                           unsafe_allow_html=True)
                
                st.subheader("⚙️ Aanbeveling")
                rec_text = RECOMMENDATIONS[criterion] if score in ['D','E'] else random.choice(POSITIVE_FEEDBACK[criterion])
                rec_icon = "🚨" if score in ['D','E'] else "💡"
                st.markdown(f"""
                    <div style="
                        background: {"#fbeee6" if score in ['D','E'] else "#e8f5e9"};
                        padding: 1rem;
                        border-radius: 0.5rem;
                        line-height: 1.6;
                    ">
                        {rec_icon} {rec_text}
                    </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.subheader("❓ Reflectiepunten")
                if score in ['D','E']:
                    for question in REFLECTION_QUESTIONS[criterion]:
                        st.markdown(f"""
                            <div style="
                                padding: 0.5rem;
                                margin: 0.2rem 0;
                                background: #fff3f3;
                                border-radius: 0.25rem;
                            ">
                                • {question}
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="
                            padding: 1rem;
                            background: #f8f9fa;
                            border-radius: 0.5rem;
                            line-height: 1.8;
                        ">
                            **Consolidatievragen:**  
                            • Hoe behoudt u deze sterke punten?  
                            • Welke kansen ziet u voor verdere optimalisatie?
                        </div>
                    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ... [rest van de code blijft hetzelfde] ...
