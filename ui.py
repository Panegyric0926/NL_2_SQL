import gradio as gr
import json
from call_llm import call_llm
from prompt import natural_language_to_structure, structure_to_sql, sql_code_check, database_meta_information
from call_database import query_record, insert_record

def natural_language_2_structure(user_input):
    prompt = natural_language_to_structure.replace('{database_meta_information}', database_meta_information).replace('{user_input}', user_input)
    answer, duration, _ = call_llm(prompt)
    position = answer.find('</think>')
    answer = answer[position + len('</think>'):].lstrip()
    answer = json.loads(answer)
    return answer

def structure_2_sql(structure):
    prompt = structure_to_sql.replace('{database_meta_information}', database_meta_information).replace('{user_input}', structure)
    answer, duration, _ = call_llm(prompt)
    position = answer.find('</think>')
    answer = answer[position + len('</think>'):].lstrip()
    return answer

def code_check(code):
    prompt = sql_code_check.replace('{database_meta_information}', database_meta_information).replace('{user_input}', code)
    answer, duration, _ = call_llm(prompt)
    position = answer.find('</think>')
    answer = answer[position + len('</think>'):].lstrip()
    return answer

def process(user_input, progress=gr.Progress(track_tqdm=True)):
    # 1. natural_language_2_structure
    try:
        nl_struct = natural_language_2_structure(user_input)
        struct_out = f"```json\n{json.dumps(nl_struct, indent=2)}\n```"
    except Exception as e:
        yield f"❌ Error: {e}", "", "", ""
        return

    # Show step 1 immediately
    yield struct_out, "", "", ""

    # Check for relevance
    relevance = nl_struct.get("Relevance", "")
    if relevance == "Irrelevant Query":
        # Show step 1 and 2 immediately (step 2 = error for irrelevance)
        yield struct_out, "❌ Irrelevant Query", "", ""
        return

    # Extract structure and tables
    structure = nl_struct.get("Structure", "")
    tables = nl_struct.get("Tables_Involved", "")
    # Normalize tables if it's a comma-separated string
    if isinstance(tables, str):
        tables = ', '.join(sorted(name.strip() for name in tables.split(',')))

    # 2. query_record
    try:
        query_result = query_record(user_input, structure, tables)
        query_out = f"```json\n{json.dumps(query_result, indent=2)}\n```"
    except Exception as e:
        yield struct_out, f"❌ Error: {e}", "", ""
        return

    # Show step 2 result as soon as it's available
    yield struct_out, query_out, "", ""

    # If a match is found, show and finish (your original logic: show 'Code' and stop)
    if query_result.get('match'):
        sql_code = query_result.get('Code', '')
        sql_out = f"```sql\n{sql_code}\n```" if sql_code else ""
        yield struct_out, query_out, sql_out, ""
        return

    # 3. structure_2_sql
    try:
        sql_code = structure_2_sql(structure)
        sql_out = f"```sql\n{sql_code}\n```"
    except Exception as e:
        yield struct_out, query_out, f"❌ Error: {e}", ""
        return

    # Show step 3 result immediately
    yield struct_out, query_out, sql_out, ""

    # 4. code_check
    try:
        check_result = code_check(sql_code)
        check_out = f"```\n{check_result}\n```"
    except Exception as e:
        yield struct_out, query_out, sql_out, f"❌ Error: {e}"
        return

    # Show step 4 result immediately
    yield struct_out, query_out, sql_out, check_out

    # 5. insert_record (if no match found)
    try:
        insert_record(user_input, tables, structure, sql_code)
    except Exception as e:
        check_out += f"\n\n❌ Insert Error: {e}"
        # Optionally show update
        yield struct_out, query_out, sql_out, check_out
        return

def clear_all():
    return [""] * 5  # 1 input + 4 outputs

with gr.Blocks(css="""
.dark .step-panel {
  background: #23272e !important;
  color: #fff !important;
  border: 2px solid #333a45 !important;
  border-radius: 12px;
  margin: 18px 0;
  padding: 24px 24px 20px 24px;
  min-height: 120px;
  box-shadow: 0 2px 7px 0 #181a1b;
  font-size: 1.11em;
}
@media (max-width: 768px) {
  .dark .step-panel {
    padding: 12px 7px;
    min-height: 60px;
  }
}
""", title="SQL Writer by Mickey") as demo:
    gr.Markdown(
        """
        # 📝 SQL Writer by Mickey

        Enter your natural language request.  
        The app will show the result of each processing step below.
        """
    )
    with gr.Row():
        user_input = gr.Textbox(lines=2, label="Your Request (Natural Language)", scale=6, placeholder="e.g. Get the top 5 products that have the highest average rating.")
        btn = gr.Button("Process", scale=1)
        clear_btn = gr.Button("Clear", scale=1)

    gr.Markdown("### 1. natural_language_2_structure")
    s1 = gr.Markdown(elem_classes="step-panel")
    gr.Markdown("### 2. query_record")
    s2 = gr.Markdown(elem_classes="step-panel")
    gr.Markdown("### 3. structure_2_sql")
    s3 = gr.Markdown(elem_classes="step-panel")
    gr.Markdown("### 4. code_check")
    s4 = gr.Markdown(elem_classes="step-panel")

    btn.click(
        process,
        inputs=[user_input],
        outputs=[s1, s2, s3, s4],
        show_progress=True,
        concurrency_limit=None,
        queue=True,  # Required for streaming
        api_name=None,
    )
    user_input.submit(
        process,
        inputs=[user_input],
        outputs=[s1, s2, s3, s4],
        show_progress=True,
        concurrency_limit=None,
        queue=True,
        api_name=None,
    )
    clear_btn.click(
        clear_all,
        inputs=[],
        outputs=[user_input, s1, s2, s3, s4]
    )

demo.launch()