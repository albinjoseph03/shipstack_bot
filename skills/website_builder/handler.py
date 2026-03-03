import os
import shutil
import uuid
import re

def create_project():
    """Create a unique project folder inside /projects/{projectId}"""
    project_id = str(uuid.uuid4())
    projects_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'projects'))
    project_path = os.path.join(projects_dir, project_id)
    os.makedirs(project_path, exist_ok=True)
    return project_id, project_path

def copy_template(project_path):
    """Copy the basic template into the target folder"""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'basic')
    for item in os.listdir(template_dir):
        s = os.path.join(template_dir, item)
        d = os.path.join(project_path, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def modify_html_content(project_path, prompt, llm_modification_fn=None):
    """
    Modify index.html content using the LLM based on user prompt.
    Constraints:
    - Replace placeholder text only
    - Not rewrite entire structure
    - Keep layout stable
    - Only update content areas
    """
    index_path = os.path.join(project_path, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if llm_modification_fn:
        content = llm_modification_fn(content, prompt)
    else:
        # Fallback if no LLM handler is provided
        content = content.replace('<!-- TITLE_PLACEHOLDER -->', f'Generated Title for: {prompt}<!-- /TITLE_PLACEHOLDER -->')

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

def save_project():
    """Save files step (placeholder for future extensions like git push / db)."""
    pass

def handle(prompt, **kwargs):
    """
    Main handler function for the website_builder skill.
    """
    llm = kwargs.get('llm')
    
    def llm_mod(html_content, user_prompt):
        if not llm: return html_content
        instructions = "Replace placeholder text comments in the HTML based on the user's prompt. Do not rewrite structure."
        return llm.generate(f"{instructions}\nPrompt: {user_prompt}\nHTML:\n{html_content}")

    project_id, project_path = create_project()
    copy_template(project_path)
    modify_html_content(project_path, prompt, llm_modification_fn=llm_mod)
    save_project()
    
    return {
        "status": "success",
        "projectId": project_id,
        "path": project_path
    }
