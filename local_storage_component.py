import streamlit.components.v1 as components
import json

def local_storage(key, default=None):
    if default is None:
        default = []

    component = components.html(
        f"""
        <script>
        const key = "{key}";
        const defaultValue = {json.dumps(default)};

        function send(value) {{
            const out = document.getElementById("out");
            out.value = JSON.stringify(value);
            out.dispatchEvent(new Event("change"));
        }}

        let data = localStorage.getItem(key);
        if (!data) {{
            localStorage.setItem(key, JSON.stringify(defaultValue));
            data = JSON.stringify(defaultValue);
        }}

        send(JSON.parse(data));

        window.addEventListener("message", (event) => {{
            if (event.data.type === "SET") {{
                localStorage.setItem(key, JSON.stringify(event.data.value));
                send(event.data.value);
            }}
        }});
        </script>

        <textarea id="out" style="display:none;"></textarea>
        """,
        height=0,
    )

    if component:
        return json.loads(component)

    return default
