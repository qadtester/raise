import re
import streamlit as st
from config.ai_config import generate_istqb_content
from config.database import supabase
from utils.export import export_to_csv, export_to_html, export_to_markdown
from utils.permissions import can_create, can_delete_items, can_edit

TEST_TYPES = ["Funcional", "Regressão", "Smoke", "Não-Funcional"]

# Mapeamento de prioridade para a ordenação dos status (Homolog)
STATUS_ORDER = {"Não Executado": 1, "Passou": 2, "Bloqueado": 3, "Falhou": 4}

def format_regression_title(original_title: str) -> str:
    """Garante que o prefixo [Regressão] apareça apenas uma vez, limpando acumulados."""
    clean_title = re.sub(r'(\s*\[Regressão\]\s*)+', ' ', original_title, flags=re.IGNORECASE).strip()
    return f"[Regressão] {clean_title}"


def render_test_cases_tab(project_id: str):
    st.subheader("📋 Gestão e Execução de Casos de Teste")
    user_info = st.session_state.get("user", {})

    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        current_cycle = st.text_input(
            "🏷️ Ciclo de Teste / Release (para novas criações ou duplicações)",
            value="",
            placeholder="Ex: Release 1.0, Sprint 12, Pós-Deploy v1.1",
            help="Preencha este campo caso vá criar, gerar por IA ou duplicar casos de teste para um novo ciclo.",
        )
    active_cycle = current_cycle.strip()

    with col_c2:
        try:
            existing_cycles_res = supabase.table("test_cases").select("test_cycle").eq("project_id", project_id).execute()
            cycles_list = sorted(
                list(set([row.get("test_cycle") for row in (existing_cycles_res.data or []) if row.get("test_cycle") and row.get("test_cycle").strip()]))
            )
        except Exception as e:
            cycles_list = []
            st.error(f"Erro ao carregar ciclos de teste: {e}")

    if can_create(user_info):
        with st.expander("🚀 Geração Inteligente de Suíte Completa via IA (Múltiplos Testes)", expanded=False):
            if not active_cycle:
                st.warning("⚠️ Preencha o **Ciclo de Teste / Release** acima para usar a geração por IA.")
            else:
                st.info(f"💡 A IA fará a leitura completa do documento do projeto e gerará a suíte atribuindo ao ciclo: **{active_cycle}**")
                foco_lote = st.text_input("Foco opcional para a suíte (ex: Priorizar testes de segurança e login):", key="batch_ai_foco")

                if st.button("✨ Gerar Suíte Completa de Testes com IA", type="primary", key="btn_gen_batch_tc"):
                    with st.spinner("A IA está analisando o documento do projeto e estruturando os casos de teste..."):
                        query_lote = project_id
                        if foco_lote.strip():
                            query_lote += f" | Foco da suíte: {foco_lote}"

                        data = generate_istqb_content("test_cases_batch", query_lote)

                        if data and isinstance(data, list):
                            sucesso_count = 0
                            erros_count = 0
                            for item in data:
                                payload = {
                                    "project_id": project_id,
                                    "test_type": item.get("test_type", "Funcional"),
                                    "title": item.get("title", "Caso de Teste Gerado por IA"),
                                    "preconditions": item.get("preconditions", ""),
                                    "steps": item.get("steps", ""),
                                    "expected_result": item.get("expected_result", ""),
                                    "status": "Não Executado",
                                    "test_cycle": active_cycle,
                                }
                                try:
                                    supabase.table("test_cases").insert(payload).execute()
                                    sucesso_count += 1
                                except Exception as db_err:
                                    erros_count += 1
                                    st.warning(f"Falha ao salvar o caso '{item.get('title')}': {db_err}")

                            if sucesso_count > 0:
                                st.success(f"Suíte gerada com sucesso! {sucesso_count} casos de teste adicionados ao ciclo `{active_cycle}`.")
                                if erros_count > 0:
                                    st.warning(f"{erros_count} itens falharam ao ser salvos.")
                                st.rerun()
                            else:
                                st.error("Houve um erro ao salvar os casos de teste gerados no Supabase.")
                        else:
                            st.error("A IA não retornou uma lista válida. Verifique a configuração da IA.")

        with st.expander("➕ Criar Caso de Teste Individual (Manual ou Unitário com IA)", expanded=False):
            mode = st.radio("Modo de Criação", ["Sem IA (Manual)", "Com IA (Unitário)"], horizontal=True, key="tc_mode_radio")
            test_type = st.selectbox("Tipo de Teste", TEST_TYPES, key="tc_type_select")

            if mode == "Com IA (Unitário)":
                if not active_cycle:
                    st.warning("⚠️ Preencha o **Ciclo de Teste / Release** acima para criar o teste.")
                else:
                    st.info(f"💡 A IA lerá o documento e salvará no ciclo: **{active_cycle}**")
                    user_story = st.text_area("O que deseja testar?:", placeholder="Ex: Validar login...", key="tc_ai_prompt")
                    if st.button("✨ Gerar e Salvar Caso de Teste via IA", type="primary", key="btn_gen_tc_ai"):
                        with st.spinner("Gerando..."):
                            query_ia = f"{project_id} | Contexto/Foco: {user_story}" if user_story.strip() else project_id
                            data = generate_istqb_content("test_case", query_ia)
                            
                            if data and isinstance(data, dict):
                                payload = {
                                    "project_id": project_id,
                                    "test_type": test_type,
                                    "title": data.get("title", "Caso de Teste Gerado por IA"),
                                    "preconditions": data.get("preconditions", ""),
                                    "steps": data.get("steps", ""),
                                    "expected_result": data.get("expected_result", ""),
                                    "status": "Não Executado",
                                    "test_cycle": active_cycle,
                                }
                                try:
                                    supabase.table("test_cases").insert(payload).execute()
                                    st.success("Caso de teste salvo com sucesso!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao salvar no Supabase: {e}")
                            else:
                                st.error("Falha ao gerar o caso de teste pela IA.")
            else:
                with st.form("manual_tc_form", clear_on_submit=True):
                    st.markdown("📝 **Preencha os campos abaixo seguindo as boas práticas ISTQB:**")
                    title = st.text_input("Título do Caso de Teste *")
                    preconditions = st.text_area("Pré-condições")
                    steps = st.text_area("Passos para Execução *")
                    expected_result = st.text_area("Resultado Esperado *")

                    if st.form_submit_button("💾 Salvar Caso de Teste"):
                        if not active_cycle:
                            st.error("Preencha o Ciclo de Teste no topo.")
                        elif title.strip() and steps.strip() and expected_result.strip():
                            payload = {
                                "project_id": project_id,
                                "test_type": test_type,
                                "title": title,
                                "preconditions": preconditions,
                                "steps": steps,
                                "expected_result": expected_result,
                                "status": "Não Executado",
                                "test_cycle": active_cycle,
                            }
                            try:
                                supabase.table("test_cases").insert(payload).execute()
                                st.success("Salvo com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao salvar no Supabase: {e}")
                        else:
                            st.error("Os campos Título, Passos e Resultado Esperado são obrigatórios.")
    else:
        st.info("🔒 Seu perfil possui permissão apenas de leitura. A criação e geração de testes estão desabilitadas.")

    st.divider()

    st.markdown("### Suíte de Testes")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_cycle = st.selectbox("Filtrar por Ciclo:", ["Todos"] + cycles_list, key="tc_filter_cycle")
    with col_f2:
        filter_type = st.selectbox("Filtrar por Tipo:", ["Todos"] + TEST_TYPES, key="tc_filter_select")
    with col_f3:
        filter_status = st.selectbox("Filtrar por Status:", ["Todos", "Não Executado", "Passou", "Falhou", "Bloqueado"], key="tc_filter_status")

    try:
        query = supabase.table("test_cases").select("*").eq("project_id", project_id)
        if filter_cycle != "Todos":
            query = query.eq("test_cycle", filter_cycle)
        if filter_type != "Todos":
            query = query.eq("test_type", filter_type)
        if filter_status != "Todos":
            query = query.eq("status", filter_status)
        test_cases = query.execute().data or []
    except Exception as e:
        test_cases = []
        st.error(f"Erro ao buscar casos de teste: {e}")

    if not test_cases:
        st.info("Nenhum caso de teste encontrado.")
    else:
        # Ordenação implementada na Homologação
        test_cases.sort(key=lambda x: (STATUS_ORDER.get(x.get("status"), 99), x.get("title", "").strip().lower()))

        col_dl1, col_dl2, col_dl3 = st.columns(3)
        with col_dl1:
            st.download_button("📥 Baixar (CSV)", export_to_csv(test_cases).encode("utf-8-sig"), f"tc_{project_id[:8]}.csv", "text/csv")
        with col_dl2:
            st.download_button("📥 Baixar (Markdown)", export_to_markdown(test_cases, title=f"TCs - {filter_cycle}"), f"tc_{project_id[:8]}.md", "text/markdown")
        with col_dl3:
            st.download_button("🌐 Baixar (HTML)", export_to_html(test_cases, title=f"TCs - {filter_cycle}").encode("utf-8"), f"tc_{project_id[:8]}.html", "text/html")

        st.markdown("---")
        
        grouped_tc = {}
        for tc in test_cases:
            grouped_tc.setdefault(tc.get("test_cycle") or "Sem Ciclo", []).append(tc)

        for cycle_name, tc_list in grouped_tc.items():
            with st.expander(f"📦 **Ciclo / Release: {cycle_name}** ({len(tc_list)} testes)", expanded=True):
                for tc in tc_list:
                    status = tc.get("status", "Não Executado")
                    cycle_tag = tc.get("test_cycle", "Sem Ciclo")
                    status_icon = "🟢" if status == "Passou" else ("🔴" if status == "Falhou" else ("🟡" if status == "Bloqueado" else "⚪"))

                    with st.expander(f"{status_icon} [{tc.get('test_type', 'Teste')}] - {tc.get('title')}"):
                        col_det, col_act = st.columns([3, 1])
                        
                        with col_det:
                            st.markdown(f"**Tipo:** `{tc.get('test_type', 'N/A')}`")
                            st.markdown(f"**Ciclo:** `{cycle_tag}`")
                            st.markdown(f"**Pré-condições:** {tc.get('preconditions') or 'N/A'}")
                            st.markdown(f"**Passos:**\n\n{tc.get('steps') or 'N/A'}")
                            st.markdown(f"**Resultado Esperado:**\n\n{tc.get('expected_result') or 'N/A'}")
                            
                            st.divider()

                            c_edit, c_clone, c_del = st.columns(3)
                            
                            with c_edit:
                                if can_edit(user_info):
                                    with st.popover("✏️ Editar", key=f"pop_edit_tc_{tc['id']}"):
                                        # Restaurados os campos da versão Prod original
                                        e_title = st.text_input("Título", value=tc["title"], key=f"e_tc_t_{tc['id']}")
                                        current_type = tc.get('test_type', 'Funcional')
                                        type_idx = TEST_TYPES.index(current_type) if current_type in TEST_TYPES else 0
                                        e_type = st.selectbox("Tipo de Teste *", TEST_TYPES, index=type_idx, key=f"e_tc_tp_{tc['id']}")
                                        e_cycle = st.text_input("Ciclo / Release", value=tc.get("test_cycle", ""), key=f"e_tc_c_{tc['id']}")
                                        e_pre = st.text_area("Pré-condições", value=tc.get('preconditions', ''), key=f"e_tc_p_{tc['id']}")
                                        e_steps = st.text_area("Passos", value=tc.get("steps", ""), key=f"e_tc_s_{tc['id']}")
                                        e_exp = st.text_area("Esperado", value=tc.get("expected_result", ""), key=f"e_tc_e_{tc['id']}")
                                        
                                        if st.button("Salvar Alterações", key=f"btn_tc_edit_{tc['id']}"):
                                            if e_cycle.strip():
                                                try:
                                                    supabase.table("test_cases").update({
                                                        "title": e_title,
                                                        "test_type": e_type,
                                                        "test_cycle": e_cycle.strip(),
                                                        "preconditions": e_pre,
                                                        "steps": e_steps,
                                                        "expected_result": e_exp,
                                                    }).eq("id", tc["id"]).execute()
                                                    st.rerun()
                                                except Exception as e:
                                                    st.error(f"Erro ao atualizar: {e}")
                                            else:
                                                st.error("O campo Ciclo é obrigatório.")

                            with c_clone:
                                if can_edit(user_info) and st.button("📋 Duplicar Teste", key=f"btn_tc_clone_{tc['id']}"):
                                    target_cycle = active_cycle if active_cycle else tc.get("test_cycle")
                                    # Restaura a formatação de Regressão da versão Prod original
                                    new_title = format_regression_title(tc['title']) if tc.get('test_type') == "Regressão" else f"{tc['title']} (Cópia)"
                                    
                                    clone_payload = {
                                        "project_id": tc.get("project_id"),
                                        "test_type": tc.get("test_type", "Funcional"),
                                        "title": new_title,
                                        "preconditions": tc.get("preconditions", ""),
                                        "steps": tc.get("steps", ""),
                                        "expected_result": tc.get("expected_result", ""),
                                        "status": "Não Executado",
                                        "test_cycle": target_cycle,
                                    }
                                    try:
                                        supabase.table("test_cases").insert(clone_payload).execute()
                                        st.success("Caso de teste duplicado!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Erro ao duplicar: {e}")

                            with c_del:
                                if can_delete_items(user_info):
                                    if st.button("🗑️ Excluir", key=f"btn_tc_del_{tc['id']}", type="primary"):
                                        try:
                                            supabase.table("test_cases").delete().eq("id", tc["id"]).execute()
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Erro ao excluir: {e}")
                                else:
                                    st.caption("🔒 Exclusão restrita")

                        with col_act:
                            st.write(f"**Status:** {status}")
                            st.write("**Executar Ciclo:**")
                            if can_edit(user_info):
                                if st.button("🟢 Passou", key=f"p_{tc['id']}", use_container_width=True):
                                    supabase.table("test_cases").update({"status": "Passou"}).eq("id", tc['id']).execute()
                                    st.rerun()
                                if st.button("🔴 Falhou", key=f"f_{tc['id']}", use_container_width=True):
                                    supabase.table("test_cases").update({"status": "Falhou"}).eq("id", tc['id']).execute()
                                    st.rerun()
                                if st.button("🟡 Bloqueado", key=f"b_{tc['id']}", use_container_width=True):
                                    supabase.table("test_cases").update({"status": "Bloqueado"}).eq("id", tc['id']).execute()
                                    st.rerun()
                                    
                                # Restaura o Resetar do Prod original
                                if status != "Não Executado":
                                    if st.button("⚪ Resetar (Não Executado)", key=f"r_{tc['id']}", use_container_width=True):
                                        try:
                                            supabase.table("test_cases").update({"status": "Não Executado"}).eq("id", tc['id']).execute()
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Erro ao resetar status: {e}")
