from app import db, PromptDataModel
from utils.basic_utils import get_prompt_texts_as_dict, generate_uuid


def add_prompts():
    prompts = get_prompt_texts_as_dict()
    db.create_all()
    for prompt_id in prompts.keys():
        prompt_uuid = generate_uuid()
        prompt = prompts[prompt_id]
        prompt_model = PromptDataModel()
        prompt_model.set_data_fields(prompt_uuid, prompt_id, prompt)
        saved = prompt_model.save_to_db()
        if saved:
            print('Added prompt: ', prompt_id)
        else:
            print('Error adding prompt: ', prompt_id)


if __name__ == '__main__':
    add_prompts()
