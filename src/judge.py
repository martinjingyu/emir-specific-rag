from openai import AzureOpenAI
import yaml
with open("config/api.yaml", "r") as f:
    config = yaml.safe_load(f)
api_base = config['azure']['api_base']
api_key = config['azure']['api_key']
api_version = config['azure']['api_version']
deployment_name = config['azure']['deployment_name']

class Judge:
    def __init__(self):
            self.deployment_name = deployment_name
            self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            base_url=f"{api_base}/openai/deployments/{deployment_name}"
            )
    def init_systemprompt(self):
        system_prompt = (
            "You are a helpful assistant. Your task is to judge whether the explanation of a financial abbreviation is correct. "
            "You will be given a question that asks for the full form of a financial abbreviation, a ground true, and an answer provided by a language model. "
            "Your job is to determine whether the answer is correct in the context of the financial domain. "
            "If the explanation is correct, respond with 'Correct'. If it is incorrect or unrelated, respond with 'Incorrect'."
        )
        return system_prompt
    def forward(self, prompt):
        system_prompt = self.init_systemprompt()

        completion = self.client.chat.completions.create(
        model=self.deployment_name,
        messages= [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": [
            {
                "type": "text",
                "text": f"{prompt}"
            },
            ]}
        ]
        )
        response = completion.choices[0].message.content
        return response
    def __call__(self, prompt):
        return self.forward(prompt)
